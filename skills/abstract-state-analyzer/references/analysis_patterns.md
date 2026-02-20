# Analysis Patterns for Common Errors

## Array Bounds Checking

### Pattern: Direct Array Access

**Code Pattern**:
```python
arr[index]
```

**Analysis Steps**:
1. Determine abstract value of `index`
2. Determine length of `arr` (if known)
3. Check: `index ∈ [0, len(arr)-1]`?

**Example 1: Safe Access**
```python
arr = [1, 2, 3, 4, 5]  # len = 5
index = 2              # index: [2, 2]
value = arr[index]     # Check: 2 ∈ [0, 4]? ✓ Safe
```

**Example 2: Potential Error**
```python
def get(arr, index):
    # arr: length unknown
    # index: ⊤
    return arr[index]  # ✗ Potential out-of-bounds
```

**Example 3: Proven Safe with Conditional**
```python
def get(arr, index):
    if 0 <= index < len(arr):
        # index: [0, len(arr)-1]
        return arr[index]  # ✓ Safe
```

### Pattern: Loop-Based Array Access

**Code Pattern**:
```python
for i in range(n):
    arr[i]
```

**Analysis Steps**:
1. Determine loop bounds: `i ∈ [0, n-1]`
2. Check: `n ≤ len(arr)`?

**Example 1: Safe Loop**
```python
arr = [1, 2, 3, 4, 5]
for i in range(len(arr)):
    # i: [0, len(arr)-1]
    print(arr[i])  # ✓ Safe
```

**Example 2: Potential Error**
```python
def process(arr, n):
    for i in range(n):
        # i: [0, n-1]
        # Check: n ≤ len(arr)? Unknown
        arr[i] = 0  # ✗ Potential out-of-bounds if n > len(arr)
```

### Pattern: Off-by-One Error

**Code Pattern**:
```python
for i in range(n+1):
    arr[i]
```

**Analysis**:
```python
arr = [1, 2, 3]  # len = 3
for i in range(4):  # i: [0, 3]
    # When i = 3: 3 ∉ [0, 2]
    arr[i] = 0  # ✗ Out-of-bounds when i = 3
```

## Null Dereference Detection

### Pattern: Unchecked Dereference

**Code Pattern**:
```python
obj.method()
obj.field
```

**Analysis Steps**:
1. Determine null status of `obj`
2. Check: `obj` is `not-null`?

**Example 1: Potential Error**
```python
def process(obj):
    # obj: ⊤ (maybe null)
    obj.method()  # ✗ Potential null dereference
```

**Example 2: Safe with Check**
```python
def process(obj):
    if obj is not None:
        # obj: not-null
        obj.method()  # ✓ Safe
```

### Pattern: Null Return Value

**Code Pattern**:
```python
result = find(...)
result.field
```

**Analysis**:
```python
def find(arr, target):
    for item in arr:
        if item == target:
            return item
    return None  # Returns null if not found

result = find(arr, x)
# result: ⊤ (maybe null)
print(result.value)  # ✗ Potential null dereference
```

**Fix**:
```python
result = find(arr, x)
if result is not None:
    # result: not-null
    print(result.value)  # ✓ Safe
```

### Pattern: Chained Dereferences

**Code Pattern**:
```python
obj.field1.field2.field3
```

**Analysis**: Check each step
```python
# obj: ⊤
obj.field1  # ✗ Potential null dereference
# Assuming obj is not-null:
# obj.field1: ⊤
obj.field1.field2  # ✗ Potential null dereference
# And so on...
```

## Division by Zero Detection

### Pattern: Direct Division

**Code Pattern**:
```python
x / y
```

**Analysis Steps**:
1. Determine abstract value of `y`
2. Check: `0 ∉ y`?

**Example 1: Safe Division**
```python
x = 10
y = 5  # y: [5, 5]
z = x / y  # Check: 0 ∉ [5, 5]? ✓ Safe
```

**Example 2: Potential Error**
```python
def divide(x, y):
    # y: ⊤
    return x / y  # ✗ Potential division by zero
```

**Example 3: Range Includes Zero**
```python
y = input()  # y: [-∞, ∞]
if -10 < y < 10:
    # y: [-9, 9]
    z = 100 / y  # ✗ Potential division by zero (y could be 0)
```

### Pattern: Safe with Check

**Code Pattern**:
```python
if y != 0:
    x / y
```

**Analysis**:
```python
def safe_divide(x, y):
    if y != 0:
        # y: [-∞, -1] ∪ [1, ∞] (excludes 0)
        return x / y  # ✓ Safe
    return None
```

### Pattern: Modulo Operation

**Code Pattern**:
```python
x % y
```

**Analysis**: Same as division
```python
index = hash(key) % size
# Check: size != 0?
```

## Integer Overflow Detection

### Pattern: Multiplication Overflow

**Code Pattern**:
```python
result = a * b
```

**Analysis Steps**:
1. Determine ranges of `a` and `b`
2. Compute `[min, max]` of `a * b`
3. Check: result fits in type bounds?

