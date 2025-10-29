"""Data management module for persisting task data."""

import json
import os
from typing import Dict, List, Any

from config import DATA_FILE


class DataManager:
    """Handles all data persistence operations."""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
    
    def load_data(self) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Returns:
            Dictionary with 'global_tasks', 'daily_ratings', and 'workspaces'
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        'global_tasks': data.get('global_tasks', {}),
                        'daily_ratings': data.get('daily_ratings', {}),
                        'workspaces': data.get('workspaces', [])
                    }
            except Exception:
                return self._get_empty_data()
        return self._get_empty_data()
    
    def save_data(self, global_tasks: Dict, daily_ratings: Dict, workspaces: List) -> bool:
        """
        Save data to JSON file.
        
        Args:
            global_tasks: Dictionary of global tasks
            daily_ratings: Dictionary of daily ratings
            workspaces: List of workspace names
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'global_tasks': global_tasks,
                'daily_ratings': daily_ratings,
                'workspaces': workspaces
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def _get_empty_data(self) -> Dict[str, Any]:
        """Return empty data structure."""
        return {
            'global_tasks': {},
            'daily_ratings': {},
            'workspaces': []
        }

