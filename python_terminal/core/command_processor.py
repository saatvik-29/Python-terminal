"""
Command processor for parsing and executing terminal commands.
"""

import time
import shlex
from typing import List
from python_terminal.core.models import CommandResult, ExecutionContext, CommandNotFoundError
from python_terminal.core.command_registry import CommandRegistry
from python_terminal.config.settings import config
from python_terminal.utils.logging_config import get_logger


class CommandProcessor:
    """Processes and executes terminal commands."""
    
    def __init__(self, command_registry: CommandRegistry):
        self.logger = get_logger('command_processor')
        self.command_registry = command_registry
        self.nlp_processor = None
        
        # Initialize NLP processor if enabled
        if config.is_nlp_enabled():
            try:
                from python_terminal.nlp.processor import SimpleNLPProcessor
                self.nlp_processor = SimpleNLPProcessor()
                self.logger.info("NLP processor initialized")
            except ImportError:
                self.logger.warning("NLP processor not available")
    
    def process(self, input_text: str, context: ExecutionContext) -> CommandResult:
        """
        Process and execute a command.
        
        Args:
            input_text: Raw command input
            context: Execution context
            
        Returns:
            CommandResult with execution details
        """
        start_time = time.time()
        
        try:
            # Try NLP processing first if enabled
            processed_input = input_text
            if self.nlp_processor and self.nlp_processor.is_natural_language(input_text):
                nlp_result = self.nlp_processor.process_natural_language(input_text)
                if nlp_result:
                    processed_input = nlp_result
                    self.logger.info(f"NLP converted: '{input_text}' -> '{processed_input}'")
            
            # Parse command and arguments
            parts = self._parse_command(processed_input)
            if not parts:
                return CommandResult(
                    success=True,
                    output="",
                    execution_time=time.time() - start_time
                )
            
            command_name = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            # Get command handler
            try:
                handler = self.command_registry.get_handler(command_name)
            except CommandNotFoundError:
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"Command '{command_name}' not found. Type 'help' for available commands.",
                    exit_code=127,
                    execution_time=time.time() - start_time
                )
            
            # Validate arguments
            if not handler.validate_args(args):
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"Invalid arguments for '{command_name}'. Use 'help {command_name}' for usage.",
                    exit_code=1,
                    execution_time=time.time() - start_time
                )
            
            # Execute command
            result = handler.execute(args, context)
            result.execution_time = time.time() - start_time
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing command '{input_text}': {e}")
            return CommandResult(
                success=False,
                output="",
                error_message=f"Error executing command: {str(e)}",
                exit_code=1,
                execution_time=time.time() - start_time
            )
    
    def _parse_command(self, input_text: str) -> List[str]:
        """
        Parse command input into command and arguments.
        
        Args:
            input_text: Raw command input
            
        Returns:
            List of command parts (command + arguments)
        """
        try:
            # Use shlex for proper shell-like parsing
            return shlex.split(input_text.strip())
        except ValueError as e:
            # Fallback to simple split if shlex fails
            self.logger.warning(f"Failed to parse command with shlex: {e}")
            return input_text.strip().split()
    
    def suggest_commands(self, partial_command: str) -> List[str]:
        """
        Suggest commands based on partial input.
        
        Args:
            partial_command: Partial command name
            
        Returns:
            List of matching command suggestions
        """
        all_commands = self.command_registry.list_commands()
        suggestions = [cmd for cmd in all_commands if cmd.startswith(partial_command)]
        return sorted(suggestions)