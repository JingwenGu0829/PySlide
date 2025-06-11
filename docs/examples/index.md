# Examples

## Basic Example: Fibonacci Sequence

```python
from pyslide import PySlide

# Define the Fibonacci function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Create presentation
presentation = PySlide()

# Add first slide: function definition
presentation.new_slide(
    code="""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    title="Fibonacci Sequence",
    description="A recursive implementation"
).annotate(1, "Function definition")
.annotate(2, "Base case: return n for n <= 1")
.annotate(4, "Recursive case: sum of previous two numbers")

# Add stack trace visualization
presentation.add_stack_trace('fibonacci', {'fibonacci': fibonacci})

# Add second slide: usage example
presentation.new_slide(
    code="""result = fibonacci(5)
print(f"Fibonacci(5) = {result}")""",
    title="Using the Fibonacci Function",
    description="Computing the 5th Fibonacci number"
)

# Execute code and capture output
presentation.execute_current_slide({'fibonacci': fibonacci})

# Display the presentation
presentation.display()
```

## Advanced Example: Binary Search Tree

```python
from pyslide import PySlide

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

# Create presentation
presentation = PySlide()

# Add first slide: Node class
presentation.new_slide(
    code="""class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None""",
    title="Binary Search Tree Node",
    description="Node class definition"
).annotate(1, "Node class represents a single node in the tree")
.annotate(3, "Store the node's value")
.annotate(4, "Left child reference (smaller values)")
.annotate(5, "Right child reference (larger values)")

# Add second slide: insert function
presentation.new_slide(
    code="""def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root""",
    title="BST Insertion",
    description="Recursive insertion into binary search tree"
).annotate(2, "Base case: create new node if empty")
.annotate(4, "Recursively insert in left subtree if value is smaller")
.annotate(6, "Recursively insert in right subtree if value is larger")

# Add visualization
tree = None
for value in [5, 3, 7, 2, 4, 6, 8]:
    tree = insert(tree, value) if tree is None else insert(tree, value)

presentation.add_visualization('tree', {
    'type': 'tree',
    'nodes': [
        {'id': 1, 'value': 5},
        {'id': 2, 'value': 3},
        {'id': 3, 'value': 7},
        {'id': 4, 'value': 2},
        {'id': 5, 'value': 4},
        {'id': 6, 'value': 6},
        {'id': 7, 'value': 8}
    ],
    'edges': [
        {'from': 1, 'to': 2},
        {'from': 1, 'to': 3},
        {'from': 2, 'to': 4},
        {'from': 2, 'to': 5},
        {'from': 3, 'to': 6},
        {'from': 3, 'to': 7}
    ]
})

# Display the presentation
presentation.display()
```

## More Examples

Check out these additional examples:

1. [Sorting Algorithms](sorting.md)
2. [Graph Algorithms](graphs.md)
3. [Dynamic Programming](dynamic_programming.md)
4. [Object-Oriented Design](oop.md) 