# Verification Guide: Writing Effective Specifications

Guide for writing preconditions, postconditions, loop invariants, and other verification annotations in Dafny.

## Preconditions (requires)

Preconditions specify what must be true before a method executes.

### Basic Preconditions

**Array bounds:**
```dafny
method get(arr: array<int>, index: nat) returns (value: int)
    requires index < arr.Length
{
    value := arr[index];
}
```

**Non-zero divisor:**
```dafny
method divide(a: int, b: int) returns (result: int)
    requires b != 0
{
    result := a / b;
}
```

**Multiple conditions:**
```dafny
method binarySearch(arr: array<int>, target: int) returns (index: int)
    requires arr.Length > 0
    requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]  // sorted
{
    // implementation
}
```

### Precondition Patterns

**Valid range:**
```dafny
method substring(s: string, start: nat, length: nat) returns (result: string)
    requires start + length <= |s|
{
    result := s[start..start + length];
}
```

**Non-empty collection:**
```dafny
method head(xs: seq<int>) returns (first: int)
    requires |xs| > 0
{
    first := xs[0];
}
```

**Sorted array:**
```dafny
predicate isSorted(arr: array<int>)
    reads arr
{
    forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
}

method insertSorted(arr: array<int>, value: int)
    requires isSorted(arr)
{
    // implementation
}
```

## Postconditions (ensures)

Postconditions specify what must be true after a method executes.

### Basic Postconditions

**Return value property:**
```dafny
method abs(x: int) returns (result: nat)
    ensures result >= 0
    ensures x >= 0 ==> result == x
    ensures x < 0 ==> result == -x
{
    if x >= 0 {
        result := x;
    } else {
        result := -x;
    }
}
```

**Array modification:**
```dafny
method swap(arr: array<int>, i: nat, j: nat)
    requires i < arr.Length && j < arr.Length
    modifies arr
    ensures arr[i] == old(arr[j])
    ensures arr[j] == old(arr[i])
    ensures forall k :: 0 <= k < arr.Length && k != i && k != j ==> arr[k] == old(arr[k])
{
    var temp := arr[i];
    arr[i] := arr[j];
    arr[j] := temp;
}
```

### Postcondition Patterns

**Preservation of properties:**
```dafny
method reverse(arr: array<int>)
    modifies arr
    ensures forall i :: 0 <= i < arr.Length ==> arr[i] == old(arr[arr.Length - 1 - i])
    ensures multiset(arr[..]) == multiset(old(arr[..]))  // Same elements
{
    // implementation
}
```

**Relationship to input:**
```dafny
method double(x: int) returns (result: int)
    ensures result == 2 * x
{
    result := x + x;
}
```

**Functional correctness:**
```dafny
function factorial(n: nat): nat
{
    if n == 0 then 1 else n * factorial(n - 1)
}

method computeFactorial(n: nat) returns (result: nat)
    ensures result == factorial(n)
{
    result := 1;
    var i := 1;
    while i <= n
        invariant 1 <= i <= n + 1
        invariant result == factorial(i - 1)
    {
        result := result * i;
        i := i + 1;
    }
}
```

## Loop Invariants

Loop invariants are properties that hold before and after each iteration.

### Essential Invariants

**1. Bounds invariant:**
```dafny
var i := 0;
while i < arr.Length
    invariant 0 <= i <= arr.Length
{
    // body
    i := i + 1;
}
```

**2. Progress invariant:**
```dafny
method sum(arr: array<int>) returns (total: int)
{
    total := 0;
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant total == arraySum(arr[..i])  // Progress
    {
        total := total + arr[i];
        i := i + 1;
    }
}
```

**3. Preservation invariant:**
```dafny
method findMax(arr: array<int>) returns (max: int)
    requires arr.Length > 0
{
    max := arr[0];
    var i := 1;
    while i < arr.Length
        invariant 1 <= i <= arr.Length
        invariant forall k :: 0 <= k < i ==> arr[k] <= max  // Preservation
        invariant exists k :: 0 <= k < i && arr[k] == max   // max is in array
    {
        if arr[i] > max {
            max := arr[i];
        }
        i := i + 1;
    }
}
```

### Complex Loop Invariants

**Binary search:**
```dafny
method binarySearch(arr: array<int>, target: int) returns (index: int)
    requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
    ensures index == -1 || (0 <= index < arr.Length && arr[index] == target)
{
    var low := 0;
    var high := arr.Length;
    while low < high
        invariant 0 <= low <= high <= arr.Length
        invariant forall i :: 0 <= i < low ==> arr[i] < target
        invariant forall i :: high <= i < arr.Length ==> arr[i] > target
    {
        var mid := (low + high) / 2;
        if arr[mid] < target {
            low := mid + 1;
        } else if arr[mid] > target {
            high := mid;
        } else {
            return mid;
        }
    }
    return -1;
}
```

**Partitioning:**
```dafny
method partition(arr: array<int>, low: nat, high: nat) returns (pivot: nat)
    requires low < high <= arr.Length
    modifies arr
    ensures low <= pivot < high
    ensures forall i :: low <= i < pivot ==> arr[i] <= arr[pivot]
    ensures forall i :: pivot < i < high ==> arr[i] >= arr[pivot]
{
    var pivotValue := arr[high - 1];
    var i := low;
    var j := low;
    while j < high - 1
        invariant low <= i <= j <= high - 1
        invariant forall k :: low <= k < i ==> arr[k] <= pivotValue
        invariant forall k :: i <= k < j ==> arr[k] > pivotValue
    {
        if arr[j] <= pivotValue {
            arr[i], arr[j] := arr[j], arr[i];
            i := i + 1;
        }
        j := j + 1;
    }
    arr[i], arr[high - 1] := arr[high - 1], arr[i];
    return i;
}
```

