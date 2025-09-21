"""
Command-line interface for the terminal.
"""

import sys
from python_terminal.utils.logging_config import get_logger


class CLIInterface:
    """Command-line interface for the terminal."""
    
    def __init__(self, terminal_core):
        self.terminal_core = terminal_core
        self.logger = get_logger('cli_interface')
    
    def start_interactive_session(self):
        """Start interactive CLI session."""
        print("Python Terminal v1.0.0")
        print("Type 'help' for available commands or 'exit' to quit.")
        print()
        
        while True:
            try:
                # Get current directory for prompt
                context = self.terminal_core.get_context()
                cwd = str(context.current_directory)
                
                # Shorten home directory path
                from pathlib import Path
                home = str(Path.home())
                if cwd.startswith(home):
                    cwd = cwd.replace(home, '~', 1)
                
                # Display prompt
                prompt = f"{context.user_id}:{cwd}$ "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Handle exit command
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                # Execute command
                result = self.terminal_core.execute_command(user_input)
                
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
            except Exception as e:
                self.logger.error(f"CLI error: {e}")
                print(f"CLI Error: {e}")
    
    def display_result(self, result):
        """Display command result."""
        if result.output:
            print(result.output)
        
        if not result.success and result.error_message:
            print(f"Error: {result.error_message}")