"""Main application class for managing character configurations."""

import os
import sys
import shutil
from typing import Dict
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

from config import load_saved_directory, save_directory
from character_scanner import scan_character_files
from file_operations import copy_character_files, get_files_to_overwrite, create_export_zip
from ui_components import create_directory_section, create_copy_tab, create_export_tab


class CharacterManager:
    """Main application class for managing character configurations."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Project Quarm Character Manager")
        self.root.geometry("900x650")
        
        # Set window icon (for title bar and taskbar)
        try:
            # Try to find icon.ico relative to the script or executable
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, 'icon.ico')
            if os.path.exists(icon_path):
                # Access the underlying Tk window for iconbitmap
                self.root.iconbitmap(icon_path)
            else:
                # Try current directory as fallback
                icon_path = 'icon.ico'
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
        except Exception:
            # If icon setting fails, continue without it
            pass
        
        self.quarm_dir = load_saved_directory()
        self.characters: Dict[str, Dict[str, str]] = {}
        self.char_checkboxes: Dict[str, ctk.CTkCheckBox] = {}
        self.directory_valid = False
        
        self.setup_ui()
        if self.quarm_dir and os.path.exists(self.quarm_dir):
            self.scan_characters()
        else:
            self.hide_main_sections()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Directory selection section
        self.dir_entry = create_directory_section(
            main_frame,
            self.quarm_dir,
            self.browse_directory,
            self.scan_characters
        )
        
        # Tabview for Copy and Export tabs
        self.tabs_container = ctk.CTkFrame(main_frame)
        # Don't pack initially - will be shown after directory is set
        
        self.tabview = ctk.CTkTabview(self.tabs_container, corner_radius=8)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Style the tabs to make them more prominent
        try:
            # Access the internal segmented button to customize
            if hasattr(self.tabview, '_segmented_button'):
                seg_button = self.tabview._segmented_button
                seg_button.configure(
                    font=("Arial", 16, "bold"),
                    height=50,
                    selected_color=("#1f538d", "#14375e"),  # Blue when selected
                    selected_hover_color=("#2a5f9f", "#1a4370"),
                    unselected_color=("gray60", "gray40"),
                    unselected_hover_color=("gray65", "gray35")
                )
        except Exception:
            # If styling fails, tabs will still work with defaults
            pass
        
        # Copy Configuration Tab
        copy_tab = self.tabview.add("Copy Configuration")
        self.copy_widgets = create_copy_tab(
            copy_tab,
            self.on_new_char_entry_change,
            self.copy_configuration
        )
        
        # Clear new character entry when target combo is selected
        self.copy_widgets['target_combo'].configure(command=self.on_target_combo_change)
        
        # Update target combo when source changes
        self.copy_widgets['source_combo'].configure(command=self.on_source_combo_change)
        
        # Export Characters Tab
        export_tab = self.tabview.add("Export Character Config")
        self.export_widgets = create_export_tab(
            export_tab,
            self.select_all_chars,
            self.deselect_all_chars,
            self.export_to_zip
        )
        
        # Hide tabs initially until directory is set
        if not self.directory_valid:
            self.tabs_container.pack_forget()
    
    def on_new_char_entry_change(self, event=None):
        """Clear the 'To Character' dropdown when typing in new character field."""
        if self.copy_widgets['new_char_entry'].get().strip():
            self.copy_widgets['target_combo'].set("")
    
    def on_target_combo_change(self, value):
        """Clear the 'New Character' entry when target combo is selected."""
        if value:
            self.copy_widgets['new_char_entry'].delete(0, "end")
    
    def update_target_combo_values(self):
        """Update target combo to exclude the currently selected source character."""
        source = self.copy_widgets['source_combo'].get()
        all_chars = sorted(self.characters.keys())
        
        if source and source in all_chars:
            # Filter out the source character from target list
            target_chars = [char for char in all_chars if char != source]
            self.copy_widgets['target_combo'].configure(values=target_chars)
            
            # If current target is the source, clear it
            current_target = self.copy_widgets['target_combo'].get()
            if current_target == source:
                self.copy_widgets['target_combo'].set("")
        else:
            # Show all characters if no source selected
            self.copy_widgets['target_combo'].configure(values=all_chars)
    
    def on_source_combo_change(self, value):
        """Update target combo when source changes."""
        self.update_target_combo_values()
    
    def browse_directory(self):
        """Open directory picker dialog."""
        directory = filedialog.askdirectory(
            title="Select Project Quarm Directory",
            initialdir=self.quarm_dir or "C:\\"
        )
        if directory:
            self.quarm_dir = directory
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, directory)
            save_directory(directory)
            self.scan_characters()
    
    def scan_characters(self, event=None):
        """Scan the directory for character files."""
        directory = self.dir_entry.get().strip()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid Project Quarm directory.")
            self.hide_main_sections()
            return
        
        self.quarm_dir = directory
        save_directory(directory)
        
        # Clear existing
        self.characters = {}
        self.char_checkboxes = {}
        
        # Clear listbox
        if self.export_widgets['char_listbox']:
            for widget in self.export_widgets['char_listbox'].winfo_children():
                widget.destroy()
        
        try:
            # Scan for characters
            self.characters = scan_character_files(directory)
            
            # Add checkboxes to export tab
            for char_name in sorted(self.characters.keys()):
                checkbox = ctk.CTkCheckBox(self.export_widgets['char_listbox'], text=char_name)
                checkbox.pack(anchor="w", padx=10, pady=2)
                self.char_checkboxes[char_name] = checkbox
            
            # Update combo boxes
            char_list = sorted(self.characters.keys())
            self.copy_widgets['source_combo'].configure(values=char_list)
            
            if char_list:
                self.copy_widgets['source_combo'].set(char_list[0])
                # Update target combo to exclude source
                self.update_target_combo_values()
                if len(char_list) > 1:
                    target_list = [c for c in char_list if c != char_list[0]]
                    if target_list:
                        self.copy_widgets['target_combo'].set(target_list[0])
            
            # Show main sections after successful scan
            self.show_main_sections()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning directory: {str(e)}")
    
    def hide_main_sections(self):
        """Hide the main sections until a valid directory is set."""
        if hasattr(self, 'tabs_container'):
            self.tabs_container.pack_forget()
        self.directory_valid = False
    
    def show_main_sections(self):
        """Show the main sections after a valid directory is set."""
        if hasattr(self, 'tabs_container'):
            self.tabs_container.pack(fill="both", expand=True, padx=10, pady=10)
        self.directory_valid = True
    
    def select_all_chars(self):
        """Select all character checkboxes."""
        for checkbox in self.char_checkboxes.values():
            checkbox.select()
    
    def deselect_all_chars(self):
        """Deselect all character checkboxes."""
        for checkbox in self.char_checkboxes.values():
            checkbox.deselect()
    
    def copy_configuration(self):
        """Copy configuration from source to target character."""
        source = self.copy_widgets['source_combo'].get()
        target = self.copy_widgets['target_combo'].get()
        new_char = self.copy_widgets['new_char_entry'].get().strip()
        
        if not source:
            messagebox.showerror("Error", "Please select a source character.")
            return
        
        if not new_char and not target:
            messagebox.showerror("Error", "Please select a target character or enter a new character name.")
            return
        
        if new_char and target:
            messagebox.showerror("Error", "Please either select a target character OR enter a new character name, not both.")
            return
        
        # Determine target
        if new_char:
            target = new_char
            is_new = True
            # Check if manually entered name matches source
            if new_char.lower() == source.lower():
                messagebox.showerror("Error", "Cannot copy to the same character. The new character name matches the source character.")
                return
            # Check if manually entered name already exists
            if new_char in self.characters:
                messagebox.showerror("Error", f"Character '{new_char}' already exists. Please select it from the 'To Character' dropdown or choose a different name.")
                return
        else:
            is_new = False
            # Check if source and target are the same
            if source == target:
                messagebox.showerror("Error", "Cannot copy to the same character. Please select a different target character.")
                return
        
        # Check which file types to copy
        copy_ui = self.copy_widgets['ui_checkbox'].get()
        copy_config = self.copy_widgets['config_checkbox'].get()
        copy_spellsets = self.copy_widgets['spellsets_checkbox'].get()
        
        if not (copy_ui or copy_config or copy_spellsets):
            messagebox.showerror("Error", "Please select at least one file type to copy.")
            return
        
        # Check which files will be overwritten
        files_to_overwrite = []
        if not is_new:
            files_to_overwrite = get_files_to_overwrite(
                target, self.quarm_dir, copy_ui, copy_config, copy_spellsets
            )
        
        # Build confirmation message
        file_types = []
        if copy_ui:
            file_types.append("UI")
        if copy_config:
            file_types.append("Config")
        if copy_spellsets:
            file_types.append("Spellsets")
        
        if is_new:
            confirm_msg = f"Are you sure you want to create {', '.join(file_types)} file(s) for new character '{target}' from '{source}'?"
        else:
            confirm_msg = f"Are you sure you want to overwrite files for '{target}' from '{source}'?\n\n"
            confirm_msg += f"This will overwrite the following existing file(s):\n"
            if files_to_overwrite:
                for file in files_to_overwrite:
                    confirm_msg += f"  • {file}\n"
            else:
                confirm_msg += f"  • {', '.join(file_types)} file(s) (will be created if they don't exist)\n"
            confirm_msg += f"\nSelected file types: {', '.join(file_types)}"
        
        if not messagebox.askyesno("Confirm", confirm_msg):
            return
        
        # Perform copy
        try:
            copied_files = copy_character_files(
                source, target, self.characters, self.quarm_dir,
                copy_ui, copy_config, copy_spellsets
            )
            
            if copied_files:
                messagebox.showinfo("Success", f"Successfully copied {len(copied_files)} file(s):\n" + "\n".join(copied_files))
                # Refresh scan to update character list, but preserve input selections
                # Store current selections
                current_source = self.copy_widgets['source_combo'].get()
                current_target = self.copy_widgets['target_combo'].get()
                current_new_char = self.copy_widgets['new_char_entry'].get()
                
                # Refresh scan
                self.scan_characters()
                
                # Restore selections
                if current_source and current_source in self.characters:
                    self.copy_widgets['source_combo'].set(current_source)
                if current_target and current_target in self.characters:
                    self.copy_widgets['target_combo'].set(current_target)
                if current_new_char:
                    self.copy_widgets['new_char_entry'].delete(0, "end")
                    self.copy_widgets['new_char_entry'].insert(0, current_new_char)
            else:
                messagebox.showwarning("Warning", "No files were copied. The source character may not have the selected file types.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while copying files:\n{str(e)}")
    
    def export_to_zip(self):
        """Export selected characters to a ZIP file."""
        # Get selected characters
        selected_chars = [name for name, checkbox in self.char_checkboxes.items() if checkbox.get()]
        
        if not selected_chars:
            messagebox.showerror("Error", "Please select at least one character to export.")
            return
        
        # Check which file types to export
        export_ui = self.export_widgets['export_ui_checkbox'].get()
        export_config = self.export_widgets['export_config_checkbox'].get()
        export_spellsets = self.export_widgets['export_spellsets_checkbox'].get()
        
        if not (export_ui or export_config or export_spellsets):
            messagebox.showerror("Error", "Please select at least one file type to export.")
            return
        
        # Ask for save location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"quarm_characters_export_{timestamp}.zip"
        zip_path = filedialog.asksaveasfilename(
            title="Save Export ZIP",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            initialfile=default_filename
        )
        
        if not zip_path:
            return
        
        zip_path_temp = None
        try:
            zip_path_temp, filename = create_export_zip(
                selected_chars, self.characters,
                export_ui, export_config, export_spellsets
            )
            
            # Move temp file to user's chosen location
            shutil.move(zip_path_temp, zip_path)
            
            messagebox.showinfo("Success", f"Successfully exported {len(selected_chars)} character(s) to:\n{zip_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting:\n{str(e)}")
            if zip_path_temp and os.path.exists(zip_path_temp):
                os.unlink(zip_path_temp)
