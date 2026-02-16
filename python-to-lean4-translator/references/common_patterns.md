# Common Translation Patterns

Frequently encountered Python patterns and their Lean4 equivalents.

## Iteration Patterns

### List Comprehension

**Python:**
```python
squares = [x * x for x in range(10)]
evens = [x for x in numbers if x % 2 == 0]
pairs = [(x, y) for x in range(3) for y in range(3)]
```

**Lean4:**
```lean
let squares := (List.range 10).map (fun x => x * x)
let evens := numbers.filter (fun x => x % 2 = 0)
let pairs := (List.range 3).bind fun x =>
  (List.range 3).map fun y => (x, y)
```

### Dictionary Comprehension

**Python:**
```python
squares_dict = {x: x * x for x in range(5)}
```

**Lean4:**
```lean
import Std.Data.HashMap

let squaresDict := (List.range 5).foldl
  (fun acc x => acc.insert x (x * x))
  Std.HashMap.empty
```

### Enumerate

**Python:**
```python
for i, value in enumerate(items):
    print(f"{i}: {value}")
```

**Lean4:**
```lean
items.enum.map fun (i, value) =>
  IO.println s!"{i}: {value}"
```

## Functional Patterns

### Map, Filter, Reduce

**Python:**
```python
# Map
doubled = list(map(lambda x: x * 2, numbers))

# Filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Reduce
from functools import reduce
total = reduce(lambda acc, x: acc + x, numbers, 0)
```

**Lean4:**
```lean
-- Map
let doubled := numbers.map (· * 2)

-- Filter
let evens := numbers.filter (· % 2 = 0)

-- Reduce (fold)
let total := numbers.foldl (· + ·) 0
```

### Lambda Functions

**Python:**
```python
add = lambda x, y: x + y
square = lambda x: x * x
```

**Lean4:**
```lean
let add := fun x y => x + y
let square := fun x => x * x

-- Or with type annotations
let add : Int → Int → Int := fun x y => x + y
```

## Control Flow Patterns

### Early Return

**Python:**
```python
def find_first_even(numbers: list[int]) -> Optional[int]:
    for n in numbers:
        if n % 2 == 0:
            return n
    return None
```

**Lean4:**
```lean
def findFirstEven (numbers : List Int) : Option Int :=
  numbers.find? (· % 2 = 0)

-- Or with explicit recursion
def findFirstEven' : List Int → Option Int
  | [] => none
  | x :: xs => if x % 2 = 0 then some x else findFirstEven' xs
```

### Guard Clauses

**Python:**
```python
def process(value: Optional[int]) -> int:
    if value is None:
        return 0
    if value < 0:
        return 0
    return value * 2
```

**Lean4:**
```lean
def process (value : Option Int) : Int :=
  match value with
  | none => 0
  | some v =>
    if v < 0 then 0
    else v * 2
```

## Data Structure Patterns

### Builder Pattern

**Python:**
```python
class QueryBuilder:
    def __init__(self):
        self.filters = []

    def where(self, condition: str):
        self.filters.append(condition)
        return self

    def build(self) -> str:
        return " AND ".join(self.filters)
```

**Lean4:**
```lean
structure QueryBuilder where
  filters : List String

def QueryBuilder.empty : QueryBuilder :=
  ⟨[]⟩

def QueryBuilder.where (qb : QueryBuilder) (condition : String) : QueryBuilder :=
  ⟨qb.filters ++ [condition]⟩

def QueryBuilder.build (qb : QueryBuilder) : String :=
  String.intercalate " AND " qb.filters

-- Usage
let query := QueryBuilder.empty
  |>.where "age > 18"
  |>.where "status = 'active'"
  |>.build
```

### Visitor Pattern

**Python:**
```python
class Expr:
    pass

class Num(Expr):
    def __init__(self, value: int):
        self.value = value

class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

def eval_expr(expr: Expr) -> int:
    if isinstance(expr, Num):
        return expr.value
    elif isinstance(expr, Add):
        return eval_expr(expr.left) + eval_expr(expr.right)
```

**Lean4:**
```lean
inductive Expr where
  | num : Int → Expr
  | add : Expr → Expr → Expr

def evalExpr : Expr → Int
  | .num n => n
  | .add left right => evalExpr left + evalExpr right
```

## Error Handling Patterns

### Try-Except to Except Monad

**Python:**
```python
def safe_divide(a: int, b: int) -> Result[float, str]:
    try:
        if b == 0:
            raise ValueError("Division by zero")
        return Ok(a / b)
    except Exception as e:
        return Err(str(e))
```

**Lean4:**
```lean
def safeDivide (a b : Int) : Except String Float :=
  if b = 0 then
    Except.error "Division by zero"
  else
    Except.ok (a.toFloat / b.toFloat)

-- Chaining operations
def compute (x y z : Int) : Except String Float :=
  safeDivide x y >>= fun r1 =>
  safeDivide r1.toInt z >>= fun r2 =>
  Except.ok r2
```

### Optional Chaining

**Python:**
```python
result = user.profile.address.city if user and user.profile and user.profile.address else None
```

**Lean4:**
```lean
let result := user.bind fun u =>
  u.profile.bind fun p =>
  p.address.bind fun a =>
  some a.city
```

## Algorithm Patterns

### Binary Search

**Python:**
```python
def binary_search(arr: list[int], target: int) -> int:
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

**Lean4:**
```lean
def binarySearch (arr : Array Int) (target : Int) : Option Nat :=
  let rec search (left right : Nat) : Option Nat :=
    if left > right then
      none
    else
      let mid := (left + right) / 2
      match compare arr[mid]! target with
      | .eq => some mid
      | .lt => search (mid + 1) right
      | .gt => if mid > 0 then search left (mid - 1) else none
  search 0 (arr.size - 1)
```

### Memoization

**Python:**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

**Lean4:**
```lean
-- Using array for memoization
def fib (n : Nat) : Nat :=
  let rec fibMemo (i : Nat) (memo : Array Nat) : Nat × Array Nat :=
    if i ≤ 1 then
      (i, memo)
    else if h : i < memo.size then
      (memo[i], memo)
    else
      let (f1, memo1) := fibMemo (i - 1) memo
      let (f2, memo2) := fibMemo (i - 2) memo1
      let result := f1 + f2
      (result, memo2.push result)
  (fibMemo n (Array.mkArray (n + 1) 0)).1
```

## I/O Patterns

### File Reading

**Python:**
```python
def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
```

**Lean4:**
```lean
def readFile (path : String) : IO String :=
  IO.FS.readFile path

-- With error handling
def readFileSafe (path : String) : IO (Except IO.Error String) :=
  try
    Except.ok <$> IO.FS.readFile path
  catch e =>
    pure (Except.error e)
```

### Command Line Arguments

**Python:**
```python
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: program <arg>")
        sys.exit(1)
    arg = sys.argv[1]
    print(f"Argument: {arg}")
```

**Lean4:**
```lean
def main (args : List String) : IO Unit := do
  match args with
  | [] =>
    IO.println "Usage: program <arg>"
    IO.Process.exit 1
  | arg :: _ =>
    IO.println s!"Argument: {arg}"
```

## Testing Patterns

### Assertions

**Python:**
```python
assert add(2, 3) == 5
assert is_prime(7) == True
```

**Lean4:**
```lean
-- Runtime checks
#eval add 2 3  -- Should output 5
#eval isPrime 7  -- Should output true

-- Compile-time proofs
example : add 2 3 = 5 := rfl
example : isPrime 7 = true := rfl
```
