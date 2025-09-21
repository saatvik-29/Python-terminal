"""
Web-based terminal interface using Flask.
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
from python_terminal.utils.logging_config import get_logger


class WebInterface:
    """Web-based terminal interface."""
    
    def __init__(self, terminal_core):
        self.terminal_core = terminal_core
        self.logger = get_logger('web_interface')
        
        # Create Flask app
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.app.config['SECRET_KEY'] = 'python-terminal-secret-key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Setup routes
        self._setup_routes()
        self._setup_socket_events()
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            return self._get_terminal_html()
        
        @self.app.route('/api/execute', methods=['POST'])
        def execute_command():
            data = request.get_json()
            command = data.get('command', '')
            
            result = self.terminal_core.execute_command(command)
            
            return jsonify({
                'success': result.success,
                'output': result.output,
                'error': result.error_message,
                'execution_time': result.execution_time
            })
    
    def _setup_socket_events(self):
        """Setup SocketIO events."""
        
        @self.socketio.on('execute_command')
        def handle_command(data):
            command = data.get('command', '')
            result = self.terminal_core.execute_command(command)
            
            emit('command_result', {
                'success': result.success,
                'output': result.output,
                'error': result.error_message,
                'execution_time': result.execution_time,
                'cwd': str(self.terminal_core.get_context().current_directory)
            })
        
        @self.socketio.on('get_cwd')
        def handle_get_cwd():
            emit('cwd_update', {
                'cwd': str(self.terminal_core.get_context().current_directory)
            })
    
    def start_server(self, host='0.0.0.0', port=5000, debug=False):
        """Start the web server."""
        self.logger.info(f"Starting web interface on {host}:{port}")
        
        # Create templates directory and files
        self._create_web_files()
        
        try:
            self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
        except Exception as e:
            self.logger.error(f"Failed to start web server: {e}")
            raise
    
    def _get_terminal_html(self):
        """Return the terminal HTML content."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Terminal</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        
        .terminal {
            width: 100%;
            height: 80vh;
            background-color: #000;
            border: 2px solid #333;
            padding: 10px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        
        .input-line {
            display: flex;
            align-items: center;
            margin-top: 10px;
        }
        
        .prompt {
            color: #00ff00;
            margin-right: 5px;
        }
        
        #command-input {
            background: transparent;
            border: none;
            color: #00ff00;
            font-family: inherit;
            font-size: inherit;
            outline: none;
            flex: 1;
        }
        
        .output {
            color: #ffffff;
            margin: 5px 0;
        }
        
        .error {
            color: #ff0000;
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Python Terminal Web Interface</h1>
        <p>Type commands below. Use 'help' for available commands.</p>
    </div>
    
    <div class="terminal" id="terminal">
        <div>Python Terminal v1.0.0 - Web Interface</div>
        <div>Type 'help' for available commands or 'exit' to quit.</div>
        <div id="output"></div>
        
        <div class="input-line">
            <span class="prompt" id="prompt">user:~$ </span>
            <input type="text" id="command-input" autocomplete="off" autofocus>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        const output = document.getElementById('output');
        const commandInput = document.getElementById('command-input');
        const prompt = document.getElementById('prompt');
        const terminal = document.getElementById('terminal');
        
        let currentDir = '~';
        
        // Handle command execution
        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const command = commandInput.value.trim();
                if (command) {
                    // Display command
                    addOutput(`${prompt.textContent}${command}`, 'command');
                    
                    // Execute command
                    socket.emit('execute_command', {command: command});
                    
                    // Clear input
                    commandInput.value = '';
                }
            }
        });
        
        // Handle command results
        socket.on('command_result', function(data) {
            if (data.output) {
                addOutput(data.output, 'output');
            }
            if (data.error) {
                addOutput(data.error, 'error');
            }
            
            // Update prompt with current directory
            if (data.cwd) {
                currentDir = data.cwd.replace(process.env.HOME || '', '~');
                prompt.textContent = `user:${currentDir}$ `;
            }
            
            // Scroll to bottom
            terminal.scrollTop = terminal.scrollHeight;
        });
        
        // Handle CWD updates
        socket.on('cwd_update', function(data) {
            currentDir = data.cwd.replace(process.env.HOME || '', '~');
            prompt.textContent = `user:${currentDir}$ `;
        });
        
        function addOutput(text, type) {
            const div = document.createElement('div');
            div.className = type;
            div.textContent = text;
            output.appendChild(div);
        }
        
        // Get initial CWD
        socket.emit('get_cwd');
    </script>
</body>
</html>'''
    
    def _create_web_files(self):
        """Placeholder for web files creation."""
        pass