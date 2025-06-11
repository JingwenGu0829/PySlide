"""
Welcome to PySlide - Interactive Python Code Presentations
This example demonstrates the core features of PySlide.
"""

from pyslide import PySlide

def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n-1)

def main():
    # Create a new presentation
    presentation = PySlide()

    # Slide 1: Welcome
    presentation.new_slide(
        code="""# Welcome to PySlide!
# A modern way to create interactive code presentations

def greet():
    return "Welcome to PySlide!"

print(greet())""",
        title="Welcome to PySlide",
        description="Create beautiful, interactive code presentations with ease"
    ).annotate(1, "PySlide helps you create engaging code presentations")
    
    # Add project logo/screenshot
    presentation.add_image(
        path="examples/welcome/example.png",
        alt="PySlide Interface Screenshot",
        caption="PySlide's modern and clean interface",
        width=800
    )
    
    # Execute the code
    presentation.execute_current_slide({'greet': None})

    # Slide 2: Key Features
    presentation.new_slide(
        code="""# Key Features of PySlide:

# 1. Code Execution
result = sum(range(5))
print(f"Sum of 0-4: {result}")

# 2. Line Annotations
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

# 3. Stack Trace Visualization
print(f"Factorial of 5: {factorial(5)}")""",
        title="Key Features",
        description="Discover what makes PySlide special"
    ).annotate(1, "PySlide comes with powerful features out of the box")
    
    # Add annotations for each feature
    presentation.annotate(3, "Real-time code execution with output capture")
    presentation.annotate(7, "Add explanatory annotations to any line")
    presentation.annotate(12, "Visualize function execution with stack traces")
    
    # Add stack trace visualization
    globals_dict = {'factorial': factorial}
    presentation.execute_current_slide(globals_dict)
    presentation.add_stack_trace('factorial', globals_dict)

    # Slide 3: Code and Images
    presentation.new_slide(
        code="""# Combining Code and Visuals

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Example usage
arr = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
result = binary_search(arr, target)
print(f"Found {target} at index {result}")""",
        title="Code and Visuals",
        description="Enhance your presentations with images and visualizations"
    )
    
    # Add annotations
    presentation.annotate(3, "Binary search operates on sorted arrays")
    presentation.annotate(6, "Find the middle element")
    presentation.annotate(8, "Found the target!")
    presentation.annotate(10, "Search in the right half")
    presentation.annotate(12, "Search in the left half")
    
    # Execute the code
    presentation.execute_current_slide()
    
    # Add visualization
    presentation.add_visualization('binary_search', {
        'array': [1, 3, 5, 7, 9, 11, 13, 15],
        'target': 7,
        'steps': [
            {'left': 0, 'right': 7, 'mid': 3, 'comparison': '7 == 7'},
            {'result': 'Found at index 3'}
        ]
    })

    # Display the presentation
    presentation.display(port=8080)

if __name__ == "__main__":
    main() 