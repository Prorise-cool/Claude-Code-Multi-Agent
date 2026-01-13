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
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv是可选的


def log_status_line(input_data, status_line_output):
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
        "input_data": input_data,
        "status_line_output": status_line_output
    }
    
    # 追加日志条目
    log_data.append(log_entry)
    
    # 格式化写回文件
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def get_git_branch():
    """如果在git仓库中，获取当前git分支。"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_status():
    """获取git状态指示器。"""
    try:
        # 检查是否有未提交的更改
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                lines = changes.split('\n')
                return f"±{len(lines)}"
    except Exception:
        pass
    return ""


def generate_status_line(input_data):
    """根据输入数据生成状态行。"""
    parts = []
    
    # 模型显示名称
    model_info = input_data.get('model', {})
    model_name = model_info.get('display_name', 'Claude')
    parts.append(f"\033[36m[{model_name}]\033[0m")  # 青色
    
    # 当前目录
    workspace = input_data.get('workspace', {})
    current_dir = workspace.get('current_dir', '')
    if current_dir:
        dir_name = os.path.basename(current_dir)
        parts.append(f"\033[34m📁 {dir_name}\033[0m")  # 蓝色
    
    # Git分支和状态
    git_branch = get_git_branch()
    if git_branch:
        git_status = get_git_status()
        git_info = f"🌿 {git_branch}"
        if git_status:
            git_info += f" {git_status}"
        parts.append(f"\033[32m{git_info}\033[0m")  # 绿色
    
    # 版本信息（可选，较小）
    version = input_data.get('version', '')
    if version:
        parts.append(f"\033[90mv{version}\033[0m")  # 灰色
    
    return " | ".join(parts)


def main():
    try:
        # 从stdin读取JSON输入
        input_data = json.loads(sys.stdin.read())
        
        # 生成状态行
        status_line = generate_status_line(input_data)
        
        # 记录状态行事件
        log_status_line(input_data, status_line)
        
        # 输出状态行（stdout的第一行成为状态行）
        print(status_line)
        
        # 成功
        sys.exit(0)
        
    except json.JSONDecodeError:
        # 优雅处理JSON解码错误 - 输出基本状态
        print("\033[31m[Claude] 📁 未知\033[0m")
        sys.exit(0)
    except Exception:
        # 优雅处理任何其他错误 - 输出基本状态
        print("\033[31m[Claude] 📁 错误\033[0m")
        sys.exit(0)


if __name__ == '__main__':
    main()
