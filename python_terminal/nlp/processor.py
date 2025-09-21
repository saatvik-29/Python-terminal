"""
Simple natural language processor for terminal commands.
"""

import re
from typing import Optional
from python_terminal.utils.logging_config import get_logger


class SimpleNLPProcessor:
    """Simple rule-based NLP processor for common terminal commands."""
    
    def __init__(self):
        self.logger = get_logger('nlp_processor')
        
        # Define command patterns
        self.patterns = [
            # Directory operations
            (r'create (?:a )?(?:new )?(?:folder|directory) (?:called |named )?(.+)', r'mkdir \1'),
            (r'make (?:a )?(?:new )?(?:folder|directory) (?:called |named )?(.+)', r'mkdir \1'),
            (r'go to (?:the )?(?:folder|directory) (.+)', r'cd \1'),
            (r'change to (?:the )?(?:folder|directory) (.+)', r'cd \1'),
            (r'navigate to (.+)', r'cd \1'),
            
            # File operations
            (r'show (?:me )?(?:the )?contents? of (?:the )?file (.+)', r'cat \1'),
            (r'display (?:the )?file (.+)', r'cat \1'),
            (r'read (?:the )?file (.+)', r'cat \1'),
            (r'copy (?:the )?file (.+) to (.+)', r'cp \1 \2'),
            (r'move (?:the )?file (.+) (?:to|into) (.+)', r'mv \1 \2'),
            (r'rename (?:the )?file (.+) to (.+)', r'mv \1 \2'),
            (r'delete (?:the )?file (.+)', r'rm \1'),
            (r'remove (?:the )?file (.+)', r'rm \1'),
            
            # Listing operations
            (r'show (?:me )?(?:all )?(?:the )?files?(?: in (?:the )?(?:current )?(?:folder|directory))?', r'ls'),
            (r'list (?:all )?(?:the )?files?(?: in (?:the )?(?:current )?(?:folder|directory))?', r'ls'),
            (r'what(?:\'s| is) in (?:this|the current) (?:folder|directory)', r'ls'),
            (r'show (?:me )?(?:the )?files in (.+)', r'ls \1'),
            (r'list (?:the )?files in (.+)', r'ls \1'),
            
            # Location operations
            (r'where am i\??', r'pwd'),
            (r'what(?:\'s| is) (?:my )?current (?:folder|directory|location)\??', r'pwd'),
            (r'show (?:me )?(?:my )?current (?:folder|directory|location)', r'pwd'),
            
            # Search operations
            (r'find (?:all )?files? (?:called |named )?(.+)', r'find . -name \1'),
            (r'search for (?:files? )?(?:called |named )?(.+)', r'find . -name \1'),
            (r'look for (.+) in (?:the )?file (.+)', r'grep \1 \2'),
            (r'search for (.+) in (?:the )?file (.+)', r'grep \1 \2'),
            
            # System operations
            (r'show (?:me )?(?:all )?(?:running )?processes', r'ps'),
            (r'list (?:all )?(?:running )?processes', r'ps'),
            (r'what processes are running\??', r'ps'),
            (r'show (?:me )?system (?:info|information|resources)', r'top'),
            (r'kill (?:the )?process (\d+)', r'kill \1'),
            (r'terminate (?:the )?process (\d+)', r'kill \1'),
            
            # Help operations
            (r'help(?: me)?', r'help'),
            (r'what can (?:i|you) do\??', r'help'),
            (r'show (?:me )?(?:available )?commands', r'help'),
            
            # Echo operations
            (r'say (.+)', r'echo \1'),
            (r'print (.+)', r'echo \1'),
        ]
    
    def process_natural_language(self, query: str) -> Optional[str]:
        """
        Convert natural language query to terminal command.
        
        Args:
            query: Natural language query
            
        Returns:
            Converted command or None if no match found
        """
        query = query.strip().lower()
        
        # Try to match against patterns
        for pattern, replacement in self.patterns:
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                try:
                    # Replace captured groups
                    command = replacement
                    for i, group in enumerate(match.groups(), 1):
                        command = command.replace(f'\\{i}', group.strip())
                    
                    self.logger.info(f"NLP: '{query}' -> '{command}'")
                    return command
                except Exception as e:
                    self.logger.error(f"Error processing NLP pattern: {e}")
                    continue
        
        return None
    
    def is_natural_language(self, text: str) -> bool:
        """
        Check if text appears to be natural language rather than a command.
        
        Args:
            text: Input text
            
        Returns:
            True if text appears to be natural language
        """
        # Simple heuristics for natural language detection
        text = text.strip().lower()
        
        # Check for question words
        question_words = ['what', 'where', 'how', 'why', 'when', 'who', 'which']
        if any(text.startswith(word) for word in question_words):
            return True
        
        # Check for common natural language phrases
        nl_phrases = ['show me', 'can you', 'i want to', 'please', 'help me']
        if any(phrase in text for phrase in nl_phrases):
            return True
        
        # Check if it contains spaces and common words
        if ' ' in text and any(word in text for word in ['the', 'a', 'an', 'to', 'in', 'of']):
            return True
        
        return False