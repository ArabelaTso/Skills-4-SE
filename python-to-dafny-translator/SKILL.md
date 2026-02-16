---
name: python-to-dafny-translator
description: Translate Python programs into equivalent Dafny code, preserving program semantics and ensuring the generated code is well-typed, executable, and verifiable. Use when the user asks to convert Python code to Dafny, port Python programs to Dafny, add formal verification to Python code, or create Dafny versions of Python algorithms with specifications.
---

# Python to Dafny Translator

## Overview

Transform Python programs into equivalent Dafny code that preserves the original semantics while adding formal specifications and leveraging Dafny's verification capabilities.

## Translation Workflow

### Step 1: Analyze Python Code

Understand the Python program structure and semantics:

1. **Identify program components:**
   - Functions and their signatures
   - Classes and methods
   - Data structures (lists, dicts, sets)
   - Control flow (loops, conditionals)
   - Variable types (infer from usage)

2. **Understand semantics:**
   - What does the program compute?
   - What are the inputs and outputs?
   - What are the preconditions and postconditions?
   - Are there invariants or constraints?

3. **Note translation challenges:**
   - Dynamic typing
   - Mutable data structures
   - Exception handling
   - Python-specific features (list comprehensions, generators)

### Step 2: Design Dafny Structure

Plan the Dafny equivalent:

1. **Choose appropriate types:**
   - `int` for integers (arbitrary precision)
   - `nat` for non-negative integers
   - `bool` for booleans
   - `string` for strings
   - `real` for floating-point (when needed)
   - `seq<T>` for lists
   - `set<T>` for sets
   - `map<K, V>` for dictionaries
   - `array<T>` for mutable arrays

2. **Determine function vs method:**
   - **Function**: Pure computation, no side effects, used in specifications
   - **Method**: Can have side effects, modify state, perform I/O

3. **Plan specifications:**
   - Preconditions (`requires`)
   - Postconditions (`ensures`)
   - Loop invariants
   - Frame conditions (`modifies`, `reads`)

### Step 3: Translate Code

Follow these translation principles:

#### Functions

**Pattern: Pure function**
```python
# Python
def add(a, b):
    return a + b
```

```dafny
// Dafny
function add(a: int, b: int): int
{
    a + b
}
```

**Pattern: Function with specifications**
```python
# Python
def max_value(a, b):
    """Returns the maximum of a and b"""
    return a if a > b else b
```

```dafny
// Dafny
function max(a: int, b: int): int
    ensures max(a, b) >= a && max(a, b) >= b
    ensures max(a, b) == a || max(a, b) == b
{
    if a > b then a else b
}
```

#### Methods

**Pattern: Method with side effects**
```python
# Python
def increment_counter(counter):
    counter[0] += 1
```

```dafny
// Dafny
method incrementCounter(counter: array<int>)
    requires counter.Length > 0
    modifies counter
    ensures counter[0] == old(counter[0]) + 1
{
    counter[0] := counter[0] + 1;
}
```

#### Control Flow

**Pattern: If-else**
```python
# Python
def abs_value(x):
    if x < 0:
        return -x
    else:
        return x
```

```dafny
// Dafny
function abs(x: int): int
    ensures abs(x) >= 0
{
    if x < 0 then -x else x
}
```

**Pattern: For loop → While loop with invariants**
```python
# Python
def sum_array(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total
```

```dafny
// Dafny
method sumArray(arr: array<int>) returns (total: int)
{
    total := 0;
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant total == sum(arr[..i])
    {
        total := total + arr[i];
        i := i + 1;
    }
}

function sum(s: seq<int>): int
{
    if |s| == 0 then 0 else s[0] + sum(s[1..])
}
```

#### Collections

**Pattern: Lists → Sequences**
```python
# Python
lst = [1, 2, 3, 4, 5]
first = lst[0]
length = len(lst)
```

