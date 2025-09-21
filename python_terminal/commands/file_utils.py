"""
File utility commands for the terminal.
"""

import re
from pathlib import Path
from typing import List
from python_terminal.core.models import BaseCommand, CommandResult, ExecutionContext


class CatCommand(BaseCommand):
    """Display file contents (cat command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute cat command."""
        if not args:
            return CommandResult(
                success=False,
                output="",
                error_message="cat: missing file operand"
            )
        
        try:
            output_lines = []
            
            for file_name in args:
                file_path = Path(file_name)
                if not file_path.is_absolute():
                    file_path = context.current_directory / file_path
                
                if not file_path.exists():
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"cat: {file_name}: No such file or directory"
                    )
                
                if file_path.is_dir():
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"cat: {file_name}: Is a directory"
                    )
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        output_lines.append(content)
                except UnicodeDecodeError:
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"cat: {file_name}: Binary file (not displayed)"
                    )
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cat: {file_name}: Permission denied"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cat: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for cat command."""
        return "cat <file>... - Display file contents"


class GrepCommand(BaseCommand):
    """Search text patterns in files (grep command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute grep command."""
        if len(args) < 2:
            return CommandResult(
                success=False,
                output="",
                error_message="grep: usage: grep <pattern> <file>..."
            )
        
        try:
            pattern = args[0]
            files = args[1:]
            output_lines = []
            
            for file_name in files:
                file_path = Path(file_name)
                if not file_path.is_absolute():
                    file_path = context.current_directory / file_path
                
                if not file_path.exists():
                    output_lines.append(f"grep: {file_name}: No such file or directory")
                    continue
                
                if file_path.is_dir():
                    output_lines.append(f"grep: {file_name}: Is a directory")
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if re.search(pattern, line):
                                if len(files) > 1:
                                    output_lines.append(f"{file_name}:{line_num}:{line.rstrip()}")
                                else:
                                    output_lines.append(f"{line_num}:{line.rstrip()}")
                except UnicodeDecodeError:
                    output_lines.append(f"grep: {file_name}: Binary file matches")
                except re.error as e:
                    return CommandResult(
                        success=False,
                        output="",
                        error_message=f"grep: invalid pattern: {e}"
                    )
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"grep: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for grep command."""
        return "grep <pattern> <file>... - Search for pattern in files"


class FindCommand(BaseCommand):
    """Find files and directories (find command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute find command."""
        if not args:
            search_path = context.current_directory
            pattern = "*"
        elif len(args) == 1:
            search_path = Path(args[0])
            if not search_path.is_absolute():
                search_path = context.current_directory / search_path
            pattern = "*"
        else:
            search_path = Path(args[0])
            if not search_path.is_absolute():
                search_path = context.current_directory / search_path
            
            # Look for -name option
            if len(args) >= 3 and args[1] == "-name":
                pattern = args[2]
            else:
                pattern = "*"
        
        try:
            if not search_path.exists():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"find: '{search_path}': No such file or directory"
                )
            
            matches = []
            
            if search_path.is_file():
                matches.append(str(search_path))
            else:
                # Search recursively
                try:
                    for item in search_path.rglob(pattern):
                        matches.append(str(item))
                except PermissionError:
                    pass  # Skip directories we can't access
            
            matches.sort()
            return CommandResult(success=True, output="\n".join(matches))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"find: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for find command."""
        return "find [path] [-name pattern] - Find files and directories"


class WordCountCommand(BaseCommand):
    """Count lines, words, and characters (wc command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute wc command."""
        if not args:
            return CommandResult(
                success=False,
                output="",
                error_message="wc: missing file operand"
            )
        
        try:
            output_lines = []
            total_lines = total_words = total_chars = 0
            
            for file_name in args:
                file_path = Path(file_name)
                if not file_path.is_absolute():
                    file_path = context.current_directory / file_path
                
                if not file_path.exists():
                    output_lines.append(f"wc: {file_name}: No such file or directory")
                    continue
                
                if file_path.is_dir():
                    output_lines.append(f"wc: {file_name}: Is a directory")
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.count('\n')
                        words = len(content.split())
                        chars = len(content)
                        
                        output_lines.append(f"{lines:>8} {words:>8} {chars:>8} {file_name}")
                        
                        total_lines += lines
                        total_words += words
                        total_chars += chars
                        
                except UnicodeDecodeError:
                    output_lines.append(f"wc: {file_name}: Binary file")
            
            # Show totals if multiple files
            if len(args) > 1:
                output_lines.append(f"{total_lines:>8} {total_words:>8} {total_chars:>8} total")
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"wc: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for wc command."""
        return "wc <file>... - Count lines, words, and characters"


class CopyCommand(BaseCommand):
    """Copy files (cp command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute cp command."""
        if len(args) < 2:
            return CommandResult(
                success=False,
                output="",
                error_message="cp: missing file operand"
            )
        
        try:
            source = Path(args[0])
            dest = Path(args[1])
            
            if not source.is_absolute():
                source = context.current_directory / source
            if not dest.is_absolute():
                dest = context.current_directory / dest
            
            if not source.exists():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"cp: cannot stat '{args[0]}': No such file or directory"
                )
            
            if source.is_dir():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"cp: omitting directory '{args[0]}'"
                )
            
            # If dest is a directory, copy into it
            if dest.is_dir():
                dest = dest / source.name
            
            import shutil
            shutil.copy2(source, dest)
            
            return CommandResult(success=True, output="")
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cp: permission denied"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"cp: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for cp command."""
        return "cp <source> <dest> - Copy files"


class MoveCommand(BaseCommand):
    """Move/rename files (mv command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute mv command."""
        if len(args) < 2:
            return CommandResult(
                success=False,
                output="",
                error_message="mv: missing file operand"
            )
        
        try:
            source = Path(args[0])
            dest = Path(args[1])
            
            if not source.is_absolute():
                source = context.current_directory / source
            if not dest.is_absolute():
                dest = context.current_directory / dest
            
            if not source.exists():
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"mv: cannot stat '{args[0]}': No such file or directory"
                )
            
            # If dest is a directory, move into it
            if dest.is_dir():
                dest = dest / source.name
            
            source.rename(dest)
            
            return CommandResult(success=True, output="")
            
        except PermissionError:
            return CommandResult(
                success=False,
                output="",
                error_message=f"mv: permission denied"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"mv: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for mv command."""
        return "mv <source> <dest> - Move/rename files"