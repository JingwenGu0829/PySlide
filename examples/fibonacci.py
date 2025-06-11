"""
Example PySlide presentation demonstrating Fibonacci sequence.
"""

from pyslide import PySlide

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    # Create a new presentation
    presentation = PySlide()
    
    # Slide 1: Introduction
    presentation.new_slide(
        """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
        title="Fibonacci Sequence",
        description="A recursive implementation of the Fibonacci sequence calculator."
    ).annotate(1, "Function definition: Takes a single parameter n")
    
    # Add stack trace visualization
    globals_dict = {'fibonacci': fibonacci}
    presentation.execute_current_slide(globals_dict)
    presentation.add_stack_trace('fibonacci', globals_dict)
    
    # Slide 2: Base Cases
    presentation.new_slide(
        """# Base cases
n = 0  # Returns 0
print(f"fibonacci(0) = {fibonacci(0)}")

n = 1  # Returns 1
print(f"fibonacci(1) = {fibonacci(1)}")
""",
        title="Base Cases",
        description="Understanding the base cases of the Fibonacci sequence."
    ).annotate(2, "First base case: n = 0")
    
    # Execute the code and capture output
    presentation.execute_current_slide(globals_dict)
    
    # Slide 3: Recursive Case
    presentation.new_slide(
        """# Recursive case
n = 5
result = fibonacci(n)
print(f"fibonacci({n}) = {result}")

# Let's break down how it works:
# fibonacci(5) = fibonacci(4) + fibonacci(3)
#              = [fibonacci(3) + fibonacci(2)] + [fibonacci(2) + fibonacci(1)]
#              = [...] = 5
""",
        title="Recursive Case",
        description="Exploring how the recursive calculation works."
    ).annotate(3, "Calculate the 5th Fibonacci number")
    
    # Execute the code and capture output
    presentation.execute_current_slide(globals_dict)
    
    # Add visualization
    presentation.add_visualization("sequence", {
        "first_6_numbers": [fibonacci(i) for i in range(6)],
        "formula": "F(n) = F(n-1) + F(n-2)"
    })
    
    # Display the presentation
    presentation.display()

if __name__ == "__main__":
    main() 