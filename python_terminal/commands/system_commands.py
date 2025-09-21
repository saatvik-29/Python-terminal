"""
System monitoring and process management commands.
"""

import psutil
import os
import signal
from typing import List
from python_terminal.core.models import BaseCommand, CommandResult, ExecutionContext


class ProcessListCommand(BaseCommand):
    """List running processes (ps command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute ps command."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Format output
            output_lines = ["PID     NAME                CPU%    MEM%"]
            output_lines.append("-" * 40)
            
            for proc in processes[:20]:  # Limit to first 20 processes
                output_lines.append(
                    f"{proc['pid']:<8} {proc['name'][:15]:<15} "
                    f"{proc['cpu_percent']:<7.1f} {proc['memory_percent']:<7.1f}"
                )
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"ps: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for ps command."""
        return "ps - Display running processes"


class KillCommand(BaseCommand):
    """Terminate processes (kill command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute kill command."""
        if not args:
            return CommandResult(
                success=False,
                output="",
                error_message="kill: missing process ID"
            )
        
        try:
            pid = int(args[0])
            
            if not psutil.pid_exists(pid):
                return CommandResult(
                    success=False,
                    output="",
                    error_message=f"kill: no such process: {pid}"
                )
            
            proc = psutil.Process(pid)
            proc.terminate()
            
            return CommandResult(success=True, output=f"Process {pid} terminated")
            
        except ValueError:
            return CommandResult(
                success=False,
                output="",
                error_message="kill: invalid process ID"
            )
        except psutil.AccessDenied:
            return CommandResult(
                success=False,
                output="",
                error_message=f"kill: permission denied for process {pid}"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"kill: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for kill command."""
        return "kill <pid> - Terminate process by ID"


class TopCommand(BaseCommand):
    """Display system resource usage (top command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute top command."""
        try:
            # Get system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            output_lines = [
                "System Resource Usage",
                "=" * 25,
                f"CPU Usage: {cpu_percent:.1f}%",
                f"Memory: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)",
                f"Disk: {disk.percent:.1f}% ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)",
                "",
                "Top Processes:",
                "PID     NAME            CPU%    MEM%"
            ]
            
            # Get top processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            for proc in processes[:10]:  # Top 10 processes
                output_lines.append(
                    f"{proc['pid']:<8} {proc['name'][:12]:<12} "
                    f"{proc['cpu_percent'] or 0:<7.1f} {proc['memory_percent'] or 0:<7.1f}"
                )
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"top: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for top command."""
        return "top - Display system resource usage and top processes"


class DiskUsageCommand(BaseCommand):
    """Display disk usage (df command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute df command."""
        try:
            output_lines = ["Filesystem     Size    Used   Avail  Use%"]
            output_lines.append("-" * 45)
            
            # Get disk usage for root filesystem
            disk = psutil.disk_usage('/')
            size_gb = disk.total // (1024**3)
            used_gb = disk.used // (1024**3)
            avail_gb = disk.free // (1024**3)
            use_percent = disk.percent
            
            output_lines.append(
                f"{'/':<15} {size_gb:>6}G {used_gb:>6}G {avail_gb:>6}G {use_percent:>5.1f}%"
            )
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"df: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for df command."""
        return "df - Display filesystem disk space usage"


class MemoryCommand(BaseCommand):
    """Display memory usage (free command)."""
    
    def execute(self, args: List[str], context: ExecutionContext) -> CommandResult:
        """Execute free command."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            output_lines = [
                "              total        used        free      shared  buff/cache   available",
                f"Mem:    {memory.total//1024:>12} {memory.used//1024:>11} {memory.free//1024:>11} "
                f"{0:>11} {0:>11} {memory.available//1024:>11}",
                f"Swap:   {swap.total//1024:>12} {swap.used//1024:>11} {swap.free//1024:>11}"
            ]
            
            return CommandResult(success=True, output="\n".join(output_lines))
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error_message=f"free: {str(e)}"
            )
    
    def get_help(self) -> str:
        """Get help text for free command."""
        return "free - Display memory usage information"