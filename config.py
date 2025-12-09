"""Configuration management for the application."""

import json
import os
from pathlib import Path
from typing import Optional


# Use standard Windows AppData\Local directory for config
# This creates: C:\Users\<Username>\AppData\Local\QuarmQuickCharacterCopy\config.json
APP_NAME = "QuarmQuickCharacterCopy"
CONFIG_DIR = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

# Create config directory if it doesn't exist
CONFIG_DIR.mkdir(exist_ok=True)


def load_saved_directory() -> Optional[str]:
    """Load saved directory from config file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('quarm_directory')
        except Exception:
            pass
    return None


def save_directory(directory: str):
    """Save directory to config file."""
    config = {'quarm_directory': directory}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

