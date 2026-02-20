# Type Mappings: C/C++ to Dafny

Comprehensive guide for mapping C/C++ types to Dafny equivalents.

## Primitive Types

### Integer Types

| C/C++ Type | Size | Dafny Type | Notes |
|-----------|------|-----------|-------|
| `char` | 1 byte | `int` or `char` | Use `char` for characters, `int` for numeric |
| `short` | 2 bytes | `int` | Dafny `int` is unbounded |
| `int` | 4 bytes | `int` | Unbounded in Dafny |
| `long` | 4/8 bytes | `int` | Platform-independent in Dafny |
| `long long` | 8 bytes | `int` | Unbounded in Dafny |
| `unsigned char` | 1 byte | `nat` | Natural numbers (≥ 0) |
| `unsigned short` | 2 bytes | `nat` | Natural numbers |
| `unsigned int` | 4 bytes | `nat` | Natural numbers |
| `unsigned long` | 4/8 bytes | `nat` | Natural numbers |
| `size_t` | Platform | `nat` | Always non-negative |

**Guidelines:**
- Use `int` for signed integers
- Use `nat` for unsigned integers and sizes
- Dafny integers are mathematical (unbounded)
- Add bounds checks if C code assumes specific sizes

### Floating Point

| C/C++ Type | Dafny Type | Notes |
|-----------|-----------|-------|
| `float` | `real` | Exact rationals in Dafny |
| `double` | `real` | No precision loss |
| `long double` | `real` | Exact arithmetic |

**Note:** Dafny's `real` represents exact rational numbers, not IEEE 754 floats.

### Boolean and Character

| C/C++ Type | Dafny Type | Notes |
|-----------|-----------|-------|
| `bool` | `bool` | Direct mapping |
| `char` | `char` | Single character |
| `wchar_t` | `char` | Unicode character |

### Void and Null

| C/C++ Type | Dafny Equivalent | Notes |
|-----------|-----------------|-------|
| `void` | `()` | Unit type for procedures |
| `NULL` | No direct equivalent | Use `Option` or ensure non-null |

## Pointer Types

### Raw Pointers

| C/C++ Type | Dafny Type | Usage Pattern |
|-----------|-----------|---------------|
| `T*` (single) | `T` (reference) | For single object reference |
| `T*` (array) | `array<T>` | For array access |
| `T*` (nullable) | Use bounds or `Option` | No null in Dafny |
| `T**` | `array<array<T>>` | 2D arrays |
| `void*` | Generic type parameter | Use `<T>` |

**Translation patterns:**
```c
// C: Single pointer
int* ptr = &x;
*ptr = 10;
```

```dafny
// Dafny: Direct reference (for class objects)
var obj := new MyClass();
obj.field := 10;
```

```c
// C: Array pointer
int* arr = malloc(n * sizeof(int));
arr[i] = value;
```

```dafny
// Dafny: Array
var arr := new int[n];
arr[i] := value;
```

### Smart Pointers (C++)

| C++ Type | Dafny Equivalent | Notes |
|---------|-----------------|-------|
| `unique_ptr<T>` | `T` (owned reference) | Automatic in Dafny |
| `shared_ptr<T>` | `T` (reference) | Garbage collected |
| `weak_ptr<T>` | Not needed | No manual memory management |

## Array Types

### Fixed-Size Arrays

```c
// C
int arr[10];
int matrix[5][5];
```

```dafny
// Dafny
var arr := new int[10];
var matrix := new int[5, 5];  // Multi-dimensional
```

### Dynamic Arrays

```c
// C
int* arr = (int*)malloc(n * sizeof(int));
```

```dafny
// Dafny
var arr := new int[n];
```

### Array of Pointers

```c
// C
int** arr = (int**)malloc(n * sizeof(int*));
for (int i = 0; i < n; i++) {
    arr[i] = (int*)malloc(m * sizeof(int));
}
```

```dafny
// Dafny
var arr := new array<int>[n];
var i := 0;
while i < n {
    arr[i] := new int[m];
    i := i + 1;
}
```

## Struct and Class Types

### C Structs

```c
struct Point {
    int x;
    int y;
};
```

**Dafny (mutable class):**
```dafny
class Point {
    var x: int
    var y: int

    constructor(x0: int, y0: int)
        ensures x == x0 && y == y0
    {
        x := x0;
        y := y0;
    }
}
```

