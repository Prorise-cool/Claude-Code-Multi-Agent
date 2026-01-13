"""
Hooks 系统统一配置
"""
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import json

# 尝试加载 .env 文件（可选依赖）
try:
    from dotenv import load_dotenv
    # 从项目根目录加载 .env 文件
    env_file = Path.cwd() / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv 是可选的

@dataclass
class HooksConfig:
    """Hooks 配置类"""
    # 路径配置
    hooks_dir: Path = Path(__file__).parent.parent
    logs_dir: Path = Path.cwd() / 'logs'
    data_dir: Path = Path.cwd() / '.claude' / 'data'

    # Ollama 配置
    ollama_model: str = "gemma3:1b"  # 默认模型，可通过环境变量覆盖
    ollama_timeout: int = 10

    # 日志配置
    max_log_entries: int = 500

    # TTS 配置
    tts_enabled: bool = True
    tts_provider: str = "pyttsx3"  # pyttsx3, openai, elevenlabs

    # 功能开关
    prompt_enhancement_enabled: bool = True
    tool_suggestion_enabled: bool = True
    knowledge_extraction_enabled: bool = True

    # 提示词配置
    _prompts: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """初始化后处理"""
        # 从环境变量读取配置（优先读取 OLLAMA_MODEL，兼容 HOOKS_OLLAMA_MODEL）
        self.ollama_model = os.getenv('OLLAMA_MODEL') or os.getenv('HOOKS_OLLAMA_MODEL', self.ollama_model)
        self.tts_provider = os.getenv('HOOKS_TTS_PROVIDER', self.tts_provider)
        self.tts_enabled = os.getenv('HOOKS_TTS_ENABLED', 'true').lower() == 'true'

        # 确保目录存在
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_prompts(self) -> Dict[str, Any]:
        """加载提示词配置"""
        if self._prompts is not None:
            return self._prompts
        
        prompts_file = self.hooks_dir / 'prompts.json'
        if prompts_file.exists():
            try:
                with open(prompts_file, 'r', encoding='utf-8') as f:
                    self._prompts = json.load(f)
                    return self._prompts
            except Exception as e:
                from .logger import logger
                logger.warning(f"加载提示词配置失败: {e}")
        
        # 返回空字典，避免后续代码报错
        return {}
    
    def get_prompt(self, section: str, key: str, **kwargs) -> str:
        """获取提示词模板并格式化"""
        prompts = self.load_prompts()
        section_data = prompts.get(section, {})
        template = section_data.get(key, '')
        
        # 简单的字符串格式化（支持 {key} 占位符）
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError):
            # 如果格式化失败，返回原始模板
            return template

# 全局配置实例
config = HooksConfig()
