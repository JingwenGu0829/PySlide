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

### For Users
```bash
pip install git+https://github.com/JingwenGu0829/PySlide.git
```

### For Developers
```bash
git clone https://github.com/JingwenGu0829/PySlide.git
cd PySlide
pip install -e .
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
presentation.display()  # Opens in your default web browser
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
│   └── fibonacci.py
├── docs/
├── pyproject.toml
├── setup.py
├── README.md
└── LICENSE
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/JingwenGu0829/PySlide.git
cd PySlide
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

4. Run the example:
```bash
python examples/fibonacci.py
```

## Features in Detail

### Code Execution Tracing
- Line-by-line execution tracking
- Variable state capture
- Call stack monitoring
- Exception tracking

### Visualization Components
- Variable timeline view
- Call stack visualization
- Code annotations
- Interactive web interface

### Extensibility
- Support for custom language adapters
- Pluggable visualization components
- Custom presentation renderers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python's built-in tracing capabilities
- Web interface powered by simple HTTP server
- Inspired by Python's debugger and code visualization tools 