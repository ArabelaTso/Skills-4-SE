# Pseudocode to Python Mapping Patterns

This document provides mappings from common pseudocode patterns to idiomatic Python code.

## Control Flow Structures

### Conditional Statements

**Pseudocode:**
```
IF condition THEN
    statements
ELSE IF condition2 THEN
    statements
ELSE
    statements
END IF
```

**Python:**
```python
if condition:
    statements
elif condition2:
    statements
else:
    statements
```

### Loops

**FOR loop (range-based):**
```
FOR i FROM 1 TO n DO
    statements
END FOR
```
→
```python
for i in range(1, n + 1):
    statements
```

**FOR loop (collection):**
```
FOR EACH item IN collection DO
    statements
END FOR
```
→
```python
for item in collection:
    statements
```

**WHILE loop:**
```
WHILE condition DO
    statements
END WHILE
```
→
```python
while condition:
    statements
```

**REPEAT-UNTIL loop:**
```
REPEAT
    statements
UNTIL condition
```
→
```python
while True:
    statements
    if condition:
        break
```

## Data Structures

### Arrays/Lists

**Declaration:**
```
DECLARE array[n]
```
→
```python
array = [None] * n  # Fixed size
# or
array = []  # Dynamic
```

**Access:**
```
array[i]
```
→
```python
array[i]  # 0-indexed in Python
```

**Common operations:**
```
APPEND item TO array
INSERT item AT index
REMOVE item FROM array
LENGTH OF array
```
→
```python
array.append(item)
array.insert(index, item)
array.remove(item)
len(array)
```

### Dictionaries/Hash Maps

**Pseudocode:**
```
DECLARE map AS DICTIONARY
map[key] = value
IF key IN map THEN
    value = map[key]
```

**Python:**
```python
map_dict = {}
map_dict[key] = value
if key in map_dict:
    value = map_dict[key]
# or use get() for safe access
value = map_dict.get(key, default_value)
```

### Sets

**Pseudocode:**
```
DECLARE set AS SET
ADD item TO set
REMOVE item FROM set
IF item IN set THEN
```

**Python:**
```python
my_set = set()
my_set.add(item)
my_set.remove(item)  # or discard() to avoid KeyError
if item in my_set:
```

### Stacks

**Pseudocode:**
```
PUSH item ONTO stack
item = POP FROM stack
item = PEEK stack
IF stack IS EMPTY
```

**Python:**
```python
stack = []
stack.append(item)  # push
item = stack.pop()  # pop
item = stack[-1]  # peek
if not stack:  # is empty
```

### Queues

**Pseudocode:**
```
ENQUEUE item TO queue
item = DEQUEUE FROM queue
```

**Python:**
```python
from collections import deque
queue = deque()
queue.append(item)  # enqueue
item = queue.popleft()  # dequeue
```

### Priority Queues

**Pseudocode:**
```
INSERT item WITH priority
item = EXTRACT_MIN
```

**Python:**
```python
import heapq
heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)
```

## Functions/Procedures

**Pseudocode:**
```
FUNCTION name(param1, param2)
    statements
    RETURN value
END FUNCTION
```

**Python:**
```python
def name(param1: type1, param2: type2) -> return_type:
    """Function description.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
    statements
    return value
```

## Common Algorithms

### Swap

**Pseudocode:**
```
temp = a
a = b
b = temp
```

**Python:**
```python
a, b = b, a  # Pythonic swap
```

### Min/Max

**Pseudocode:**
```
min_val = INFINITY
FOR EACH item IN array
    IF item < min_val THEN
        min_val = item
```

**Python:**
```python
min_val = min(array)  # Built-in
# or
min_val = float('inf')
for item in array:
    if item < min_val:
        min_val = item
```

### Sum/Count

**Pseudocode:**
```
sum = 0
FOR EACH item IN array
    sum = sum + item
```

**Python:**
```python
total = sum(array)  # Built-in
# or
total = 0
for item in array:
    total += item
```

### Search

**Linear search:**
```
FOR i FROM 0 TO LENGTH(array) - 1
    IF array[i] = target THEN
        RETURN i
RETURN -1
```
→
```python
try:
    return array.index(target)
except ValueError:
    return -1
# or
for i, item in enumerate(array):
    if item == target:
        return i
return -1
```

**Binary search:**
```
left = 0
right = LENGTH(array) - 1
WHILE left <= right
    mid = (left + right) / 2
    IF array[mid] = target THEN
        RETURN mid
    ELSE IF array[mid] < target THEN
        left = mid + 1
    ELSE
        right = mid - 1
RETURN -1
```
→
```python
import bisect
# For sorted array
index = bisect.bisect_left(array, target)
if index < len(array) and array[index] == target:
    return index
return -1

# or manual implementation
left, right = 0, len(array) - 1
while left <= right:
    mid = (left + right) // 2
    if array[mid] == target:
        return mid
    elif array[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

## Object-Oriented Patterns

### Class Definition

**Pseudocode:**
```
CLASS ClassName
    PRIVATE attribute1
    PUBLIC attribute2

    CONSTRUCTOR(params)
        initialize attributes

    METHOD methodName(params)
        statements
        RETURN value
END CLASS
```

**Python:**
```python
class ClassName:
    """Class description."""

    def __init__(self, params):
        """Initialize the class.

        Args:
            params: Description
        """
        self._attribute1 = value  # private by convention
        self.attribute2 = value   # public

    def method_name(self, params) -> return_type:
        """Method description.

        Args:
            params: Description

        Returns:
            Description
        """
        statements
        return value
```

### Inheritance

**Pseudocode:**
```
CLASS Child EXTENDS Parent
    OVERRIDE method()
        CALL SUPER.method()
        additional statements
END CLASS
```

**Python:**
```python
class Child(Parent):
    """Child class description."""

    def method(self):
        """Override parent method."""
        super().method()
        # additional statements
```

## Special Patterns

### Infinity

**Pseudocode:**
```
min_val = INFINITY
max_val = -INFINITY
```

**Python:**
```python
min_val = float('inf')
max_val = float('-inf')
```

### Null/None

**Pseudocode:**
```
IF value IS NULL
```

**Python:**
```python
if value is None:
```

### Boolean Operations

**Pseudocode:**
```
IF condition1 AND condition2
IF condition1 OR condition2
IF NOT condition
```

**Python:**
```python
if condition1 and condition2:
if condition1 or condition2:
if not condition:
```

### Division

**Pseudocode:**
```
result = a / b  (integer division)
result = a / b  (float division)
remainder = a MOD b
```

**Python:**
```python
result = a // b  # integer division
result = a / b   # float division
remainder = a % b  # modulo
```

## Error Handling

**Pseudocode:**
```
TRY
    statements
CATCH exception
    handle error
FINALLY
    cleanup
```

**Python:**
```python
try:
    statements
except ExceptionType as e:
    # handle error
finally:
    # cleanup
```

## Input/Output

**Pseudocode:**
```
READ input
PRINT output
```

**Python:**
```python
input_value = input("Prompt: ")
print(output)
```
