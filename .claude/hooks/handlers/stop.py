"""
Stop Hook - 会话结束知识沉淀
使用 Ollama 提取可复用知识
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.ollama_client import ollama
from core.logger import logger
from core.config import config
from core.document_manager import DocumentManager


class StopHook(BaseHook):
    """会话结束处理 - 知识沉淀"""

    def execute(self) -> HookResult:
        summary = self.input_data.get("summary", "")

        if not summary or len(summary) < 50:
            return self.allow()

        # 使用 Ollama 提取知识
        knowledge = ollama.extract_knowledge(summary)

        if knowledge:
            logger.info("已提取会话知识")
            # 【核心改进】改为更新 KNOWLEDGE.md 文档，而不是使用 Memory MCP
            doc_manager = DocumentManager(Path.cwd())
            doc_manager.initialize_documents()
            
            additional_context = (
                config.get_prompt("stop", "knowledge_extraction_header", knowledge=knowledge) +
                config.get_prompt("stop", "knowledge_update_requirement", knowledge=knowledge)
            )
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "Stop",
                    "additionalContext": additional_context
                },
                "systemMessage": config.get_prompt("stop", "ui_knowledge_extracted", knowledge_preview=knowledge[:60])
            }
            # 任务结束播报
            if config.tts_enabled:
                self._speak(config.get_prompt("stop", "tts_task_completed"))
            return self.allow(output)

        return self.allow()

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
    handler = StopHook()
    sys.exit(handler.run())
