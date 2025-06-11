"""
Code execution and stack tracing functionality.
"""

import sys
import inspect
import traceback
from io import StringIO
from typing import Dict, Any, List, Optional, Callable

def execute_code(code: str, globals_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute code and capture output."""
    output_buffer = StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer
    
    try:
        # Execute code
        exec_globals = globals_dict or {}
        exec(code, exec_globals)
        output = output_buffer.getvalue()
        return {
            'success': True,
            'output': output if output else None,
            'error': None
        }
    except Exception:
        return {
            'success': False,
            'output': None,
            'error': traceback.format_exc()
        }
    finally:
        sys.stdout = old_stdout

def generate_stack_trace(func: Callable, test_input: Any = 5) -> Dict[str, Any]:
    """Generate a stack trace for a function."""
    calls: List[Dict[str, Any]] = []
    
    try:
        # Capture stdout
        old_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        
        # Call the function and track the stack
        def tracer(frame, event, arg):
            if event == 'call' and frame.f_code.co_name == func.__name__:
                # Get the call context
                args = inspect.getargvalues(frame)
                calls.append({
                    'line': frame.f_lineno,
                    'args': {name: args.locals[name] for name in args.args},
                    'caller': frame.f_back.f_code.co_name if frame.f_back else None
                })
            return tracer
        
        # Set up the tracer
        sys.settrace(tracer)
        result = func(test_input)  # Call with test input
        sys.settrace(None)
        
        # Get output
        output = output_buffer.getvalue()
        
        return {
            'calls': calls,
            'result': result,
            'output': output,
            'error': None,
            'traceback': None
        }
    except Exception as e:
        return {
            'calls': calls,
            'result': None,
            'output': None,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
    finally:
        sys.stdout = old_stdout
        sys.settrace(None) 