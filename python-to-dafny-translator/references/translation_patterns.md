# Python to Dafny Translation Patterns

This reference provides detailed patterns for translating common Python constructs to Dafny.

## Table of Contents

1. [Basic Types](#basic-types)
2. [Variables and Constants](#variables-and-constants)
3. [Functions and Methods](#functions-and-methods)
4. [Control Flow](#control-flow)
5. [Collections](#collections)
6. [Classes and Objects](#classes-and-objects)
7. [Error Handling](#error-handling)
8. [Specifications and Verification](#specifications-and-verification)

## Basic Types

### Integer Types

**Python:**
```python
x = 42
y = -10
```

**Dafny:**
```dafny
var x: int := 42;
var y: int := -10;
```

**Notes:**
- Dafny's `int` is arbitrary precision (like Python)
- Use `nat` for non-negative integers

### Boolean Type

**Python:**
```python
flag = True
result = False
```

**Dafny:**
```dafny
var flag: bool := true;
var result: bool := false;
```

**Notes:**
- Python uses `True`/`False`, Dafny uses `true`/`false`

### String Type

**Python:**
```python
s = "hello"
name = 'world'
```

**Dafny:**
```dafny
var s: string := "hello";
var name: string := "world";
```

### None/Null

**Python:**
```python
x = None
```

**Dafny:**
```dafny
// Use Option type for nullable values
datatype Option<T> = None | Some(value: T)

var x: Option<int> := None;
```

## Variables and Constants

### Variable Declaration

**Python:**
```python
x = 10
y = 20
x = x + y
```

**Dafny:**
```dafny
var x: int := 10;
var y: int := 20;
x := x + y;
```

**Notes:**
- Dafny requires explicit type annotations (can be inferred in some cases)
- Use `:=` for assignment in Dafny

### Constants

**Python:**
```python
MAX_SIZE = 100
PI = 3.14159
```

**Dafny:**
```dafny
const MAX_SIZE: int := 100
const PI: real := 3.14159
```

## Functions and Methods

### Pure Function

**Python:**
```python
def add(a, b):
    return a + b
```

**Dafny:**
```dafny
function add(a: int, b: int): int
{
    a + b
}
```

**Notes:**
- Dafny `function` is pure (no side effects)
- Functions are used in specifications

### Method (with side effects)

**Python:**
```python
def print_sum(a, b):
    print(a + b)
```

**Dafny:**
```dafny
method printSum(a: int, b: int)
{
    print a + b;
}
```

**Notes:**
- Dafny `method` can have side effects
- Methods are used for executable code

### Function with Multiple Returns

**Python:**
```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder
```

**Dafny:**
```dafny
method divide(a: int, b: int) returns (quotient: int, remainder: int)
    requires b != 0
{
    quotient := a / b;
    remainder := a % b;
}
```

## Control Flow

### If-Else

**Python:**
```python
def max_value(a, b):
    if a > b:
        return a
    else:
        return b
```

**Dafny:**
```dafny
function max(a: int, b: int): int
{
    if a > b then a else b
}
```

### If-Elif-Else

**Python:**
```python
def classify(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
```

**Dafny:**
```dafny
function classify(x: int): string
{
    if x > 0 then "positive"
    else if x < 0 then "negative"
    else "zero"
}
```

### For Loop (Range)

**Python:**
```python
def sum_n(n):
    total = 0
    for i in range(n):
        total += i
    return total
```

**Dafny:**
```dafny
method sumN(n: nat) returns (total: int)
{
    total := 0;
    var i := 0;
    while i < n
        invariant 0 <= i <= n
        invariant total == i * (i - 1) / 2
    {
        total := total + i;
        i := i + 1;
    }
}
```

**Notes:**
- Dafny uses `while` loops instead of `for`
- Loop invariants are required for verification

### While Loop

**Python:**
```python
def factorial(n):
    result = 1
    while n > 1:
        result *= n
        n -= 1
    return result
```

**Dafny:**
```dafny
method factorial(n: nat) returns (result: nat)
    ensures result >= 1
{
    result := 1;
    var i := n;
    while i > 1
        invariant result >= 1
    {
        result := result * i;
        i := i - 1;
    }
}
```

## Collections

### Lists

**Python:**
```python
lst = [1, 2, 3, 4, 5]
first = lst[0]
length = len(lst)
```

**Dafny:**
```dafny
var lst: seq<int> := [1, 2, 3, 4, 5];
var first: int := lst[0];
var length: int := |lst|;
```

**Notes:**
- Dafny uses `seq<T>` for sequences (immutable lists)
- Use `|s|` for length
- Indexing is 0-based like Python

### List Operations

**Python:**
```python
# Append
lst.append(6)

# Concatenation
combined = lst1 + lst2

# Slicing
sub = lst[1:4]
```

**Dafny:**
```dafny
// Append (creates new sequence)
var newLst := lst + [6];

// Concatenation
var combined := lst1 + lst2;

// Slicing
var sub := lst[1..4];
```

### List Comprehension

**Python:**
```python
squares = [x * x for x in range(10)]
evens = [x for x in lst if x % 2 == 0]
```

**Dafny:**
```dafny
// Use sequence comprehension
var squares := seq(10, i => i * i);

// Filtering requires a method
method filterEvens(lst: seq<int>) returns (result: seq<int>)
{
    result := [];
    var i := 0;
    while i < |lst|
    {
        if lst[i] % 2 == 0 {
            result := result + [lst[i]];
        }
        i := i + 1;
    }
}
```

### Sets

**Python:**
```python
s = {1, 2, 3}
s.add(4)
has_two = 2 in s
```

**Dafny:**
```dafny
var s: set<int> := {1, 2, 3};
s := s + {4};
var hasTwo: bool := 2 in s;
```

### Dictionaries/Maps

**Python:**
```python
d = {"a": 1, "b": 2}
value = d["a"]
d["c"] = 3
```

**Dafny:**
```dafny
var d: map<string, int> := map["a" := 1, "b" := 2];
var value: int := d["a"];
d := d["c" := 3];
```

## Classes and Objects

### Simple Class

**Python:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

**Dafny:**
```dafny
class Point {
    var x: int
    var y: int

    constructor(x: int, y: int)
        ensures this.x == x && this.y == y
    {
        this.x := x;
        this.y := y;
    }

    method distanceFromOrigin() returns (dist: real)
    {
        dist := Sqrt(x * x + y * y);
    }
}
```

### Class with Invariants

**Python:**
```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count
```

**Dafny:**
```dafny
class Counter {
    var count: nat

    constructor()
        ensures count == 0
    {
        count := 0;
    }

    method increment()
        modifies this
        ensures count == old(count) + 1
    {
        count := count + 1;
    }

    function getCount(): nat
        reads this
    {
        count
    }
}
```

**Notes:**
- `modifies` clause specifies what can be modified
- `ensures` specifies postconditions
- `reads` clause for functions that read object state

## Error Handling

### Exceptions to Preconditions

**Python:**
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

**Dafny:**
```dafny
method divide(a: int, b: int) returns (result: int)
    requires b != 0  // Precondition prevents error
{
    result := a / b;
}
```

**Notes:**
- Dafny uses preconditions instead of exceptions
- Caller must ensure preconditions are met

### Optional Return Values

**Python:**
```python
def find_index(lst, value):
    try:
        return lst.index(value)
    except ValueError:
        return None
```

**Dafny:**
```dafny
method findIndex(lst: seq<int>, value: int) returns (result: Option<int>)
{
    var i := 0;
    while i < |lst|
    {
        if lst[i] == value {
            return Some(i);
        }
        i := i + 1;
    }
    return None;
}
```

## Specifications and Verification

### Function Specifications

**Python:**
```python
def abs_value(x):
    """Returns the absolute value of x"""
    if x < 0:
        return -x
    else:
        return x
```

**Dafny:**
```dafny
function abs(x: int): int
    ensures abs(x) >= 0
    ensures x >= 0 ==> abs(x) == x
    ensures x < 0 ==> abs(x) == -x
{
    if x < 0 then -x else x
}
```

### Method Specifications

**Python:**
```python
def swap(arr, i, j):
    """Swaps elements at indices i and j"""
    arr[i], arr[j] = arr[j], arr[i]
```

**Dafny:**
```dafny
method swap(arr: array<int>, i: nat, j: nat)
    requires arr.Length > 0
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

### Loop Invariants

**Python:**
```python
def array_sum(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total
```

**Dafny:**
```dafny
method arraySum(arr: array<int>) returns (total: int)
    requires arr.Length >= 0
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

// Helper function for specification
function sum(s: seq<int>): int
{
    if |s| == 0 then 0
    else s[0] + sum(s[1..])
}
```

### Assertions

**Python:**
```python
def process(x):
    assert x > 0, "x must be positive"
    result = x * 2
    assert result > x, "result should be greater than x"
    return result
```

**Dafny:**
```dafny
method process(x: int) returns (result: int)
    requires x > 0
    ensures result > x
{
    result := x * 2;
    assert result > x;  // Verified by Dafny
}
```

## Common Patterns

### Recursive Functions

**Python:**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Dafny:**
```dafny
function fib(n: nat): nat
{
    if n <= 1 then n
    else fib(n-1) + fib(n-2)
}
```

### Binary Search

**Python:**
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

**Dafny:**
```dafny
method binarySearch(arr: array<int>, target: int) returns (index: int)
    requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]  // sorted
    ensures 0 <= index < arr.Length ==> arr[index] == target
    ensures index == -1 ==> forall k :: 0 <= k < arr.Length ==> arr[k] != target
{
    var left := 0;
    var right := arr.Length - 1;

    while left <= right
        invariant 0 <= left <= arr.Length
        invariant -1 <= right < arr.Length
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
