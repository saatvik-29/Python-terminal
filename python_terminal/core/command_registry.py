"""
Command registry for managing available terminal commands.
"""

from typing import Dict, List, Optional
from python_terminal.core.models import BaseCommand, CommandNotFoundError
from python_terminal.utils.logging_config import get_logger


class CommandRegistry:
    """Registry for managing all available terminal commands."""
    
    def __init__(self):
        self.logger = get_logger('command_registry')
        self.commands: Dict[str, BaseCommand] = {}
        self.aliases: Dict[str, str] = {}
        
        # Load built-in commands
        self._load_builtin_commands()
    
    def register(self, name: str, handler: BaseCommand, aliases: Optional[List[str]] = None) -> None:
        """
        Register a command handler.
        
        Args:
            name: Command name
            handler: Command handler instance
            aliases: Optional list of command aliases
        """
        self.commands[name] = handler
        self.logger.debug(f"Registered command: {name}")
        
        # Register aliases
        if aliases:
            for alias in aliases:
                self.aliases[alias] = name
                self.logger.debug(f"Registered alias: {alias} -> {name}")
    
    def get_handler(self, command_name: str) -> BaseCommand:
        """
        Get command handler by name or alias.
        
        Args:
            command_name: Name or alias of the command
            
        Returns:
            Command handler instance
            
        Raises:
            CommandNotFoundError: If command is not found
        """
        # Check if it's an alias first
        actual_name = self.aliases.get(command_name, command_name)
        
        if actual_name in self.commands:
            return self.commands[actual_name]
        
        raise CommandNotFoundError(f"Command '{command_name}' not found")
    
    def list_commands(self) -> List[str]:
        """Get list of all available command names."""
        return sorted(self.commands.keys())
    
    def list_aliases(self) -> Dict[str, str]:
        """Get dictionary of all aliases."""
        return self.aliases.copy()
    
    def command_exists(self, command_name: str) -> bool:
        """Check if a command exists."""
        actual_name = self.aliases.get(command_name, command_name)
        return actual_name in self.commands
    
    def _load_builtin_commands(self) -> None:
        """Load built-in terminal commands."""
        try:
            # Import and register filesystem commands
            from python_terminal.commands.filesystem_commands import (
                ListCommand, ChangeDirectoryCommand, PrintWorkingDirectoryCommand,
                MakeDirectoryCommand, RemoveCommand, EchoCommand
            )
            
            # Import file utility commands
            from python_terminal.commands.file_utils import (
                CatCommand, GrepCommand, FindCommand, WordCountCommand,
                CopyCommand, MoveCommand
            )
            
            # Import system commands
            from python_terminal.commands.system_commands import (
                ProcessListCommand, KillCommand, TopCommand,
                DiskUsageCommand, MemoryCommand
            )
            
            # Register filesystem commands
            self.register('ls', ListCommand())
            self.register('cd', ChangeDirectoryCommand())
            self.register('pwd', PrintWorkingDirectoryCommand())
            self.register('mkdir', MakeDirectoryCommand())
            self.register('rm', RemoveCommand())
            self.register('echo', EchoCommand())
            
            # Register file utility commands
            self.register('cat', CatCommand())
            self.register('grep', GrepCommand())
            self.register('find', FindCommand())
            self.register('wc', WordCountCommand())
            self.register('cp', CopyCommand())
            self.register('mv', MoveCommand())
            
            # Register system commands
            self.register('ps', ProcessListCommand())
            self.register('kill', KillCommand())
            self.register('top', TopCommand())
            self.register('df', DiskUsageCommand())
            self.register('free', MemoryCommand())
            
            # Register fallback commands (help, exit)
            self._register_fallback_commands()
            
            self.logger.info(f"Loaded {len(self.commands)} built-in commands")
            
        except ImportError as e:
            self.logger.warning(f"Could not load some built-in commands: {e}")
            # Register minimal fallback commands only
            self._register_fallback_commands()
    
    def _register_fallback_commands(self) -> None:
        """Register minimal fallback commands."""
        from python_terminal.commands.fallback_commands import (
            FallbackHelpCommand, FallbackExitCommand
        )
        
        self.register('help', FallbackHelpCommand(self))
        self.register('exit', FallbackExitCommand(), ['quit'])
        
        self.logger.info("Loaded fallback commands")