"""
CodeCast - Interactive Code Execution Visualization Library
"""

from typing import Dict, Any, Optional

from .core.engine import ExecutionEngine
from .core.models import ExecutionTrace
from .languages.base import LanguageAdapter
from .presentation.server import PresentationServer
from .visualization.renderers import PresentationRenderer, WebRenderer

class CodeCast:
    """Main API for the CodeCast library."""
    
    def __init__(self):
        self.engine = ExecutionEngine()
        self.renderers = {
            'web': WebRenderer()
        }
    
    def from_file(self, filepath: str, language: str = 'python') -> 'CodeCastPresentation':
        """Create presentation from file.
        
        Args:
            filepath: Path to source file
            language: Programming language (default: python)
            
        Returns:
            CodeCastPresentation instance
        """
        trace = self.engine.execute_file(filepath, language)
        return CodeCastPresentation(trace, self.renderers)
    
    def from_code(self, code: str, filename: str = '<string>', language: str = 'python') -> 'CodeCastPresentation':
        """Create presentation from code string.
        
        Args:
            code: Source code to execute
            filename: Name for the code (default: <string>)
            language: Programming language (default: python)
            
        Returns:
            CodeCastPresentation instance
        """
        trace = self.engine.execute_code(code, filename, language)
        return CodeCastPresentation(trace, self.renderers)
    
    def register_language(self, name: str, adapter: LanguageAdapter):
        """Register new language support.
        
        Args:
            name: Language identifier
            adapter: Language adapter instance
        """
        self.engine.register_language(name, adapter)
    
    def register_renderer(self, name: str, renderer: PresentationRenderer):
        """Register new presentation renderer.
        
        Args:
            name: Renderer identifier
            renderer: Renderer instance
        """
        self.renderers[name] = renderer

class CodeCastPresentation:
    """A presentation generated from executed code."""
    
    def __init__(self, trace: ExecutionTrace, renderers: Dict[str, PresentationRenderer]):
        self.trace = trace
        self.renderers = renderers
        self.server = PresentationServer()
    
    def annotate(self, line_number: int, text: str) -> 'CodeCastPresentation':
        """Add annotation to specific line.
        
        Args:
            line_number: Line number to annotate
            text: Annotation text
            
        Returns:
            Self for method chaining
        """
        self.trace.annotations[line_number] = text
        return self
    
    def render(self, format: str = 'web', config: Optional[Dict[str, Any]] = None) -> str:
        """Render presentation in specified format.
        
        Args:
            format: Output format (default: web)
            config: Rendering configuration
            
        Returns:
            String representation of the presentation
            
        Raises:
            ValueError: If format is not supported
        """
        if format not in self.renderers:
            raise ValueError(f"Unsupported format: {format}")
        
        config = config or {}
        return self.renderers[format].render(self.trace, config)
    
    def display(self, port: int = 8000):
        """Display the presentation in a web browser.
        
        Args:
            port: Port to serve on (default: 8000)
        """
        presentation_data = self.render('web', {
            'enable_variables': True,
            'enable_callstack': True,
            'theme': 'dark'
        })
        self.server.serve_presentation(presentation_data, port)

# Version
__version__ = '0.1.0' 