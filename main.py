# CodeCast - Interactive Code Execution Presentation Library
# Core Architecture and Backbone Implementation

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import ast
import sys
import traceback
from pathlib import Path
import importlib.util
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import tempfile
import os

# ================================
# Core Data Models
# ================================

class ExecutionEventType(Enum):
    LINE = "line"
    CALL = "call"
    RETURN = "return"
    EXCEPTION = "exception"
    VARIABLE_CHANGE = "variable_change"
    OUTPUT = "output"
    ANNOTATION = "annotation"

@dataclass
class ExecutionEvent:
    """Single event in code execution trace"""
    timestamp: float
    event_type: ExecutionEventType
    line_number: int
    function_name: str
    filename: str
    locals_snapshot: Dict[str, Any]
    globals_snapshot: Dict[str, Any]
    output: Optional[str] = None
    exception: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionTrace:
    """Complete execution trace with metadata"""
    events: List[ExecutionEvent]
    source_code: str
    filename: str
    execution_time: float
    annotations: Dict[int, str] = field(default_factory=dict)  # line_no -> annotation
    visualizations: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

# ================================
# Language Abstraction Layer
# ================================

class LanguageAdapter(ABC):
    """Abstract base for language-specific execution tracing"""
    
    @abstractmethod
    def execute_and_trace(self, code: str, filename: str) -> ExecutionTrace:
        """Execute code and return execution trace"""
        pass
    
    @abstractmethod
    def parse_source(self, code: str) -> Any:
        """Parse source code into AST or equivalent"""
        pass
    
    @abstractmethod
    def extract_functions(self, parsed_code: Any) -> List[str]:
        """Extract function names from parsed code"""
        pass

class PythonAdapter(LanguageAdapter):
    """Python-specific execution tracing"""
    
    def __init__(self):
        self.trace_events: List[ExecutionEvent] = []
        self.start_time = 0
    
    def execute_and_trace(self, code: str, filename: str) -> ExecutionTrace:
        """Execute Python code with tracing"""
        self.trace_events = []
        self.start_time = time.time()
        
        # Parse and validate code
        try:
            parsed = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
        
        # Set up tracing
        old_trace = sys.gettrace()
        sys.settrace(self._trace_calls)
        
        # Prepare execution environment
        globals_dict = {'__name__': '__main__', '__file__': filename}
        locals_dict = {}
        
        try:
            # Execute code
            exec(compile(parsed, filename, 'exec'), globals_dict, locals_dict)
        except Exception as e:
            # Record exception
            self.trace_events.append(ExecutionEvent(
                timestamp=time.time() - self.start_time,
                event_type=ExecutionEventType.EXCEPTION,
                line_number=getattr(e, 'lineno', -1),
                function_name='<module>',
                filename=filename,
                locals_snapshot={},
                globals_snapshot={},
                exception=str(e)
            ))
        finally:
            sys.settrace(old_trace)
        
        return ExecutionTrace(
            events=self.trace_events,
            source_code=code,
            filename=filename,
            execution_time=time.time() - self.start_time
        )
    
    def _trace_calls(self, frame, event, arg):
        """Internal tracing function"""
        if event in ['call', 'line', 'return']:
            self.trace_events.append(ExecutionEvent(
                timestamp=time.time() - self.start_time,
                event_type=ExecutionEventType(event),
                line_number=frame.f_lineno,
                function_name=frame.f_code.co_name,
                filename=frame.f_code.co_filename,
                locals_snapshot=dict(frame.f_locals),
                globals_snapshot=dict(frame.f_globals)
            ))
        return self._trace_calls
    
    def parse_source(self, code: str) -> ast.AST:
        return ast.parse(code)
    
    def extract_functions(self, parsed_code: ast.AST) -> List[str]:
        functions = []
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions

# ================================
# Execution Engine
# ================================

class ExecutionEngine:
    """Core engine for code execution and tracing"""
    
    def __init__(self):
        self.adapters = {
            'python': PythonAdapter(),
            # Add more languages here
        }
        self.preprocessors: List[Callable] = []
        self.postprocessors: List[Callable] = []
    
    def register_language(self, name: str, adapter: LanguageAdapter):
        """Register a new language adapter"""
        self.adapters[name] = adapter
    
    def add_preprocessor(self, func: Callable):
        """Add code preprocessor"""
        self.preprocessors.append(func)
    
    def add_postprocessor(self, func: Callable):
        """Add trace postprocessor"""
        self.postprocessors.append(func)
    
    def execute_file(self, filepath: str, language: str = 'python') -> ExecutionTrace:
        """Execute a file and return trace"""
        if language not in self.adapters:
            raise ValueError(f"Unsupported language: {language}")
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        code = path.read_text()
        return self.execute_code(code, str(path), language)
    
    def execute_code(self, code: str, filename: str, language: str = 'python') -> ExecutionTrace:
        """Execute code string and return trace"""
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

