#!/usr/bin/env python3
"""
Main entry point for the Python-based Command Terminal.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from python_terminal.core.terminal_core import TerminalCore
from python_terminal.config.settings import config
from python_terminal.utils.logging_config import setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Python-based Command Terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start CLI interface
  python main.py --web              # Start web interface
  python main.py --nlp              # Enable natural language processing
  python main.py --log-level DEBUG  # Enable debug logging
        """
    )
    
    parser.add_argument(
        '--interface', '-i',
        choices=['cli', 'web'],
        default='cli',
        help='Interface type to use (default: cli)'
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Start web interface (shortcut for --interface web)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=int(os.environ.get('PORT', 5000)),
        help='Port for web interface (default: 5000 or PORT env var)'
    )
    
    parser.add_argument(
        '--nlp',
        action='store_true',
        help='Enable natural language processing'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path (default: ~/.python_terminal/terminal.log)'
    )
    
    parser.add_argument(
        '--config-dir',
        type=str,
        help='Configuration directory path'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Python Terminal 1.0.0'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Set up logging
        log_file = args.log_file or str(config.log_file)
        logger = setup_logging(
            log_level=args.log_level,
            log_file=log_file,
            console_output=True
        )
        
        logger.info("Starting Python Terminal...")
        
        # Update configuration based on arguments
        if args.nlp:
            config.set('nlp_enabled', True)
            logger.info("Natural language processing enabled")
        
        if args.web or args.interface == 'web':
            config.set('web_port', args.port)
            interface_type = 'web'
        else:
            interface_type = 'cli'
        
        # Create and start terminal
        terminal = TerminalCore()
        
        logger.info(f"Starting {interface_type.upper()} interface...")
        terminal.start(interface_type=interface_type)
        
    except KeyboardInterrupt:
        print("\nTerminal interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting terminal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()