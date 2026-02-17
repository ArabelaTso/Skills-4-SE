# Abstract Trace Summarization Examples

This document provides complete examples of abstract trace summarization for various program patterns.

## Example 1: Simple Loop with Interval Analysis

### Source Code
```python
def sum_array(arr, n):
    total = 0
    i = 0
    while i < n:
        total = total + arr[i]
        i = i + 1
    return total
```

### Control Flow Graph
```
Entry → L1 → L2 → L3 → L4 → L5 → L2 (loop back)
                    ↓
                   Exit
```

### Abstract Trace (Interval Domain)

**Initial State (Entry):**
```
arr: array reference (non-null)
n: [0, +∞]
```

**L1: total = 0**
```
total: [0, 0]
i: ⊤ (uninitialized)
n: [0, +∞]
```

**L2: i = 0**
```
total: [0, 0]
i: [0, 0]
n: [0, +∞]
```

**L3: Loop head (before widening)**
```
Iteration 0: total: [0, 0], i: [0, 0]
Iteration 1: total: ⊤, i: [0, 1]
Iteration 2: total: ⊤, i: [0, 2]
```

**L3: Loop head (after widening)**
```
total: [0, +∞]
i: [0, +∞]
n: [0, +∞]
Invariant: 0 ≤ i ≤ n
```

**L4: Condition (i < n) - True Branch**
```
total: [0, +∞]
i: [0, +∞]
n: [1, +∞]
Constraint: i < n
```

**L5: total = total + arr[i], i = i + 1**
```
total: [0, +∞]  (after addition)
i: [1, +∞]      (after increment)
```

**Exit: Condition (i < n) - False Branch**
```
total: [0, +∞]
i: [0, +∞]
n: [0, +∞]
Constraint: i ≥ n
```

### Summary
```
Function: sum_array(arr, n)
Precondition: arr is non-null array, n ≥ 0
Postcondition: returns value in [0, +∞]
Loop invariant: 0 ≤ i ≤ n, total ≥ 0
Loop bound: n iterations
Side effects: None
```

---

## Example 2: Conditional Branches with Sign Analysis

### Source Code
```python
def classify_number(x):
    if x > 0:
        result = 1
    elif x < 0:
        result = -1
    else:
        result = 0
    return result
```

### Abstract Trace (Sign Domain)

**Entry:**
```
x: ⊤ (unknown sign)
```

**Branch 1: x > 0**
```
x: + (positive)
result: + (1)
```

**Branch 2: x < 0**
```
x: - (negative)
result: - (-1)
```

**Branch 3: else**
```
x: 0 (zero)
result: 0 (zero)
```

**Join at Exit:**
```
x: ⊤ (any sign)
result: {-, 0, +} (any sign)
```

### Summary
```
Function: classify_number(x)
Precondition: x is integer
Postcondition: returns -1, 0, or 1
Control flow: 3 paths (positive, negative, zero)
Variable relationships: sign(result) = sign(x)
```

---

## Example 3: Nested Loops with Relational Analysis

### Source Code
```python
def matrix_multiply(A, B, n):
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C
```

### Abstract Trace (Interval + Relational Domain)

**Entry:**
```
A: n×n matrix
B: n×n matrix
n: [1, +∞]
```

**After C initialization:**
```
C: n×n matrix, all elements = 0
```

**Outer loop (i):**
```
Loop invariant: 0 ≤ i < n
Iterations: n
```

**Middle loop (j):**
```
Loop invariant: 0 ≤ i < n, 0 ≤ j < n
Iterations: n per outer iteration
```

**Inner loop (k):**
```
Loop invariant: 0 ≤ i < n, 0 ≤ j < n, 0 ≤ k < n
Iterations: n per middle iteration
C[i][j]: accumulates sum
```

**Relational constraints:**
```
i ∈ [0, n-1]
j ∈ [0, n-1]
k ∈ [0, n-1]
i, j, k are independent
```

### Summary
```
Function: matrix_multiply(A, B, n)
Precondition: A, B are n×n matrices, n ≥ 1
Postcondition: C is n×n matrix, C[i][j] = Σ(A[i][k] * B[k][j])
Loop structure: 3 nested loops
Total iterations: n³
Complexity: O(n³)
Memory: O(n²) for result matrix
```

---

