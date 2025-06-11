"""
Example demonstrating CodeCast with Fibonacci sequence visualization.
"""

from codecast import CodeCast

def main():
    # Create CodeCast instance
    codecast = CodeCast()
    
    # Example code to visualize
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 5 Fibonacci numbers
results = []
for i in range(5):
    result = fibonacci(i)
    results.append(result)
    print(f"fibonacci({i}) = {result}")

print("Final sequence:", results)
"""
    
    # Create presentation
    presentation = codecast.from_code(code, "fibonacci_example.py")
    
    # Add annotations
    presentation.annotate(2, "Base case: return n for n <= 1")
    presentation.annotate(4, "Recursive case: sum of two previous numbers")
    presentation.annotate(7, "Calculate and store results")
    
    # Display the presentation
    presentation.display()

if __name__ == "__main__":
    main() 