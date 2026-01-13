"""
PostToolUse Hook - 工具使用后处理
强制文档维护 + Git 集成
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.ollama_client import ollama
from core.logger import logger
from core.document_manager import DocumentManager
from core.config import config


class PostToolUseHook(BaseHook):
    """工具使用后处理 - 强制文档维护 + Git 集成"""

    def execute(self) -> HookResult:
        tool_name = self.input_data.get("tool_name", "")
        tool_input = self.input_data.get("tool_input", {})
        tool_result = self.input_data.get("tool_result", "")

        if not tool_name:
            return self.allow()

        # 初始化文档管理器
        project_root = Path.cwd()
        doc_manager = DocumentManager(project_root)
        doc_manager.initialize_documents()  # 确保文档存在

        context_parts = []
        ui_parts = []

        # 1. 强制更新文档（重要操作才更新，自动去重）
        if doc_manager.should_update_documents(tool_name, tool_input, tool_result):
            updates = doc_manager.update_documents(tool_name, tool_input, tool_result)
            
            if updates:
                logger.info(f"准备更新文档: {tool_name} -> {tool_input.get('file_path', 'unknown')}")
                
                # 添加强制文档更新提示词（使用配置）
                context_parts.append(config.get_prompt("post_tool_use", "document_update_header"))
                
                # DEVELOPMENT.md 更新
                if updates.get('development'):
                    context_parts.append(config.get_prompt("post_tool_use", "document_update_development"))
                    context_parts.append(updates['development'])
                    context_parts.append("\n")
                
                # KNOWLEDGE.md 更新
                if updates.get('knowledge'):
                    context_parts.append(config.get_prompt("post_tool_use", "document_update_knowledge"))
                    context_parts.append(updates['knowledge'])
                    context_parts.append("\n")
                
                # CHANGELOG.md 更新
                if updates.get('changelog'):
                    context_parts.append(config.get_prompt("post_tool_use", "document_update_changelog"))
                    context_parts.append(updates['changelog'])
                    context_parts.append("\n")
                
                ui_parts.append(config.get_prompt("post_tool_use", "ui_document_update"))
                
                # 2. Git 提交（文档更新后）
                if doc_manager.check_git_repo():
                    workflow = doc_manager.get_git_workflow() or 'github-flow'
                    
                    # 提示 Git 提交（使用配置）
                    context_parts.append(config.get_prompt("post_tool_use", "git_commit_header"))
                    context_parts.append(config.get_prompt("post_tool_use", "git_commit_requirement", workflow=workflow))
                    ui_parts.append(config.get_prompt("post_tool_use", "ui_git_commit"))
                else:
                    # 没有 Git，需要询问用户（使用配置）
                    context_parts.append(config.get_prompt("post_tool_use", "git_not_initialized_header"))
                    context_parts.append(config.get_prompt("post_tool_use", "git_not_initialized_requirement"))
                    ui_parts.append(config.get_prompt("post_tool_use", "ui_git_not_initialized"))

        # 输出结果
        if context_parts:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": "\n".join(context_parts)
                },
                "systemMessage": " | ".join(ui_parts) if ui_parts else None
            }
            return self.allow(output)

        return self.allow()


if __name__ == "__main__":
    handler = PostToolUseHook()
    sys.exit(handler.run())
