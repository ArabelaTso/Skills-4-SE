# Type Mappings: Python to Lean4

Comprehensive guide for mapping Python types to Lean4 equivalents.

## Primitive Types

### Integers

**Python `int`:**
- Unbounded integers in Python
- Map to `Int` (signed) or `Nat` (natural numbers ≥ 0) in Lean4

**Guidelines:**
- Use `Nat` when values are always non-negative (indices, counts, sizes)
- Use `Int` when values can be negative
- Convert between them: `Int.natAbs`, `Int.ofNat`

### Floating Point

**Python `float`:**
- 64-bit floating point
- Maps to `Float` in Lean4

**Note:** Lean4's `Float` is also 64-bit IEEE 754

### Booleans

**Python `bool`:**
- Direct mapping to `Bool` in Lean4
- Values: `True`/`False` → `true`/`false`

### Strings

**Python `str`:**
- Direct mapping to `String` in Lean4
- String interpolation: `f"Hello {name}"` → `s!"Hello {name}"`

## Container Types

### Lists

**Python `list[T]`:**
- Maps to `List α` in Lean4
- Homogeneous (all elements same type)

**Operations:**
```lean
-- Creation
let xs := [1, 2, 3]
let ys := List.range 10

-- Access
xs.head?  -- Option α
xs.get? 0  -- Option α

-- Modification (returns new list)
xs.append ys
xs.map (· + 1)
xs.filter (· > 0)
```

### Tuples

**Python `tuple`:**
- Fixed-size tuples map to product types

**Examples:**
```python
# Python
pair: tuple[int, str] = (1, "hello")
triple: tuple[int, int, int] = (1, 2, 3)
```

```lean
-- Lean4
let pair : Int × String := (1, "hello")
let triple : Int × Int × Int := (1, 2, 3)

-- Or use structures for named fields
structure Pair where
  first : Int
  second : String
```

### Dictionaries

**Python `dict[K, V]`:**
- Maps to `Std.HashMap K V` (requires import)
- Or `List (K × V)` for simple cases

**Example:**
```lean
import Std.Data.HashMap

def ages : Std.HashMap String Nat :=
  Std.HashMap.empty
    |>.insert "Alice" 30
    |>.insert "Bob" 25
```

### Sets

**Python `set[T]`:**
- Maps to `Std.HashSet α` (requires import)
- Or `List α` with uniqueness maintained

## Optional and Error Types

### None/Optional

**Python `None` and `Optional[T]`:**
- Maps to `Option α` in Lean4

**Example:**
```python
# Python
def find_user(id: int) -> Optional[User]:
    if id in users:
        return users[id]
    return None
```

```lean
-- Lean4
def findUser (id : Nat) : Option User :=
  users.find? id

-- Pattern matching
match findUser 42 with
| some user => s!"Found: {user.name}"
| none => "Not found"
```

### Exceptions

**Python exceptions:**
- Map to `Except E α` in Lean4

**Example:**
```python
# Python
def parse_int(s: str) -> int:
    try:
        return int(s)
    except ValueError as e:
        raise ValueError(f"Invalid integer: {s}")
```

```lean
-- Lean4
def parseInt (s : String) : Except String Int :=
  match s.toInt? with
  | some n => Except.ok n
  | none => Except.error s!"Invalid integer: {s}"
```

## Function Types

**Python function types:**
```python
def apply(f: Callable[[int], int], x: int) -> int:
    return f(x)
```

**Lean4:**
```lean
def apply (f : Int → Int) (x : Int) : Int :=
  f x
```

## Class to Structure Mapping

**Python class:**
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
```

**Lean4 structure:**
```lean
structure Person where
  name : String
  age : Nat

def Person.greet (p : Person) : String :=
  s!"Hello, I'm {p.name}"
```

## Union Types

**Python `Union[A, B]`:**
- Maps to sum types in Lean4

**Example:**
```python
# Python
def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value * 2)
    else:
        return value.upper()
```

```lean
-- Lean4
inductive IntOrString where
  | int : Int → IntOrString
  | string : String → IntOrString

def process (value : IntOrString) : String :=
  match value with
  | .int n => toString (n * 2)
  | .string s => s.toUpper
```

## Generic Types

**Python generics:**
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value
```

**Lean4:**
```lean
structure Box (α : Type) where
  value : α

def Box.map {α β : Type} (f : α → β) (box : Box α) : Box β :=
  ⟨f box.value⟩
```

## Type Aliases

**Python:**
```python
UserId = int
UserName = str
```

**Lean4:**
```lean
abbrev UserId := Nat
abbrev UserName := String
```

## Advanced: Dependent Types

Lean4 supports dependent types, which Python doesn't have:

```lean
-- Vector: list with length in type
def Vector (α : Type) (n : Nat) := { xs : List α // xs.length = n }

-- Function that requires non-empty list
def head {α : Type} (xs : List α) (h : xs ≠ []) : α :=
  match xs with
  | x :: _ => x
  | [] => absurd rfl h
```

## Type Conversion Utilities

```lean
-- Int ↔ Nat
def natToInt (n : Nat) : Int := Int.ofNat n
def intToNat (i : Int) : Option Nat :=
  if i ≥ 0 then some i.natAbs else none

-- String ↔ Int
def stringToInt (s : String) : Option Int := s.toInt?
def intToString (i : Int) : String := toString i

-- List ↔ Array
def listToArray {α : Type} (xs : List α) : Array α := xs.toArray
def arrayToList {α : Type} (xs : Array α) : List α := xs.toList
```
