# Memory Patterns: C/C++ to Dafny

Handling memory management, pointers, and ownership when translating to Dafny.

## Pointer Usage Patterns

### Single Object Reference

**C/C++:**
```c
void increment(int* x) {
    (*x)++;
}

int main() {
    int value = 5;
    increment(&value);
    return value;  // 6
}
```

**Dafny:**
```dafny
method increment(x: array<int>, index: nat)
    requires index < x.Length
    modifies x
    ensures x[index] == old(x[index]) + 1
{
    x[index] := x[index] + 1;
}

method Main() {
    var arr := new int[1];
    arr[0] := 5;
    increment(arr, 0);
    assert arr[0] == 6;
}
```

### Array Access

**C/C++:**
```c
int sum(int* arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}
```

**Dafny:**
```dafny
method sum(arr: array<int>) returns (total: int)
    ensures total == arraySum(arr[..])
{
    total := 0;
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant total == arraySum(arr[..i])
    {
        total := total + arr[i];
        i := i + 1;
    }
}

function arraySum(s: seq<int>): int
{
    if |s| == 0 then 0 else s[0] + arraySum(s[1..])
}
```

## Dynamic Memory Allocation

### Malloc/Free Pattern

**C:**
```c
int* create_array(int n) {
    int* arr = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        arr[i] = 0;
    }
    return arr;
}

void process() {
    int* data = create_array(10);
    // ... use data ...
    free(data);
}
```

**Dafny:**
```dafny
method createArray(n: nat) returns (arr: array<int>)
    ensures arr.Length == n
    ensures forall i :: 0 <= i < arr.Length ==> arr[i] == 0
{
    arr := new int[n];
    var i := 0;
    while i < n
        invariant 0 <= i <= n
        invariant arr.Length == n
        invariant forall j :: 0 <= j < i ==> arr[j] == 0
    {
        arr[i] := 0;
        i := i + 1;
    }
}

method process()
{
    var data := createArray(10);
    // ... use data ...
    // No explicit free needed
}
```

### Dynamic Resizing

**C:**
```c
typedef struct {
    int* data;
    int size;
    int capacity;
} Vector;

void vector_push(Vector* vec, int value) {
    if (vec->size >= vec->capacity) {
        vec->capacity *= 2;
        vec->data = (int*)realloc(vec->data, vec->capacity * sizeof(int));
    }
    vec->data[vec->size++] = value;
}
```

**Dafny (using sequences):**
```dafny
class Vector {
    var data: seq<int>

    constructor()
        ensures data == []
    {
        data := [];
    }

    method push(value: int)
        modifies this
        ensures data == old(data) + [value]
    {
        data := data + [value];
    }
}
```

## Pointer Arithmetic

### Array Traversal

**C:**
```c
void fill_array(int* arr, int n, int value) {
    int* ptr = arr;
    int* end = arr + n;
    while (ptr < end) {
        *ptr = value;
        ptr++;
    }
}
```

**Dafny:**
```dafny
method fillArray(arr: array<int>, value: int)
    modifies arr
    ensures forall i :: 0 <= i < arr.Length ==> arr[i] == value
{
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant forall j :: 0 <= j < i ==> arr[j] == value
    {
        arr[i] := value;
        i := i + 1;
    }
}
```

### Pointer Offset

**C:**
```c
int get_element(int* base, int offset) {
    return *(base + offset);
}
```

**Dafny:**
```dafny
method getElement(arr: array<int>, offset: nat) returns (value: int)
    requires offset < arr.Length
    ensures value == arr[offset]
{
    value := arr[offset];
}
```

## Multi-Level Pointers

### 2D Arrays

**C:**
```c
int** create_matrix(int rows, int cols) {
    int** matrix = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
    }
    return matrix;
}
```

**Dafny:**
```dafny
method createMatrix(rows: nat, cols: nat) returns (matrix: array<array<int>>)
    ensures matrix.Length == rows
    ensures forall i :: 0 <= i < matrix.Length ==> matrix[i].Length == cols
{
    matrix := new array<int>[rows];
    var i := 0;
    while i < rows
        invariant 0 <= i <= rows
        invariant matrix.Length == rows
        invariant forall j :: 0 <= j < i ==> matrix[j].Length == cols
    {
        matrix[i] := new int[cols];
        i := i + 1;
    }
}
```

