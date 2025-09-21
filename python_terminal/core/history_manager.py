"""
Command history management for the terminal.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional
from python_terminal.core.models import CommandHistoryEntry
from python_terminal.config.settings import config
from python_terminal.utils.logging_config import get_logger


class HistoryManager:
    """Manages command history storage and retrieval."""
    
    def __init__(self):
        self.logger = get_logger('history_manager')
        self.history: List[CommandHistoryEntry] = []
        self.history_file = config.history_file
        self.max_history = config.get_history_size()
        
        # Load existing history
        self._load_history()
    
    def add_command(self, command: str, execution_time: float = 0.0, success: bool = True) -> None:
        """
        Add a command to history.
        
        Args:
            command: Command string
            execution_time: Time taken to execute
            success: Whether command succeeded
        """
        entry = CommandHistoryEntry(
            command=command,
            timestamp=datetime.now(),
            execution_time=execution_time,
            success=success,
            working_directory=str(Path.cwd())
        )
        
        self.history.append(entry)
        
        # Trim history if it exceeds max size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # Save to file
        self._save_history()
    
    def get_history(self, limit: Optional[int] = None) -> List[CommandHistoryEntry]:
        """
        Get command history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries
        """
        if limit:
            return self.history[-limit:]
        return self.history.copy()
    
    def get_command_by_index(self, index: int) -> Optional[str]:
        """
        Get command by history index.
        
        Args:
            index: History index (negative for recent commands)
            
        Returns:
            Command string or None if index is invalid
        """
        try:
            return self.history[index].command
        except IndexError:
            return None
    
    def search_history(self, pattern: str) -> List[CommandHistoryEntry]:
        """
        Search history for commands containing pattern.
        
        Args:
            pattern: Search pattern
            
        Returns:
            List of matching history entries
        """
        return [entry for entry in self.history if pattern in entry.command]
    
    def clear_history(self) -> None:
        """Clear all command history."""
        self.history.clear()
        self._save_history()
        self.logger.info("Command history cleared")
    
    def _load_history(self) -> None:
        """Load history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        command = line.strip()
                        if command:
                            # Create basic history entry (timestamp will be approximate)
                            entry = CommandHistoryEntry(
                                command=command,
                                timestamp=datetime.now(),
                                execution_time=0.0,
                                success=True,
                                working_directory=str(Path.cwd())
                            )
                            self.history.append(entry)
                
                self.logger.info(f"Loaded {len(self.history)} commands from history")
        except Exception as e:
            self.logger.warning(f"Could not load history: {e}")
    
    def _save_history(self) -> None:
        """Save history to file."""
        try:
            # Ensure directory exists
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for entry in self.history:
                    f.write(f"{entry.command}\n")
                    
        except Exception as e:
            self.logger.warning(f"Could not save history: {e}")