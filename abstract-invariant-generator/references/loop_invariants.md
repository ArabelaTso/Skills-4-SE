# Loop Invariant Patterns and Generation Strategies

## Loop Invariant Fundamentals

A loop invariant must satisfy three properties:
1. **Initialization**: True before the first iteration
2. **Maintenance**: If true before an iteration, remains true after
3. **Termination**: Combined with loop exit condition, establishes desired postcondition

## Common Loop Patterns

### 1. Counter Loop Pattern

**Code Pattern**:
```python
i = start
while i < end:
    process(i)
    i += step
```

**Invariant Template**:
```
invariant start ≤ i ≤ end
invariant ∀k. start ≤ k < i ⟹ processed(k)
```

**Example - Array Initialization**:
```python
i = 0
while i < n:
    arr[i] = 0
    i += 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ arr[k] = 0
```

### 2. Accumulator Pattern

**Code Pattern**:
```python
acc = initial_value
i = 0
while i < len(arr):
    acc = combine(acc, arr[i])
    i += 1
```

**Invariant Template**:
```
invariant 0 ≤ i ≤ len(arr)
invariant acc = aggregate(arr[0..i-1])
```

**Example - Sum**:
```python
sum = 0
i = 0
while i < len(arr):
    sum += arr[i]
    i += 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ len(arr)
invariant sum = Σ(arr[0..i-1])
```

**Example - Product**:
```python
product = 1
i = 0
while i < len(arr):
    product *= arr[i]
    i += 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ len(arr)
invariant product = Π(arr[0..i-1])
```

### 3. Search Pattern

**Code Pattern**:
```python
i = 0
found = False
while i < len(arr) and not found:
    if arr[i] == target:
        found = True
    else:
        i += 1
```

**Invariant Template**:
```
invariant 0 ≤ i ≤ len(arr)
invariant ∀k. 0 ≤ k < i ⟹ arr[k] ≠ target
invariant found ⟹ arr[i] = target
```

**Example - Linear Search**:
```python
index = -1
i = 0
while i < len(arr):
    if arr[i] == target:
        index = i
        break
    i += 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ len(arr)
invariant index = -1 ⟹ (∀k. 0 ≤ k < i ⟹ arr[k] ≠ target)
invariant index ≥ 0 ⟹ arr[index] = target
```

### 4. Binary Search Pattern

**Code Pattern**:
```python
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
```

**Invariant Template**:
```
invariant 0 ≤ low ≤ high + 1 ≤ len(arr)
invariant ∀k. 0 ≤ k < low ⟹ arr[k] < target
invariant ∀k. high < k < len(arr) ⟹ arr[k] > target
invariant sorted(arr)
```

### 5. Partitioning Pattern

**Code Pattern** (Quicksort partition):
```python
pivot = arr[high]
i = low - 1
for j in range(low, high):
    if arr[j] <= pivot:
        i += 1
        swap(arr[i], arr[j])
```

**Invariant Template**:
```
invariant low - 1 ≤ i < j ≤ high
invariant ∀k. low ≤ k ≤ i ⟹ arr[k] ≤ pivot
invariant ∀k. i < k < j ⟹ arr[k] > pivot
```

### 6. Two-Pointer Pattern

**Code Pattern**:
```python
left = 0
right = len(arr) - 1
while left < right:
    if condition(arr[left], arr[right]):
        left += 1
    else:
        right -= 1
```

**Invariant Template**:
```
invariant 0 ≤ left ≤ right < len(arr)
invariant ∀k. 0 ≤ k < left ⟹ property_left(arr[k])
invariant ∀k. right < k < len(arr) ⟹ property_right(arr[k])
```

**Example - Remove Duplicates**:
```python
i = 0
j = 1
while j < len(arr):
    if arr[i] != arr[j]:
        i += 1
        arr[i] = arr[j]
    j += 1
```

**Invariants**:
```
invariant 0 ≤ i < j ≤ len(arr)
invariant ∀k, l. 0 ≤ k < l ≤ i ⟹ arr[k] ≠ arr[l]
invariant ∀k. 0 ≤ k ≤ i ⟹ arr[k] ∈ arr[0..j-1]
```

### 7. Sliding Window Pattern

**Code Pattern**:
```python
window_sum = sum(arr[0:k])
max_sum = window_sum
for i in range(k, len(arr)):
    window_sum = window_sum - arr[i-k] + arr[i]
    max_sum = max(max_sum, window_sum)
```

**Invariant Template**:
```
invariant k ≤ i ≤ len(arr)
invariant window_sum = Σ(arr[i-k..i-1])
invariant max_sum = max(all window sums seen so far)
```

### 8. Nested Loop Pattern

**Code Pattern**:
```python
for i in range(n):
    for j in range(m):
        process(i, j)
```

**Invariant Template**:
```
Outer loop:
  invariant 0 ≤ i ≤ n
  invariant ∀r. 0 ≤ r < i ⟹ (∀c. 0 ≤ c < m ⟹ processed(r, c))

Inner loop:
  invariant 0 ≤ j ≤ m
  invariant ∀c. 0 ≤ c < j ⟹ processed(i, c)
```

**Example - Matrix Zeroing**:
```python
for i in range(rows):
    for j in range(cols):
        matrix[i][j] = 0
```

