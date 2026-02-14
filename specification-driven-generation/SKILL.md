---
name: specification-driven-generation
description: Generate implementation code and tests from written specifications. Use when the user provides specifications (natural language descriptions, formal specs, requirements documents, API specs) and asks Claude to implement the described functionality. Supports data structures, algorithms, classes, functions, and includes automatic test generation to validate implementation against specification.
---

# Specification-Driven Generation

Generate implementation code and validation tests from written specifications through a systematic specification-to-code workflow.

## Workflow

### 1. Analyze Specification

Read and extract requirements from the specification:

- Identify functional requirements (what the code must do)
- Extract input/output contracts (parameters, return types, constraints)
- Note edge cases, error conditions, and validation rules
- Understand performance requirements or complexity constraints
- Identify data structures and algorithms needed

### 2. Design Implementation

Plan the code structure before writing:

- Choose appropriate data structures
- Select efficient algorithms
- Plan class/function organization
- Identify helper functions needed
- Consider error handling approach

### 3. Generate Implementation

Write clean, well-documented code that satisfies the specification:

**Code Structure:**
- Use clear, descriptive names that reflect the specification
- Add docstrings/comments explaining the specification being implemented
- Include type hints/annotations where applicable
- Implement all required functionality
- Handle edge cases and errors per specification

**Common Patterns:**
- **Data structures**: Classes with proper encapsulation, initialization, and methods
- **Algorithms**: Step-by-step implementation with complexity documentation
- **Validators**: Input validation matching specification constraints
- **Utilities**: Helper functions for complex operations

### 4. Generate Tests

Create comprehensive tests that validate the implementation against the specification:

**Test Coverage:**
- Normal cases from specification examples
- Edge cases mentioned in specification
- Error cases and validation rules
- Boundary conditions
- Performance requirements (if specified)

**Test Structure:**
```python
# Example: Testing a sorted list data structure
def test_basic_functionality():
    # From spec: "Insert elements in sorted order"
    sl = SortedList()
    sl.insert(5)
    sl.insert(2)
    sl.insert(8)
    assert sl.to_list() == [2, 5, 8]

def test_edge_case_duplicates():
    # From spec: "Allow duplicate elements"
    sl = SortedList()
    sl.insert(3)
    sl.insert(3)
    assert sl.to_list() == [3, 3]

def test_error_handling():
    # From spec: "Raise TypeError for non-comparable items"
    sl = SortedList()
    with pytest.raises(TypeError):
        sl.insert("string")
        sl.insert(5)
```

### 5. Verify Implementation

Run tests to ensure implementation matches specification:

**Python:**
```bash
pytest test_<module>.py -v
```

**Java:**
```bash
mvn test
```

If tests fail, debug and fix implementation to match specification.

## Specification Analysis

### Natural Language Specifications

Extract key information from prose descriptions:

**Example specification:**
> "Implement a priority queue that supports insertion in O(log n) time and removal of the minimum element in O(log n) time. The queue should handle duplicate priorities and raise an error when attempting to remove from an empty queue."

**Extracted requirements:**
- Data structure: Priority queue
- Operations: insert, remove_min
- Complexity: O(log n) for both operations
- Edge cases: Duplicates allowed, error on empty removal
- Implementation hint: Heap-based structure

### Formal Specifications

Parse structured requirements:

**Example (mathematical notation):**
```
Function: binary_search(arr: sorted array, target: int) → int
Precondition: arr is sorted in ascending order
Postcondition: returns index i where arr[i] = target, or -1 if not found
Complexity: O(log n)
```

**Extracted requirements:**
- Input: Sorted array and target value
- Output: Index or -1
- Algorithm: Binary search
- Validation: Assumes sorted input

### API Specifications

For OpenAPI/Swagger specs, extract:
- Endpoints and HTTP methods
- Request/response schemas
- Validation rules
- Error codes
- Authentication requirements

## Best Practices

