"""
Core data models for PySlide.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

@dataclass
class Image:
    """An image in a slide."""
    path: str  # Path to the image file
    alt: str  # Alt text for accessibility
    caption: Optional[str] = None  # Optional caption
    width: Optional[int] = None  # Optional width in pixels
    height: Optional[int] = None  # Optional height in pixels

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
    images: List[Image] = field(default_factory=list)  # List of images in the slide 