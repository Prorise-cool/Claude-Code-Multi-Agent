"""
PreToolUse Hook - 工具使用前检查
使用 Ollama 语义分析安全性和建议
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.ollama_client import ollama
from core.logger import logger
from core.config import config


class PreToolUseHook(BaseHook):
    """工具使用前处理 - 纯提示词驱动"""

    def execute(self) -> HookResult:
        tool_name = self.input_data.get("tool_name", "")
        tool_input = self.input_data.get("tool_input", {})

        if not tool_name:
            return self.allow()

        # 只分析高风险工具，减少不必要的 Ollama 调用
        high_risk_tools = ['Write', 'Edit', 'Bash', 'Delete', 'MultiEdit', 'Glob']
        if tool_name not in high_risk_tools:
            return self.allow()  # 跳过分析

        # 使用 Ollama 分析工具调用
        analysis = ollama.analyze_tool_use(tool_name, tool_input)

        ui_messages = []

        # 高风险操作警告 - 显示在 UI
        if analysis.get("risk_level") == "high":
            warning = analysis.get('warning', '')
            logger.warning(f"高风险操作: {warning}")
            ui_messages.append(config.get_prompt("pre_tool_use", "ui_warning", warning=warning))
            # 如果需要阻止，可以返回 block，这里只记录日志
            # return self.block(warning)

        # 工具建议 - 显示在 UI
        if analysis.get("suggestion"):
            suggestion = analysis.get('suggestion', '')
            logger.info(f"工具建议: {suggestion}")
            ui_messages.append(config.get_prompt("pre_tool_use", "ui_suggestion", suggestion=suggestion))

        # 如果有 UI 消息，输出
        if ui_messages:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": "\n".join(ui_messages)
                },
                "systemMessage": " | ".join(ui_messages)
            }
            return self.allow(output)

        # PreToolUse 主要用于权限控制，如果不需要阻止操作，则不输出
        # 如果需要阻止操作，使用: return self.block("reason")
        return self.allow()


if __name__ == "__main__":
    handler = PreToolUseHook()
    sys.exit(handler.run())
