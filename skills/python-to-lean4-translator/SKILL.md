---
name: python-to-lean4-translator
description: Translate Python programs to equivalent Lean4 code while preserving semantics and ensuring type safety. Use when users ask to convert, translate, or port Python code to Lean4, or when they need to verify Python algorithms using Lean4's theorem proving capabilities. Handles functions, classes, data structures, control flow, and ensures the generated Lean4 code is well-typed, executable, and can successfully run.
---

# Python to Lean4 Translator

Translate Python programs into equivalent, executable Lean4 code while preserving program semantics and ensuring type safety.

## Overview

This skill provides systematic guidance for translating Python code to Lean4, handling type inference, function translations, data structures, control flow, and ensuring well-typed, executable output.

## Translation Workflow

```
Python Input → Analyze Structure → Map Types → Translate Constructs → Verify → Output Lean4
    ├─ Identify types and signatures
    ├─ Map Python constructs to Lean4 equivalents
    ├─ Handle type conversions
    ├─ Ensure totality and termination
    └─ Validate executability
```

## Core Translation Principles

### 1. Type Safety First

Lean4 is strongly typed. Every translation must:
- Infer or specify explicit types for all variables
- Ensure type consistency across operations
- Handle Python's dynamic typing by choosing appropriate Lean4 types
- Use `Option` for nullable values, `Except` for error handling

### 2. Preserve Semantics

The translated code must maintain the same computational behavior, preserve function input-output relationships, keep the same algorithmic complexity, and handle edge cases equivalently.

### 3. Ensure Executability

Generated Lean4 code must compile without errors, be executable (use `#eval` to verify), terminate (prove termination for recursive functions), and follow Lean4 syntax and conventions.

## Type Mapping Reference

### Basic Types

| Python Type | Lean4 Type | Notes |
|------------|-----------|-------|
| `int` | `Int` or `Nat` | Use `Nat` for non-negative integers |
| `float` | `Float` | Lean4's floating point type |
| `bool` | `Bool` | Direct mapping |
| `str` | `String` | Direct mapping |
| `None` | `Option α` | Use `none` for None, `some x` for values |
| `list` | `List α` | Homogeneous lists |
| `tuple` | Product types `α × β` or custom structure | |
| `dict` | `Std.HashMap` or `List (α × β)` | Requires import |
| `set` | `Std.HashSet` or `List α` | Requires import |

For detailed type system information, see [references/type_mappings.md](references/type_mappings.md).

## Translation Patterns

### Functions

**Simple function:**
```python
def add(a: int, b: int) -> int:
    return a + b
```

**Lean4:**
```lean
def add (a : Int) (b : Int) : Int :=
  a + b
```

**Recursive function:**
```python
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

**Lean4:**
```lean
def factorial (n : Nat) : Nat :=
  if n ≤ 1 then
    1
  else
    n * factorial (n - 1)
```

### Control Flow

**If-else:**
```python
if condition:
    result = value1
else:
    result = value2
```

**Lean4:**
```lean
let result := if condition then value1 else value2
```

**For loops (list iteration):**
```python
total = 0
for x in items:
    total += x
```

**Lean4 (using fold):**
```lean
let total := items.foldl (· + ·) 0
```

### List Operations

**List comprehension:**
```python
squares = [x * x for x in range(10)]
```

**Lean4:**
```lean
let squares := (List.range 10).map (fun x => x * x)
```

**Filter:**
```python
evens = [x for x in numbers if x % 2 == 0]
```

**Lean4:**
```lean
let evens := numbers.filter (fun x => x % 2 == 0)
```

### Classes and Structures

**Python class:**
```python
class Rectangle:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self) -> int:
        return self.width * self.height
```

**Lean4:**
```lean
structure Rectangle where
  width : Int
  height : Int

def Rectangle.area (r : Rectangle) : Int :=
  r.width * r.height
