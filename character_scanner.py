"""Character file scanning functionality."""

import os
from typing import Dict, Set


def scan_character_files(directory: str) -> Dict[str, Dict[str, str]]:
    """
    Scan directory for character files.
    
    Returns a dictionary mapping character names to their file paths:
    {
        'CharacterName': {
            'config': 'path/to/CharacterName_pq.proj.ini',
            'ui': 'path/to/UI_CharacterName_pq.proj.ini',
            'spellsets': 'path/to/CharacterName_spellsets.ini'
        }
    }
    """
    characters: Dict[str, Dict[str, str]] = {}
    char_names: Set[str] = set()
    
    # Scan for config files
    for file in os.listdir(directory):
        if file.endswith("_pq.proj.ini") and not file.startswith("UI_"):
            char_name = file.replace("_pq.proj.ini", "")
            char_names.add(char_name)
    
    # Scan for UI files
    for file in os.listdir(directory):
        if file.startswith("UI_") and file.endswith("_pq.proj.ini"):
            char_name = file.replace("UI_", "").replace("_pq.proj.ini", "")
            char_names.add(char_name)
    
    # Scan for spellsets
    for file in os.listdir(directory):
        if file.endswith("_spellsets.ini"):
            char_name = file.replace("_spellsets.ini", "")
            char_names.add(char_name)
    
    # Build character info
    for char_name in sorted(char_names):
        char_info = {
            'config': None,
            'ui': None,
            'spellsets': None
        }
        
        config_file = os.path.join(directory, f"{char_name}_pq.proj.ini")
        ui_file = os.path.join(directory, f"UI_{char_name}_pq.proj.ini")
        spellsets_file = os.path.join(directory, f"{char_name}_spellsets.ini")
        
        if os.path.exists(config_file):
            char_info['config'] = config_file
        if os.path.exists(ui_file):
            char_info['ui'] = ui_file
        if os.path.exists(spellsets_file):
            char_info['spellsets'] = spellsets_file
        
        # Only add if at least one file exists
        if any(char_info.values()):
            characters[char_name] = char_info
    
    return characters

