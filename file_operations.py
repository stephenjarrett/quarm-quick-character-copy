"""File operations for copying and exporting character files."""

import os
import shutil
import zipfile
import tempfile
from typing import Dict, List, Tuple
from datetime import datetime


def copy_character_files(
    source_char: str,
    target_char: str,
    characters: Dict[str, Dict[str, str]],
    directory: str,
    copy_ui: bool,
    copy_config: bool,
    copy_spellsets: bool
) -> List[str]:
    """
    Copy character files from source to target.
    
    Returns list of copied file names.
    """
    copied_files = []
    
    if copy_ui and characters[source_char]['ui']:
        source_file = characters[source_char]['ui']
        target_file = os.path.join(directory, f"UI_{target_char}_pq.proj.ini")
        shutil.copy2(source_file, target_file)
        copied_files.append(f"UI_{target_char}_pq.proj.ini")
    
    if copy_config and characters[source_char]['config']:
        source_file = characters[source_char]['config']
        target_file = os.path.join(directory, f"{target_char}_pq.proj.ini")
        shutil.copy2(source_file, target_file)
        copied_files.append(f"{target_char}_pq.proj.ini")
    
    if copy_spellsets and characters[source_char]['spellsets']:
        source_file = characters[source_char]['spellsets']
        target_file = os.path.join(directory, f"{target_char}_spellsets.ini")
        shutil.copy2(source_file, target_file)
        copied_files.append(f"{target_char}_spellsets.ini")
    
    return copied_files


def get_files_to_overwrite(
    target_char: str,
    directory: str,
    copy_ui: bool,
    copy_config: bool,
    copy_spellsets: bool
) -> List[str]:
    """Get list of files that will be overwritten."""
    files_to_overwrite = []
    
    if copy_ui and os.path.exists(os.path.join(directory, f"UI_{target_char}_pq.proj.ini")):
        files_to_overwrite.append(f"UI_{target_char}_pq.proj.ini")
    if copy_config and os.path.exists(os.path.join(directory, f"{target_char}_pq.proj.ini")):
        files_to_overwrite.append(f"{target_char}_pq.proj.ini")
    if copy_spellsets and os.path.exists(os.path.join(directory, f"{target_char}_spellsets.ini")):
        files_to_overwrite.append(f"{target_char}_spellsets.ini")
    
    return files_to_overwrite


def create_export_zip(
    selected_chars: List[str],
    characters: Dict[str, Dict[str, str]],
    export_ui: bool,
    export_config: bool,
    export_spellsets: bool
) -> Tuple[str, str]:
    """
    Create a ZIP file with exported character files.
    
    Returns tuple of (zip_path, filename).
    """
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
        zip_path = tmp_file.name
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quarm_characters_export_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for char_name in selected_chars:
            if char_name not in characters:
                continue
            
            char_info = characters[char_name]
            
            # Save files flat at root of zip (no character folders)
            if export_ui and char_info['ui']:
                zipf.write(char_info['ui'], f"UI_{char_name}_pq.proj.ini")
            
            if export_config and char_info['config']:
                zipf.write(char_info['config'], f"{char_name}_pq.proj.ini")
            
            if export_spellsets and char_info['spellsets']:
                zipf.write(char_info['spellsets'], f"{char_name}_spellsets.ini")
    
    return zip_path, filename

