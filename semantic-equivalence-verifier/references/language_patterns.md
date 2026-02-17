# Language-Specific Equivalence Patterns

## Overview

Different programming languages have unique semantics, idioms, and equivalence considerations. This guide provides language-specific patterns for equivalence checking.

## Python

### Dynamic Typing Considerations

**Duck Typing:**
```python
# Artifact A
def process(items):
    return [x * 2 for x in items]

# Artifact B
def process(items):
    result = []
    for x in items:
        result.append(x + x)
    return result
```

Equivalent for numeric types, but behavior differs for strings:
- `[2] * 2` → `[4]`
- `"2" + "2"` → `"22"`

**Type checking strategy:**
- Test with multiple types (int, float, str, list, custom objects)
- Consider `__add__`, `__mul__` operator overloading
- Check for AttributeError on method calls

### Mutability and Side Effects

```python
# Artifact A
def append_item(lst, item):
    lst.append(item)
    return lst

# Artifact B
def append_item(lst, item):
    return lst + [item]
```

Not equivalent:
- A modifies input list (side effect)
- B creates new list (no side effect)

**Check for:**
- In-place modifications vs. new object creation
- Shared reference mutations
- Global variable modifications

### Iterator vs. List

```python
# Artifact A
def get_squares(n):
    return [i*i for i in range(n)]

# Artifact B
def get_squares(n):
    return (i*i for i in range(n))
```

Not strictly equivalent:
- A returns list (can iterate multiple times)
- B returns generator (single-use iterator)

### Exception Handling

```python
# Artifact A
def divide(a, b):
    if b == 0:
        return None
    return a / b

# Artifact B
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

Equivalent for integer division, but:
- A prevents exception
- B catches exception (different performance)

## Java

### Object Equality vs. Reference Equality

```java
// Artifact A
boolean areEqual(String a, String b) {
    return a == b;
}

// Artifact B
boolean areEqual(String a, String b) {
    return a.equals(b);
}
```

Not equivalent:
- A checks reference equality
- B checks value equality

**Check for:**
- `==` vs. `.equals()`
- `hashCode()` consistency
- Null handling

### Checked Exceptions

```java
// Artifact A
int readFile(String path) throws IOException {
    return Files.readAllBytes(Paths.get(path)).length;
}

// Artifact B
int readFile(String path) {
    try {
        return Files.readAllBytes(Paths.get(path)).length;
    } catch (IOException e) {
        return -1;
    }
}
```

Not equivalent:
- A propagates exception (caller must handle)
- B swallows exception (returns error code)

### Autoboxing and Unboxing

```java
// Artifact A
Integer sum(Integer a, Integer b) {
    return a + b;
}

// Artifact B
Integer sum(Integer a, Integer b) {
    return Integer.valueOf(a.intValue() + b.intValue());
}
```

Equivalent, but watch for:
- NullPointerException when unboxing null
- Integer cache (-128 to 127)

### Concurrency

```java
// Artifact A
class Counter {
    private int count = 0;
    void increment() { count++; }
    int get() { return count; }
}

// Artifact B
class Counter {
    private int count = 0;
    synchronized void increment() { count++; }
    synchronized int get() { return count; }
}
```

Not equivalent in concurrent contexts:
- A has race conditions
- B is thread-safe

## C/C++

### Undefined Behavior

```c
// Artifact A
int sum_array(int* arr, int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

// Artifact B
int sum_array(int* arr, int n) {
    int sum = 0;
    for (int i = 0; i <= n; i++) {  // Bug: <= instead of <
        sum += arr[i];
    }
    return sum;
}
```

B has undefined behavior (buffer overflow).

**Check for:**
- Buffer overflows
- Null pointer dereferences
- Integer overflow
- Use-after-free
- Uninitialized variables

### Memory Management

```cpp
// Artifact A
char* create_string() {
    char* str = new char[10];
    strcpy(str, "hello");
    return str;
}

// Artifact B
char* create_string() {
    char str[10];
    strcpy(str, "hello");
    return str;  // Bug: returning stack memory
}
```

Not equivalent:
- A allocates on heap (valid)
- B returns dangling pointer (undefined behavior)

### Pointer Arithmetic

```c
// Artifact A
int get_third(int* arr) {
    return arr[2];
}

// Artifact B
int get_third(int* arr) {
    return *(arr + 2);
}
```

Equivalent, but verify:
- Array bounds
- Pointer validity
- Alignment requirements

## JavaScript

### Type Coercion

```javascript
// Artifact A
function isEqual(a, b) {
    return a == b;
}

// Artifact B
function isEqual(a, b) {
    return a === b;
}
```

Not equivalent:
- `==` performs type coercion (`"5" == 5` → true)
- `===` checks strict equality (`"5" === 5` → false)

### Asynchronous Behavior

```javascript
// Artifact A
function fetchData(url) {
    return fetch(url).then(r => r.json());
}

// Artifact B
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}
```

Semantically equivalent, but:
- Different syntax (Promise vs. async/await)
- Error handling differs slightly

### Closure and Scope

```javascript
// Artifact A
function createCounters() {
    var counters = [];
    for (var i = 0; i < 3; i++) {
        counters.push(function() { return i; });
    }
    return counters;
}

