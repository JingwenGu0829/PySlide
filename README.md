# CodeCast

CodeCast is an interactive code execution visualization library that helps developers and educators understand code behavior through dynamic visualizations.

## Features

- Real-time code execution tracing
- Variable state visualization
- Call stack tracking
- Interactive web-based visualization
- Support for multiple programming languages (extensible)
- Code annotation support

## Installation

```bash
pip install codecast
```

## Quick Start

```python
from codecast import CodeCast

# Create a new CodeCast instance
codecast = CodeCast()

# Example code to visualize
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(5)
print(f"Fibonacci(5) = {result}")
"""

# Create and display the visualization
presentation = codecast.from_code(code, "fibonacci_example.py")
presentation.annotate(2, "Base case: return n for n <= 1")
presentation.display()
```

## Project Structure

```
codecast/
├── codecast/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── models.py
│   ├── languages/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── python.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── components.py
│   │   └── renderers.py
│   └── presentation/
│       ├── __init__.py
│       ├── templates/
│       └── server.py
├── tests/
├── examples/
├── docs/
├── pyproject.toml
├── README.md
└── LICENSE
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/codecast.git
cd codecast
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 