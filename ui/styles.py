"""Styling configuration for Modern Task Manager using CustomTkinter."""

import customtkinter as ctk
from config import COLORS


class StyleManager:
    """Manages CustomTkinter styles and theme configuration."""
    
    def __init__(self):
        self.colors = COLORS
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    @property
    def bg_color(self):
        return self.colors['bg']
    
    @property
    def card_bg_color(self):
        return self.colors['card_bg']
    
    @property
    def accent_color(self):
        return self.colors['accent']
    
    @property
    def accent_hover_color(self):
        return self.colors['accent_hover']
    
    @property
    def text_color(self):
        return self.colors['text']
    
    @property
    def text_secondary_color(self):
        return self.colors['text_secondary']
    
    @property
    def danger_color(self):
        return self.colors['danger']
    
    @property
    def success_color(self):
        return self.colors['success']
