"""
PySlide - Interactive Python Code Presentations
"""

import os
from typing import Dict, Any, Optional, List
from .core.models import Slide, Image
from .core.execution import execute_code, generate_stack_trace
from .visualization.renderer import create_html_content
from .utils.server import serve_presentation

__version__ = '0.1.0'

class PySlide:
    """Main class for creating interactive Python code presentations."""
    
    def __init__(self):
        self.slides: List[Slide] = []
        self.current_slide: Optional[Slide] = None
        self.static_files: Dict[str, str] = {}
    
    def new_slide(self, code: str, title: Optional[str] = None, description: Optional[str] = None) -> 'PySlide':
        """Create a new slide with the given code."""
        self.current_slide = Slide(code=code, title=title, description=description)
        self.slides.append(self.current_slide)
        return self
    
    def annotate(self, line_number: int, text: str) -> 'PySlide':
        """Add an annotation to the current slide."""
        if self.current_slide is None:
            raise ValueError("No current slide. Call new_slide() first.")
        self.current_slide.annotations[line_number] = text
        return self
    
    def add_visualization(self, name: str, data: Any) -> 'PySlide':
        """Add a visualization to the current slide."""
        if self.current_slide is None:
            raise ValueError("No current slide. Call new_slide() first.")
        self.current_slide.visualizations[name] = data
        return self
    
    def add_image(self, path: str, alt: str, caption: Optional[str] = None, 
                 width: Optional[int] = None, height: Optional[int] = None) -> 'PySlide':
        """Add an image to the current slide.
        
        Args:
            path (str): Path to the image file (can be local path or URL)
            alt (str): Alternative text for accessibility
            caption (Optional[str]): Optional caption text to display under the image
            width (Optional[int]): Optional width in pixels
            height (Optional[int]): Optional height in pixels
            
        Returns:
            PySlide: The PySlide instance (for method chaining)
            
        Raises:
            ValueError: If no current slide exists or if image file doesn't exist
        """
        if self.current_slide is None:
            raise ValueError("No current slide. Call new_slide() first.")
        
        # 检查文件是否存在
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise ValueError(f"Image file not found: {path}")
        
        # 为图片创建一个唯一的URL路径
        url_path = f"/static/{os.path.basename(path)}"
        self.static_files[url_path] = abs_path
        
        image = Image(path=url_path, alt=alt, caption=caption, width=width, height=height)
        self.current_slide.images.append(image)
        return self
    
    def execute_current_slide(self, globals_dict: Optional[Dict[str, Any]] = None) -> 'PySlide':
        """Execute the current slide's code and capture output."""
        if self.current_slide is None:
            raise ValueError("No current slide. Call new_slide() first.")
        
        result = execute_code(self.current_slide.code, globals_dict)
        if result['output']:
            self.current_slide.execution_output = result['output']
        elif result['error']:
            self.current_slide.execution_output = result['error']
        
        return self
    
    def add_stack_trace(self, function_name: str, globals_dict: Optional[Dict[str, Any]] = None) -> 'PySlide':
        """Add stack trace visualization for a function."""
        if self.current_slide is None:
            raise ValueError("No current slide. Call new_slide() first.")
        
        # Get the function from globals
        func = (globals_dict or {}).get(function_name)
        if func is None:
            raise ValueError(f"Function {function_name} not found in globals_dict")
        
        # Generate stack trace
        trace_info = generate_stack_trace(func)
        
        # Store trace information
        self.current_slide.stack_trace = {
            'function_name': function_name,
            'source': self.current_slide.code,
            'trace_info': trace_info
        }
        
        return self
    
    def display(self, port: int = 8000):
        """Display the presentation in a web browser."""
        presentation_data = {
            'slides': [
                {
                    'code': slide.code,
                    'annotations': slide.annotations,
                    'title': slide.title,
                    'description': slide.description,
                    'visualizations': slide.visualizations,
                    'execution_output': slide.execution_output,
                    'stack_trace': slide.stack_trace,
                    'images': [
                        {
                            'path': img.path,
                            'alt': img.alt,
                            'caption': img.caption,
                            'width': img.width,
                            'height': img.height
                        }
                        for img in slide.images
                    ]
                }
                for slide in self.slides
            ]
        }
        
        html_content = create_html_content(presentation_data)
        serve_presentation(html_content, self.static_files, port) 