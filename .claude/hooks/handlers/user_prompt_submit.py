"""
UserPromptSubmit Hook - 意图识别 + MCP 引导 + 智能 Skills 推荐
使用 Ollama 分析用户意图，引导使用关键 MCP 工具，自动推荐相关 Skills
"""
import sys
import os
import re
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.base_hook import BaseHook, HookResult
from core.ollama_client import ollama
from core.logger import logger
from core.config import config


def get_skills_list() -> List[Dict[str, str]]:
    """扫描 skills 目录，提取名称和描述"""
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    skills = []

    if not skills_dir.exists():
        return skills

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir() or skill_path.name.startswith(('_', '.')):
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text(encoding='utf-8')
            # 提取 YAML frontmatter 中的 name 和 description
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    frontmatter = content[3:end]
                    name = skill_path.name
                    desc = ""
                    for line in frontmatter.split('\n'):
                        if line.startswith('name:'):
                            name = line.split(':', 1)[1].strip().strip('"\'')
                        elif line.startswith('description:'):
                            desc = line.split(':', 1)[1].strip().strip('"\'')
                    if desc:
                        skills.append({"name": name, "desc": desc})
        except Exception:
            continue

    return skills


class UserPromptSubmitHook(BaseHook):
    """用户提示词提交处理 - 意图识别 + MCP 引导"""

    def execute(self) -> HookResult:
        prompt = self.input_data.get("prompt", "")
        if not prompt or len(prompt) < 5:
            logger.debug("提示词太短，跳过处理")
            return self.allow()

        context_parts = []
        ui_message_parts = []

        # 1. 使用 Ollama 分析用户意图（判断需要使用哪些 MCP，移除 Memory）
        try:
            intent_analysis = ollama.analyze_intent(prompt)
            logger.info(f"意图分析: {intent_analysis.get('intent_type')} - {intent_analysis.get('reason')}")

            # 根据意图分析，强制引导使用相应 MCP（移除 Memory）
            mcp_guidance = []

            if intent_analysis.get("needs_sequential_thinking"):
                mcp_guidance.append(config.get_prompt("user_prompt_submit", "sequential_thinking_guidance"))
                ui_message_parts.append(config.get_prompt("user_prompt_submit", "ui_sequential_thinking"))

            if intent_analysis.get("needs_task_manager"):
                mcp_guidance.append(config.get_prompt("user_prompt_submit", "task_manager_guidance"))
                ui_message_parts.append(config.get_prompt("user_prompt_submit", "ui_task_manager"))

            if mcp_guidance:
                context_parts.append(config.get_prompt("user_prompt_submit", "intent_analysis_header"))
                context_parts.append(config.get_prompt("user_prompt_submit", "intent_type_label", type=intent_analysis.get('intent_type', 'other')))
                context_parts.append(config.get_prompt("user_prompt_submit", "intent_reason_label", reason=intent_analysis.get('reason', '')))
                context_parts.append("\n" + "\n".join(mcp_guidance))

        except Exception as e:
            logger.debug(f"Ollama 意图分析失败（可选功能）: {e}")

        # 2. 智能 Skills 推荐（按需推荐，并显式提示结果）
        try:
            skills = get_skills_list()
            if skills:
                skills_recommendation = ollama.recommend_skills(prompt, skills)
                recommended = skills_recommendation.get("recommended", [])
                confidence = skills_recommendation.get("confidence", "low")

                if recommended:
                    logger.info(f"推荐 Skills (置信度: {confidence}): {recommended}")
                    # 构建「先用 Skills 再思考」的强制流程提示（使用配置）
                    skills_hint_parts = [
                        config.get_prompt("user_prompt_submit", "skills_recommendation_header")
                    ]
                    for skill_name in recommended:
                        skills_hint_parts.append(config.get_prompt("user_prompt_submit", "skills_recommendation_item", name=skill_name))

                    if skills_recommendation.get("reason"):
                        skills_hint_parts.append(config.get_prompt("user_prompt_submit", "skills_recommendation_reason", reason=skills_recommendation.get('reason')))

                    skills_hint_parts.append(config.get_prompt("user_prompt_submit", "skills_recommendation_workflow"))

                    context_parts.append("\n" + "\n".join(skills_hint_parts))
                    # 在 UI 明确展示具体推荐了哪些 Skills，避免黑箱
                    skills_str = ', '.join('/' + s for s in recommended)
                    ui_message_parts.append(config.get_prompt("user_prompt_submit", "ui_skills_recommended", skills=skills_str))
                else:
                    # 显式告知已检查但暂无推荐，避免用户感觉是黑箱
                    reason = skills_recommendation.get("reason", "当前需求无需专门的 Skills 推荐")
                    logger.debug(f"Skills 推荐: {reason}")
                    context_parts.append(config.get_prompt("user_prompt_submit", "skills_check_no_recommendation"))
                    ui_message_parts.append(config.get_prompt("user_prompt_submit", "ui_skills_checked"))
        except Exception as e:
            logger.debug(f"Skills 推荐失败（可选功能）: {e}")

        # 3. 使用 Ollama 语义分析是否需要优化（可选，失败不影响主流程）
        enhanced_prompt_data = None  # 用于日志记录
        try:
            analysis = ollama.analyze_prompt(prompt)
            if analysis.get("needs_enhance"):
                logger.info(f"检测到可优化提示词: {analysis.get('reason')}")
                enhanced = ollama.enhance_prompt(prompt)
                if enhanced:
                    # 保存优化数据用于日志记录
                    enhanced_prompt_data = {
                        "original": prompt,
                        "enhanced": enhanced,
                        "reason": analysis.get('reason', ''),
                        "type": analysis.get('type', 'other')
                    }
                    
                    context_parts.append(config.get_prompt("user_prompt_submit", "prompt_enhancement_header"))
                    context_parts.append(config.get_prompt("user_prompt_submit", "prompt_enhancement_reason", reason=analysis.get('reason')))
                    context_parts.append(config.get_prompt("user_prompt_submit", "prompt_enhancement_original", prompt=prompt))
                    context_parts.append(config.get_prompt("user_prompt_submit", "prompt_enhancement_enhanced", enhanced=enhanced))
                    ui_message_parts.append(config.get_prompt("user_prompt_submit", "ui_prompt_enhanced"))
        except Exception as e:
            logger.debug(f"Ollama 分析失败（可选功能）: {e}")

        # 3. 构建符合 Claude Code Schema 的输出
        if context_parts:
            additional_context = "\n".join(context_parts)
            
            ui_message = " | ".join(ui_message_parts) if ui_message_parts else None
            
            # 符合 Claude Code UserPromptSubmit Hook Schema
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": additional_context
                }
            }
            
            # 添加 systemMessage 让信息在 UI 中可见
            if ui_message:
                output["systemMessage"] = ui_message
            
            # 【重要】完整记录 Ollama 优化后的提示词到日志（供人工审查）
            if enhanced_prompt_data:
                logger.log(
                    "prompt_enhancement",
                    {
                        "original_prompt": enhanced_prompt_data["original"],
                        "enhanced_prompt": enhanced_prompt_data["enhanced"],
                        "enhancement_reason": enhanced_prompt_data["reason"],
                        "prompt_type": enhanced_prompt_data["type"]
                    },
                    summary=f"提示词优化: {enhanced_prompt_data['reason']}"
                )
            
            logger.info(f"输出上下文长度: {len(additional_context)} 字符")
            if ui_message:
                logger.info(f"UI 提示: {ui_message}")
            return self.allow(output)
        else:
            logger.debug("未检测到需要引导的意图")
        
        return self.allow()


if __name__ == "__main__":
    handler = UserPromptSubmitHook()
    sys.exit(handler.run())