```

## Handling Common Challenges

### 1. Dynamic Typing

Analyze usage to infer types, use sum types for multiple possible types, use `Option` for nullable values, and document type assumptions.

### 2. Mutability

Use immutable bindings with `let`, thread state through function parameters, or use monadic state (`StateM`) if needed.

### 3. Exceptions

Convert Python exceptions to `Except` or `Option`:

```python
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

**Lean4:**
```lean
def divide (a b : Int) : Except String Float :=
  if b = 0 then
    Except.error "Division by zero"
  else
    Except.ok (a.toFloat / b.toFloat)
```

### 4. Recursion and Termination

Use structural recursion when possible, add `termination_by` clause for complex recursion:

```lean
def fibonacci (n : Nat) : Nat :=
  match n with
  | 0 => 0
  | 1 => 1
  | n + 2 => fibonacci n + fibonacci (n + 1)
termination_by n
```

### 5. Side Effects and I/O

Use `IO` monad for I/O operations:

```python
def greet(name: str):
    print(f"Hello, {name}!")
```

**Lean4:**
```lean
def greet (name : String) : IO Unit :=
  IO.println s!"Hello, {name}!"
```

## Translation Process

### Step 1: Analyze Python Code

Identify all functions, classes, and global variables. Infer types from usage and annotations. Identify dependencies and imports. Note any dynamic behavior or side effects.

### Step 2: Plan Type Mappings

Map Python types to Lean4 types. Identify where `Option`, `Except`, or sum types are needed. Plan structure definitions for classes. Determine function signatures.

### Step 3: Translate Constructs

Start with data structures (classes → structures). Translate pure functions first. Handle control flow (convert loops to recursion). Translate functions with side effects using `IO`. Add necessary imports.

### Step 4: Ensure Well-Typedness

Add explicit type annotations. Resolve type mismatches. Handle implicit conversions. Add termination proofs for recursive functions.

### Step 5: Verify Executability

Check syntax with Lean4 compiler. Test with `#eval` for simple cases. Verify output matches Python behavior. Document any semantic differences.

## Required Imports

Common imports for translated code:

```lean
import Std.Data.HashMap
import Std.Data.HashSet
import Init.Data.List.Basic
import Init.Data.Option.Basic
```

## Example Translation

**Python:**
```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def primes_up_to(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_prime(n)]
```

**Lean4:**
```lean
def isPrime (n : Nat) : Bool :=
  if n < 2 then
    false
  else
    let rec checkDivisors (i : Nat) : Bool :=
      if i * i > n then
        true
      else if n % i = 0 then
        false
      else
        checkDivisors (i + 1)
    checkDivisors 2

def primesUpTo (limit : Nat) : List Nat :=
  (List.range (limit + 1)).drop 2 |>.filter isPrime

-- Test
#eval primesUpTo 20  -- [2, 3, 5, 7, 11, 13, 17, 19]
```

## Best Practices

1. **Start Simple**: Translate simple functions first, then build up to complex ones
2. **Test Incrementally**: Use `#eval` to test each function as you translate
3. **Document Assumptions**: Note any assumptions about types or behavior
4. **Preserve Structure**: Keep similar code organization when possible
5. **Use Lean4 Idioms**: Prefer pattern matching over if-else chains
6. **Handle Errors Explicitly**: Use `Option` or `Except` instead of exceptions
7. **Prove Termination**: Add termination proofs for recursive functions
8. **Comment Differences**: Note where Lean4 behavior differs from Python

## Verification Checklist

Before finalizing translation:

- [ ] All types are explicitly specified or correctly inferred
- [ ] Code compiles without errors
- [ ] `#eval` produces expected results for test cases
- [ ] Recursive functions have termination proofs
- [ ] Error handling uses `Option` or `Except` appropriately
- [ ] Side effects are properly wrapped in `IO`
- [ ] Imports are included
- [ ] Comments explain non-obvious translations

## Additional Resources

For complex translations, refer to:
- [Type Mappings](references/type_mappings.md) - Comprehensive type conversion guide
- [Common Patterns](references/common_patterns.md) - Frequently used translation patterns
- [Advanced Features](references/advanced_features.md) - Monads, type classes, and advanced Lean4 features
