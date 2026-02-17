# Python Idioms and Best Practices

This document provides Python-specific idioms and best practices for generating clean, idiomatic code.

## Code Style

### PEP 8 Conventions

- Use 4 spaces for indentation
- Maximum line length: 79 characters (88 for Black formatter)
- Use snake_case for functions and variables
- Use PascalCase for class names
- Use UPPER_CASE for constants

### Type Hints

Always include type hints for function parameters and return values:

```python
def function_name(param1: int, param2: str) -> bool:
    return True
```

For complex types:
```python
from typing import List, Dict, Optional, Tuple, Set

def process_data(items: List[int]) -> Dict[str, int]:
    pass

def find_item(key: str) -> Optional[int]:
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: int, param2: str) -> bool:
    """Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is negative
    """
    pass
```

## Pythonic Patterns

### List Comprehensions

**Instead of:**
```python
result = []
for item in items:
    if condition(item):
        result.append(transform(item))
```

**Use:**
```python
result = [transform(item) for item in items if condition(item)]
```

### Dictionary Comprehensions

```python
squares = {x: x**2 for x in range(10)}
```

### Generator Expressions

For large datasets, use generators to save memory:
```python
total = sum(x**2 for x in range(1000000))
```

### Enumerate

**Instead of:**
```python
i = 0
for item in items:
    print(i, item)
    i += 1
```

**Use:**
```python
for i, item in enumerate(items):
    print(i, item)
```

### Zip

**Instead of:**
```python
for i in range(len(list1)):
    process(list1[i], list2[i])
```

**Use:**
```python
for item1, item2 in zip(list1, list2):
    process(item1, item2)
```

### Unpacking

```python
# Multiple assignment
a, b = 1, 2

# Swap
a, b = b, a

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
```

### Context Managers

**Instead of:**
```python
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()
```

**Use:**
```python
with open('file.txt') as f:
    data = f.read()
```

### Default Dictionary

**Instead of:**
```python
counts = {}
for item in items:
    if item not in counts:
        counts[item] = 0
    counts[item] += 1
```

**Use:**
```python
from collections import defaultdict
counts = defaultdict(int)
for item in items:
    counts[item] += 1
```

### Counter

For counting occurrences:
```python
from collections import Counter
counts = Counter(items)
most_common = counts.most_common(5)
```

## Data Structure Selection

### When to Use Each

- **list**: Ordered, mutable, allows duplicates, indexed access
- **tuple**: Ordered, immutable, allows duplicates, indexed access
- **set**: Unordered, mutable, no duplicates, fast membership testing
- **dict**: Key-value pairs, fast lookup by key
- **deque**: Double-ended queue, fast append/pop from both ends
- **heapq**: Priority queue, efficient min-heap operations
- **OrderedDict**: Dictionary that remembers insertion order (Python 3.7+ dicts are ordered)

## Common Algorithms

### Sorting

```python
# Sort in place
items.sort()

# Return sorted copy
sorted_items = sorted(items)

# Custom key
sorted_items = sorted(items, key=lambda x: x.attribute)

# Reverse
sorted_items = sorted(items, reverse=True)
```

### Filtering

```python
# Filter with list comprehension
filtered = [x for x in items if condition(x)]

# Filter with filter()
filtered = list(filter(condition, items))
```

### Mapping

```python
# Map with list comprehension
transformed = [transform(x) for x in items]

# Map with map()
transformed = list(map(transform, items))
```

### Reducing

```python
from functools import reduce

# Sum
total = reduce(lambda acc, x: acc + x, items, 0)
# Better: use sum()
total = sum(items)

# Product
product = reduce(lambda acc, x: acc * x, items, 1)
```

## Error Handling

### Specific Exceptions

```python
try:
    value = int(input())
except ValueError:
    print("Invalid integer")
except KeyboardInterrupt:
    print("Interrupted")
```

### EAFP vs LBYL

**EAFP (Easier to Ask for Forgiveness than Permission)** - Pythonic:
```python
try:
    value = my_dict[key]
except KeyError:
    value = default
```

**LBYL (Look Before You Leap)** - Less Pythonic:
```python
if key in my_dict:
    value = my_dict[key]
else:
    value = default
```

Better yet, use dict methods:
```python
value = my_dict.get(key, default)
```

## Performance Tips

### Use Built-in Functions

Built-in functions are implemented in C and are faster:
- `sum()`, `min()`, `max()`, `any()`, `all()`
- `sorted()`, `reversed()`
- `map()`, `filter()`, `zip()`

### Avoid Repeated Lookups

**Instead of:**
```python
for i in range(len(items)):
    process(items[i])
```

**Use:**
```python
for item in items:
    process(item)
```

### Use Local Variables

Local variable access is faster than global:
```python
def process_items(items):
    # Cache global function as local
    process = global_process_function
    for item in items:
        process(item)
```

### String Concatenation

**Instead of:**
```python
result = ""
for s in strings:
    result += s  # Creates new string each time
```

**Use:**
```python
result = "".join(strings)  # Much faster
```

## Testing Patterns

### Basic Test Structure

```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = setup_test_data()
    expected = expected_result()

    # Act
    actual = function_under_test(input_data)

    # Assert
    assert actual == expected
```

### Edge Cases to Test

- Empty input ([], "", None)
- Single element
- Duplicate elements
- Negative numbers
- Zero
- Large numbers
- Boundary conditions

### Example Test Cases

```python
def test_sort_algorithm():
    """Test sorting algorithm with various inputs."""
    # Empty list
    assert sort([]) == []

    # Single element
    assert sort([1]) == [1]

    # Already sorted
    assert sort([1, 2, 3]) == [1, 2, 3]

    # Reverse sorted
    assert sort([3, 2, 1]) == [1, 2, 3]

    # Duplicates
    assert sort([3, 1, 2, 1]) == [1, 1, 2, 3]

    # Negative numbers
    assert sort([-1, -3, -2]) == [-3, -2, -1]
```

## Code Organization

### Module Structure

```python
"""Module docstring describing the module."""

# Standard library imports
import os
import sys

# Third-party imports
import numpy as np

# Local imports
from .utils import helper_function

# Constants
MAX_SIZE = 100

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main execution
if __name__ == "__main__":
    main()
```

### Function Length

- Keep functions short and focused (< 50 lines)
- One function should do one thing
- Extract complex logic into helper functions

### Naming Conventions

- Functions: `calculate_total()`, `get_user_name()`
- Variables: `user_count`, `total_price`
- Classes: `UserAccount`, `DataProcessor`
- Constants: `MAX_RETRIES`, `DEFAULT_TIMEOUT`
- Private: `_internal_method()`, `_private_var`

## Common Pitfalls to Avoid

### Mutable Default Arguments

**Wrong:**
```python
def append_to(element, target=[]):
    target.append(element)
    return target
```

**Correct:**
```python
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target
```

### Late Binding Closures

**Wrong:**
```python
functions = [lambda: i for i in range(5)]
# All functions return 4
```

**Correct:**
```python
functions = [lambda i=i: i for i in range(5)]
```

### Comparing with None

**Wrong:**
```python
if value == None:
```

**Correct:**
```python
if value is None:
```

### Using `is` for Value Comparison

**Wrong:**
```python
if x is 5:  # Don't use 'is' for values
```

**Correct:**
```python
if x == 5:  # Use '==' for value comparison
```
