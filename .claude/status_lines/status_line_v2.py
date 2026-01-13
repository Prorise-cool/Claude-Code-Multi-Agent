#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv是可选的


def log_status_line(input_data, status_line_output, error_message=None):
    """将状态行事件记录到logs目录。"""
    # 确保logs目录存在
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'status_line.json'
    
    # 读取现有日志数据或初始化空列表
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []
    
    # 创建包含输入数据和生成输出的日志条目
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "version": "v2",
        "input_data": input_data,
        "status_line_output": status_line_output,
    }
    
    if error_message:
        log_entry["error"] = error_message
    
    # 追加日志条目
    log_data.append(log_entry)
    
    # 格式化写回文件
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def get_last_prompt(session_id):
    """获取当前会话的最后一个提示。"""
    # 使用JSON结构
    session_file = Path(f".claude/data/sessions/{session_id}.json")
    
    if not session_file.exists():
        return None, f"会话文件 {session_file} 不存在"
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
            prompts = session_data.get("prompts", [])
            if prompts:
                return prompts[-1], None
            return None, "会话中没有提示"
    except Exception as e:
        return None, f"读取会话文件错误: {str(e)}"


def generate_status_line(input_data):
    """生成显示最后一个提示的状态行。"""
    # 从输入数据中提取会话ID
    session_id = input_data.get('session_id', 'unknown')
    
    # 获取模型名称作为前缀
    model_info = input_data.get('model', {})
    model_name = model_info.get('display_name', 'Claude')
    
    # 获取最后一个提示
    prompt, error = get_last_prompt(session_id)
    
    if error:
        # 记录错误但显示默认消息
        log_status_line(input_data, f"[{model_name}] 💭 无最近提示", error)
        return f"\033[36m[{model_name}]\033[0m \033[90m💭 无最近提示\033[0m"
    
    # 格式化状态行的提示
    # 删除换行符和过多的空白
    prompt = ' '.join(prompt.split())
    
    # 根据提示类型进行颜色编码
    if prompt.startswith('/'):
        # 命令提示 - 黄色
        prompt_color = "\033[33m"
        icon = "⚡"
    elif '?' in prompt:
        # 问题 - 蓝色
        prompt_color = "\033[34m"
        icon = "❓"
    elif any(word in prompt.lower() for word in ['create', 'write', 'add', 'implement', 'build']):
        # 创建任务 - 绿色
        prompt_color = "\033[32m"
        icon = "💡"
    elif any(word in prompt.lower() for word in ['fix', 'debug', 'error', 'issue']):
        # 修复/调试任务 - 红色
        prompt_color = "\033[31m"
        icon = "🐛"
    elif any(word in prompt.lower() for word in ['refactor', 'improve', 'optimize']):
        # 重构任务 - 洋红色
        prompt_color = "\033[35m"
        icon = "♻️"
    else:
        # 默认 - 白色
        prompt_color = "\033[37m"
        icon = "💬"
    
    # 构建状态行
    status_line = f"\033[36m[{model_name}]\033[0m {icon} {prompt_color}{prompt}\033[0m"
    
    return status_line


def main():
    try:
        # 从stdin读取JSON输入
        input_data = json.loads(sys.stdin.read())
        
        # 生成状态行
        status_line = generate_status_line(input_data)
        
        # 记录状态行事件（无错误，因为成功）
        log_status_line(input_data, status_line)
        
        # 输出状态行（stdout的第一行成为状态行）
        print(status_line)
        
        # 成功
        sys.exit(0)
        
    except json.JSONDecodeError:
        # 优雅处理JSON解码错误 - 输出基本状态
        print("\033[31m[Claude] 💭 JSON错误\033[0m")
        sys.exit(0)
    except Exception as e:
        # 优雅处理任何其他错误 - 输出基本状态
        print(f"\033[31m[Claude] 💭 错误: {str(e)}\033[0m")
        sys.exit(0)


if __name__ == '__main__':
    main()
