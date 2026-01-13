#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PostToolUse Hook 入口"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from handlers.post_tool_use import PostToolUseHook

if __name__ == '__main__':
    sys.exit(PostToolUseHook().run())
