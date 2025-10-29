"""Configuration module for Modern Task Manager."""

import customtkinter as ctk

# Modern color scheme for CustomTkinter
COLORS = {
    'bg': '#1a1a2e',
    'card_bg': '#16213e',
    'accent': '#0f3460',
    'accent_hover': '#0d7cff',
    'text': '#eeeeee',
    'text_secondary': '#a8a8a8',
    'danger': '#e94560',
    'success': '#00ff88'
}

# Default workspaces
DEFAULT_WORKSPACES = ["Развитие", "Bug Bounty", "CTF", "Тренировки"]

# File settings
DATA_FILE = "task_data.json"

# UI settings
WINDOW_SIZE = "1100x750"
WINDOW_TITLE = "Progress Tracker"

# CustomTkinter settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