## Example 4: Pointer Analysis with Nullness

### Source Code (Java)
```java
public class Node {
    int value;
    Node next;

    public int sumList(Node head) {
        int sum = 0;
        Node current = head;
        while (current != null) {
            sum += current.value;
            current = current.next;
        }
        return sum;
    }
}
```

### Abstract Trace (Nullness Domain)

**Entry:**
```
head: {null, non-null, ⊤}
```

**L1: sum = 0**
```
sum: 0
head: {null, non-null, ⊤}
```

**L2: current = head**
```
sum: 0
current: {null, non-null, ⊤}
```

**L3: Loop head**
```
sum: [0, +∞]
current: {null, non-null, ⊤}
```

**L4: Condition (current != null) - True Branch**
```
sum: [0, +∞]
current: non-null (refined by condition)
```

**L5: sum += current.value**
```
sum: [0, +∞]
current: non-null
Access: SAFE (current is non-null)
```

**L6: current = current.next**
```
sum: [0, +∞]
current: {null, non-null, ⊤} (next may be null)
```

**Exit: Condition (current != null) - False Branch**
```
sum: [0, +∞]
current: null (refined by condition)
```

### Summary
```
Function: sumList(head)
Precondition: head may be null
Postcondition: returns sum ≥ 0
Null safety: All dereferences are safe
Loop invariant: current is null or valid Node
Loop termination: Guaranteed (list is finite)
Potential issues: None detected
```

---

## Example 5: Exception Flow Analysis

### Source Code (Python)
```python
def divide_and_process(a, b, arr):
    try:
        result = a / b
        index = int(result)
        value = arr[index]
        return value * 2
    except ZeroDivisionError:
        return -1
    except IndexError:
        return -2
    except Exception:
        return -3
```

### Abstract Trace with Exception States

**Entry:**
```
a: ℝ (real number)
b: ℝ (real number)
arr: array
```

**Normal flow:**

**L1: result = a / b**
```
If b ≠ 0:
    result: ℝ
    Continue to L2
If b = 0:
    Exception: ZeroDivisionError
    Jump to handler 1
```

**L2: index = int(result)**
```
index: ℤ (integer)
May raise: ValueError (if result is NaN/Inf)
```

**L3: value = arr[index]**
```
If 0 ≤ index < len(arr):
    value: arr[index]
    Continue to L4
If index < 0 or index ≥ len(arr):
    Exception: IndexError
    Jump to handler 2
```

**L4: return value * 2**
```
Return: value * 2
```

**Exception handlers:**

**Handler 1: ZeroDivisionError**
```
Catches: b = 0
Return: -1
```

**Handler 2: IndexError**
```
Catches: index out of bounds
Return: -2
```

**Handler 3: Exception**
```
Catches: Any other exception
Return: -3
```

### Summary
```
Function: divide_and_process(a, b, arr)
Precondition: a, b are numbers, arr is array
Postcondition: returns integer

Execution paths:
1. Normal: b ≠ 0, 0 ≤ int(a/b) < len(arr) → returns arr[int(a/b)] * 2
2. ZeroDivisionError: b = 0 → returns -1
3. IndexError: int(a/b) out of bounds → returns -2
4. Other exceptions → returns -3

Exception safety: All exceptions handled
Return value: integer (may be negative)
```

---

## Example 6: Recursive Function with Call Stack

### Source Code
```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

### Abstract Trace (Interval Domain with Call Stack)

**Call: factorial(5)**

**Stack frame 1: n = 5**
```
n: [5, 5]
Condition: n > 1 (true)
Recursive call: factorial(4)
```

**Stack frame 2: n = 4**
```
n: [4, 4]
Condition: n > 1 (true)
Recursive call: factorial(3)
```

**Stack frame 3: n = 3**
```
n: [3, 3]
Condition: n > 1 (true)
Recursive call: factorial(2)
```

**Stack frame 4: n = 2**
```
n: [2, 2]
Condition: n > 1 (true)
Recursive call: factorial(1)
```

**Stack frame 5: n = 1**
```
n: [1, 1]
Condition: n ≤ 1 (true)
Return: 1
```

**Unwinding:**
```
Frame 4: return 2 * 1 = 2
Frame 3: return 3 * 2 = 6
Frame 2: return 4 * 6 = 24
Frame 1: return 5 * 24 = 120
```

### Abstract Summary

**General case: factorial(n)**
```
Precondition: n ≥ 0
Base case: n ≤ 1 → return 1
Recursive case: n > 1 → return n * factorial(n-1)
Call depth: n
Return value: n! (factorial of n)
Termination: Guaranteed for n ≥ 0
```

**Abstract trace for arbitrary n:**
```
Entry: n ∈ [0, +∞]

