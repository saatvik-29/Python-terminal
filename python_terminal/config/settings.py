"""
Configuration settings for the Python terminal.
"""

import os
from pathlib import Path
from typing import Dict, Any


class TerminalConfig:
    """Configuration manager for terminal settings."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.python_terminal'
        self.config_file = self.config_dir / 'config.json'
        self.history_file = self.config_dir / 'history.txt'
        self.log_file = self.config_dir / 'terminal.log'
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.defaults = {
            'prompt_format': '{user}@{hostname}:{cwd}$ ',
            'history_size': 1000,
            'auto_completion': True,
            'colored_output': True,
            'log_level': 'INFO',
            'nlp_enabled': False,
            'web_port': 5000,
            'max_output_lines': 1000,
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.defaults.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.defaults[key] = value
    
    def get_prompt_format(self) -> str:
        """Get the current prompt format."""
        return self.get('prompt_format')
    
    def get_history_size(self) -> int:
        """Get maximum history size."""
        return self.get('history_size')
    
    def is_auto_completion_enabled(self) -> bool:
        """Check if auto-completion is enabled."""
        return self.get('auto_completion')
    
    def is_colored_output_enabled(self) -> bool:
        """Check if colored output is enabled."""
        return self.get('colored_output')
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get('log_level')
    
    def is_nlp_enabled(self) -> bool:
        """Check if natural language processing is enabled."""
        return self.get('nlp_enabled')


# Global configuration instance
config = TerminalConfig()