## Frame Conditions

### Reads Clauses

Specify what a function can read:

```dafny
class Counter {
    var value: int

    function getValue(): int
        reads this
    {
        value
    }

    function isPositive(): bool
        reads this
    {
        value > 0
    }
}
```

**Reading arrays:**
```dafny
function sum(arr: array<int>): int
    reads arr
{
    if arr.Length == 0 then 0
    else arr[0] + sum(arr[1..])
}
```

### Modifies Clauses

Specify what a method can modify:

```dafny
method increment(counter: Counter)
    modifies counter
    ensures counter.value == old(counter.value) + 1
{
    counter.value := counter.value + 1;
}
```

**Multiple objects:**
```dafny
method swap(a: Counter, b: Counter)
    modifies a, b
    ensures a.value == old(b.value)
    ensures b.value == old(a.value)
{
    var temp := a.value;
    a.value := b.value;
    b.value := temp;
}
```

**Array modification:**
```dafny
method fill(arr: array<int>, value: int)
    modifies arr
    ensures forall i :: 0 <= i < arr.Length ==> arr[i] == value
{
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant forall j :: 0 <= j < i ==> arr[j] == value
        modifies arr
    {
        arr[i] := value;
        i := i + 1;
    }
}
```

## Termination (decreases)

Specify termination measures for recursive functions:

**Simple recursion:**
```dafny
function factorial(n: nat): nat
    decreases n
{
    if n == 0 then 1 else n * factorial(n - 1)
}
```

**Multiple parameters:**
```dafny
function ackermann(m: nat, n: nat): nat
    decreases m, n
{
    if m == 0 then n + 1
    else if n == 0 then ackermann(m - 1, 1)
    else ackermann(m - 1, ackermann(m, n - 1))
}
```

**Loop termination:**
```dafny
method countdown(n: nat)
{
    var i := n;
    while i > 0
        invariant 0 <= i <= n
        decreases i
    {
        i := i - 1;
    }
}
```

## Helper Functions and Predicates

Define pure functions to express properties:

**Predicates:**
```dafny
predicate isSorted(arr: array<int>)
    reads arr
{
    forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
}

predicate contains(arr: array<int>, value: int)
    reads arr
{
    exists i :: 0 <= i < arr.Length && arr[i] == value
}
```

**Functions:**
```dafny
function arraySum(s: seq<int>): int
{
    if |s| == 0 then 0 else s[0] + arraySum(s[1..])
}

function count(s: seq<int>, value: int): nat
{
    if |s| == 0 then 0
    else (if s[0] == value then 1 else 0) + count(s[1..], value)
}
```

## Common Verification Patterns

### Permutation Preservation

Use multisets to express that elements are preserved:

```dafny
method sort(arr: array<int>)
    modifies arr
    ensures isSorted(arr)
    ensures multiset(arr[..]) == multiset(old(arr[..]))
{
    // implementation
}
```

### Partial Correctness

Specify what happens when preconditions are met:

```dafny
method safeDivide(a: int, b: int) returns (result: int)
    requires b != 0
    ensures result == a / b
{
    result := a / b;
}
```

### Total Correctness

Handle all cases including errors:

```dafny
method divide(a: int, b: int) returns (result: Option<int>)
    ensures b == 0 ==> result.None?
    ensures b != 0 ==> result.Some? && result.value == a / b
{
    if b == 0 {
        return None;
    } else {
        return Some(a / b);
    }
}
```

## Debugging Verification Failures

### Common Issues

**1. Weak invariants:**
```dafny
// Too weak - doesn't prove postcondition
while i < n
    invariant 0 <= i <= n  // Missing progress invariant
{
    sum := sum + arr[i];
    i := i + 1;
}
```

**2. Missing frame conditions:**
```dafny
// Missing reads clause
function getValue(counter: Counter): int
    // reads this  // MISSING!
{
    counter.value  // Error: insufficient reads clause
}
```

**3. Incomplete postconditions:**
```dafny
// Incomplete - doesn't specify other elements unchanged
method swap(arr: array<int>, i: nat, j: nat)
    requires i < arr.Length && j < arr.Length
    modifies arr
    ensures arr[i] == old(arr[j])
    ensures arr[j] == old(arr[i])
    // Missing: ensures forall k :: k != i && k != j ==> arr[k] == old(arr[k])
```

### Verification Strategies

**1. Start simple:** Verify basic properties first, then add complexity.

**2. Use assertions:** Add intermediate assertions to guide the verifier:
```dafny
method example(arr: array<int>)
{
    var x := arr[0];
    assert x == arr[0];  // Intermediate assertion
    var y := x + 1;
    assert y == arr[0] + 1;  // Helps verifier
}
```

**3. Split complex conditions:** Break down complex specifications into smaller pieces.

**4. Use lemmas:** Prove helper lemmas for complex properties:
```dafny
lemma distributivity(a: int, b: int, c: int)
    ensures a * (b + c) == a * b + a * c
{
    // Proof by Dafny's automatic reasoning
}
```