If n ∈ [0, 1]:
    Return: 1

If n ∈ [2, +∞]:
    Recursive calls: n-1 times
    Return: [1, +∞] (grows exponentially)
    Stack depth: n
```

---

## Example 7: Concurrent Program with Thread Interleaving

### Source Code (Java)
```java
class Counter {
    private int count = 0;

    public void increment() {
        int temp = count;
        temp = temp + 1;
        count = temp;
    }
}

// Thread 1 and Thread 2 both call increment()
```

### Abstract Trace (Interleaving Analysis)

**Initial state:**
```
count: 0
```

**Possible interleavings:**

**Interleaving 1: Sequential (T1 then T2)**
```
T1: temp1 = count (0)
T1: temp1 = temp1 + 1 (1)
T1: count = temp1 (1)
T2: temp2 = count (1)
T2: temp2 = temp2 + 1 (2)
T2: count = temp2 (2)
Final: count = 2 ✓
```

**Interleaving 2: Sequential (T2 then T1)**
```
T2: temp2 = count (0)
T2: temp2 = temp2 + 1 (1)
T2: count = temp2 (1)
T1: temp1 = count (1)
T1: temp1 = temp1 + 1 (2)
T1: count = temp1 (2)
Final: count = 2 ✓
```

**Interleaving 3: Race condition**
```
T1: temp1 = count (0)
T2: temp2 = count (0)
T1: temp1 = temp1 + 1 (1)
T2: temp2 = temp2 + 1 (1)
T1: count = temp1 (1)
T2: count = temp2 (1)
Final: count = 1 ✗ (lost update)
```

**Interleaving 4: Another race**
```
T1: temp1 = count (0)
T2: temp2 = count (0)
T2: temp2 = temp2 + 1 (1)
T1: temp1 = temp1 + 1 (1)
T2: count = temp2 (1)
T1: count = temp1 (1)
Final: count = 1 ✗ (lost update)
```

### Summary
```
Method: increment()
Precondition: count ≥ 0
Expected postcondition: count increases by 1
Actual postcondition: count ∈ [1, 2] (with 2 threads)

Concurrency issues:
- Data race on 'count' variable
- Lost update problem
- Non-atomic read-modify-write

Possible final states:
- count = 2 (correct, if no interleaving)
- count = 1 (incorrect, if race occurs)

Fix: Use synchronization (synchronized, locks, atomic operations)
```

---

## Example 8: Array Bounds Analysis

### Source Code
```python
def process_array(arr, start, end):
    result = 0
    for i in range(start, end):
        result += arr[i]
    return result
```

### Abstract Trace (Interval Domain with Bounds Checking)

**Entry:**
```
arr: array of length L
start: ℤ
end: ℤ
L: [0, +∞]
```

**Precondition analysis:**
```
Required: 0 ≤ start ≤ end ≤ L
```

**Loop analysis:**
```
Loop variable: i ∈ [start, end-1]
Array access: arr[i]
```

**Bounds checking:**

**Case 1: Safe access**
```
If 0 ≤ start ≤ end ≤ L:
    All accesses arr[i] are safe
    i ∈ [start, end-1] ⊆ [0, L-1]
```

**Case 2: Potential underflow**
```
If start < 0:
    arr[start] → IndexError
    Access out of bounds (negative index)
```

**Case 3: Potential overflow**
```
If end > L:
    arr[end-1] → IndexError
    Access out of bounds (beyond array length)
```

**Case 4: Empty range**
```
If start ≥ end:
    Loop doesn't execute
    result = 0
    No array access
```

### Summary
```
Function: process_array(arr, start, end)
Precondition: 0 ≤ start ≤ end ≤ len(arr)
Postcondition: returns sum of arr[start:end]

