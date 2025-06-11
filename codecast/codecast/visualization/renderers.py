"""
Presentation renderers for code execution traces.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from ..core.models import ExecutionEvent, ExecutionTrace
from .components import VariableVisualizer, CallStackVisualizer

class PresentationRenderer(ABC):
    """Abstract base for presentation renderers."""
    
    @abstractmethod
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> str:
        """Render trace as presentation.
        
        Args:
            trace: Execution trace to render
            config: Rendering configuration
            
        Returns:
            String representation of the presentation
        """
        pass

class WebRenderer(PresentationRenderer):
    """Render trace as interactive web presentation."""
    
    def __init__(self):
        self.visualizers = {
            'variables': VariableVisualizer(),
            'callstack': CallStackVisualizer()
        }
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> str:
        """Generate interactive web presentation."""
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
        """Serialize execution event for JSON."""
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
        """Serialize variables for JSON (handle non-serializable types)."""
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