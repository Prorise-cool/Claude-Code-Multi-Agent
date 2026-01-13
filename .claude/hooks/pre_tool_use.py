#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PreToolUse Hook 入口"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from handlers.pre_tool_use import PreToolUseHook

if __name__ == '__main__':
    sys.exit(PreToolUseHook().run())
