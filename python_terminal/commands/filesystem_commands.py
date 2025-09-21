"""
File system operation commands for the terminal.
"""

import os
import shutil
from pathlib import Path
from typing import List
from python_terminal.core.models import BaseCommand, CommandResult, ExecutionContext


class ListCommand(BaseCommand):
    """List directory contents (ls command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute ls command."""
        try:
            # Determine target directory
            if args:
                target_path = Path(args[0])
                if not target_path.is_absolute():
                    target_path = context.current_directory / target_path
            else:
                target_path = context.current_directory
            
            if not target_path.exists():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"ls: cannot access '{target_path}': No such file or directory"
                )
            
            if target_path.is_file():
                return CommandResult(success=True, output=str(target_path.name))
            
            # List directory contents
            items = []
            try:
                for item in sorted(target_path.iterdir()):
                    if item.is_dir():
                        items.append(f"{item.name}/")
                    else:
                        items.append(item.name)
            except PermissionError:
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"ls: cannot open directory '{target_path}': Permission denied"
                )
            
            output = "  ".join(items) if items else ""
            return CommandResult(success=True, output=output)
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"ls: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for ls command."""
        return "ls [directory] - List directory contents"


class ChangeDirectoryCommand(BaseCommand):
    """Change directory (cd command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute cd command."""
        try:
            if not args:
                # cd with no arguments goes to home directory
                target_path = Path.home()
            else:
                target_path = Path(args[0])
                if not target_path.is_absolute():
                    target_path = context.current_directory / target_path
            
            # Resolve path (handle .. and . properly)
            target_path = target_path.resolve()
            
            if not target_path.exists():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"cd: no such file or directory: {target_path}"
                )
            
            if not target_path.is_dir():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"cd: not a directory: {target_path}"
                )
            
            # Change directory
            os.chdir(target_path)
            context.current_directory = target_path
            
            return CommandResult(success=True, output="")
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cd: permission denied: {args[0] if args else '~'}"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cd: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for cd command."""
        return "cd [directory] - Change current directory"


class PrintWorkingDirectoryCommand(BaseCommand):
    """Print working directory (pwd command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute pwd command."""
        try:
            current_dir = str(context.current_directory)
            return CommandResult(success=True, output=current_dir)
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"pwd: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for pwd command."""
        return "pwd - Print current working directory"


class MakeDirectoryCommand(BaseCommand):
    """Create directory (mkdir command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute mkdir command."""
        if not args:
            return CommandResult(
                success=False,
                output="",
                error_message="mkdir: missing operand"
            )
        
        try:
            for dir_name in args:
                target_path = Path(dir_name)
                if not target_path.is_absolute():
                    target_path = context.current_directory / target_path
                
                if target_path.exists():
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"mkdir: cannot create directory '{dir_name}': File exists"
                    )
                
                target_path.mkdir(parents=True, exist_ok=False)
            
            return CommandResult(success=True, output="")
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"mkdir: cannot create directory '{dir_name}': Permission denied"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"mkdir: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for mkdir command."""
        return "mkdir <directory>... - Create directories"


class RemoveCommand(BaseCommand):
    """Remove files (rm command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute rm command."""
        if not args:
            return CommandResult(
                success=False,
                output="",
                error_message="rm: missing operand"
            )
        
        try:
            for file_name in args:
                target_path = Path(file_name)
                if not target_path.is_absolute():
                    target_path = context.current_directory / target_path
                
                if not target_path.exists():
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"rm: cannot remove '{file_name}': No such file or directory"
                    )
                
                if target_path.is_dir():
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"rm: cannot remove '{file_name}': Is a directory"
                    )
                
                target_path.unlink()
            
            return CommandResult(success=True, output="")
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"rm: cannot remove '{file_name}': Permission denied"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"rm: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for rm command."""
        return "rm <file>... - Remove files"


class EchoCommand(BaseCommand):
    """Echo command for displaying text."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute echo command."""
        output = " ".join(args)
        return CommandResult(success=True, output=output)
    
    def get_help(self) -> str:
        """Get help text for echo command."""
        return "echo [text...] - Display text"