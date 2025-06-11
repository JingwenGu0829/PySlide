"""
Base class for language-specific adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, List

from ..core.models import ExecutionTrace

class LanguageAdapter(ABC):
    """Abstract base for language-specific execution tracing."""
    
    @abstractmethod
    def execute_and_trace(self, code: str, filename: str) -> ExecutionTrace:
        """Execute code and return execution trace.
        
        Args:
            code: Source code to execute
            filename: Name of the file (for reference)
            
        Returns:
            ExecutionTrace containing the complete execution trace
        """
        pass
    
    @abstractmethod
    def parse_source(self, code: str) -> Any:
        """Parse source code into AST or equivalent.
        
        Args:
            code: Source code to parse
            
        Returns:
            Language-specific parsed code representation
        """
        pass
    
    @abstractmethod
    def extract_functions(self, parsed_code: Any) -> List[str]:
        """Extract function names from parsed code.
        
        Args:
            parsed_code: Parsed code from parse_source()
            
        Returns:
            List of function names found in the code
        """
        pass 