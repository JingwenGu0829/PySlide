"""
Visualization components for code execution data.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from ..core.models import ExecutionTrace

class VisualizationComponent(ABC):
    """Abstract base for visualization components."""
    
    @abstractmethod
    def render(self, data: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """Render visualization data.
        
        Args:
            data: Data to visualize
            config: Visualization configuration
            
        Returns:
            Dictionary containing visualization data
        """
        pass

class VariableVisualizer(VisualizationComponent):
    """Visualize variable changes over time."""
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate variable timeline visualization."""
        variables_timeline = {}
        
        for event in trace.events:
            if event.event_type == "line":
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
    """Visualize function call stack."""
    
    def render(self, trace: ExecutionTrace, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate call stack visualization."""
        stack_events = []
        current_stack = []
        
        for event in trace.events:
            if event.event_type == "call":
                current_stack.append(event.function_name)
                stack_events.append({
                    'timestamp': event.timestamp,
                    'action': 'push',
                    'function': event.function_name,
                    'line': event.line_number,
                    'stack': list(current_stack)
                })
            elif event.event_type == "return":
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