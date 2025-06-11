# User Guide

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setting Up

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install PySlide:
```bash
pip install pyslide
```

## Basic Concepts

### Slides

A PySlide presentation consists of one or more slides. Each slide can contain:
- Python code
- Title (optional)
- Description (optional)
- Line annotations
- Visualizations
- Execution output

### Code Execution

PySlide can execute the code in your slides and capture the output. This is useful for:
- Demonstrating code behavior
- Showing function output
- Creating interactive examples

### Annotations

Annotations help explain your code by attaching comments to specific lines. Use them to:
- Explain algorithms
- Point out important concepts
- Highlight key implementation details

### Visualizations

PySlide supports various types of visualizations:
- Stack traces for function calls
- Tree structures
- Custom JSON-based visualizations

## Best Practices

### Code Organization

1. Keep code snippets focused and concise
2. Use meaningful variable and function names
3. Include comments for complex logic
4. Break down complex examples into multiple slides

### Annotations

1. Keep annotations brief and clear
2. Annotate key concepts and decision points
3. Use consistent terminology
4. Don't over-annotate obvious code

### Visualizations

1. Use visualizations to complement code, not replace it
2. Keep visualizations simple and focused
3. Use appropriate visualization types for your data
4. Consider performance with large datasets

## Advanced Topics

### Custom Visualizations

You can create custom visualizations by providing JSON data:

```python
presentation.add_visualization('custom', {
    'type': 'custom',
    'data': {
        # Your custom visualization data
    }
})
```

### Stack Trace Visualization

Track function execution with stack traces:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

presentation.add_stack_trace('factorial', {'factorial': factorial})
```

### Multiple Slides

Create multi-slide presentations:

```python
# First slide
presentation.new_slide(
    code="# Implementation",
    title="Algorithm Overview"
)

# Second slide
presentation.new_slide(
    code="# Example usage",
    title="Using the Algorithm"
)
```

### Error Handling

Handle execution errors gracefully:

```python
try:
    presentation.execute_current_slide()
except Exception as e:
    presentation.add_visualization('error', {
        'type': 'error',
        'message': str(e)
    })
```

## Troubleshooting

### Common Issues

1. **Code Not Executing**
   - Check that all required variables are defined
   - Verify syntax is correct
   - Ensure all dependencies are installed

2. **Visualization Not Showing**
   - Verify JSON data is properly formatted
   - Check that visualization type is supported
   - Ensure data size is reasonable

3. **Browser Issues**
   - Try a different port number
   - Check if another service is using the port
   - Verify browser JavaScript is enabled

### Getting Help

- Check the [API Reference](../api/index.md)
- Look through [Examples](../examples/index.md)
- Submit issues on GitHub
- Join the community discussion 