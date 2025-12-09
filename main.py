"""Main entry point for the application."""

import customtkinter as ctk
from character_manager import CharacterManager

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    """Main entry point."""
    root = ctk.CTk()
    app = CharacterManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
