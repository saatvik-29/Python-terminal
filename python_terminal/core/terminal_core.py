"""
Core terminal orchestrator that coordinates all system components.
"""

import os
import uuid
from pathlib import Path
from typing import Dict, Optional

from python_terminal.core.models import ExecutionContext, CommandResult
from python_terminal.core.command_registry import CommandRegistry
from python_terminal.core.command_processor import CommandProcessor
from python_terminal.core.history_manager import HistoryManager
from python_terminal.config.settings import config
from python_terminal.utils.logging_config import get_logger


class TerminalCore:
    """Main terminal orchestrator that coordinates all system components."""
    
    def __init__(self):
        self.logger = get_logger('terminal_core')
        self.session_id = str(uuid.uuid4())
        
        # Initialize core components
        self.command_registry = CommandRegistry()
        self.command_processor = CommandProcessor(self.command_registry)
        self.history_manager = HistoryManager()
        
        # Initialize execution context
        self.context = ExecutionContext(
            current_directory=Path.cwd(),
            environment_variables=dict(os.environ),
            user_id=os.getenv('USER', 'user'),
            session_id=self.session_id,
            history=[]
        )
        
        self.ui_interface = None
        self.logger.info(f"Terminal core initialized with session ID: {self.session_id}")
    
    def start(self, interface_type: str = 'cli') -> None:
        """
        Start the terminal with specified interface type.
        
        Args:
            interface_type: Type of interface ('cli' or 'web')
        """
        try:
            if interface_type == 'cli':
                self._start_cli_interface()
            elif interface_type == 'web':
                self._start_web_interface()
            else:
                raise ValueError(f"Unknown interface type: {interface_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to start {interface_type} interface: {e}")
            raise
    
    def _start_cli_interface(self) -> None:
        """Start the CLI interface."""
        try:
            from python_terminal.interfaces.cli_interface import CLIInterface
            self.ui_interface = CLIInterface(self)
            self.ui_interface.start_interactive_session()
        except ImportError:
            # Fallback to basic CLI if full interface not available
            self._start_basic_cli()
    
    def _start_web_interface(self) -> None:
        """Start the web interface."""
        try:
            from python_terminal.interfaces.web_interface import WebInterface
            port = config.get('web_port', 5000)
            self.ui_interface = WebInterface(self)
            self.ui_interface.start_server(port=port)
        except ImportError:
            self.logger.error("Web interface dependencies not available")
            print("Web interface not available. Please install Flask dependencies.")
            print("Run: pip install flask flask-socketio")
    
    def _start_basic_cli(self) -> None:
        """Start a basic CLI interface as fallback."""
        print("Python Terminal v1.0.0")
        print("Type 'help' for available commands or 'exit' to quit.")
        print()
        
        while True:
            try:
                # Display prompt
                prompt = self._get_prompt()
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Handle exit command
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                # Execute command
                result = self.execute_command(user_input)
                
                # Display result
                if result.output:
                    print(result.output)
                
                if not result.success and result.error_message:
                    print(f"Error: {result.error_message}")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit the terminal.")
            except EOFError:
                print("\nGoodbye!")
                break
    
    def execute_command(self, command_input: str) -> CommandResult:
        """
        Execute a command and return the result.
        
        Args:
            command_input: Raw command input from user
            
        Returns:
            CommandResult with execution details
        """
        try:
            # Add to history
            self.history_manager.add_command(command_input)
            self.context.history.append(command_input)
            
            # Process and execute command
            result = self.command_processor.process(command_input, self.context)
            
            # Log execution
            self.logger.info(
                f"Command executed: '{command_input}' -> "
                f"Success: {result.success}, Time: {result.execution_time:.3f}s"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing command '{command_input}': {e}")
            return CommandResult(
                success=False,
                output="",
                error_message=f"Internal error: {str(e)}",
                exit_code=1
            )
    
    def _get_prompt(self) -> str:
        """Generate the command prompt string."""
        try:
            cwd = str(self.context.current_directory)
            # Shorten home directory path
            home = str(Path.home())
            if cwd.startswith(home):
                cwd = cwd.replace(home, '~', 1)
            
            return f"{self.context.user_id}:{cwd}$ "
        except Exception:
            return "$ "
    
    def get_context(self) -> ExecutionContext:
        """Get the current execution context."""
        return self.context
    
    def update_working_directory(self, new_path: Path) -> None:
        """Update the current working directory."""
        self.context.current_directory = new_path
        os.chdir(new_path)