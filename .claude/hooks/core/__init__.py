"""
Claude Code Hooks 核心模块
提供统一的配置、日志、LLM 客户端等基础设施
"""

from .config import HooksConfig as Config, config
from .logger import HookLogger
from .ollama_client import OllamaClient
from .base_hook import BaseHook, HookResult

__all__ = ['Config', 'HookLogger', 'OllamaClient', 'BaseHook', 'HookResult']
