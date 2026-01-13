"""
PreCompact Hook - 上下文压缩前摘要
使用 Ollama 生成智能摘要
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.ollama_client import ollama
from core.logger import logger
from core.config import config


class PreCompactHook(BaseHook):
    """上下文压缩前处理 - 智能摘要"""

    def execute(self) -> HookResult:
        context = self.input_data.get("context", "")

        if not context or len(context) < 100:
            return self.allow()

        # 使用 Ollama 生成摘要
        summary = ollama.summarize(context, max_length=200)

        if summary:
            logger.info("已生成上下文摘要")
            # 构建符合 Claude Code Schema 的输出
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreCompact",
                    "additionalContext": config.get_prompt("pre_compact", "context_summary_header", summary=summary)
                },
                "systemMessage": config.get_prompt("pre_compact", "ui_context_compressed", summary_preview=summary[:80])
            }
            return self.allow(output)

        return self.allow()


if __name__ == "__main__":
    handler = PreCompactHook()
    sys.exit(handler.run())
