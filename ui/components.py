"""UI Components for Modern Task Manager."""

import tkinter as tk
from datetime import datetime, timedelta

from ui.styles import StyleManager


class CalendarComponent:
    """Handles calendar rendering and interactions."""
    
    def __init__(self, style_manager: StyleManager, get_daily_rating_callback):
        self.canvas = None  # Will be set from outside
        self.style = style_manager
        self.get_daily_rating_callback = get_daily_rating_callback
        self.current_date = datetime.now()
    
    def update_calendar(self, on_day_click_callback):
        """Update calendar display."""
        self.canvas.delete("all")
        self.on_day_click = on_day_click_callback
        
        # Calendar dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas not yet rendered
            return
        
        cell_size = min((canvas_width - 40) // 7, (canvas_height - 60) // 6)
        start_x = (canvas_width - cell_size * 7) // 2
        start_y = 40
        
        # Day headers (Sunday = 6, Monday = 0 in Python)
        # But we show Monday first
        days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
        for i, day in enumerate(days):
            x = start_x + i * cell_size + cell_size // 2
            self.canvas.create_text(x, start_y - 20, text=day, 
                                   fill=self.style.text_secondary_color,
                                   font=('Arial', 12, 'bold'))
        
        # Get month data
        year = self.current_date.year
        month = self.current_date.month
        
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
        
        # Python weekday: Monday=0, Sunday=6
        # We want to show Sunday-Saturday
        start_col = (first_day.weekday() + 1) % 7  # Convert to Sun=0, Mon=1...
        current_day = first_day
        
        # Draw days
        row = 0
        col = start_col
        
        while current_day <= last_day:
            day_str = current_day.strftime("%Y-%m-%d")
            day_number = current_day.day
            
            x = start_x + col * cell_size + cell_size // 2
            y = start_y + row * cell_size + cell_size // 2
            
            # Day circle
            radius = cell_size // 2 - 5
            rating = self.get_daily_rating_callback(day_str)
            
            # Color based on rating with smooth gradient every 0.1
            if rating > 0:
                if rating < 2.0:
                    # Red to Orange: FF0000 → FF8000 (1.0 → 2.0)
                    progress = (rating - 1.0) / 1.0
                    red = 255
                    green = int(0 + progress * 128)  # 0 → 128
                    blue = 0
                    color = f'#{red:02x}{green:02x}{blue:02x}'
                elif rating < 3.0:
                    # Orange to Yellow: FF8000 → FFFF00 (2.0 → 3.0)
                    progress = (rating - 2.0) / 1.0
                    red = 255
                    green = int(128 + progress * 127)  # 128 → 255
                    blue = 0
                    color = f'#{red:02x}{green:02x}{blue:02x}'
                elif rating < 4.0:
                    # Yellow to Olive green: FFFF00 → 808000 (3.0 → 4.0)
                    progress = (rating - 3.0) / 1.0
                    red = int(255 - progress * 127)  # 255 → 128
                    green = int(255 - progress * 127)  # 255 → 128
                    blue = 0
                    color = f'#{red:02x}{green:02x}{blue:02x}'
                else:
                    # Olive green to Bright green: 808000 → 00FF00 (4.0 → 5.0)
                    progress = (rating - 4.0) / 1.0
                    red = int(128 - progress * 128)  # 128 → 0
                    green = 255
                    blue = 0
                    color = f'#{red:02x}{green:02x}{blue:02x}'
            else:
                color = '#2a2a2a'
            
            # Highlight current day
            if current_day.date() == datetime.now().date():
                self.canvas.create_oval(x-radius-2, y-radius-2, 
                                       x+radius+2, y+radius+2,
                                       fill=self.style.accent_color, outline="")
            
            # Day circle
            day_circle = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                               fill=color, outline="")
            
            # Determine text color based on background brightness
            # If rating is bright (yellow range 2-4), use dark text
            text_color = '#000000' if 2.0 <= rating < 4.0 else '#ffffff'
            text_color = '#000000' if rating == 0 else text_color
            
            # Day number
            self.canvas.create_text(x, y-8, text=str(day_number),
                                   fill=text_color,
                                   font=('Arial', 12, 'bold'))
            
            # Rating
            if rating > 0:
                self.canvas.create_text(x, y+8, text=f"{rating:.1f}",
                                       fill=text_color,
                                       font=('Arial', 10))
            
            # Bind click event with proper closure
            def make_click_handler(day):
                return lambda e: self.on_day_click(day)
            
            self.canvas.tag_bind(day_circle, '<Button-1>', make_click_handler(day_str))
            
            current_day += timedelta(days=1)
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def get_month_label_text(self) -> str:
        """Get formatted month/year label text."""
        return self.current_date.strftime("%B %Y")
    
    def previous_month(self):
        """Navigate to previous month."""
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
    
    def next_month(self):
        """Navigate to next month."""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1, day=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1, day=1)
    
    def go_today(self):
        """Navigate to current month."""
        self.current_date = datetime.now()

