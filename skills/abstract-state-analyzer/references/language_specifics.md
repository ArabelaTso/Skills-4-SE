# Language-Specific Analysis Considerations

## C/C++

### Memory Management

**Pointer Arithmetic**:
```c
int arr[10];
int *ptr = arr;
ptr += 5;  // ptr now points to arr[5]
*ptr = 0;  // Check: 5 < 10? ✓ Safe

ptr += 10;  // ptr now points beyond array
*ptr = 0;   // ✗ Out-of-bounds
```

**Analysis**: Track pointer offsets relative to base
```
ptr: (base: arr, offset: [5, 5])
ptr + 10: (base: arr, offset: [15, 15])
Check: offset < array_size? ✗ Error
```

**Dynamic Allocation**:
```c
int *arr = malloc(n * sizeof(int));
// arr: not-null (if malloc succeeds)
// size: n * sizeof(int)
arr[i] = 0;
// Check: i < n?
```

**Use-After-Free**:
```c
int *ptr = malloc(sizeof(int));
free(ptr);
// ptr: freed (dangling)
*ptr = 5;  // ✗ Use-after-free
```

**Analysis**: Track allocation status
```
States: {allocated, freed, null, ⊤}
After malloc: allocated
After free: freed
Dereference freed: ✗ Error
```

### Undefined Behavior

**Signed Integer Overflow**:
```c
int x = INT_MAX;
int y = x + 1;  // ✗ Undefined behavior
```

**Analysis**: Check signed arithmetic
```
x: [INT_MAX, INT_MAX]
x + 1: [INT_MAX + 1, INT_MAX + 1]
Check: result > INT_MAX? ✗ Undefined behavior
```

**Null Pointer Dereference**:
```c
int *ptr = NULL;
*ptr = 5;  // ✗ Undefined behavior
```

**Uninitialized Variables**:
```c
int x;
int y = x + 1;  // ✗ Undefined behavior
```

**Analysis**: Track initialization status
```
States: {initialized, uninitialized}
After declaration: uninitialized
After assignment: initialized
Use uninitialized: ✗ Error
```

### String Operations

**Buffer Overflow**:
```c
char buf[10];
strcpy(buf, user_input);  // ✗ Potential overflow
```

**Analysis**:
```
buf: size = 10
user_input: length = ⊤
Check: length(user_input) < 10? Unknown → ✗ Potential error
```

**Safe Alternative**:
```c
char buf[10];
strncpy(buf, user_input, sizeof(buf) - 1);
buf[sizeof(buf) - 1] = '\0';  // ✓ Safe
```

### Type Casting

**Narrowing Conversion**:
```c
long x = 1000000000000L;
int y = (int)x;  // ✗ Potential data loss
```

**Analysis**:
```
x: [1000000000000, 1000000000000]
y: truncated to int range
Check: x fits in int? ✗ No
```

## Python

### Dynamic Typing

**Type Tracking**:
```python
def process(x):
    # x: ⊤ (any type)
    if isinstance(x, int):
        # x: {int}
        return x + 1  # ✓ Safe
    elif isinstance(x, str):
        # x: {str}
        return x.upper()  # ✓ Safe
    else:
        # x: ⊤ \ {int, str}
        return x + 1  # ✗ Potential TypeError
```

**Duck Typing**:
```python
def process(obj):
    # obj: ⊤
    obj.method()  # ✗ Potential AttributeError
```

**Analysis**: Track available attributes
```
obj: {ClassA, ClassB}
Check: both have method()? If not → ✗ Error
```

### None Handling

**Implicit None Return**:
```python
def find(arr, target):
    for item in arr:
        if item == target:
            return item
    # Implicit: return None

result = find(arr, x)
# result: {type(arr[0]), NoneType}
print(result.value)  # ✗ Potential AttributeError if None
```

**None in Operations**:
```python
x = None
y = x + 1  # ✗ TypeError
```

### List Operations

**Index Out of Range**:
```python
arr = [1, 2, 3]
x = arr[5]  # ✗ IndexError
```

**Negative Indexing**:
```python
arr = [1, 2, 3]
x = arr[-1]  # ✓ Safe (arr[2])
y = arr[-10]  # ✗ IndexError
```

**Analysis**: Handle negative indices
```
index: [-10, -10]
Normalized: index + len(arr) = -10 + 3 = -7
Check: -7 ∈ [0, 2]? ✗ Error
```

### Dictionary Operations

**KeyError**:
```python
d = {'a': 1, 'b': 2}
x = d['c']  # ✗ KeyError
```

**Analysis**: Track known keys
```
d: keys = {'a', 'b'}
Access: 'c'
Check: 'c' ∈ keys? ✗ Error
```

**Safe Access**:
```python
x = d.get('c', default=0)  # ✓ Safe
```

## Java

### Null Pointer Exceptions

**Unchecked Dereference**:
```java
String s = getString();  // May return null
int len = s.length();  // ✗ Potential NullPointerException
```

**Analysis**:
```
s: ⊤ (maybe null)
s.length(): ✗ Potential NPE
```

**Safe with Check**:
```java
String s = getString();
if (s != null) {
    // s: not-null
    int len = s.length();  // ✓ Safe
}
```

