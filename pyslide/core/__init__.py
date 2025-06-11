"""
Core functionality for PySlide.
"""

from .models import Slide
from .execution import execute_code, generate_stack_trace

__all__ = ['Slide', 'execute_code', 'generate_stack_trace'] 