// Artifact B
function createCounters() {
    var counters = [];
    for (let i = 0; i < 3; i++) {
        counters.push(function() { return i; });
    }
    return counters;
}
```

Not equivalent:
- A: all functions return 3 (var has function scope)
- B: functions return 0, 1, 2 (let has block scope)

## Rust

### Ownership and Borrowing

```rust
// Artifact A
fn process(s: String) -> String {
    s.to_uppercase()
}

// Artifact B
fn process(s: &String) -> String {
    s.to_uppercase()
}
```

Not equivalent:
- A takes ownership (caller loses access)
- B borrows (caller retains access)

### Lifetime Annotations

```rust
// Artifact A
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}

// Artifact B
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

B is correct (explicit lifetimes), A won't compile without lifetime elision.

### Error Handling

```rust
// Artifact A
fn divide(a: i32, b: i32) -> Option<i32> {
    if b == 0 { None } else { Some(a / b) }
}

// Artifact B
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}
```

Not equivalent:
- A uses Option (no error info)
- B uses Result (includes error message)

## Functional Languages (Haskell, OCaml)

### Lazy vs. Strict Evaluation

```haskell
-- Artifact A (lazy)
sumSquares n = sum [x*x | x <- [1..n]]

-- Artifact B (strict)
sumSquares n = foldl' (\acc x -> acc + x*x) 0 [1..n]
```

Semantically equivalent, but:
- A may build large thunks (space leak)
- B evaluates strictly (constant space)

### Referential Transparency

In pure functional languages, equivalence is simpler:
- No side effects to consider
- Can use equational reasoning
- Substitution preserves semantics

```haskell
-- These are equivalent by definition
f x = x + x
g x = 2 * x
```

## SQL

### Query Equivalence

```sql
-- Artifact A
SELECT * FROM users WHERE age > 18 AND country = 'US';

-- Artifact B
SELECT * FROM users WHERE country = 'US' AND age > 18;
```

Logically equivalent, but:
- Different execution plans possible
- Performance may differ based on indexes

### NULL Handling

```sql
-- Artifact A
SELECT * FROM users WHERE email = NULL;

-- Artifact B
SELECT * FROM users WHERE email IS NULL;
```

Not equivalent:
- A always returns empty (NULL = NULL is NULL, not TRUE)
- B correctly checks for NULL

## Cross-Language Considerations

### Numeric Precision

```python
# Python
0.1 + 0.2 == 0.3  # False (floating point error)

# Java
0.1 + 0.2 == 0.3  // False

# Use BigDecimal for exact arithmetic
```

### String Encoding

Different languages handle Unicode differently:
- Python 3: strings are Unicode by default
- C: strings are byte arrays
- Java: strings are UTF-16

### Integer Overflow

```python
# Python: arbitrary precision
x = 10**100  # Works fine

# Java: fixed precision
int x = Integer.MAX_VALUE + 1;  // Overflow to MIN_VALUE

# C: undefined behavior
int x = INT_MAX + 1;  // Undefined
```

## Equivalence Checking Strategy by Language

**Python:**
1. Test with multiple types
2. Check for side effects on mutable objects
3. Verify iterator vs. list semantics
4. Test exception handling

**Java:**
1. Check object vs. reference equality
2. Verify exception handling (checked vs. unchecked)
3. Test thread safety for concurrent code
4. Check autoboxing edge cases

**C/C++:**
1. Verify no undefined behavior
2. Check memory management (leaks, dangling pointers)
3. Test pointer arithmetic bounds
4. Verify integer overflow handling

**JavaScript:**
1. Test type coercion (== vs. ===)
2. Verify async behavior
3. Check closure and scope
4. Test this binding

**Rust:**
1. Verify ownership semantics
2. Check lifetime correctness
3. Test error handling (Option vs. Result)
4. Verify borrowing rules

**Functional:**
1. Use equational reasoning
2. Check strictness vs. laziness
3. Verify purity (no side effects)
4. Test recursion termination