**Alternative (multi-dimensional array):**
```dafny
method createMatrix2D(rows: nat, cols: nat) returns (matrix: array2<int>)
    ensures matrix.Length0 == rows
    ensures matrix.Length1 == cols
{
    matrix := new int[rows, cols];
}
```

## Ownership and Aliasing

### Unique Ownership

**C++ (unique_ptr):**
```cpp
std::unique_ptr<int> create() {
    return std::make_unique<int>(42);
}

void process() {
    auto ptr = create();
    // ptr owns the memory
}  // automatically freed
```

**Dafny:**
```dafny
class IntBox {
    var value: int

    constructor(v: int)
        ensures value == v
    {
        value := v;
    }
}

method create() returns (box: IntBox)
    ensures box.value == 42
{
    box := new IntBox(42);
}

method process()
{
    var box := create();
    // box owns the object
}  // automatically garbage collected
```

### Shared References

**C++ (shared_ptr):**
```cpp
std::shared_ptr<Data> data = std::make_shared<Data>();
std::shared_ptr<Data> alias = data;  // Both point to same object
```

**Dafny:**
```dafny
class Data {
    var value: int
}

method example()
{
    var data := new Data;
    var alias := data;  // Both refer to same object
    data.value := 10;
    assert alias.value == 10;  // Same object
}
```

## Memory Safety Patterns

### Bounds Checking

**C (unsafe):**
```c
int get(int* arr, int index) {
    return arr[index];  // No bounds check
}
```

**Dafny (safe):**
```dafny
method get(arr: array<int>, index: nat) returns (value: int)
    requires index < arr.Length  // Explicit bounds check
    ensures value == arr[index]
{
    value := arr[index];
}
```

### Null Pointer Handling

**C:**
```c
int* find(int* arr, int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) {
            return &arr[i];
        }
    }
    return NULL;
}
```

**Dafny (return index instead):**
```dafny
method find(arr: array<int>, target: int) returns (index: int)
    ensures index == -1 || (0 <= index < arr.Length && arr[index] == target)
{
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
    {
        if arr[i] == target {
            return i;
        }
        i := i + 1;
    }
    return -1;
}
```

**Dafny (using Option):**
```dafny
method findOption(arr: array<int>, target: int) returns (result: Option<nat>)
    ensures result.Some? ==> result.value < arr.Length && arr[result.value] == target
{
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
    {
        if arr[i] == target {
            return Some(i);
        }
        i := i + 1;
    }
    return None;
}
```

## Buffer Management

### Fixed-Size Buffers

**C:**
```c
void copy_string(char* dest, const char* src, int max_len) {
    int i = 0;
    while (i < max_len - 1 && src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}
```

**Dafny:**
```dafny
method copyString(dest: array<char>, src: seq<char>, maxLen: nat)
    requires maxLen <= dest.Length
    modifies dest
    ensures forall i :: 0 <= i < min(|src|, maxLen - 1) ==> dest[i] == src[i]
{
    var i := 0;
    while i < maxLen - 1 && i < |src|
        invariant 0 <= i <= maxLen - 1
        invariant i <= |src|
        invariant forall j :: 0 <= j < i ==> dest[j] == src[j]
    {
        dest[i] := src[i];
        i := i + 1;
    }
    if i < dest.Length {
        dest[i] := '\0';
    }
}

function min(a: nat, b: nat): nat
{
    if a < b then a else b
}
```

## Common Patterns Summary

| C/C++ Pattern | Dafny Equivalent | Notes |
|--------------|------------------|-------|
| `int* ptr` (single) | `array<int>` with index | Use index 0 for single value |
| `int* arr` (array) | `array<int>` | Direct mapping |
| `int** matrix` | `array<array<int>>` or `array2<int>` | Choose based on usage |
| `malloc/new` | `new T[n]` or `new T` | Automatic memory management |
| `free/delete` | Not needed | Garbage collected |
| `NULL` | Return index -1 or `Option` | No null references |
| Pointer arithmetic | Array indexing | Use indices instead |
| `&variable` | Wrap in array | Single element array |
