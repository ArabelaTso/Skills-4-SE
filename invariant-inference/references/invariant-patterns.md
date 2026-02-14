# Loop Invariant Patterns

## Common Loop Invariant Categories

### 1. Bounds Invariants

Properties about variable ranges and bounds.

**Array Index Bounds:**
```python
# Loop: for i in range(len(arr))
# Invariant: 0 <= i < len(arr)

# Loop: while i < n
# Invariant: 0 <= i <= n
```

**Counter Bounds:**
```python
# Loop: while count < target
# Invariant: 0 <= count <= target

# Loop: for i in range(start, end)
# Invariant: start <= i < end
```

### 2. Relationship Invariants

Properties about relationships between variables.

**Sum/Accumulation:**
```python
# Loop: sum += arr[i]
# Invariant: sum == sum(arr[0:i+1])

# Loop: total += value
# Invariant: total represents sum of processed items
```

**Product:**
```python
# Loop: product *= arr[i]
# Invariant: product == arr[0] * arr[1] * ... * arr[i]
```

**Max/Min:**
```python
# Loop: if arr[i] > max_val: max_val = arr[i]
# Invariant: max_val == max(arr[0:i+1])

# Loop: if arr[i] < min_val: min_val = arr[i]
# Invariant: min_val == min(arr[0:i+1])
```

### 3. Progress Invariants

Properties showing forward progress toward termination.

**Decreasing:**
```python
# Loop: while n > 0: n -= 1
# Invariant: n decreases each iteration, n >= 0

# Loop: while len(queue) > 0: queue.pop()
# Invariant: len(queue) decreases, len(queue) >= 0
```

**Increasing:**
```python
# Loop: while i < n: i += 1
# Invariant: i increases each iteration, i <= n
```

### 4. Data Structure Invariants

Properties about data structure integrity.

**Sorted Property:**
```python
# Loop: insertion sort
# Invariant: arr[0:i] is sorted

# Loop: bubble sort
# Invariant: largest i elements are in final position
```

**Partition Property:**
```python
# Loop: partition in quicksort
# Invariant: elements left of pivot < pivot, elements right > pivot

# Loop: binary search
# Invariant: if target exists, it's in range [left, right]
```

**Size/Length:**
```python
# Loop: building result list
# Invariant: len(result) == i

# Loop: copying elements
# Invariant: len(output) == number of processed inputs
```

### 5. Conditional Invariants

Properties that depend on conditions.

**Flag-based:**
```python
# Loop: searching for element
# Invariant: if found == True, then arr[found_idx] == target
# Invariant: if found == False, then target not in arr[0:i]
```

**Parity:**
```python
# Loop: counting even numbers
# Invariant: even_count == number of even elements in arr[0:i]

# Loop: alternating states
# Invariant: (i % 2 == 0) implies certain state
```

## Language-Specific Patterns

### Python

**List Comprehension Equivalent:**
```python
# Loop: for x in items: if condition(x): result.append(f(x))
# Invariant: result == [f(x) for x in items[0:i] if condition(x)]
```

**Dictionary Building:**
```python
# Loop: for key, val in pairs: dict[key] = val
# Invariant: dict contains all processed pairs
```

**Set Operations:**
```python
# Loop: for item in items: seen.add(item)
# Invariant: seen == set(items[0:i])
```

### C/C++

**Pointer Invariants:**
```c
// Loop: while (p != end) { p++; }
// Invariant: start <= p <= end
// Invariant: p points to valid memory or end

// Loop: for (int* p = arr; p < arr + n; p++)
// Invariant: arr <= p <= arr + n
```

**Memory Safety:**
```c
// Loop: copying memory
// Invariant: no overlap between src and dest regions
// Invariant: all accessed memory is valid
```

### Java

**Iterator Invariants:**
```java
// Loop: while (it.hasNext()) { it.next(); }
// Invariant: iterator has processed i elements
// Invariant: iterator is valid
```

**Array Bounds:**
```java
// Loop: for (int i = 0; i < arr.length; i++)
// Invariant: 0 <= i < arr.length
// Invariant: no ArrayIndexOutOfBoundsException
```

## Complex Invariants

### Nested Loops

**2D Array Processing:**
```python
# Loop: for i in range(rows):
#         for j in range(cols):
#           process(matrix[i][j])
# Outer invariant: 0 <= i < rows, processed i complete rows
# Inner invariant: 0 <= j < cols, processed j elements in row i
```

**Multiplication Table:**
```python
# Loop: for i in range(n):
#         for j in range(n):
#           table[i][j] = i * j
# Invariant: table[i][j] == i * j for all processed positions
```

### Loop with Multiple Variables

**Two Pointers:**
```python
# Loop: while left < right:
#         if condition: left += 1
#         else: right -= 1
# Invariant: 0 <= left <= right < len(arr)
# Invariant: target not in arr[0:left] or arr[right+1:]
```

**Simultaneous Updates:**
```python
# Loop: i = 0; j = n-1
#       while i < j:
#         i += 1; j -= 1
# Invariant: i + j == n - 1 (before first update: 0 + (n-1) == n-1)
```

## Verification Patterns

### Pre-condition to Invariant

The loop invariant typically:
1. Is true before the loop starts (initialization)
2. Remains true after each iteration (maintenance)
3. Combined with loop termination, proves the post-condition

**Example:**
```python
# Pre-condition: arr is not empty
# Loop: max_val = arr[0]
#       for i in range(1, len(arr)):
#         if arr[i] > max_val:
#           max_val = arr[i]
# Invariant: max_val == max(arr[0:i+1])
# Post-condition: max_val == max(arr)
```

### Assertion Placement

```python
# Invariant as assertion
def find_max(arr):
    assert len(arr) > 0  # Pre-condition
    max_val = arr[0]

    for i in range(1, len(arr)):
        assert max_val == max(arr[0:i])  # Invariant at loop start
        if arr[i] > max_val:
            max_val = arr[i]

    assert max_val == max(arr)  # Post-condition
    return max_val
```

## Common Mistakes

### Invariant Too Weak

```python
# Weak: i >= 0 (doesn't help prove correctness)
# Better: 0 <= i < len(arr) and sum == sum(arr[0:i])
```

### Invariant Not Maintained

```python
# Claimed invariant: i < n
# Loop: while i < n: i += 2
# Problem: if n is even, i might equal n, not maintain i < n
# Correct: i <= n
```

### Off-by-One Errors

```python
# Loop: for i in range(n)
# Wrong: processed i elements
# Right: processed i+1 elements (since range(n) includes 0...n-1)
```
