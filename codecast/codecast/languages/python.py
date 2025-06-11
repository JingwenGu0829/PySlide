"""
Python-specific implementation of the language adapter.
"""

import ast
import sys
import time
from typing import Any, Dict, List

from ..core.models import ExecutionEvent, ExecutionEventType, ExecutionTrace
from .base import LanguageAdapter

class PythonAdapter(LanguageAdapter):
    """Python-specific execution tracing implementation."""
    
    def __init__(self):
        self.trace_events: List[ExecutionEvent] = []
        self.start_time = 0
    
    def execute_and_trace(self, code: str, filename: str) -> ExecutionTrace:
        """Execute Python code with tracing."""
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
        """Internal tracing function."""
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
        """Parse Python source into AST."""
        return ast.parse(code)
    
    def extract_functions(self, parsed_code: ast.AST) -> List[str]:
        """Extract function names from Python AST."""
        functions = []
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions 