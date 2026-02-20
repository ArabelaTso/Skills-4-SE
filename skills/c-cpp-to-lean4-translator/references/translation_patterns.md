# C/C++ to Lean4 Translation Patterns

This reference provides detailed patterns for translating common C/C++ constructs to Lean4.

## Table of Contents

1. [Basic Types](#basic-types)
2. [Variables and Constants](#variables-and-constants)
3. [Functions](#functions)
4. [Control Flow](#control-flow)
5. [Pointers and References](#pointers-and-references)
6. [Arrays](#arrays)
7. [Structs and Classes](#structs-and-classes)
8. [Memory Management](#memory-management)
9. [Standard Library Functions](#standard-library-functions)

## Basic Types

### Integer Types

**C/C++:**
```c
int x;
unsigned int y;
long z;
short w;
```

**Lean4:**
```lean
def x : Int := 0
def y : Nat := 0
def z : Int := 0
def w : Int := 0
```

**Notes:**
- Use `Int` for signed integers
- Use `Nat` for unsigned integers (natural numbers)
- Lean4's `Int` is arbitrary precision by default

### Floating Point Types

**C/C++:**
```c
float f;
double d;
```

**Lean4:**
```lean
def f : Float := 0.0
def d : Float := 0.0
```

**Notes:**
- Lean4's `Float` is IEEE 754 double precision
- For exact rational arithmetic, use `Rat`

### Boolean Type

**C/C++:**
```c
bool flag = true;
```

**Lean4:**
```lean
def flag : Bool := true
```

### Character and String Types

**C/C++:**
```c
char c = 'a';
const char* str = "hello";
std::string s = "world";
```

**Lean4:**
```lean
def c : Char := 'a'
def str : String := "hello"
def s : String := "world"
```

## Variables and Constants

### Variable Declaration

**C/C++:**
```c
int x = 10;
int y;
y = 20;
```

**Lean4:**
```lean
def x : Int := 10
def y : Int := 20
```

**Notes:**
- Lean4 requires initialization at declaration
- Use `let` for local variables in functions

### Constants

**C/C++:**
```c
const int MAX = 100;
#define PI 3.14159
```

**Lean4:**
```lean
def MAX : Int := 100
def PI : Float := 3.14159
```

## Functions

### Basic Function

**C/C++:**
```c
int add(int a, int b) {
    return a + b;
}
```

**Lean4:**
```lean
def add (a b : Int) : Int :=
  a + b
```

### Void Functions (Procedures)

**C/C++:**
```c
void printMessage(const char* msg) {
    printf("%s\n", msg);
}
```

**Lean4:**
```lean
def printMessage (msg : String) : IO Unit :=
  IO.println msg
```

**Notes:**
- Functions with side effects return `IO Unit`
- Pure functions don't need `IO`

### Function with Multiple Statements

**C/C++:**
```c
int calculate(int x, int y) {
    int sum = x + y;
    int product = x * y;
    return sum + product;
}
```

**Lean4:**
```lean
def calculate (x y : Int) : Int :=
  let sum := x + y
  let product := x * y
  sum + product
```

## Control Flow

### If-Else

**C/C++:**
```c
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

**Lean4:**
```lean
def max (a b : Int) : Int :=
  if a > b then a else b
```

### Nested If-Else

**C/C++:**
```c
int classify(int x) {
    if (x > 0) {
        return 1;
    } else if (x < 0) {
        return -1;
    } else {
        return 0;
    }
}
```

**Lean4:**
```lean
def classify (x : Int) : Int :=
  if x > 0 then 1
  else if x < 0 then -1
  else 0
```

### For Loop

**C/C++:**
```c
int sum_n(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i;
    }
    return sum;
}
```

**Lean4:**
```lean
def sumN (n : Nat) : Nat :=
  let rec loop (i acc : Nat) : Nat :=
    if i >= n then acc
    else loop (i + 1) (acc + i)
  loop 0 0
```

**Notes:**
- Lean4 uses recursion instead of imperative loops
- Use `let rec` for recursive helper functions

### While Loop

**C/C++:**
```c
int factorial(int n) {
    int result = 1;
    while (n > 1) {
        result *= n;
        n--;
    }
    return result;
}
```

**Lean4:**
```lean
def factorial (n : Nat) : Nat :=
  let rec loop (n acc : Nat) : Nat :=
    if n <= 1 then acc
    else loop (n - 1) (acc * n)
  loop n 1
```

### Switch/Case

**C/C++:**
```c
int getDays(int month) {
    switch(month) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            return 31;
        case 4: case 6: case 9: case 11:
            return 30;
        case 2:
            return 28;
        default:
            return 0;
    }
}
```

**Lean4:**
```lean
def getDays (month : Nat) : Nat :=
  match month with
  | 1 | 3 | 5 | 7 | 8 | 10 | 12 => 31
  | 4 | 6 | 9 | 11 => 30
  | 2 => 28
  | _ => 0
```

## Pointers and References

### Pointer Dereferencing

**C/C++:**
```c
int getValue(int* ptr) {
    return *ptr;
}
```

**Lean4:**
```lean
-- Lean4 doesn't have raw pointers
-- Use references or pass by value
def getValue (val : Int) : Int :=
  val
```

**Notes:**
- Lean4 is a functional language without raw pointers
- Use immutable references or pass values directly
- For mutable state, use `IO` monad or `ST` monad

### Reference Parameters

**C/C++:**
```c
void increment(int& x) {
    x++;
}
```

**Lean4:**
```lean
-- Return new value instead of mutation
def increment (x : Int) : Int :=
  x + 1

-- Or use IO for side effects
def incrementIO (ref : IO.Ref Int) : IO Unit := do
  let val ← ref.get
  ref.set (val + 1)
```

## Arrays

### Fixed-Size Arrays

**C/C++:**
```c
int arr[5] = {1, 2, 3, 4, 5};
int sum = 0;
for (int i = 0; i < 5; i++) {
    sum += arr[i];
}
```

**Lean4:**
```lean
def arr : Array Int := #[1, 2, 3, 4, 5]

def sumArray (arr : Array Int) : Int :=
  arr.foldl (· + ·) 0
```

### Dynamic Arrays (Vectors)

**C/C++:**
```cpp
std::vector<int> vec;
vec.push_back(1);
vec.push_back(2);
```

**Lean4:**
```lean
def vec : Array Int := #[]
def vec1 := vec.push 1
def vec2 := vec1.push 2
```

**Notes:**
- Arrays in Lean4 are immutable by default
- Operations return new arrays
- Use `Array` for dynamic arrays

## Structs and Classes

### Simple Struct

**C/C++:**
```c
struct Point {
    int x;
    int y;
};

Point p = {10, 20};
int sum = p.x + p.y;
```

**Lean4:**
```lean
structure Point where
  x : Int
  y : Int

def p : Point := { x := 10, y := 20 }
def sum := p.x + p.y
```

### Struct with Methods

**C/C++:**
```cpp
struct Rectangle {
    int width;
    int height;

    int area() {
        return width * height;
    }
};
```

**Lean4:**
```lean
structure Rectangle where
  width : Int
  height : Int

def Rectangle.area (r : Rectangle) : Int :=
  r.width * r.height
```

### Class with Constructor

**C/C++:**
```cpp
class Counter {
private:
    int count;
public:
    Counter() : count(0) {}
    void increment() { count++; }
    int getCount() { return count; }
};
```

**Lean4:**
```lean
structure Counter where
  count : Nat
  deriving Repr

def Counter.new : Counter :=
  { count := 0 }

def Counter.increment (c : Counter) : Counter :=
  { c with count := c.count + 1 }

def Counter.getCount (c : Counter) : Nat :=
  c.count
```

## Memory Management

### Dynamic Allocation

**C/C++:**
```c
int* ptr = (int*)malloc(sizeof(int));
*ptr = 42;
free(ptr);
```

**Lean4:**
```lean
-- Lean4 has automatic memory management
def value : Int := 42
-- No manual allocation/deallocation needed
```

**Notes:**
- Lean4 has automatic garbage collection
- No manual memory management required
- Memory safety is guaranteed by the type system

## Standard Library Functions

### String Operations

**C/C++:**
```c
strlen(str);
strcmp(s1, s2);
strcat(dest, src);
```

**Lean4:**
```lean
str.length
s1 == s2
dest ++ src
```

### Math Functions

**C/C++:**
```c
abs(x);
pow(x, y);
sqrt(x);
```

**Lean4:**
```lean
x.natAbs  -- for Int
x ^ y     -- power
-- For sqrt, use Float operations
```

### I/O Operations

**C/C++:**
```c
printf("Hello %d\n", x);
scanf("%d", &x);
```

**Lean4:**
```lean
IO.println s!"Hello {x}"

-- For input:
def readInt : IO Int := do
  let line ← IO.getStdIn >>= (·.getLine)
  match line.toInt? with
  | some n => pure n
  | none => pure 0
```
