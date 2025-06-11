# PySlide Documentation

PySlide is a Python library for creating interactive code presentations that bridges the gap between Jupyter notebooks and PowerPoint slides. It allows you to create beautiful, executable presentations with code, annotations, and optional visualizations.

## Quick Start

```python
from pyslide import PySlide

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Create presentation
presentation = PySlide()

# Add a slide
presentation.new_slide(
    code="""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    title="Fibonacci Sequence",
    description="A recursive implementation"
).annotate(1, "Function definition")

# Add stack trace visualization
presentation.add_stack_trace('fibonacci', {'fibonacci': fibonacci})

# Execute code and capture output
presentation.execute_current_slide({'fibonacci': fibonacci})

# Display the presentation
presentation.display()
```

## Features

- Create slides with Python code and annotations
- Execute code and capture output in real-time
- Add optional visualizations and stack traces
- Beautiful syntax highlighting
- Keyboard navigation (arrow keys and space)
- Modern, clean interface

## Installation

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install PySlide
pip install pyslide
```

## Documentation Sections

- [API Reference](api/index.md) - Detailed documentation of all PySlide classes and methods
- [Examples](examples/index.md) - Example presentations and use cases
- [User Guide](guides/index.md) - In-depth guides and tutorials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 