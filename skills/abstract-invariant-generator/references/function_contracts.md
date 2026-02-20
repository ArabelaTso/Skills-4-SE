# Function Contracts: Preconditions and Postconditions

## Contract Fundamentals

A function contract consists of:
- **Precondition** (`requires`): What must be true when function is called
- **Postcondition** (`ensures`): What function guarantees on return
- **Frame condition** (`modifies`): What the function may change

## Precondition Generation

### Strategy 1: Identify Unsafe Operations

Find operations that can fail and add preconditions to prevent failure.

**Array Access**:
```python
def get_element(arr, index):
    return arr[index]
```

**Unsafe**: `index` could be out of bounds

**Generated Precondition**:
```
requires 0 ≤ index < len(arr)
requires arr is not None
```

**Division**:
```python
def divide(x, y):
    return x / y
```

**Unsafe**: `y` could be zero

**Generated Precondition**:
```
requires y ≠ 0
```

**Pointer/Reference Dereference**:
```python
def get_next(node):
    return node.next
```

**Unsafe**: `node` could be null

**Generated Precondition**:
```
requires node is not None
```

### Strategy 2: Analyze Function Body

Trace through function to find assumptions.

**Example**:
```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

**Analysis**:
- Accesses `arr[mid]` → needs `arr` not null, valid indices
- Comparison `arr[mid] < target` → assumes array is sorted
- `high = len(arr) - 1` → needs `len(arr) > 0` for meaningful search

**Generated Preconditions**:
```
requires arr is not None
requires sorted(arr)
```

### Strategy 3: Backward from Postcondition

What must be true initially for postcondition to hold?

**Example**:
```python
def find_max(arr):
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
```

**Desired Postcondition**: `result = max(arr)`

**Backward Reasoning**:
- To return max, need to examine all elements
- `arr[0]` accessed → need `len(arr) > 0`
- Loop from 1 to len(arr) → need `len(arr) ≥ 1`

**Generated Precondition**:
```
requires len(arr) > 0
requires arr is not None
```

## Postcondition Generation

### Strategy 1: Characterize Return Value

Describe properties of the returned value.

**Maximum Function**:
```python
def find_max(arr):
    # ... implementation ...
    return max_val
```

**Generated Postconditions**:
```
ensures result ∈ arr
ensures ∀x ∈ arr. x ≤ result
```

**Search Function**:
```python
def find_index(arr, target):
    # ... implementation ...
    return index
```

**Generated Postconditions**:
```
ensures result = -1 ∨ (0 ≤ result < len(arr) ∧ arr[result] = target)
ensures result ≠ -1 ⟹ arr[result] = target
ensures result = -1 ⟹ target ∉ arr
```

### Strategy 2: Relate Output to Input

Express how output relates to input.

**Sorting Function**:
```python
def sort(arr):
    # ... implementation ...
    return sorted_arr
```

**Generated Postconditions**:
```
ensures len(result) = len(arr)
ensures sorted(result)
ensures multiset(result) = multiset(arr)
```

**Filtering Function**:
```python
def filter_positive(arr):
    return [x for x in arr if x > 0]
```

**Generated Postconditions**:
```
ensures ∀x ∈ result. x > 0
ensures ∀x ∈ result. x ∈ arr
ensures ∀x ∈ arr. x > 0 ⟹ x ∈ result
```

### Strategy 3: Specify Side Effects

For functions that modify state, specify what changes.

**Array Modification**:
```python
def fill_zeros(arr):
    for i in range(len(arr)):
        arr[i] = 0
```

**Generated Postconditions**:
```
modifies arr
ensures ∀i. 0 ≤ i < len(arr) ⟹ arr[i] = 0
ensures len(arr) = old(len(arr))
```

**Linked List Insertion**:
```python
def insert(list, value):
    # ... insert value into list ...