**Invariants**:
```
Outer:
  invariant 0 ≤ i ≤ rows
  invariant ∀r, c. 0 ≤ r < i ∧ 0 ≤ c < cols ⟹ matrix[r][c] = 0

Inner:
  invariant 0 ≤ j ≤ cols
  invariant ∀c. 0 ≤ c < j ⟹ matrix[i][c] = 0
```

## Invariant Generation Strategies

### Strategy 1: Forward Reasoning

Start from precondition and propagate through loop:

**Example**:
```python
# Precondition: n > 0, arr.length = n
i = 0
# i = 0, so 0 ≤ i ≤ n holds
while i < n:
    # 0 ≤ i < n (from loop condition)
    arr[i] = 0
    # arr[0..i] are now 0
    i += 1
    # i increased by 1, still 0 ≤ i ≤ n
```

**Generated Invariant**: `0 ≤ i ≤ n ∧ ∀k. 0 ≤ k < i ⟹ arr[k] = 0`

### Strategy 2: Backward Reasoning

Start from postcondition and work backward:

**Example**:
```python
# Postcondition: result = max(arr)
max_val = arr[0]
i = 1
while i < len(arr):
    if arr[i] > max_val:
        max_val = arr[i]
    i += 1
# Want: max_val = max(arr)
```

**Reasoning**: After loop, need `max_val = max(arr[0..len(arr)-1])`
During loop, need `max_val = max(arr[0..i-1])`

**Generated Invariant**: `1 ≤ i ≤ len(arr) ∧ max_val = max(arr[0..i-1])`

### Strategy 3: Template Matching

Recognize common patterns and apply templates:

**Pattern Recognition**:
- Counter variable incrementing → Counter pattern
- Accumulating values → Accumulator pattern
- Searching for element → Search pattern
- Two indices moving → Two-pointer pattern

### Strategy 4: Abstract Interpretation

Use abstract domains to infer properties:

**Interval Domain**:
```python
i = 0  # i: [0, 0]
while i < n:  # i: [0, n-1]
    i += 1  # i: [1, n]
# After loop: i: [n, n]
```

**Invariant**: `0 ≤ i ≤ n`

**Relational Domain**:
```python
i = 0
j = 0
while i < n:
    i += 1
    j += 1
# Relation: i = j
```

**Invariant**: `i = j ∧ 0 ≤ i ≤ n`

### Strategy 5: Strengthening

Start with weak invariant and strengthen:

**Initial (too weak)**:
```
invariant 0 ≤ i ≤ n
```

**Strengthened**:
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ arr[k] = 0
```

**Technique**: Add properties about what has been accomplished.

## Handling Difficult Cases

### Multiple Loop Variables

Track relationships:
```python
i = 0
j = n - 1
while i < j:
    i += 1
    j -= 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ j < n
invariant i + j = n - 1  (initially)
```

### Complex Loop Bodies

Break into phases:
```python
while condition:
    # Phase 1: preparation
    x = compute1()
    # Invariant after phase 1: P1(x)

    # Phase 2: main work
    y = compute2(x)
    # Invariant after phase 2: P2(x, y)

    # Phase 3: update
    update(y)
    # Invariant after phase 3: P3(...)
```

### Early Exit

Handle all exit paths:
```python
while i < n:
    if arr[i] == target:
        return i
    i += 1
return -1
```

**Invariants**:
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ arr[k] ≠ target
# If loop exits normally: target ∉ arr
# If loop exits early: arr[i] = target
```

## Verification with Invariants

### Proving Initialization

Show invariant holds before first iteration:
```python
i = 0
# Check: 0 ≤ 0 ≤ n? ✓ (assuming n ≥ 0)
# Check: ∀k. 0 ≤ k < 0 ⟹ arr[k] = 0? ✓ (vacuously true)
```

### Proving Maintenance

Show invariant preserved by loop body:
```python
# Assume: 0 ≤ i < n ∧ ∀k. 0 ≤ k < i ⟹ arr[k] = 0
arr[i] = 0
# Now: arr[0..i] are all 0
i += 1
# Now: 0 ≤ i ≤ n ∧ ∀k. 0 ≤ k < i ⟹ arr[k] = 0 ✓
```

### Proving Termination

Show invariant + exit condition ⟹ postcondition:
```python
# Invariant: 0 ≤ i ≤ n ∧ ∀k. 0 ≤ k < i ⟹ arr[k] = 0
# Exit condition: i ≥ n
# Combined: i = n ∧ ∀k. 0 ≤ k < n ⟹ arr[k] = 0
# Postcondition: ∀k. 0 ≤ k < n ⟹ arr[k] = 0 ✓
```

## Common Mistakes

### Too Weak

**Problem**: Invariant doesn't establish postcondition
```
invariant i ≤ n  # Too weak! Doesn't say i ≥ 0
```

**Fix**: Strengthen
```
invariant 0 ≤ i ≤ n
```

### Too Strong

**Problem**: Invariant doesn't hold initially or isn't maintained
```
invariant i < n  # Too strong! Fails when i = n
```

**Fix**: Weaken
```
invariant i ≤ n
```

### Missing Progress Property

**Problem**: Doesn't capture what's been accomplished
```
invariant 0 ≤ i ≤ n  # Doesn't say anything about arr
```

**Fix**: Add progress property
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ arr[k] = 0
```
