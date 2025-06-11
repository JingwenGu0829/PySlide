# API Reference

## PySlide Class

The main class for creating and managing presentations.

### Constructor

```python
PySlide()
```

Creates a new PySlide instance.

### Methods

#### new_slide

```python
new_slide(code: str, title: Optional[str] = None, description: Optional[str] = None) -> PySlide
```

Creates a new slide with the given code.

**Parameters:**
- `code` (str): The Python code to display in the slide
- `title` (Optional[str]): The slide title
- `description` (Optional[str]): A description of the slide

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

#### annotate

```python
annotate(line_number: int, text: str) -> PySlide
```

Adds an annotation to a specific line in the current slide.

**Parameters:**
- `line_number` (int): The line number to annotate (1-based)
- `text` (str): The annotation text

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

#### add_visualization

```python
add_visualization(name: str, data: Any) -> PySlide
```

Adds a visualization to the current slide.

**Parameters:**
- `name` (str): The name of the visualization
- `data` (Any): The data to visualize (will be JSON-serialized)

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

#### add_image

```python
add_image(path: str, alt: str, caption: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None) -> PySlide
```

Adds an image to the current slide.

**Parameters:**
- `path` (str): Path to the image file (can be local path or URL)
- `alt` (str): Alternative text for accessibility
- `caption` (Optional[str]): Optional caption text to display under the image
- `width` (Optional[int]): Optional width in pixels
- `height` (Optional[int]): Optional height in pixels

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

**Example:**
```python
presentation.add_image(
    path="images/algorithm.png",
    alt="Algorithm flowchart",
    caption="Visual representation of the algorithm",
    width=800
)
```

#### execute_current_slide

```python
execute_current_slide(globals_dict: Optional[Dict[str, Any]] = None) -> PySlide
```

Executes the current slide's code and captures output.

**Parameters:**
- `globals_dict` (Optional[Dict[str, Any]]): Global variables to use during execution

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

#### add_stack_trace

```python
add_stack_trace(function_name: str, globals_dict: Optional[Dict[str, Any]] = None) -> PySlide
```

Adds a stack trace visualization for a function.

**Parameters:**
- `function_name` (str): The name of the function to trace
- `globals_dict` (Optional[Dict[str, Any]]): Global variables containing the function

**Returns:**
- `PySlide`: The PySlide instance (for method chaining)

#### display

```python
display(port: int = 8000)
```

Displays the presentation in a web browser.

**Parameters:**
- `port` (int): The port to serve the presentation on (default: 8000)

## Slide Class

Represents a single slide in the presentation.

### Attributes

- `code` (str): The Python code in the slide
- `annotations` (Dict[int, str]): Line number to annotation text mapping
- `title` (Optional[str]): The slide title
- `description` (Optional[str]): The slide description
- `visualizations` (Dict[str, Any]): Name to visualization data mapping
- `execution_output` (Optional[str]): Output from code execution
- `stack_trace` (Optional[Dict[str, Any]]): Stack trace visualization data
- `images` (List[Image]): List of images in the slide

## Image Class

Represents an image in a slide.

### Attributes

- `path` (str): Path to the image file (can be local path or URL)
- `alt` (str): Alternative text for accessibility
- `caption` (Optional[str]): Optional caption text to display under the image
- `width` (Optional[int]): Optional width in pixels
- `height` (Optional[int]): Optional height in pixels 