**Example 1: Potential Overflow**
```c
int32_t a = 100000;  // a: [100000, 100000]
int32_t b = 100000;  // b: [100000, 100000]
int32_t result = a * b;  // result: [10000000000, 10000000000]
// Check: 10000000000 > INT32_MAX (2147483647)? ✗ Overflow!
```

**Example 2: Safe Multiplication**
```c
int32_t a = 100;  // a: [100, 100]
int32_t b = 200;  // b: [200, 200]
int32_t result = a * b;  // result: [20000, 20000]
// Check: 20000 ≤ INT32_MAX? ✓ Safe
```

### Pattern: Addition Overflow

**Code Pattern**:
```python
result = a + b
```

**Example**:
```c
uint32_t a = 4000000000;  // a: [4000000000, 4000000000]
uint32_t b = 1000000000;  // b: [1000000000, 1000000000]
uint32_t result = a + b;  // result: [5000000000, 5000000000]
// Check: 5000000000 > UINT32_MAX (4294967295)? ✗ Overflow!
```

### Pattern: Size Calculation

**Code Pattern**:
```c
size_t total = count * element_size;
buffer = malloc(total);
```

**Analysis**:
```c
size_t count = user_input;  // count: [0, ∞]
size_t element_size = 1024;  // element_size: [1024, 1024]
size_t total = count * element_size;
// If count > SIZE_MAX / 1024: ✗ Overflow
// Result: small value due to wraparound
// malloc(small_value): allocates small buffer
// Later: buffer overflow when writing count * 1024 bytes
```

## Type Inconsistency Detection

### Pattern: Dynamic Type Error

**Code Pattern** (Python):
```python
result = x + y
```

**Analysis**:
```python
def add(x, y):
    # x: ⊤, y: ⊤
    return x + y  # ✗ Potential type error

# If x: {int}, y: {str} → TypeError
```

**Safe Version**:
```python
def add(x, y):
    if isinstance(x, int) and isinstance(y, int):
        # x: {int}, y: {int}
        return x + y  # ✓ Safe
```

### Pattern: Attribute Access

**Code Pattern**:
```python
obj.method()
```

**Analysis**:
```python
def process(obj):
    # obj: {ClassA, ClassB}
    obj.method()
    # Check: both ClassA and ClassB have method()?
    # If only ClassA has method(): ✗ Potential AttributeError
```

### Pattern: Function Argument Type

**Code Pattern**:
```python
def process(x: int):
    return x + 1

result = process(arg)
```

**Analysis**:
```python
arg = "hello"  # arg: {str}
result = process(arg)
# Check: {str} ⊆ {int}? ✗ Type error
```

## Loop Invariant Analysis

### Pattern: Loop Counter Bounds

**Code Pattern**:
```python
i = 0
while i < n:
    # Loop body
    i += 1
```

**Analysis**:
```
Iteration 0: i = [0, 0]
Iteration 1: i = [0, 1]
Iteration 2: i = [0, 2]
...
Fixpoint: i = [0, n-1] (inside loop)
After loop: i = [n, n]
```

### Pattern: Accumulator

**Code Pattern**:
```python
sum = 0
for i in range(n):
    sum += arr[i]
```

**Analysis**:
```
Initial: sum = [0, 0]
After iteration 1: sum = [arr[0], arr[0]]
After iteration 2: sum = [arr[0]+arr[1], arr[0]+arr[1]]
...
Widening: sum = [-∞, ∞] (if array values unknown)
```

### Pattern: Nested Loops

**Code Pattern**:
```python
for i in range(n):
    for j in range(m):
        matrix[i][j] = 0
```

**Analysis**:
```
Outer loop: i ∈ [0, n-1]
Inner loop: j ∈ [0, m-1]
Access: matrix[i][j]
Check: i < rows and j < cols?
```

## Conditional Analysis

### Pattern: Range Refinement

**Code Pattern**:
```python
if x > 10:
    # Branch 1
else:
    # Branch 2
```

**Analysis**:
```
Before: x: [-∞, ∞]
Branch 1: x: [11, ∞]
Branch 2: x: [-∞, 10]
```

### Pattern: Null Check

**Code Pattern**:
```python
if obj is None:
    return
# Continue
```

**Analysis**:
```
Before: obj: ⊤
True branch: obj: null
False branch (after if): obj: not-null
```

### Pattern: Bounds Check

**Code Pattern**:
```python
if 0 <= index < len(arr):
    arr[index]
```

**Analysis**:
```
Before: index: ⊤
True branch: index: [0, len(arr)-1]
Access arr[index]: ✓ Safe
```

## Function Call Analysis

### Pattern: Unknown Function

**Code Pattern**:
```python
result = unknown_function(x)
```

**Analysis**:
```
x: [0, 10]
result: ⊤ (unknown return value)
```

### Pattern: Function Summary

**Code Pattern**:
```python
def increment(x):
    return x + 1

y = increment(5)
```

**Analysis with Summary**:
```
Summary: increment(x) returns x + 1
x: [5, 5]
y: [6, 6]
```

### Pattern: Side Effects

**Code Pattern**:
```python
def modify(arr):
    arr[0] = 0

modify(my_arr)
```

**Analysis**:
```
Before: my_arr[0]: [1, 10]
After: my_arr[0]: [0, 0]
```
