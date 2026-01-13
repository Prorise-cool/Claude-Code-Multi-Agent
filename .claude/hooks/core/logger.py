"""
Hooks 系统统一日志管理
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
from .config import config

class HookLogger:
    """统一的 Hook 日志管理器"""

    def __init__(self, hook_name: str):
        self.hook_name = hook_name
        self.log_file = config.logs_dir / f'{hook_name}.json'

    def log(self, event_type: str, data: dict, summary: Optional[str] = None) -> None:
        """记录日志条目"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "hook": self.hook_name,
            "event": event_type,
            "summary": summary or self._auto_summary(event_type, data),
            "data": self._sanitize_data(data)
        }
        self._append_entry(entry)

    def _auto_summary(self, event_type: str, data: dict) -> str:
        """自动生成摘要"""
        if 'tool_name' in data:
            return f"{event_type}: {data['tool_name']}"
        if 'prompt' in data:
            prompt = data['prompt'][:50] + '...' if len(data.get('prompt', '')) > 50 else data.get('prompt', '')
            return f"{event_type}: {prompt}"
        return event_type

    def _sanitize_data(self, data: dict) -> dict:
        """清理敏感数据，只保留关键信息"""
        sanitized = {}
        safe_keys = [
            'tool_name', 'file_path', 'command', 'session_id', 'status',
            'prompt', 'systemMessage', 'hookEventName', 
            'additionalContext_length', 'additionalContext_preview',
            'tool_input', 'tool_result'
        ]
        # 完整记录的字段（不截断）
        full_record_keys = [
            'original_prompt', 'enhanced_prompt', 'enhancement_reason', 'prompt_type'
        ]
        
        for key in safe_keys:
            if key in data:
                value = data[key]
                # 截断过长的值（但优化提示词相关字段不截断）
                if isinstance(value, str) and len(value) > 200:
                    value = value[:200] + '...'
                sanitized[key] = value
        
        # 完整记录优化提示词相关字段（不截断，供人工审查）
        for key in full_record_keys:
            if key in data:
                sanitized[key] = data[key]  # 完整记录，不截断
                
        return sanitized

    def _append_entry(self, entry: dict) -> None:
        """追加日志条目到文件"""
        entries = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except (json.JSONDecodeError, ValueError):
                entries = []

        entries.append(entry)

        # 限制条目数量
        if len(entries) > config.max_log_entries:
            entries = entries[-config.max_log_entries:]

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)

    def error(self, message: str, exception: Optional[Exception] = None) -> None:
        """记录错误"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "hook": self.hook_name,
            "event": "error",
            "message": message,
            "exception": str(exception) if exception else None
        }
        self._append_entry(entry)

    def info(self, message: str) -> None:
        """记录信息"""
        self.log("info", {"message": message}, summary=message)

    def warning(self, message: str) -> None:
        """记录警告"""
        self.log("warning", {"message": message}, summary=message)

    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.log("debug", {"message": message}, summary=message)


# 全局实例（用于通用日志）
logger = HookLogger('general')
