"""
Core data models for PySlide.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class Slide:
    """A single slide in the presentation."""
    code: str
    annotations: Dict[int, str] = field(default_factory=dict)  # line_no -> annotation
    title: Optional[str] = None
    description: Optional[str] = None
    visualizations: Dict[str, Any] = field(default_factory=dict)
    execution_output: Optional[str] = None
    stack_trace: Optional[Dict[str, Any]] = None 