# Python-Based Command Terminal

A fully functioning command terminal that mimics the behavior of a real system terminal, built entirely in Python.

## Features

- **Complete File Operations**: Support for ls, cd, pwd, mkdir, rm, cp, mv, cat, grep, find, and more
- **System Monitoring**: Built-in commands for process management (ps, top, kill) and resource monitoring
- **Natural Language Processing**: AI-driven terminal that understands natural language queries
- **Command History**: Full command history with navigation and search capabilities
- **Auto-completion**: Intelligent tab completion for commands and file paths
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Multiple Interfaces**: Both CLI and web-based interfaces available
- **Extensible Architecture**: Plugin-based system for easy command additions

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-command-terminal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Deploy on Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Select this repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

The application will be automatically deployed and accessible via the provided URL.

## Usage

### CLI Interface (Local)
```bash
python main.py
```

### Web Interface (Local)
```bash
python main.py --web --port 5000
```

### Web Interface (Deployed)
Access the deployed URL provided by Render

### Natural Language Mode
```bash
python main.py --nlp
```

## Supported Commands

### File Operations
- `ls` - List directory contents
- `cd` - Change directory
- `pwd` - Print working directory
- `mkdir` - Create directories
- `rm` - Remove files
- `rmdir` - Remove directories
- `cp` - Copy files
- `mv` - Move/rename files
- `cat` - Display file contents
- `grep` - Search text patterns
- `find` - Find files and directories
- `wc` - Word, line, character count

### System Monitoring
- `ps` - List running processes
- `top` - Real-time system monitor
- `kill` - Terminate processes
- `df` - Disk usage information
- `free` - Memory usage statistics

### Utility Commands
- `history` - Command history
- `help` - Command help
- `exit` - Exit terminal

## Natural Language Examples

Instead of remembering exact command syntax, you can use natural language:

- "create a new folder called test" → `mkdir test`
- "move file1.txt into the test folder" → `mv file1.txt test/`
- "show me all files in the current directory" → `ls -la`
- "delete the file named example.txt" → `rm example.txt`

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black python_terminal/
```

### Type Checking
```bash
mypy python_terminal/
```

## Architecture

The terminal follows a modular, plugin-based architecture:

- **Core**: Terminal orchestration and command processing
- **Commands**: Individual command implementations
- **Interfaces**: CLI and web interface implementations
- **Utils**: Shared utilities and helpers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.