### Specification Clarity
- Ask clarifying questions if specification is ambiguous
- Verify assumptions about edge cases
- Confirm expected behavior for unspecified scenarios

### Implementation Quality
- Write self-documenting code with clear variable names
- Add comments linking code to specific specification requirements
- Use appropriate design patterns
- Follow language conventions and style guides

### Test Quality
- Map each test to a specific requirement in the specification
- Use descriptive test names that reference the specification
- Include comments like `# From spec: "requirement text"`
- Test boundary conditions and edge cases thoroughly

### Validation
- Ensure ALL specification requirements have corresponding tests
- Check that implementation handles ALL specified error cases
- Verify performance requirements if specified
- Confirm output format matches specification exactly

## Common Patterns

### Data Structure Implementation

**Specification → Implementation:**
1. Define the data structure class
2. Implement initialization
3. Add required operations
4. Include helper methods for internal logic
5. Add validation and error handling

### Algorithm Implementation

**Specification → Implementation:**
1. Understand input/output requirements
2. Choose efficient algorithm approach
3. Implement step-by-step with clear logic
4. Add complexity analysis in comments
5. Optimize if performance constraints specified

### Class Design

**Specification → Implementation:**
1. Identify attributes from specification
2. Design initialization and validation
3. Implement public methods per specification
4. Add private helper methods as needed
5. Include properties/getters as appropriate

## Example Session

**User provides specification:**
> "Implement a Stack data structure with push, pop, and peek operations. The stack should have a maximum capacity and raise an exception when pushing to a full stack or popping from an empty stack. Include a method to check if the stack is empty."

**Step 1: Analyze**
- Operations: push, pop, peek, is_empty
- Constraints: Maximum capacity
- Errors: StackOverflowError (full), StackUnderflowError (empty)
- Data structure: Array/list-based stack

**Step 2: Design**
- Use list as internal storage
- Track current size and max capacity
- Custom exception classes

**Step 3: Generate Implementation**
```python
class StackOverflowError(Exception):
    pass

class StackUnderflowError(Exception):
    pass

class Stack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def push(self, item):
        if len(self.items) >= self.capacity:
            raise StackOverflowError("Stack is full")
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise StackUnderflowError("Stack is empty")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise StackUnderflowError("Stack is empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0
```

**Step 4: Generate Tests**
```python
import pytest

def test_push_and_peek():
    # From spec: "push and peek operations"
    stack = Stack(capacity=3)
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2

def test_pop():
    # From spec: "pop operation"
    stack = Stack(capacity=3)
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1

def test_is_empty():
    # From spec: "check if stack is empty"
    stack = Stack(capacity=3)
    assert stack.is_empty() == True
    stack.push(1)
    assert stack.is_empty() == False

def test_overflow():
    # From spec: "raise exception when pushing to full stack"
    stack = Stack(capacity=2)
    stack.push(1)
    stack.push(2)
    with pytest.raises(StackOverflowError):
        stack.push(3)

def test_underflow_pop():
    # From spec: "raise exception when popping from empty stack"
    stack = Stack(capacity=2)
    with pytest.raises(StackUnderflowError):
        stack.pop()

def test_underflow_peek():
    # From spec: "raise exception when peeking empty stack"
    stack = Stack(capacity=2)
    with pytest.raises(StackUnderflowError):
        stack.peek()
```

**Step 5: Verify**
```bash
pytest test_stack.py -v
```

All tests pass → Implementation satisfies specification.

## Tips

### Handling Ambiguity
- If specification is unclear, identify multiple interpretations
- Ask user which interpretation is correct
- Document assumptions in code comments

### Performance Specifications
- Note Big-O requirements in docstrings
- Choose appropriate algorithms/data structures
- Add complexity analysis comments

### Error Handling
- Create custom exceptions for domain-specific errors
- Match exception types to specification requirements
- Include descriptive error messages

### Incremental Implementation
- Implement and test one requirement at a time
- Start with core functionality, then edge cases
- Verify each piece before moving to the next