### Array Bounds

**ArrayIndexOutOfBoundsException**:
```java
int[] arr = new int[10];
arr[15] = 0;  // ✗ ArrayIndexOutOfBoundsException
```

**Analysis**:
```
arr: length = 10
index: [15, 15]
Check: 15 < 10? ✗ Error
```

### Integer Overflow

**Silent Wraparound**:
```java
int x = Integer.MAX_VALUE;
int y = x + 1;  // Wraps to Integer.MIN_VALUE
```

**Analysis**:
```
x: [2147483647, 2147483647]
y: [-2147483648, -2147483648] (after wraparound)
```

### Type Casting

**ClassCastException**:
```java
Object obj = "hello";
Integer num = (Integer) obj;  // ✗ ClassCastException
```

**Analysis**:
```
obj: {String}
Cast to: Integer
Check: String ⊆ Integer? ✗ Error
```

**Safe with instanceof**:
```java
if (obj instanceof Integer) {
    // obj: {Integer}
    Integer num = (Integer) obj;  // ✓ Safe
}
```

## JavaScript

### Undefined and Null

**Two Null-like Values**:
```javascript
let x;  // x: undefined
let y = null;  // y: null

x.field;  // ✗ TypeError
y.field;  // ✗ TypeError
```

**Analysis**: Track both undefined and null
```
States: {undefined, null, defined, ⊤}
```

**Nullish Coalescing**:
```javascript
let x = value ?? default;
// If value is null or undefined: x = default
// Otherwise: x = value
```

### Type Coercion

**Implicit Conversions**:
```javascript
let x = "5" + 3;  // x: "53" (string concatenation)
let y = "5" - 3;  // y: 2 (numeric subtraction)
let z = "5" * 3;  // z: 15 (numeric multiplication)
```

**Analysis**: Track type coercion rules
```
string + number → string
string - number → number (if string is numeric)
```

**Truthy/Falsy**:
```javascript
if (x) {
    // x is truthy (not: false, 0, "", null, undefined, NaN)
}
```

### Array Bounds

**No Exception on Out-of-Bounds**:
```javascript
let arr = [1, 2, 3];
let x = arr[10];  // x: undefined (no error)
```

**Analysis**: Different from other languages
```
arr[10]: returns undefined (not an error)
```

### Property Access

**Undefined Properties**:
```javascript
let obj = {a: 1};
let x = obj.b;  // x: undefined (no error)
let y = obj.b.c;  // ✗ TypeError (undefined.c)
```

**Analysis**:
```
obj.b: undefined
obj.b.c: ✗ Error (accessing property of undefined)
```

**Optional Chaining**:
```javascript
let y = obj.b?.c;  // y: undefined (safe)
```

## Rust

### Ownership and Borrowing

**Move Semantics**:
```rust
let s1 = String::from("hello");
let s2 = s1;  // s1 moved to s2
println!("{}", s1);  // ✗ Compile error (use after move)
```

**Analysis**: Track ownership
```
After move: s1 = moved (invalid)
Use of moved value: ✗ Error
```

**Borrowing**:
```rust
let s1 = String::from("hello");
let s2 = &s1;  // Borrow
println!("{}", s1);  // ✓ Safe (s1 still valid)
```

### Option and Result Types

**Explicit Null Handling**:
```rust
fn find(arr: &[i32], target: i32) -> Option<i32> {
    for &item in arr {
        if item == target {
            return Some(item);
        }
    }
    None
}

let result = find(&arr, x);
// result: Option<i32>
let value = result.unwrap();  // ✗ Panics if None
```

**Safe Handling**:
```rust
if let Some(value) = result {
    // value: i32 (not Option)
    println!("{}", value);  // ✓ Safe
}
```

### Array Bounds

**Checked at Runtime**:
```rust
let arr = [1, 2, 3];
let x = arr[5];  // ✗ Panics at runtime
```

**Safe Access**:
```rust
let x = arr.get(5);  // x: Option<&i32> = None
```

## Go

### Nil Pointers

**Nil Dereference**:
```go
var ptr *int
*ptr = 5  // ✗ Panic (nil pointer dereference)
```

**Analysis**:
```
ptr: nil
*ptr: ✗ Error
```

### Slice Bounds

**Out-of-Bounds Panic**:
```go
arr := []int{1, 2, 3}
x := arr[5]  // ✗ Panic
```

**Slice Operations**:
```go
arr := []int{1, 2, 3}
slice := arr[1:10]  // ✗ Panic (10 > len(arr))
```

### Interface Nil

**Nil Interface**:
```go
var i interface{}
// i: nil
i.Method()  // ✗ Panic
```

**Non-nil Interface with Nil Value**:
```go
var ptr *int
var i interface{} = ptr
// i: not nil (contains type info)
// i's value: nil
```

## Analysis Strategy Summary

**C/C++**: Focus on memory safety, pointer arithmetic, undefined behavior
**Python**: Track types dynamically, handle None, check attribute existence
**Java**: Null checks, array bounds, type casting
**JavaScript**: Handle undefined and null, type coercion, property access
**Rust**: Ownership tracking, Option/Result types (compile-time checked)
**Go**: Nil pointers, slice bounds, interface nil
