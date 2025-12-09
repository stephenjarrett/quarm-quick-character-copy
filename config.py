"""Configuration management for the application."""

import json
from pathlib import Path
from typing import Optional


CONFIG_FILE = Path("config.json")


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

