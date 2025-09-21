"""
Core data models for the Python terminal system.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


@dataclass
class CommandResult:
    """Result of command execution."""
    success: bool
    output: str
    error_message: Optional[str] = None
    exit_code: int = 0
    execution_time: float = 0.0


@dataclass
class ExecutionContext:
    """Context information for command execution."""
    current_directory: Path
    environment_variables: Dict[str, str]
    user_id: str
    session_id: str
    history: List[str]


@dataclass
class CommandHistoryEntry:
    """Single entry in command history."""
    command: str
    timestamp: datetime
    execution_time: float
    success: bool
    working_directory: str


class BaseCommand(ABC):
    """Abstract base class for all terminal commands."""
    
    @abstractmethod
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute the command with given arguments and context."""
        pass
    
    @abstractmethod
    def get_help(self) -> str:
        """Return help text for the command."""
        pass
    
    def validate_args(self, args: List[str]) -> bool:
        """Validate command arguments. Override in subclasses as needed."""
        return True
    
    def get_name(self) -> str:
        """Get the command name. Default implementation uses class name."""
        return self.__class__.__name__.lower().replace('command', '')


class CommandNotFoundError(Exception):
    """Raised when a command is not found in the registry."""
    pass


class InvalidArgumentError(Exception):
    """Raised when invalid arguments are provided to a command."""
    pass


class PermissionError(Exception):
    """Raised when insufficient permissions for operation."""
    pass


class FileSystemError(Exception):
    """Raised for file system related errors."""
    pass