#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PreCompact Hook 入口"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from handlers.pre_compact import PreCompactHook

if __name__ == '__main__':
    sys.exit(PreCompactHook().run())
