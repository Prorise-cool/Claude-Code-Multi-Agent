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
    log_file = log_dir / "status_line.json"

    # 读取现有日志数据或初始化空列表
    if log_file.exists():
        with open(log_file, "r") as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # 创建包含输入数据和生成输出的日志条目
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "version": "v3",
        "input_data": input_data,
        "status_line_output": status_line_output,
    }

    if error_message:
        log_entry["error"] = error_message

    # 追加日志条目
    log_data.append(log_entry)

    # 格式化写回文件
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def get_session_data(session_id):
    """获取会话数据，包括代理名称和提示。"""
    session_file = Path(f".claude/data/sessions/{session_id}.json")

    if not session_file.exists():
        return None, f"会话文件 {session_file} 不存在"

    try:
        with open(session_file, "r") as f:
            session_data = json.load(f)
            return session_data, None
    except Exception as e:
        return None, f"读取会话文件错误: {str(e)}"


def truncate_prompt(prompt, max_length=75):
    """将提示截断到指定长度。"""
    # 删除换行符和过多的空白
    prompt = " ".join(prompt.split())

    if len(prompt) > max_length:
        return prompt[: max_length - 3] + "..."
    return prompt


def get_prompt_icon(prompt):
    """根据提示类型获取图标。"""
    if prompt.startswith("/"):
        return "⚡"
    elif "?" in prompt:
        return "❓"
    elif any(
        word in prompt.lower()
        for word in ["create", "write", "add", "implement", "build"]
    ):
        return "💡"
    elif any(word in prompt.lower() for word in ["fix", "debug", "error", "issue"]):
        return "🐛"
    elif any(word in prompt.lower() for word in ["refactor", "improve", "optimize"]):
        return "♻️"
    else:
        return "💬"


def generate_status_line(input_data):
    """生成包含代理名称和最后3个提示的状态行。"""
    # 从输入数据中提取会话ID
    session_id = input_data.get("session_id", "unknown")

    # 获取模型名称
    model_info = input_data.get("model", {})
    model_name = model_info.get("display_name", "Claude")

    # 获取会话数据
    session_data, error = get_session_data(session_id)

    if error:
        # 记录错误但显示默认消息
        log_status_line(input_data, f"[{model_name}] 💭 无会话数据", error)
        return f"\033[36m[{model_name}]\033[0m \033[90m💭 无会话数据\033[0m"

    # 提取代理名称和提示
    agent_name = session_data.get("agent_name", "Agent")
    prompts = session_data.get("prompts", [])

    # 构建状态行组件
    parts = []

    # 代理名称 - 亮绿色
    parts.append(f"\033[91m[{agent_name}]\033[0m")

    # 模型名称 - 蓝色
    parts.append(f"\033[34m[{model_name}]\033[0m")

    # 最后3个提示（最新的在前）
    if prompts:
        # 当前提示 - 白色/亮色
        current_prompt = prompts[-1]
        icon = get_prompt_icon(current_prompt)
        truncated = truncate_prompt(current_prompt, 75)
        parts.append(f"{icon} \033[97m{truncated}\033[0m")

        # 上一个提示 - 灰色
        if len(prompts) > 1:
            prev_prompt = prompts[-2]
            truncated = truncate_prompt(prev_prompt, 50)
            parts.append(f"\033[90m{truncated}\033[0m")

        # 两个提示前 - 深灰色
        if len(prompts) > 2:
            older_prompt = prompts[-3]
            truncated = truncate_prompt(older_prompt, 40)
            parts.append(f"\033[90m{truncated}\033[0m")
    else:
        parts.append("\033[90m💭 尚无提示\033[0m")

    # 使用分隔符连接
    status_line = " | ".join(parts)

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
        print("\033[31m[Agent] [Claude] 💭 JSON错误\033[0m")
        sys.exit(0)
    except Exception as e:
        # 优雅处理任何其他错误 - 输出基本状态
        print(f"\033[31m[Agent] [Claude] 💭 错误: {str(e)}\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()
