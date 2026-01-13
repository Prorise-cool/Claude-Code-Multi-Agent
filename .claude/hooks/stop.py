#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyttsx3"]
# ///
"""Stop Hook 入口"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from handlers.stop import StopHook

if __name__ == '__main__':
    sys.exit(StopHook().run())
