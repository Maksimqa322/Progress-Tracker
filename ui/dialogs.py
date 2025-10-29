"""Dialog windows for Modern Task Manager using CustomTkinter."""

import customtkinter as ctk
import tkinter.messagebox as messagebox
from ui.styles import StyleManager


class DialogManager:
    """Manages dialog windows for the application."""
    
    def __init__(self, root, style_manager: StyleManager):
        self.root = root
        self.style = style_manager
    
    def show_workspace_dialog(self) -> str:
        """
        Show dialog to create a new workspace.
        
        Returns:
            Workspace name or None if cancelled
        """
        dialog = ctk.CTkInputDialog(
            text="Введите название рабочего пространства:",
            title="Новое рабочее пространство"
        )
        workspace_name = dialog.get_input()
        
        if workspace_name and workspace_name.strip():
            return workspace_name.strip()
        return None
    
    def show_rating_dialog(self, task_description: str) -> int:
        """
        Show dialog to rate a task.
        
        Args:
            task_description: Description of the task to rate
            
        Returns:
            Rating value (1-5) or 0 if cancelled
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Оценка задачи")
        dialog.geometry("400x280")
        dialog.transient(self.root)
        
        # Center dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 300, 
                                   self.root.winfo_rooty() + 200))
        
        # Update to make window visible before grab
        dialog.update()
        dialog.grab_set()
        
        rating_value = {'value': 0}
        
        # Task description
        task_label = ctk.CTkLabel(dialog, text=task_description, 
                                  font=ctk.CTkFont(size=15, weight="bold"),
                                  wraplength=360, justify="left")
        task_label.pack(pady=(25, 15), padx=20)
        
        # Rating label
        ctk.CTkLabel(dialog, text="Выберите оценку:", 
                    font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(0, 8))
        
        # Rating buttons frame
        rating_frame = ctk.CTkFrame(dialog)
        rating_frame.pack(pady=15)
        
        def set_1(): 
            rating_value['value'] = 1
            dialog.destroy()
        
        def set_2(): 
            rating_value['value'] = 2
            dialog.destroy()
        
        def set_3(): 
            rating_value['value'] = 3
            dialog.destroy()
        
        def set_4(): 
            rating_value['value'] = 4
            dialog.destroy()
        
        def set_5(): 
            rating_value['value'] = 5
            dialog.destroy()
        
        # Create rating buttons 1-5
        for i, handler in enumerate([set_1, set_2, set_3, set_4, set_5], 1):
            btn = ctk.CTkButton(rating_frame, text=str(i),
                               font=ctk.CTkFont(size=24, weight="bold"),
                               width=55, height=45,
                               command=handler,
                               corner_radius=10)
            btn.pack(side="left", padx=3)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(dialog, text="Отмена",
                                   font=ctk.CTkFont(size=13),
                                   width=120, command=dialog.destroy,
                                   corner_radius=10)
        cancel_btn.pack(pady=20)
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        return rating_value['value']
    
    def show_warning(self, title: str, message: str):
        """Show warning messagebox."""
        messagebox.showwarning(title, message)
    
    def show_error(self, title: str, message: str):
        """Show error messagebox."""
        messagebox.showerror(title, message)
    
    def ask_confirmation(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog.
        
        Returns:
            True if confirmed, False otherwise
        """
        return messagebox.askyesno(title, message)
