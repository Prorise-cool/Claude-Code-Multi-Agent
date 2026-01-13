"""
Ollama LLM 客户端
所有判断逻辑都通过提示词完成，不使用硬编码规则
"""
import subprocess
import json
from typing import Optional, Dict, Any
from .config import config


class OllamaClient:
    """Ollama LLM 客户端 - 纯提示词驱动"""

    def __init__(self, model: Optional[str] = None):
        self.model = model or config.ollama_model
        self.timeout = config.ollama_timeout

    def _call(self, prompt: str) -> Optional[str]:
        """调用 Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, timeout=self.timeout
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _call_json(self, prompt: str) -> Optional[Dict]:
        """调用并解析 JSON 响应"""
        result = self._call(prompt)
        if not result:
            return None
        try:
            # 尝试提取 JSON
            if '{' in result:
                start = result.index('{')
                end = result.rindex('}') + 1
                return json.loads(result[start:end])
        except (json.JSONDecodeError, ValueError):
            pass
        return None

    # ===== 用户提示词分析 =====
    def analyze_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """分析用户提示词，判断是否需要优化"""
        from .config import config
        prompt_template = config.get_prompt("ollama", "analyze_prompt")
        prompt = prompt_template.format(user_prompt=user_prompt)

        result = self._call_json(prompt)
        return result or {"needs_enhance": False, "reason": "", "type": "other"}

    def enhance_prompt(self, user_prompt: str) -> Optional[str]:
        """优化用户提示词"""
        from .config import config
        prompt_template = config.get_prompt("ollama", "enhance_prompt")
        prompt = prompt_template.format(user_prompt=user_prompt)
        return self._call(prompt)

    def analyze_intent(self, user_prompt: str) -> Dict[str, Any]:
        """分析用户意图，判断需要使用哪些 MCP 工具（移除 Memory）"""
        from .config import config
        prompt_template = config.get_prompt("ollama", "analyze_intent")
        prompt = prompt_template.format(user_prompt=user_prompt)

        result = self._call_json(prompt)
        return result or {
            "needs_sequential_thinking": False,
            "needs_task_manager": False,
            "intent_type": "other",
            "reason": ""
        }

    # ===== 工具使用分析 =====
    def analyze_tool_use(self, tool_name: str, tool_input: Dict) -> Dict[str, Any]:
        """分析工具调用的安全性和建议"""
        from .config import config
        input_str = json.dumps(tool_input, ensure_ascii=False)[:500]
        prompt_template = config.get_prompt("ollama", "analyze_tool_use")
        prompt = prompt_template.format(tool_name=tool_name, tool_input=input_str)

        result = self._call_json(prompt)
        return result or {"risk_level": "none", "warning": "", "suggestion": ""}

    # ===== 操作重要性分析 =====
    def analyze_operation(self, tool_name: str, tool_input: Dict, result_summary: str) -> Dict[str, Any]:
        """分析操作是否值得记录到文档（改为文档分析，移除 Memory）"""
        from .config import config
        input_str = json.dumps(tool_input, ensure_ascii=False)[:300]
        prompt_template = config.get_prompt("ollama", "analyze_operation")
        prompt = prompt_template.format(
            tool_name=tool_name,
            tool_input=input_str,
            result_summary=result_summary[:200]
        )

        result = self._call_json(prompt)
        return result or {"should_document": False, "document_note": "", "target_doc": ""}

    # ===== 通知分析 =====
    def analyze_notification(self, message: str) -> Dict[str, Any]:
        """分析通知重要性"""
        prompt = f'''分析这个通知消息的重要性，返回 JSON：
"{message[:300]}"

判断：是否需要立即通知用户，还是可以忽略

返回格式（只返回JSON）：
{{"importance": "high/medium/low", "should_notify": true/false}}'''

        result = self._call_json(prompt)
        return result or {"importance": "medium", "should_notify": True}

    # ===== 知识提取 =====
    def extract_knowledge(self, session_summary: str) -> Optional[str]:
        """从会话中提取可复用知识"""
        prompt = f'''从这个会话中提取可复用的知识：
{session_summary[:1500]}

输出格式：
1. 解决了什么问题
2. 使用了什么方法
3. 可复用的模式

要求：简洁要点，不超过100字'''
        return self._call(prompt)

    # ===== 摘要生成 =====
    def summarize(self, content: str, max_length: int = 100) -> Optional[str]:
        """生成内容摘要"""
        prompt = f'''用不超过{max_length}字总结以下内容的关键信息：
{content[:1000]}

要求：简洁、准确、保留关键信息'''
        return self._call(prompt)

    # ===== Skills 推荐（按需推荐） =====
    def recommend_skills(self, user_prompt: str, skills_list: list) -> Dict[str, Any]:
        """智能推荐适合当前任务的 Skills - 只在真正需要时推荐"""
        from .config import config
        if not skills_list:
            return {"recommended": [], "reason": "没有可用的 Skills"}

        # 构建 Skills 描述
        skills_desc = "\n".join([
            f"- {s['name']}: {s['desc']}"
            for s in skills_list
        ])

        prompt_template = config.get_prompt("ollama", "recommend_skills")
        prompt = prompt_template.format(
            user_prompt=user_prompt,
            skills_desc=skills_desc
        )

        result = self._call_json(prompt)
        if not result:
            # 无法从模型获取结构化结果时，保持静默，不做强行推荐
            return {"recommended": [], "reason": "无法分析"}

        # 只要模型明确给出了推荐列表，就直接透传给上层
        # 置信度仅作为参考信息，不再用来过滤结果
        recommended = result.get("recommended", [])
        if not recommended:
            return {"recommended": [], "reason": result.get("reason", "模型认为当前不需要推荐 Skills")}

        return result

    # ===== 项目类型检测 =====
    def detect_project_type(self, project_context: str) -> Dict[str, Any]:
        """使用 LLM 智能分析项目类型和框架"""
        from .config import config
        prompt_template = config.get_prompt("ollama", "detect_project_type")
        prompt = prompt_template.format(project_context=project_context[:2000])

        result = self._call_json(prompt)
        return result or {
            "type": "unknown",
            "frameworks": [],
            "characteristics": [],
            "confidence": "low"
        }


# 全局实例
ollama = OllamaClient()
