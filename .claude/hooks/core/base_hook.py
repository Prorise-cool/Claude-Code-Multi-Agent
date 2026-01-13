"""
Hook 基类
提供统一的 Hook 执行框架
"""
import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from .logger import HookLogger
from .config import config

@dataclass
class HookResult:
    """Hook 执行结果"""
    exit_code: int = 0  # 0=继续, 2=阻止
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_json(self) -> str:
        """转换为 JSON 输出"""
        if self.output:
            return json.dumps(self.output, ensure_ascii=False)
        return ""

class BaseHook(ABC):
    """Hook 基类"""

    def __init__(self):
        self.logger = HookLogger(self.__class__.__name__)
        self.input_data: Dict[str, Any] = {}

    def run(self) -> int:
        """执行 Hook 的主入口"""
        try:
            # 读取输入
            self.input_data = self._read_input()

            # 执行 Hook 逻辑
            result = self.execute()

            # 输出结果
            if result.output:
                print(result.to_json())

            if result.error:
                print(result.error, file=sys.stderr)

            # 记录日志（包含输出信息）
            log_data = self.input_data.copy()
            if result.output:
                # 提取关键输出信息
                if isinstance(result.output, dict):
                    if "systemMessage" in result.output:
                        log_data["systemMessage"] = result.output["systemMessage"]
                    if "hookSpecificOutput" in result.output:
                        hook_output = result.output["hookSpecificOutput"]
                        if "hookEventName" in hook_output:
                            log_data["hookEventName"] = hook_output["hookEventName"]
                        if "additionalContext" in hook_output:
                            # 只记录前100字符，避免日志过大
                            ctx = hook_output["additionalContext"]
                            log_data["additionalContext_length"] = len(ctx)
                            log_data["additionalContext_preview"] = ctx[:100] + "..." if len(ctx) > 100 else ctx
            
            self.logger.log(
                event_type=self.__class__.__name__,
                data=log_data,
                summary=result.error if result.error else None
            )

            return result.exit_code

        except json.JSONDecodeError:
            return 0  # 容错
        except Exception as e:
            self.logger.error(str(e), e)
            return 0  # 容错

    def _read_input(self) -> Dict[str, Any]:
        """从 stdin 读取 JSON 输入"""
        try:
            return json.load(sys.stdin)
        except:
            return {}

    @abstractmethod
    def execute(self) -> HookResult:
        """执行 Hook 逻辑，子类必须实现"""
        pass

    def block(self, message: str) -> HookResult:
        """阻止操作"""
        return HookResult(exit_code=2, error=f"BLOCKED: {message}")

    def allow(self, output: Optional[Dict[str, Any]] = None) -> HookResult:
        """允许操作"""
        return HookResult(exit_code=0, output=output)

    def hook_output(self, **kwargs) -> Dict[str, Any]:
        """生成 hookSpecificOutput"""
        return {"hookSpecificOutput": kwargs}
