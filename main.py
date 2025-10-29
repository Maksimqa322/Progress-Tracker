"""Modern Task Manager - Main application with CustomTkinter."""

import customtkinter as ctk
from datetime import datetime, timedelta
from config import WINDOW_SIZE, WINDOW_TITLE, DEFAULT_WORKSPACES
from data_manager import DataManager
from ui.styles import StyleManager
from ui.dialogs import DialogManager
from ui.components import CalendarComponent


class ModernTaskManager:
    """Main application class for Modern Task Manager."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Initialize managers
        self.data_manager = DataManager()
        self.style_manager = StyleManager()
        self.dialog_manager = DialogManager(root, self.style_manager)
        
        # Data storage
        self.global_tasks = {}
        self.daily_ratings = {}
        self.workspaces = []
        self.current_selected_date = None
        
        # Initialize data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
        # Select today by default and update calendar
        self.go_today()
        self.calendar.update_calendar(self.show_day_tasks)
        self.root.after(100, lambda: self.calendar.update_calendar(self.show_day_tasks))
    
    def setup_ui(self):
        """Setup the main UI layout."""
        # Main container with padding
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left and Right panels
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)
    
    def create_header(self, parent):
        """Create header with title and date."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame, text=WINDOW_TITLE,
                                   font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(side="left")
        
        self.date_label = ctk.CTkLabel(header_frame, text="",
                                       font=ctk.CTkFont(size=14))
        self.date_label.pack(side="right")
    
    def create_left_panel(self, parent):
        """Create left panel with calendar."""
        left_panel = ctk.CTkFrame(parent)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Calendar navigation
        nav_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        nav_frame.pack(fill="x", pady=10)
        
        prev_btn = ctk.CTkButton(nav_frame, text="←", width=40,
                                command=self.previous_month)
        prev_btn.pack(side="left")
        
        self.month_label = ctk.CTkLabel(nav_frame, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.month_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(nav_frame, text="→", width=40,
                                command=self.next_month)
        next_btn.pack(side="right")
        
        today_btn = ctk.CTkButton(nav_frame, text="Сегодня", width=80,
                                 command=self.go_today)
        today_btn.pack(side="right", padx=(5, 0))
        
        # Calendar frame
        self.calendar_frame = ctk.CTkFrame(left_panel)
        self.calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Calendar canvas for custom drawing
        import tkinter as tk
        self.calendar_canvas = tk.Canvas(self.calendar_frame, bg="#1a1a2e",
                                        highlightthickness=0, borderwidth=0)
        self.calendar_canvas.pack(fill="both", expand=True)
        
        # Initialize calendar component
        self.calendar = CalendarComponent(self.style_manager, self.get_daily_rating)
        self.calendar.canvas = self.calendar_canvas
        self.calendar.current_date = datetime.now()
        
        # Big metrics under calendar: day, week, total
        metrics_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.metric_day = ctk.CTkLabel(metrics_frame, text="0.0",
                                       font=ctk.CTkFont(size=36, weight="bold"),
                                       width=120)
        self.metric_day.pack(side="left", expand=True)
        
        self.metric_week = ctk.CTkLabel(metrics_frame, text="0.0",
                                        font=ctk.CTkFont(size=36, weight="bold"),
                                        width=120)
        self.metric_week.pack(side="left", expand=True)
        
        self.metric_total = ctk.CTkLabel(metrics_frame, text="0.0",
                                         font=ctk.CTkFont(size=36, weight="bold"),
                                         width=120)
        self.metric_total.pack(side="left", expand=True)
        
        # Daily stats card
        stats_card = ctk.CTkFrame(left_panel)
        stats_card.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(stats_card, text="Итоги дня",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.daily_rating = ctk.CTkLabel(stats_card, text="0.0 / 5.0",
                                         font=ctk.CTkFont(size=32, weight="bold"))
        self.daily_rating.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Mini graph showing last 7 days trend
        graph_frame = ctk.CTkFrame(stats_card, fg_color="transparent")
        graph_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(graph_frame, text="Неделя:",
                    font=ctk.CTkFont(size=11)).pack(side="left")
        
        self.mini_graph = ctk.CTkLabel(graph_frame, text="────────────────",
                                      font=("Courier", 12))
        self.mini_graph.pack(side="left", padx=(10, 0))
    
    def create_right_panel(self, parent):
        """Create right panel with task management."""
        right_panel = ctk.CTkFrame(parent)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Task input card
        input_card = ctk.CTkFrame(right_panel)
        input_card.pack(fill="x", padx=10, pady=(10, 10))
        
        # Workspace management
        workspace_header = ctk.CTkFrame(input_card, fg_color="transparent")
        workspace_header.pack(fill="x", padx=15, pady=(15, 0))
        
        ctk.CTkLabel(workspace_header, text="Рабочее пространство",
                    font=ctk.CTkFont(size=13)).pack(side="left")
        
        ctk.CTkButton(workspace_header, text="✕ Удалить", width=90,
                     command=self.delete_workspace, 
                     fg_color="#e94560", hover_color="#d63031").pack(side="right", padx=(0, 5))
        
        ctk.CTkButton(workspace_header, text="+ Создать", width=80,
                     command=self.create_workspace).pack(side="right")
        
        workspace_combo_frame = ctk.CTkFrame(workspace_header, fg_color="transparent")
        workspace_combo_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        self.workspace_var = ctk.StringVar()
        self.workspace_combo = ctk.CTkComboBox(workspace_combo_frame,
                                              variable=self.workspace_var,
                                              state="readonly")
        self.workspace_combo.pack(fill="x")
        self.update_workspace_combo()
        
        # Task input
        ctk.CTkLabel(input_card, text="Новая задача",
                    font=ctk.CTkFont(size=13)).pack(anchor="w", padx=15)
        
        input_group = ctk.CTkFrame(input_card, fg_color="transparent")
        input_group.pack(fill="x", padx=15, pady=(5, 15))
        
        self.task_entry = ctk.CTkEntry(input_group, placeholder_text="Введите задачу...")
        self.task_entry.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(input_group, text="+", width=40,
                     command=self.add_global_task).pack(side="right", padx=(5, 0))
        
        # Tasks list card
        tasks_card = ctk.CTkFrame(right_panel)
        tasks_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(tasks_card, text="Задачи на сегодня",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=10)

        # Workspace tiles bar
        tiles_container = ctk.CTkFrame(tasks_card, fg_color="transparent")
        tiles_container.pack(fill="x", padx=15, pady=(0, 8))
        self.workspace_tiles_container = tiles_container
        self.update_workspace_tiles()
        
        # Tasks scrollable frame
        self.tasks_frame = ctk.CTkScrollableFrame(tasks_card)
        self.tasks_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Bind Enter key
        self.task_entry.bind("<Return>", lambda e: self.add_global_task())
        
    def on_frame_configure(self, event):
        """Update scroll region when frame content changes."""
        pass  # Not needed with CTkScrollableFrame
    
    def previous_month(self):
        """Navigate to previous month."""
        self.calendar.previous_month()
        self.update_calendar()
    
    def next_month(self):
        """Navigate to next month."""
        self.calendar.next_month()
        self.update_calendar()
    
    def go_today(self):
        """Navigate to today's date."""
        self.calendar.go_today()
        self.update_calendar()
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.show_day_tasks(today_str)
    
    def update_calendar(self):
        """Update calendar display."""
        self.calendar.update_calendar(self.show_day_tasks)
        self.month_label.configure(text=self.calendar.get_month_label_text())
        self.date_label.configure(text=f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}")
        
        # Schedule another update if canvas not rendered yet
        if self.calendar_canvas.winfo_width() <= 1:
            self.root.after(100, self.update_calendar)
        else:
            # Update metrics for current day
            self.update_big_metrics(datetime.now().strftime("%Y-%m-%d"))
    
    def get_daily_rating(self, date_str: str) -> float:
        """Calculate average daily rating."""
        if date_str in self.daily_ratings:
            ratings = [rating for rating in self.daily_ratings[date_str].values() if rating > 0]
            if ratings:
                return sum(ratings) / len(ratings)
        return 0.0
    
    def show_day_tasks(self, date_str: str):
        """Display tasks for selected day."""
        self.current_selected_date = date_str
        self.update_tasks_list()
        
        rating = self.get_daily_rating(date_str)
        self.daily_rating.configure(text=f"{rating:.1f} / 5.0")
        
        # Update mini graph showing last 7 days
        self.update_mini_graph(date_str)
        # Update big metrics
        self.update_big_metrics(date_str)
        
        # Update date display
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        self.date_label.configure(text=f"Выбрано: {selected_date.strftime('%d.%m.%Y')}")
    
    def update_mini_graph(self, date_str: str):
        """Update mini graph showing last 7 days trend."""
        # Get last 7 days ratings
        last_7_ratings = []
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        for i in range(6, -1, -1):  # 6 days ago to today
            day = selected_date - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            rating = self.get_daily_rating(day_str)
            last_7_ratings.append(rating)
        
        # Create visual graph with characters
        # Use: ▁▂▃▄▅▆▇█ for different heights based on rating
        bars = []
        blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        
        for rating in last_7_ratings:
            # Convert 0-5 rating to 0-8 block index
            block_index = int((rating / 5.0) * 8) if rating > 0 else 0
            if block_index > 8:
                block_index = 8
            bars.append(blocks[block_index])
        
        graph_text = ''.join(bars)
        self.mini_graph.configure(text=graph_text)

    def _rating_color(self, value: float) -> str:
        """Map rating value to color consistent with UI labels."""
        if value <= 0:
            return "#888888"
        if value <= 2:
            return "#ff4444"  # Red
        if value <= 3:
            return "#ffaa00"  # Orange
        if value <= 4:
            return "#ffaa00"  # Yellow
        return "#00ff88"  # Green

    def update_big_metrics(self, date_str: str):
        """Update three big numbers: day, week, total with colors."""
        # Day
        day_val = self.get_daily_rating(date_str)
        self.metric_day.configure(text=f"{day_val:.1f}", text_color=self._rating_color(day_val))
        
        # Week (last 7 days including selected), average over days with rating > 0
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        week_vals = []
        for i in range(6, -1, -1):
            d = selected_date - timedelta(days=i)
            v = self.get_daily_rating(d.strftime("%Y-%m-%d"))
            if v > 0:
                week_vals.append(v)
        week_avg = sum(week_vals) / len(week_vals) if week_vals else 0.0
        self.metric_week.configure(text=f"{week_avg:.1f}", text_color=self._rating_color(week_avg))
        
        # Total (over all dates)
        all_vals = []
        for dstr in self.daily_ratings.keys():
            v = self.get_daily_rating(dstr)
            if v > 0:
                all_vals.append(v)
        total_avg = sum(all_vals) / len(all_vals) if all_vals else 0.0
        self.metric_total.configure(text=f"{total_avg:.1f}", text_color=self._rating_color(total_avg))
    
    def update_tasks_list(self):
        """Update the tasks list display."""
        # Clear existing tasks
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Add tasks filtered by selected workspace
        if self.current_selected_date:
            current_ws = self.workspace_var.get()
            for task_id, task in self.global_tasks.items():
                if task.get('workspace') == current_ws:
                    self.create_task_widget(task_id, task)

    def update_workspace_tiles(self):
        """Render workspace tiles with per-day rating and selection."""
        # If container not ready, skip
        if not hasattr(self, 'workspace_tiles_container'):
            return
        for w in self.workspace_tiles_container.winfo_children():
            w.destroy()
        
        selected = self.workspace_var.get()
        day = self.current_selected_date or datetime.now().strftime("%Y-%m-%d")
        
        for ws in self.workspaces:
            vals = []
            if day in self.daily_ratings:
                for task_id, rating in self.daily_ratings[day].items():
                    task = self.global_tasks.get(task_id)
                    if task and task.get('workspace') == ws and rating > 0:
                        vals.append(rating)
            ws_avg = sum(vals)/len(vals) if vals else 0.0
            color = self._rating_color(ws_avg)
            
            btn = ctk.CTkButton(self.workspace_tiles_container,
                                 text=f"{ws}\n{ws_avg:.1f}",
                                 width=120, height=48,
                                 fg_color=("#2a2a2a" if ws != selected else "#0f3460"),
                                 hover_color="#3a3a3a",
                                 text_color=color,
                                 command=lambda name=ws: self._on_workspace_tile_click(name))
            btn.pack(side="left", padx=4)

    def _on_workspace_tile_click(self, name: str):
        self.workspace_var.set(name)
        self.update_workspace_tiles()
        self.update_tasks_list()
    
    def create_task_widget(self, task_id: str, task: dict):
        """Create a compact task tile."""
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(fill="x", pady=3)
        
        # Main content in one line
        content_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=8, pady=6)
        
        # Task text (compact)
        task_text = task['description']
        task_label = ctk.CTkLabel(content_frame, text=task_text,
                                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                text_color="#00d4ff")
        task_label.pack(side="left", padx=(0, 8))
        
        # Rating display with color based on value (compact)
        current_rating = 0
        if (self.current_selected_date and 
            self.current_selected_date in self.daily_ratings and 
            task_id in self.daily_ratings[self.current_selected_date]):
            current_rating = self.daily_ratings[self.current_selected_date][task_id]
        
        if current_rating > 0:
            # Color based on rating: red for low, green for high
            if current_rating <= 2:
                rating_color = "#ff4444"
            elif current_rating <= 3:
                rating_color = "#ffaa00"
            elif current_rating <= 4:
                rating_color = "#ffaa00"
            else:
                rating_color = "#00ff88"
            rating_text = f"{current_rating}/5"
        else:
            rating_color = "#666666"
            rating_text = "?"
            
        rating_label = ctk.CTkLabel(content_frame, text=rating_text,
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   text_color=rating_color,
                                   width=40)
        rating_label.pack(side="right")
        
        # Edit button (small)
        edit_btn = ctk.CTkButton(content_frame, text="✎",
                                font=ctk.CTkFont(size=10),
                                width=24, height=24,
                                fg_color="#2a2a2a",
                                hover_color="#3a3a3a",
                                command=lambda: self.edit_task_description(task_id))
        edit_btn.pack(side="right", padx=(0, 8))
        
        # Delete button (small)
        delete_btn = ctk.CTkButton(content_frame, text="✕",
                                   font=ctk.CTkFont(size=11, weight="bold"),
                                   width=24, height=24,
                                   fg_color="#e94560",
                                   hover_color="#d63031",
                                   command=lambda: self.delete_global_task(task_id))
        delete_btn.pack(side="right", padx=(0, 8))
        
        # Bind click events for rating
        def make_click_handler(tid):
            return lambda e: self.show_rating_dialog(tid)
        
        for widget in [task_frame, content_frame, task_label, rating_label]:
            widget.bind("<Button-1>", make_click_handler(task_id))
    
    def edit_task_description(self, task_id: str):
        """Edit task description and criteria."""
        task = self.global_tasks[task_id]
        current_criteria = task.get('description_criteria', '')
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Редактировать задачу")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.update()
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Название задачи:",
                    font=ctk.CTkFont(size=13)).pack(pady=(15, 5), padx=20, anchor="w")
        
        name_entry = ctk.CTkEntry(dialog, width=450,
                                font=ctk.CTkFont(size=13))
        name_entry.insert(0, task['description'])
        name_entry.pack(padx=20)
        
        ctk.CTkLabel(dialog, text="Критерии оценки (необязательно):",
                    font=ctk.CTkFont(size=13)).pack(pady=(15, 5), padx=20, anchor="w")
        
        criteria_entry = ctk.CTkTextbox(dialog, width=450, height=100,
                                       font=ctk.CTkFont(size=12))
        criteria_entry.insert("1.0", current_criteria)
        criteria_entry.pack(padx=20)
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_criteria = criteria_entry.get("1.0", "end-1c").strip()
            
            if new_name:
                self.global_tasks[task_id]['description'] = new_name
                self.global_tasks[task_id]['description_criteria'] = new_criteria
                self.update_tasks_list()
                self.save_data()
                dialog.destroy()
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ctk.CTkButton(button_frame, text="Сохранить", width=100,
                     command=save_changes, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Отмена", width=100,
                     command=dialog.destroy, corner_radius=10).pack(side="left", padx=5)
    
    def show_rating_dialog(self, task_id: str):
        """Show rating dialog when task is clicked."""
        if not self.current_selected_date:
            return
        
        # Check if trying to rate future dates
        from datetime import datetime
        selected_date = datetime.strptime(self.current_selected_date, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if selected_date > today:
            self.dialog_manager.show_warning("Предупреждение",
                                             "Нельзя ставить оценки на будущие дни!")
            return
        
        task = self.global_tasks[task_id]
        rating = self.dialog_manager.show_rating_dialog(task['description'])
        
        if rating > 0:
            # Initialize date if not exists
            if self.current_selected_date not in self.daily_ratings:
                self.daily_ratings[self.current_selected_date] = {}
            
            # Set rating for this task on current date
            self.daily_ratings[self.current_selected_date][task_id] = rating
            
            self.update_tasks_list()
            self.update_calendar()
            
            # Update daily rating
            daily_rating = self.get_daily_rating(self.current_selected_date)
            self.daily_rating.configure(text=f"{daily_rating:.1f} / 5.0")
            
            self.save_data()
    
    def create_workspace(self):
        """Create new workspace."""
        workspace_name = self.dialog_manager.show_workspace_dialog()
        if workspace_name:
            if workspace_name not in self.workspaces:
                self.workspaces.append(workspace_name)
                self.update_workspace_combo()
                self.workspace_var.set(workspace_name)
                self.update_workspace_tiles()
                self.save_data()
            else:
                self.dialog_manager.show_warning(
                    "Предупреждение",
                    "Рабочее пространство с таким названием уже существует"
                )
    
    def delete_workspace(self):
        """Delete current workspace."""
        workspace_name = self.workspace_var.get()
        
        if not workspace_name:
            self.dialog_manager.show_warning("Предупреждение", 
                                           "Выберите рабочее пространство для удаления")
            return
        
        if len(self.workspaces) <= 1:
            self.dialog_manager.show_warning("Предупреждение",
                                           "Нельзя удалить последнее рабочее пространство")
            return
        
        if self.dialog_manager.ask_confirmation("Подтверждение",
                                              f"Удалить рабочее пространство '{workspace_name}'?\nВсе задачи этого пространства будут сохранены."):
            # Remove workspace
            self.workspaces.remove(workspace_name)
            
            # Remove workspace from tasks (keep tasks, just remove workspace reference)
            for task_id in self.global_tasks:
                if self.global_tasks[task_id]['workspace'] == workspace_name:
                    # Move to default workspace
                    self.global_tasks[task_id]['workspace'] = "Без категории"
            
            self.update_workspace_combo()
            # Reset selection
            if self.workspaces:
                self.workspace_var.set(self.workspaces[0])
            self.update_workspace_tiles()
            self.save_data()
    
    def update_workspace_combo(self):
        """Update workspace combobox values."""
        if not self.workspaces:
            self.workspaces = DEFAULT_WORKSPACES.copy()
        
        self.workspace_combo.configure(values=self.workspaces)
        if self.workspaces and not self.workspace_var.get():
            self.workspace_var.set(self.workspaces[0])
        # Also refresh tiles
        if hasattr(self, 'workspace_tiles_container'):
            self.update_workspace_tiles()
    
    def add_global_task(self):
        """Add a global task that appears every day."""
        task_text = self.task_entry.get().strip()
        workspace = self.workspace_var.get()
        
        if not task_text:
            self.dialog_manager.show_warning("Предупреждение", "Введите описание задачи")
            return
        
        if not workspace:
            self.dialog_manager.show_warning("Предупреждение",
                                           "Выберите или создайте рабочее пространство")
            return
        
        # Generate unique task ID
        task_id = f"task_{len(self.global_tasks)}_{datetime.now().timestamp()}"
        
        # Add to global tasks
        self.global_tasks[task_id] = {
            'description': task_text,
            'workspace': workspace,
            'description_criteria': ''  # For future criteria
        }
        
        self.task_entry.delete(0, "end")
        self.update_tasks_list()
        self.update_workspace_tiles()
        self.save_data()
    
    def delete_global_task(self, task_id: str):
        """Delete global task from everywhere."""
        if self.dialog_manager.ask_confirmation("Подтверждение",
                                               "Удалить эту задачу из всех дней?"):
            # Remove from global tasks
            if task_id in self.global_tasks:
                del self.global_tasks[task_id]
            
            # Remove from all daily ratings
            for date in self.daily_ratings:
                if task_id in self.daily_ratings[date]:
                    del self.daily_ratings[date][task_id]
            
            self.update_tasks_list()
            self.update_calendar()
            self.update_workspace_tiles()
            
            # Update daily rating
            if self.current_selected_date:
                rating = self.get_daily_rating(self.current_selected_date)
                self.daily_rating.configure(text=f"{rating:.1f} / 5.0")
            
            self.save_data()
    
    def load_data(self):
        """Load data from JSON file."""
        data = self.data_manager.load_data()
        self.global_tasks = data['global_tasks']
        self.daily_ratings = data['daily_ratings']
        self.workspaces = data['workspaces']
    
    def save_data(self):
        """Save data to JSON file."""
        success = self.data_manager.save_data(self.global_tasks, self.daily_ratings,
                                             self.workspaces)
        if not success:
            self.dialog_manager.show_error("Ошибка", "Не удалось сохранить данные")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernTaskManager(root)
    root.mainloop()

