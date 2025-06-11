"""
Core data models for CodeCast.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

class ExecutionEventType(Enum):
    """Types of execution events that can be tracked."""
    LINE = "line"
    CALL = "call"
    RETURN = "return"
    EXCEPTION = "exception"
    VARIABLE_CHANGE = "variable_change"
    OUTPUT = "output"
    ANNOTATION = "annotation"

@dataclass
class ExecutionEvent:
    """Single event in code execution trace."""
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
    """Complete execution trace with metadata."""
    events: List[ExecutionEvent]
    source_code: str
    filename: str
    execution_time: float
    annotations: Dict[int, str] = field(default_factory=dict)  # line_no -> annotation
    visualizations: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict) 