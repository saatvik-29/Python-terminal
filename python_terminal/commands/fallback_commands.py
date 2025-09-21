"""
Fallback commands for basic terminal functionality.
"""

from typing import List
from python_terminal.core.models import BaseCommand, CommandResult, ExecutionContext


class FallbackHelpCommand(BaseCommand):
    """Basic help command."""
    
    def __init__(self, command_registry):
        self.command_registry = command_registry
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute help command."""
        if args:
            # Help for specific command
            command_name = args[0]
            try:
                handler = self.command_registry.get_handler(command_name)
                help_text = handler.get_help()
            except:
                help_text = f"No help available for '{command_name}'"
        else:
            # General help
            commands = self.command_registry.list_commands()
            help_text = "Available commands:\n" + "\n".join(f"  {cmd}" for cmd in commands)
            help_text += "\n\nType 'help <command>' for specific command help."
        
        return CommandResult(success=True, output=help_text)
    
    def get_help(self) -> str:
        """Get help text for this command."""
        return "help [command] - Show help information"


class FallbackExitCommand(BaseCommand):
    """Basic exit command."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute exit command."""
        import sys
        sys.exit(0)
    
    def get_help(self) -> str:
        """Get help text for this command."""
        return "exit - Exit the terminal"