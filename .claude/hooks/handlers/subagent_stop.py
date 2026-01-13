#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
SubagentStop Hook - 子代理结束处理器
功能：任务状态更新 + TTS 通知
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_hook import BaseHook, HookResult
from core.config import config
from core.logger import logger

class SubagentStopHook(BaseHook):
    """子代理结束 Hook"""

    def execute(self) -> HookResult:
        # 记录子代理完成
        logger.info("子代理任务完成")

        # TTS 通知
        if config.tts_enabled:
            self._speak(config.get_prompt("subagent_stop", "tts_subtask_completed"))

        # 显示在 UI
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "additionalContext": config.get_prompt("subagent_stop", "subagent_completed")
            },
            "systemMessage": config.get_prompt("subagent_stop", "ui_subagent_completed")
        }
        return self.allow(output)

    def _speak(self, message: str) -> None:
        """TTS 播报"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)
            engine.say(message)
            engine.runAndWait()
        except ImportError:
            pass


if __name__ == '__main__':
    hook = SubagentStopHook()
    sys.exit(hook.run())
