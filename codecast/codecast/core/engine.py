"""
Core execution engine for code tracing and visualization.
"""

from pathlib import Path
from typing import Any, Callable, Dict, List

from ..languages.base import LanguageAdapter
from ..languages.python import PythonAdapter
from .models import ExecutionTrace

class ExecutionEngine:
    """Core engine for code execution and tracing."""
    
    def __init__(self):
        self.adapters: Dict[str, LanguageAdapter] = {
            'python': PythonAdapter(),
            # Add more languages here
        }
        self.preprocessors: List[Callable] = []
        self.postprocessors: List[Callable] = []
    
    def register_language(self, name: str, adapter: LanguageAdapter):
        """Register a new language adapter.
        
        Args:
            name: Language identifier
            adapter: Language adapter instance
        """
        self.adapters[name] = adapter
    
    def add_preprocessor(self, func: Callable):
        """Add code preprocessor.
        
        Args:
            func: Preprocessor function that takes code string and returns modified code
        """
        self.preprocessors.append(func)
    
    def add_postprocessor(self, func: Callable):
        """Add trace postprocessor.
        
        Args:
            func: Postprocessor function that takes ExecutionTrace and returns modified trace
        """
        self.postprocessors.append(func)
    
    def execute_file(self, filepath: str, language: str = 'python') -> ExecutionTrace:
        """Execute a file and return trace.
        
        Args:
            filepath: Path to source file
            language: Programming language (default: python)
            
        Returns:
            ExecutionTrace containing execution data
            
        Raises:
            ValueError: If language is not supported
            FileNotFoundError: If file doesn't exist
        """
        if language not in self.adapters:
            raise ValueError(f"Unsupported language: {language}")
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        code = path.read_text()
        return self.execute_code(code, str(path), language)
    
    def execute_code(self, code: str, filename: str = '<string>', language: str = 'python') -> ExecutionTrace:
        """Execute code string and return trace.
        
        Args:
            code: Source code to execute
            filename: Name for the code (default: <string>)
            language: Programming language (default: python)
            
        Returns:
            ExecutionTrace containing execution data
            
        Raises:
            ValueError: If language is not supported
        """
        if language not in self.adapters:
            raise ValueError(f"Unsupported language: {language}")
        
        # Apply preprocessors
        for preprocessor in self.preprocessors:
            code = preprocessor(code)
        
        # Execute with appropriate adapter
        adapter = self.adapters[language]
        trace = adapter.execute_and_trace(code, filename)
        
        # Apply postprocessors
        for postprocessor in self.postprocessors:
            trace = postprocessor(trace)
        
        return trace 