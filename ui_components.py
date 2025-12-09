"""UI component builders for the application."""

import customtkinter as ctk
from typing import Callable


def create_directory_section(parent, quarm_dir: str, on_browse: Callable, on_scan: Callable) -> ctk.CTkEntry:
    """Create the directory selection section."""
    dir_frame = ctk.CTkFrame(parent, fg_color="transparent")
    dir_frame.pack(fill="x", padx=10, pady=10)
    
    ctk.CTkLabel(dir_frame, text="Project Quarm Directory:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
    
    dir_input_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
    dir_input_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    dir_entry = ctk.CTkEntry(dir_input_frame, width=300)
    dir_entry.pack(side="left", padx=(0, 10))
    if quarm_dir:
        dir_entry.insert(0, quarm_dir)
    
    # Auto-scan when Enter is pressed or field loses focus
    dir_entry.bind("<Return>", lambda e: on_scan())
    dir_entry.bind("<FocusOut>", lambda e: on_scan())
    
    ctk.CTkButton(dir_input_frame, text="Browse", command=on_browse, width=100).pack(side="left")
    
    return dir_entry


def create_copy_tab(parent, on_new_char_change: Callable, on_copy: Callable) -> dict:
    """Create the Copy Configuration tab and return widget references."""
    widgets = {}
    
    # Use parent directly - it's already the tab panel with proper background
    copy_content_frame = parent
    
    # Source character selection
    ctk.CTkLabel(copy_content_frame, text="From Character:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(15, 3))
    widgets['source_combo'] = ctk.CTkComboBox(copy_content_frame, values=[], width=300, state="readonly")
    widgets['source_combo'].pack(anchor="w", padx=20, pady=(0, 10))
    
    # Target character selection
    ctk.CTkLabel(copy_content_frame, text="To Character:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 3))
    widgets['target_combo'] = ctk.CTkComboBox(copy_content_frame, values=[], width=300, state="readonly")
    widgets['target_combo'].pack(anchor="w", padx=20, pady=(0, 10))
    
    # New character entry
    ctk.CTkLabel(copy_content_frame, text="Or New Character:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 3))
    widgets['new_char_entry'] = ctk.CTkEntry(copy_content_frame, placeholder_text="Enter character name", width=300)
    widgets['new_char_entry'].pack(anchor="w", padx=20, pady=(0, 10))
    widgets['new_char_entry'].bind("<KeyRelease>", lambda e: on_new_char_change())
    
    # File type checkboxes
    ctk.CTkLabel(copy_content_frame, text="File Types to Copy:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 3))
    
    checkbox_frame = ctk.CTkFrame(copy_content_frame, fg_color="transparent")
    checkbox_frame.pack(fill="x", padx=20, pady=(0, 12))
    
    widgets['ui_checkbox'] = ctk.CTkCheckBox(checkbox_frame, text="UI", state="normal")
    widgets['ui_checkbox'].pack(side="left", padx=10)
    widgets['ui_checkbox'].select()
    
    widgets['config_checkbox'] = ctk.CTkCheckBox(checkbox_frame, text="Friends/Ignore/Ability Bars", state="normal")
    widgets['config_checkbox'].pack(side="left", padx=10)
    widgets['config_checkbox'].select()
    
    widgets['spellsets_checkbox'] = ctk.CTkCheckBox(checkbox_frame, text="Spellsets", state="normal")
    widgets['spellsets_checkbox'].pack(side="left", padx=10)
    widgets['spellsets_checkbox'].select()
    
    # Copy button - left aligned
    ctk.CTkButton(copy_content_frame, text="Copy Configuration", command=on_copy,
                 font=("Arial", 12, "bold"), height=40).pack(anchor="w", padx=20, pady=(10, 15))
    
    return widgets


def create_export_tab(parent, on_select_all: Callable, on_deselect_all: Callable, on_export: Callable) -> dict:
    """Create the Export Characters tab and return widget references."""
    widgets = {}
    
    # Use parent directly - it's already the tab panel with proper background
    export_content_frame = parent
    
    # Main horizontal container for character list and controls
    main_export_frame = ctk.CTkFrame(export_content_frame, fg_color="transparent")
    main_export_frame.pack(fill="both", expand=True, padx=20, pady=(15, 0))
    
    # Left side - Character list
    left_frame = ctk.CTkFrame(main_export_frame, fg_color="transparent")
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    ctk.CTkLabel(left_frame, text="Select Characters to Export:", font=("Arial", 12)).pack(anchor="w", pady=(0, 3))
    
    # Scrollable character list with border
    widgets['char_listbox'] = ctk.CTkScrollableFrame(left_frame, border_width=2, border_color=("gray60", "gray40"))
    widgets['char_listbox'].pack(fill="both", expand=True)
    
    # Right side - Controls and options
    right_frame = ctk.CTkFrame(main_export_frame, fg_color="transparent")
    right_frame.pack(side="right", fill="y", padx=(10, 0))
    
    # Select All/Deselect All buttons
    ctk.CTkLabel(right_frame, text="Selection:", font=("Arial", 12)).pack(anchor="w", pady=(0, 3))
    export_controls_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    export_controls_frame.pack(fill="x", pady=(0, 15))
    
    ctk.CTkButton(export_controls_frame, text="Select All", command=on_select_all, width=120).pack(fill="x", pady=(0, 3))
    ctk.CTkButton(export_controls_frame, text="Deselect All", command=on_deselect_all, width=120).pack(fill="x")
    
    # Export file types
    ctk.CTkLabel(right_frame, text="Export File Types:", font=("Arial", 12)).pack(anchor="w", pady=(0, 3))
    
    export_checkbox_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    export_checkbox_frame.pack(fill="x", pady=(0, 15))
    
    widgets['export_ui_checkbox'] = ctk.CTkCheckBox(export_checkbox_frame, text="UI Files", state="normal")
    widgets['export_ui_checkbox'].pack(anchor="w", pady=2)
    widgets['export_ui_checkbox'].select()
    
    widgets['export_config_checkbox'] = ctk.CTkCheckBox(export_checkbox_frame, text="Config Files", state="normal")
    widgets['export_config_checkbox'].pack(anchor="w", pady=2)
    widgets['export_config_checkbox'].select()
    
    widgets['export_spellsets_checkbox'] = ctk.CTkCheckBox(export_checkbox_frame, text="Spellsets", state="normal")
    widgets['export_spellsets_checkbox'].pack(anchor="w", pady=2)
    widgets['export_spellsets_checkbox'].select()
    
    # Export button - left aligned
    ctk.CTkButton(export_content_frame, text="Export Selected to ZIP", command=on_export,
                 font=("Arial", 12, "bold"), height=40).pack(anchor="w", padx=20, pady=(10, 15))
    
    return widgets