```dafny
// Dafny
var lst: seq<int> := [1, 2, 3, 4, 5];
var first: int := lst[0];
var length: int := |lst|;
```

**Pattern: Dictionaries → Maps**
```python
# Python
d = {"a": 1, "b": 2}
value = d["a"]
```

```dafny
// Dafny
var d: map<string, int> := map["a" := 1, "b" := 2];
var value: int := d["a"];
```

#### Classes

**Pattern: Simple class**
```python
# Python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
```

```dafny
// Dafny
class Point {
    var x: int
    var y: int

    constructor(x: int, y: int)
        ensures this.x == x && this.y == y
    {
        this.x := x;
        this.y := y;
    }

    method move(dx: int, dy: int)
        modifies this
        ensures x == old(x) + dx
        ensures y == old(y) + dy
    {
        x := x + dx;
        y := y + dy;
    }
}
```

### Step 4: Add Specifications

Enhance the Dafny code with formal specifications:

1. **Preconditions (`requires`):**
   - What must be true before the function/method executes?
   - Example: `requires n >= 0` for factorial

2. **Postconditions (`ensures`):**
   - What is guaranteed after execution?
   - Example: `ensures result >= 0` for absolute value

3. **Loop invariants:**
   - What is true at the start of each iteration?
   - Example: `invariant 0 <= i <= n` for loop counter

4. **Frame conditions:**
   - `modifies`: What can be modified?
   - `reads`: What can be read?

### Step 5: Verify and Test

Ensure the translated code is correct:

1. **Run Dafny verifier:**
   ```bash
   dafny verify program.dfy
   ```

2. **Fix verification errors:**
   - Add missing invariants
   - Strengthen postconditions
   - Add helper lemmas if needed

3. **Test execution:**
   ```bash
   dafny run program.dfy
   ```

4. **Compare outputs:**
   - Run original Python program
   - Run translated Dafny program
   - Verify outputs match

### Step 6: Refine and Optimize

Improve the translated code:

1. **Simplify specifications:**
   - Remove redundant conditions
   - Use helper functions for complex specs

2. **Add documentation:**
   ```dafny
   // Computes the factorial of n
   function factorial(n: nat): nat
   ```

3. **Optimize for verification:**
   - Break complex functions into smaller pieces
   - Add intermediate assertions
   - Use lemmas for complex proofs

## Common Translation Patterns

For detailed patterns, see [translation_patterns.md](references/translation_patterns.md).

### Quick Reference

| Python | Dafny |
|--------|-------|
| `x = 10` | `var x: int := 10;` |
| `def f(x):` | `function f(x: int): int` or `method f(x: int)` |
| `return x` | `x` (function) or `return x;` (method) |
| `if x > 0:` | `if x > 0 then` or `if x > 0 {` |
| `for i in range(n):` | `while i < n` with invariants |
| `[1, 2, 3]` | `[1, 2, 3]` (seq) |
| `{1, 2, 3}` | `{1, 2, 3}` (set) |
| `{"a": 1}` | `map["a" := 1]` |
| `len(lst)` | `\|lst\|` |
| `lst[i]` | `lst[i]` |
| `class C:` | `class C {` |
| `None` | Use `Option<T>` datatype |

## Examples

### Example 1: Simple Function

**Python Input:**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Dafny Output:**
```dafny
function factorial(n: nat): nat
    ensures factorial(n) >= 1
{
    if n <= 1 then 1
    else n * factorial(n - 1)
}
```

### Example 2: Array Processing

**Python Input:**
```python
def find_max(arr):
    if len(arr) == 0:
        return None
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
```

**Dafny Output:**
```dafny
method findMax(arr: array<int>) returns (maxVal: int)
    requires arr.Length > 0
    ensures forall k :: 0 <= k < arr.Length ==> maxVal >= arr[k]
    ensures exists k :: 0 <= k < arr.Length && maxVal == arr[k]
{
    maxVal := arr[0];
    var i := 1;
    while i < arr.Length
        invariant 1 <= i <= arr.Length
        invariant forall k :: 0 <= k < i ==> maxVal >= arr[k]
        invariant exists k :: 0 <= k < i && maxVal == arr[k]
    {
        if arr[i] > maxVal {
            maxVal := arr[i];
        }
        i := i + 1;
    }
}
```