Safety analysis:
✓ Safe if: 0 ≤ start ≤ end ≤ len(arr)
✗ Unsafe if: start < 0 (underflow)
✗ Unsafe if: end > len(arr) (overflow)
✓ Safe if: start ≥ end (empty range, no access)

Recommendations:
1. Add precondition check: assert 0 <= start <= end <= len(arr)
2. Or use Python slicing: sum(arr[start:end])
3. Or add bounds validation at function entry
```

---

## Example 9: String Analysis with Length Tracking

### Source Code (C)
```c
void concat_strings(char *dest, const char *src, int dest_size) {
    int dest_len = strlen(dest);
    int src_len = strlen(src);
    int i = 0;

    while (src[i] != '\0' && dest_len + i < dest_size - 1) {
        dest[dest_len + i] = src[i];
        i++;
    }
    dest[dest_len + i] = '\0';
}
```

### Abstract Trace (String Length Domain)

**Entry:**
```
dest: string buffer of size dest_size
src: string of length src_len
dest_size: [1, +∞]
```

**L1: dest_len = strlen(dest)**
```
dest_len: [0, dest_size-1]
```

**L2: src_len = strlen(src)**
```
src_len: [0, +∞]
```

**L3: i = 0**
```
i: 0
```

**Loop invariant:**
```
0 ≤ i ≤ src_len
0 ≤ dest_len + i < dest_size
dest[0..dest_len+i-1] contains valid data
```

**Loop condition:**
```
src[i] != '\0': i < src_len
dest_len + i < dest_size - 1: space available
```

**Loop body:**
```
dest[dest_len + i] = src[i]
i++
```

**After loop:**
```
i ∈ [0, min(src_len, dest_size - dest_len - 1)]
dest_len + i < dest_size
```

**Final null terminator:**
```
dest[dest_len + i] = '\0'
Access: dest_len + i ∈ [dest_len, dest_size-1]
```

### Summary
```
Function: concat_strings(dest, src, dest_size)
Precondition:
  - dest is valid buffer of size dest_size
  - dest contains null-terminated string
  - src is null-terminated string
  - dest_size ≥ 1

Postcondition:
  - dest contains concatenation (possibly truncated)
  - dest is null-terminated
  - Length: min(dest_len + src_len, dest_size - 1)

Buffer safety:
✓ No buffer overflow (loop condition prevents it)
✓ Always null-terminated
✓ Handles truncation gracefully

Behavior:
- Copies up to (dest_size - dest_len - 1) characters from src
- Stops at src null terminator or buffer limit
- Always adds null terminator
```

---

## Example 10: State Machine Analysis

### Source Code
```python
class TrafficLight:
    def __init__(self):
        self.state = "RED"

    def next_state(self):
        if self.state == "RED":
            self.state = "GREEN"
        elif self.state == "GREEN":
            self.state = "YELLOW"
        elif self.state == "YELLOW":
            self.state = "RED"
```

### Abstract Trace (State Domain)

**State space:**
```
States: {RED, GREEN, YELLOW}
```

**Initial state:**
```
state: RED
```

**Transition function:**
```
RED → GREEN
GREEN → YELLOW
YELLOW → RED
```

**Abstract state graph:**
```
    RED
     ↓
   GREEN
     ↓
  YELLOW
     ↓
    RED (cycle)
```

**Reachability analysis:**
```
From RED: can reach {RED, GREEN, YELLOW}
From GREEN: can reach {RED, GREEN, YELLOW}
From YELLOW: can reach {RED, GREEN, YELLOW}
```

**Cycle detection:**
```
Cycle: RED → GREEN → YELLOW → RED
Cycle length: 3
All states are in the cycle
```

**Invariants:**
```
- state ∈ {RED, GREEN, YELLOW} (always)
- After 3 transitions, returns to initial state
- No invalid states reachable
```

### Summary
```
Class: TrafficLight
State space: {RED, GREEN, YELLOW}
Initial state: RED
Transitions: RED→GREEN→YELLOW→RED (cyclic)

Properties:
- Deterministic: Each state has exactly one successor
- Total: Transition defined for all states
- Cyclic: Returns to initial state after 3 steps
- Safe: No invalid states reachable

Temporal properties:
- Eventually RED (after at most 3 steps)
- Eventually GREEN (after at most 3 steps)
- Eventually YELLOW (after at most 3 steps)
- Always in {RED, GREEN, YELLOW}
```
