"""Notification Hook - 简单 TTS 提示
任何 Notification 事件一律触发本地 TTS 提示（从简，不做重要性分析）
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.logger import logger
from core.config import config


class NotificationHook(BaseHook):
    """通知处理 - 直接触发 TTS 提示"""

    def execute(self) -> HookResult:
        message = self.input_data.get("message", "")

        # 任何 Notification 事件都视为需要用户关注
        logger.info(f"收到 Notification: {message[:80]}")

        # 本地 TTS 播报（简体中文，尽量从简）
        if config.tts_enabled:
            # 可选：跳过最通用的提示文案，避免过于频繁
            if message != "Claude is waiting for your input":
                self._speak(config.get_prompt("notification", "tts_need_input"))

        # 保持一个简单的 hook 输出，方便日志对齐
        return self.allow(self.hook_output(importance="high"))

    def _speak(self, content: str) -> None:
        """本地 TTS 播报（pyttsx3），失败时静默"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)
            engine.say(content)
            engine.runAndWait()
        except Exception:
            pass


if __name__ == "__main__":
    handler = NotificationHook()
    sys.exit(handler.run())