### Example 3: Class with Methods

**Python Input:**
```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
```

**Dafny Output:**
```dafny
class BankAccount {
    var balance: int

    constructor(balance: int)
        requires balance >= 0
        ensures this.balance == balance
    {
        this.balance := balance;
    }

    method deposit(amount: int)
        requires amount >= 0
        modifies this
        ensures balance == old(balance) + amount
    {
        balance := balance + amount;
    }

    method withdraw(amount: int) returns (success: bool)
        requires amount >= 0
        modifies this
        ensures success ==> balance == old(balance) - amount
        ensures !success ==> balance == old(balance)
        ensures success <==> amount <= old(balance)
    {
        if amount <= balance {
            balance := balance - amount;
            return true;
        }
        return false;
    }
}
```

### Example 4: Binary Search

**Python Input:**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Dafny Output:**
```dafny
method binarySearch(arr: array<int>, target: int) returns (index: int)
    requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
    ensures 0 <= index < arr.Length ==> arr[index] == target
    ensures index == -1 ==> forall k :: 0 <= k < arr.Length ==> arr[k] != target
{
    var left := 0;
    var right := arr.Length - 1;

    while left <= right
        invariant 0 <= left <= arr.Length
        invariant -1 <= right < arr.Length
        invariant forall k :: 0 <= k < left ==> arr[k] < target
        invariant forall k :: right < k < arr.Length ==> arr[k] > target
    {
        var mid := (left + right) / 2;
        if arr[mid] == target {
            return mid;
        } else if arr[mid] < target {
            left := mid + 1;
        } else {
            right := mid - 1;
        }
    }
    return -1;
}
```

## Best Practices

1. **Start with specifications:** Think about preconditions and postconditions first
2. **Use appropriate types:** Choose `nat` for non-negative values, `seq` for immutable lists
3. **Add loop invariants:** Essential for verification, document loop behavior
4. **Prefer functions over methods:** Functions are easier to verify and use in specs
5. **Test incrementally:** Verify small pieces before combining
6. **Use helper functions:** Break complex logic into smaller, verifiable pieces
7. **Document assumptions:** Make implicit Python assumptions explicit in Dafny
8. **Handle edge cases:** Explicitly handle empty collections, zero values, etc.

## Key Differences: Python vs Dafny

1. **Typing:** Python is dynamically typed, Dafny is statically typed
2. **Mutability:** Python has mutable lists/dicts, Dafny prefers immutable sequences
3. **Verification:** Dafny requires specifications and proofs
4. **Loops:** Dafny requires loop invariants for verification
5. **Exceptions:** Python uses exceptions, Dafny uses preconditions
6. **None:** Python has `None`, Dafny uses `Option<T>` datatype
7. **Functions vs Methods:** Dafny distinguishes pure functions from methods with side effects

## Limitations and Considerations

1. **Dynamic features:** Python's dynamic typing and reflection are not directly translatable
2. **Libraries:** Python standard library functions need manual translation
3. **Generators:** Python generators require different approaches in Dafny
4. **Decorators:** Python decorators don't have direct Dafny equivalents
5. **Multiple inheritance:** Dafny has limited inheritance support
6. **Performance:** Verification adds compile-time overhead
7. **Learning curve:** Dafny specifications require understanding of formal methods

## Resources

- **Translation patterns:** See [translation_patterns.md](references/translation_patterns.md) for comprehensive pattern catalog
- **Dafny documentation:** https://dafny.org/
- **Dafny tutorial:** https://dafny.org/dafny/OnlineTutorial/guide
- **Dafny reference:** https://dafny.org/latest/DafnyRef/DafnyRef