**Dafny (immutable datatype):**
```dafny
datatype Point = Point(x: int, y: int)
```

### C++ Classes

```cpp
class Rectangle {
private:
    int width;
    int height;
public:
    Rectangle(int w, int h) : width(w), height(h) {}
    int area() { return width * height; }
};
```

**Dafny:**
```dafny
class Rectangle {
    var width: int
    var height: int

    constructor(w: int, h: int)
        ensures width == w && height == h
    {
        width := w;
        height := h;
    }

    function area(): int
        reads this
    {
        width * height
    }
}
```

## Enum Types

```c
// C
enum Color {
    RED,
    GREEN,
    BLUE
};
```

**Dafny:**
```dafny
datatype Color = Red | Green | Blue
```

## Union Types

```c
// C
union Data {
    int i;
    float f;
    char str[20];
};
```

**Dafny (tagged union):**
```dafny
datatype Data =
    | IntData(i: int)
    | FloatData(f: real)
    | StrData(str: seq<char>)
```

## Function Pointer Types

```c
// C
typedef int (*BinaryOp)(int, int);

int apply(BinaryOp op, int a, int b) {
    return op(a, b);
}
```

**Dafny:**
```dafny
type BinaryOp = (int, int) -> int

function apply(op: BinaryOp, a: int, b: int): int
{
    op(a, b)
}
```

## Container Types

### Sequences

```c
// C: Dynamic array/vector
int* vec;
int size;
int capacity;
```

**Dafny:**
```dafny
var vec: seq<int> := [];
// Sequences are immutable, use concatenation
vec := vec + [newElement];
```

### Sets

```c
// C: No built-in set
// Use hash table or sorted array
```

**Dafny:**
```dafny
var s: set<int> := {};
s := s + {element};
```

### Maps

```c
// C: No built-in map
// Use hash table
```

**Dafny:**
```dafny
var m: map<string, int> := map[];
m := m[key := value];
```

## Type Qualifiers

### Const

```c
// C
const int x = 10;
const int* ptr;  // Pointer to const
int* const ptr2; // Const pointer
```

**Dafny:**
```dafny
// Dafny: Use immutable bindings
const x: int := 10

// For functions, use reads clause
function getValue(arr: array<int>, i: nat): int
    requires i < arr.Length
    reads arr
{
    arr[i]
}
```

### Volatile

```c
// C
volatile int flag;
```

**Dafny:** No direct equivalent. Model as external state or I/O.

## Reference Types (C++)

```cpp
// C++
void increment(int& x) {
    x++;
}
```

**Dafny:**
```dafny
method increment(arr: array<int>, index: nat)
    requires index < arr.Length
    modifies arr
    ensures arr[index] == old(arr[index]) + 1
{
    arr[index] := arr[index] + 1;
}
```

## Template/Generic Types

```cpp
// C++
template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
```

**Dafny:**
```dafny
function max<T>(a: T, b: T, greater: (T, T) -> bool): T
{
    if greater(a, b) then a else b
}

// Or with type class (trait)
trait Comparable<T> {
    predicate lessThan(other: T)
}

function max<T(Comparable<T>)>(a: T, b: T): T
{
    if a.lessThan(b) then b else a
}
```

## Type Conversion

### Implicit Conversions

```c
// C: Implicit conversions
int i = 10;
float f = i;  // int to float
```

**Dafny:** Explicit conversions required
```dafny
var i: int := 10;
var r: real := i as real;
```

### Casts

```c
// C
int i = (int)3.14;
void* ptr = &i;
int* iptr = (int*)ptr;
```

**Dafny:** Type-safe, no arbitrary casts
```dafny
// Use appropriate types from the start
// Or use datatypes for variant types
```

## Special Types

### Size and Offset Types

| C/C++ Type | Dafny Type | Notes |
|-----------|-----------|-------|
| `size_t` | `nat` | Array sizes, lengths |
| `ptrdiff_t` | `int` | Pointer differences |
| `intptr_t` | Not needed | No pointer arithmetic |

### String Types

```c
// C
char* str = "Hello";
char str2[100];
```

**Dafny:**
```dafny
var str: string := "Hello";
var str2: seq<char> := [];
```