```

**Generated Postconditions**:
```
modifies list
ensures value ∈ list
ensures ∀x. x ∈ old(list) ⟹ x ∈ list
ensures size(list) = size(old(list)) + 1
```

## Common Contract Patterns

### 1. Array/Collection Operations

**Access**:
```
requires 0 ≤ index < len(arr)
ensures result = arr[index]
```

**Update**:
```
requires 0 ≤ index < len(arr)
modifies arr
ensures arr[index] = value
ensures ∀i. i ≠ index ⟹ arr[i] = old(arr[i])
```

**Append**:
```
modifies arr
ensures len(arr) = old(len(arr)) + 1
ensures arr[len(arr)-1] = value
ensures ∀i. 0 ≤ i < old(len(arr)) ⟹ arr[i] = old(arr[i])
```

### 2. Search Operations

**Linear Search**:
```
ensures result = -1 ∨ (0 ≤ result < len(arr) ∧ arr[result] = target)
ensures result ≠ -1 ⟹ arr[result] = target
ensures result = -1 ⟹ target ∉ arr
```

**Binary Search** (sorted array):
```
requires sorted(arr)
ensures result = -1 ∨ (0 ≤ result < len(arr) ∧ arr[result] = target)
ensures result ≠ -1 ⟹ arr[result] = target
ensures result = -1 ⟹ target ∉ arr
```

### 3. Sorting Operations

**In-place Sort**:
```
modifies arr
ensures sorted(arr)
ensures multiset(arr) = multiset(old(arr))
ensures len(arr) = old(len(arr))
```

**Return New Sorted Array**:
```
ensures sorted(result)
ensures multiset(result) = multiset(arr)
ensures len(result) = len(arr)
```

### 4. Aggregation Operations

**Sum**:
```
ensures result = Σ(arr)
```

**Count**:
```
ensures result = |{x ∈ arr | predicate(x)}|
```

**All/Any**:
```
ensures result ⟺ (∀x ∈ arr. predicate(x))
ensures result ⟺ (∃x ∈ arr. predicate(x))
```

### 5. Transformation Operations

**Map**:
```
ensures len(result) = len(arr)
ensures ∀i. 0 ≤ i < len(arr) ⟹ result[i] = f(arr[i])
```

**Filter**:
```
ensures ∀x ∈ result. predicate(x) ∧ x ∈ arr
ensures ∀x ∈ arr. predicate(x) ⟹ x ∈ result
```

**Reduce**:
```
ensures result = fold(op, initial, arr)
```

### 6. Data Structure Operations

**Stack Push**:
```
modifies stack
ensures top(stack) = value
ensures size(stack) = old(size(stack)) + 1
```

**Stack Pop**:
```
requires size(stack) > 0
modifies stack
ensures result = old(top(stack))
ensures size(stack) = old(size(stack)) - 1
```

**Queue Enqueue**:
```
modifies queue
ensures value ∈ queue
ensures size(queue) = old(size(queue)) + 1
ensures ∀x ∈ old(queue). x ∈ queue
```

**Queue Dequeue**:
```
requires size(queue) > 0
modifies queue
ensures result = old(front(queue))
ensures size(queue) = old(size(queue)) - 1
```

## Complete Examples

### Example 1: Insertion Sort

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

**Generated Contract**:
```
requires arr is not None
modifies arr
ensures sorted(arr)
ensures multiset(arr) = multiset(old(arr))
ensures len(arr) = old(len(arr))
```

### Example 2: Binary Search

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

**Generated Contract**:
```
requires arr is not None
requires sorted(arr)
ensures result = -1 ∨ (0 ≤ result < len(arr) ∧ arr[result] = target)
ensures result ≠ -1 ⟹ arr[result] = target
ensures result = -1 ⟹ target ∉ arr
```

### Example 3: Partition (Quicksort)

```python
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Generated Contract**:
```
requires 0 ≤ low ≤ high < len(arr)
modifies arr
ensures low ≤ result ≤ high
ensures arr[result] = old(arr[high])
ensures ∀k. low ≤ k < result ⟹ arr[k] ≤ arr[result]
ensures ∀k. result < k ≤ high ⟹ arr[k] ≥ arr[result]
ensures multiset(arr[low..high]) = multiset(old(arr[low..high]))
```

### Example 4: Merge Sorted Arrays

```python
def merge(arr1, arr2):
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

**Generated Contract**:
```
requires sorted(arr1)
requires sorted(arr2)
ensures sorted(result)
ensures len(result) = len(arr1) + len(arr2)
ensures multiset(result) = multiset(arr1) ∪ multiset(arr2)
```

## Strengthening Contracts

### Weak Contract

```
requires arr is not None
ensures result ≥ 0
```

### Strengthened Contract

```
requires arr is not None
requires len(arr) > 0
ensures result ∈ arr
ensures ∀x ∈ arr. x ≤ result
```

## Frame Conditions

Specify what the function may modify:

**Read-only**:
```
ensures arr = old(arr)  // No modifications
```

**Partial modification**:
```
modifies arr[index]
ensures ∀i. i ≠ index ⟹ arr[i] = old(arr[i])
```

**Full modification**:
```
modifies arr
// No guarantees about preservation
```

## Handling Exceptions

**Precondition prevents exception**:
```
requires y ≠ 0  // Prevents division by zero
ensures result = x / y
```

**Postcondition describes exception**:
```
ensures (y = 0 ⟹ throws DivisionByZeroException) ∧
        (y ≠ 0 ⟹ result = x / y)
```