# ================================
# Visualization Framework
# ================================

class VisualizationComponent(ABC):
    """Abstract base for visualization components"""
    
    @abstractmethod
    def render(self, data: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """Render visualization data"""
        pass

class VariableVisualizer(VisualizationComponent):
    """Visualize variable changes over time"""
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate variable timeline visualization"""
        variables_timeline = {}
        
        for event in trace.events:
            if event.event_type == ExecutionEventType.LINE:
                for var_name, var_value in event.locals_snapshot.items():
                    if var_name not in variables_timeline:
                        variables_timeline[var_name] = []
                    
                    variables_timeline[var_name].append({
                        'timestamp': event.timestamp,
                        'line': event.line_number,
                        'value': str(var_value),
                        'type': type(var_value).__name__
                    })
        
        return {
            'type': 'variable_timeline',
            'data': variables_timeline,
            'config': config
        }

class CallStackVisualizer(VisualizationComponent):
    """Visualize function call stack"""
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> Dict[str, Any]:
        stack_events = []
        current_stack = []
        
        for event in trace.events:
            if event.event_type == ExecutionEventType.CALL:
                current_stack.append(event.function_name)
                stack_events.append({
                    'timestamp': event.timestamp,
                    'action': 'push',
                    'function': event.function_name,
                    'line': event.line_number,
                    'stack': list(current_stack)
                })
            elif event.event_type == ExecutionEventType.RETURN:
                if current_stack:
                    current_stack.pop()
                stack_events.append({
                    'timestamp': event.timestamp,
                    'action': 'pop',
                    'function': event.function_name,
                    'line': event.line_number,
                    'stack': list(current_stack)
                })
        
        return {
            'type': 'call_stack',
            'data': stack_events,
            'config': config
        }

# ================================
# Presentation Generator
# ================================

class PresentationRenderer(ABC):
    """Abstract base for presentation renderers"""
    
    @abstractmethod
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> str:
        """Render trace as presentation"""
        pass

class WebRenderer(PresentationRenderer):
    """Render trace as interactive web presentation"""
    
    def __init__(self):
        self.visualizers = {
            'variables': VariableVisualizer(),
            'callstack': CallStackVisualizer()
        }
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> str:
        """Generate interactive web presentation"""
        # Generate visualizations
        visualizations = {}
        for name, visualizer in self.visualizers.items():
            if config.get(f'enable_{name}', True):
                visualizations[name] = visualizer.render(trace, config.get(name, {}))
        
        # Prepare data for frontend
        presentation_data = {
            'trace': {
                'events': [self._serialize_event(e) for e in trace.events],
                'source_code': trace.source_code,
                'filename': trace.filename,
                'execution_time': trace.execution_time,
                'annotations': trace.annotations
            },
            'visualizations': visualizations,
            'config': config
        }
        
        return json.dumps(presentation_data, indent=2)
    
    def _serialize_event(self, event: ExecutionEvent) -> Dict[str, Any]:
        """Serialize execution event for JSON"""
        return {
            'timestamp': event.timestamp,
            'event_type': event.event_type.value,
            'line_number': event.line_number,
            'function_name': event.function_name,
            'filename': event.filename,
            'locals_snapshot': self._serialize_variables(event.locals_snapshot),
            'globals_snapshot': self._serialize_variables(event.globals_snapshot),
            'output': event.output,
            'exception': event.exception,
            'metadata': event.metadata
        }
    
    def _serialize_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize variables for JSON (handle non-serializable types)"""
        serialized = {}
        for name, value in variables.items():
            try:
                json.dumps(value)  # Test if serializable
                serialized[name] = value
            except (TypeError, ValueError):
                serialized[name] = {
                    'type': type(value).__name__,
                    'repr': repr(value),
                    'serializable': False
                }
        return serialized

# ================================
# Main API
# ================================

class CodeCast:
    """Main API for the CodeCast library"""
    
    def __init__(self):
        self.engine = ExecutionEngine()
        self.renderers = {
            'web': WebRenderer()
        }
    
    def from_file(self, filepath: str, language: str = 'python') -> 'CodeCastPresentation':
        """Create presentation from file"""
        trace = self.engine.execute_file(filepath, language)
        return CodeCastPresentation(trace, self.renderers)
    
    def from_code(self, code: str, filename: str = '<string>', language: str = 'python') -> 'CodeCastPresentation':
        """Create presentation from code string"""
        trace = self.engine.execute_code(code, filename, language)
        return CodeCastPresentation(trace, self.renderers)
    
    def register_language(self, name: str, adapter: LanguageAdapter):
        """Register new language support"""
        self.engine.register_language(name, adapter)
    
    def register_renderer(self, name: str, renderer: PresentationRenderer):
        """Register new presentation renderer"""
        self.renderers[name] = renderer

class CodeCastPresentation:
    """A presentation generated from executed code"""
    
    def __init__(self, trace: ExecutionTrace, renderers: Dict[str, PresentationRenderer]):
        self.trace = trace
        self.renderers = renderers
    
    def annotate(self, line_number: int, text: str):
        """Add annotation to specific line"""
        self.trace.annotations[line_number] = text
        return self
    
    def render(self, format: str = 'web', config: Optional[Dict[str, Any]] = None) -> str:
        """Render presentation in specified format"""
        if format not in self.renderers:
            raise ValueError(f"Unsupported format: {format}")
        
        config = config or {}
        return self.renderers[format].render(self.trace, config)
    
    def save(self, filepath: str, format: str = 'web', config: Optional[Dict[str, Any]] = None):
        """Save presentation to file"""
        content = self.render(format, config)
        Path(filepath).write_text(content)
    
    def display(self, port: int = 8000):
        """Display the presentation in a web browser"""
        # Create HTML template
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CodeCast Visualization</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                pre { background: #f5f5f5; padding: 10px; border-radius: 4px; }
                .visualization { margin: 20px 0; }
            </style>
            <script>
                // Parse and display the presentation data
                const presentationData = PRESENTATION_DATA_PLACEHOLDER;
                
                function displayPresentation() {
                    const container = document.getElementById('presentation');
                    
                    // Display source code
                    const codeSection = document.createElement('div');
                    codeSection.innerHTML = `<h2>Source Code</h2><pre>${presentationData.trace.source_code}</pre>`;
                    container.appendChild(codeSection);
                    
                    // Display execution trace
                    const traceSection = document.createElement('div');
                    traceSection.innerHTML = '<h2>Execution Trace</h2>';
                    presentationData.trace.events.forEach(event => {
                        traceSection.innerHTML += `<div>
                            <strong>Line ${event.line_number}</strong> - ${event.event_type}
                            ${event.output ? `<br>Output: ${event.output}` : ''}
                            ${event.exception ? `<br>Exception: ${event.exception}` : ''}
                        </div>`;
                    });
                    container.appendChild(traceSection);
                    
                    // Display visualizations
                    if (presentationData.visualizations) {
                        const visSection = document.createElement('div');
                        visSection.innerHTML = '<h2>Visualizations</h2>';
                        for (const [name, vis] of Object.entries(presentationData.visualizations)) {
                            visSection.innerHTML += `
                                <div class="visualization">
                                    <h3>${name}</h3>
                                    <pre>${JSON.stringify(vis, null, 2)}</pre>
                                </div>
                            `;
                        }
                        container.appendChild(visSection);
                    }
                }
            </script>
        </head>
        <body onload="displayPresentation()">
            <h1>CodeCast Visualization</h1>
            <div id="presentation"></div>
        </body>
        </html>
        """
        
        # Generate presentation data
        presentation_data = self.render('web', {
            'enable_variables': True,
            'enable_callstack': True,
            'theme': 'dark'
        })
        
        # Create HTML file with presentation data
        html_content = html_template.replace('PRESENTATION_DATA_PLACEHOLDER', presentation_data)
        
        # Create temporary directory for serving files
        temp_dir = tempfile.mkdtemp()
        html_path = os.path.join(temp_dir, 'index.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        # Set up simple HTTP server
        os.chdir(temp_dir)
        server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
        print(f"Starting server at http://localhost:{port}")
        
        # Open browser
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.shutdown()

# ================================
# Example Usage
# ================================

if __name__ == "__main__":
    # Example usage
    codecast = CodeCast()
    
    # Simple example code
    example_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(5)
print(f"Fibonacci(5) = {result}")
"""
    
    # Create presentation
    presentation = codecast.from_code(example_code, "fibonacci_example.py")
    
    # Add annotations
    presentation.annotate(2, "Base case: return n for n <= 1")
    presentation.annotate(4, "Recursive case: sum of two previous numbers")
    
    # Display the presentation in a web browser
    presentation.display()