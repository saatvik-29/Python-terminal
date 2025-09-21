#!/usr/bin/env python3
"""
Web application entry point for deployment platforms like Render.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from python_terminal.core.terminal_core import TerminalCore
from python_terminal.config.settings import config
from python_terminal.utils.logging_config import setup_logging

# Initialize logging
logger = setup_logging(
    log_level=os.environ.get('LOG_LEVEL', 'INFO'),
    console_output=True
)

# Create terminal core
terminal = TerminalCore()

# Get the Flask app from web interface
from python_terminal.interfaces.web_interface import WebInterface
web_interface = WebInterface(terminal)
app = web_interface.app
socketio = web_interface.socketio

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting web server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)