# Advanced Lean4 Features

Advanced Lean4 features useful for Python translations.

## Monads

### Option Monad

**Chaining optional operations:**
```lean
def getUserEmail (userId : Nat) : Option String := do
  let user ← findUser userId
  let profile ← user.profile
  let email ← profile.email
  return email

-- Or with bind
def getUserEmail' (userId : Nat) : Option String :=
  findUser userId >>= fun user =>
  user.profile >>= fun profile =>
  profile.email
```

### Except Monad

**Error handling with context:**
```lean
def processData (input : String) : Except String Int := do
  let parsed ← parseInput input
    |>.mapError (fun e => s!"Parse error: {e}")
  let validated ← validate parsed
    |>.mapError (fun e => s!"Validation error: {e}")
  let result ← compute validated
    |>.mapError (fun e => s!"Computation error: {e}")
  return result
```

### IO Monad

**Sequencing I/O operations:**
```lean
def processFile (path : String) : IO Unit := do
  let content ← IO.FS.readFile path
  let lines := content.splitOn "\n"
  for line in lines do
    IO.println s!"Processing: {line}"
  IO.println "Done!"
```

### State Monad

**Threading state through computations:**
```lean
def Counter := StateM Nat

def increment : Counter Unit :=
  modify (· + 1)

def getCount : Counter Nat :=
  get

def runCounter : Counter α → Nat → α × Nat :=
  StateT.run

-- Usage
def example : Counter Nat := do
  increment
  increment
  let count ← getCount
  increment
  return count

#eval runCounter example 0  -- (2, 3)
```

## Type Classes

### Custom Type Classes

**Defining a type class:**
```lean
class Serializable (α : Type) where
  serialize : α → String
  deserialize : String → Option α

-- Instances
instance : Serializable Int where
  serialize := toString
  deserialize := String.toInt?

instance : Serializable Bool where
  serialize b := if b then "true" else "false"
  deserialize s := if s = "true" then some true
                   else if s = "false" then some false
                   else none

-- Generic function using type class
def saveToFile [Serializable α] (value : α) (path : String) : IO Unit :=
  IO.FS.writeFile path (Serializable.serialize value)
```

### Functor, Applicative, Monad

**Using standard type classes:**
```lean
-- Functor
#eval (· + 1) <$> some 5  -- some 6
#eval (· + 1) <$> [1, 2, 3]  -- [2, 3, 4]

-- Applicative
#eval some (· + 1) <*> some 5  -- some 6
#eval [(· + 1), (· * 2)] <*> [1, 2, 3]  -- [2, 3, 4, 2, 4, 6]

-- Monad
def example : Option Int := do
  let x ← some 5
  let y ← some 3
  return x + y
```

## Dependent Types

### Vectors (Length-Indexed Lists)

**Defining vectors:**
```lean
def Vector (α : Type) (n : Nat) := { xs : List α // xs.length = n }

def Vector.mk {α : Type} (xs : List α) : Vector α xs.length :=
  ⟨xs, rfl⟩

def Vector.head {α : Type} {n : Nat} (v : Vector α (n + 1)) : α :=
  match v.val with
  | x :: _ => x
  | [] => absurd v.property (Nat.succ_ne_zero n)

def Vector.append {α : Type} {m n : Nat}
    (v1 : Vector α m) (v2 : Vector α n) : Vector α (m + n) :=
  ⟨v1.val ++ v2.val, by simp [List.length_append, v1.property, v2.property]⟩
```

### Dependent Pairs

**Sigma types:**
```lean
-- Pair where second component depends on first
def DependentPair := (n : Nat) × Vector Int n

def example : DependentPair :=
  ⟨3, Vector.mk [1, 2, 3]⟩
```

## Proof-Carrying Code

### Preconditions and Postconditions

**Functions with proofs:**
```lean
def safeDiv (a : Int) (b : Int) (h : b ≠ 0) : Int :=
  a / b

-- Usage requires proof
example : Int := safeDiv 10 2 (by decide)

-- Or with Option
def safeDivOption (a b : Int) : Option Int :=
  if h : b ≠ 0 then
    some (safeDiv a b h)
  else
    none
```

### Invariants

**Maintaining invariants:**
```lean
structure SortedList where
  data : List Nat
  sorted : data.Sorted (· ≤ ·)

def SortedList.insert (sl : SortedList) (x : Nat) : SortedList :=
  let newData := insertSorted x sl.data
  ⟨newData, proof_of_sorted newData⟩
```

## Metaprogramming

### Macros

**Defining custom syntax:**
```lean
macro "unless " c:term " then " t:term : term =>
  `(if !$c then $t else ())

-- Usage
unless x > 10 then
  IO.println "x is not greater than 10"
```

### Tactics

**Custom proof tactics:**
```lean
syntax "my_tactic" : tactic

macro_rules
  | `(tactic| my_tactic) => `(tactic| simp; omega)

example (x : Nat) : x + 0 = x := by
  my_tactic
```

## Performance Optimization

### Tail Recursion

**Converting to tail-recursive form:**
```python
# Python (not tail-recursive)
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

```lean
-- Lean4 (tail-recursive with accumulator)
def factorial (n : Nat) : Nat :=
  let rec go (n acc : Nat) : Nat :=
    if n ≤ 1 then acc
    else go (n - 1) (n * acc)
  go n 1
```

### Lazy Evaluation

**Using lazy lists:**
```lean
-- Infinite stream
def Stream (α : Type) := Nat → α

def Stream.iterate {α : Type} (f : α → α) (x : α) : Stream α :=
  fun n => (List.range n).foldl (fun acc _ => f acc) x

-- Take first n elements
def Stream.take {α : Type} (s : Stream α) (n : Nat) : List α :=
  (List.range n).map s

-- Example: infinite sequence of natural numbers
def nats : Stream Nat := id

#eval (nats.take 10)  -- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## FFI (Foreign Function Interface)

### Calling External Code

**Interfacing with C:**
```lean
@[extern "my_c_function"]
opaque myCFunction (x : UInt32) : UInt32

-- Usage
def example : IO Unit := do
  let result := myCFunction 42
  IO.println s!"Result: {result}"
```

## Compile-Time Computation

### Compile-Time Evaluation

**Using `#eval` and `#reduce`:**
```lean
def fibonacci : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fibonacci n + fibonacci (n + 1)

-- Computed at compile time
def fib10 : Nat := fibonacci 10

#eval fib10  -- 55

-- Prove properties
example : fibonacci 5 = 5 := rfl
```

## Pattern Matching Extensions

### Guards

**Pattern matching with conditions:**
```lean
def classify (n : Int) : String :=
  match n with
  | n if n < 0 => "negative"
  | 0 => "zero"
  | n if n % 2 = 0 => "positive even"
  | _ => "positive odd"
```

### As-Patterns

**Binding matched values:**
```lean
def processTree (t : Tree α) : String :=
  match t with
  | node (left@(leaf _)) (right@(leaf _)) =>
    s!"Two leaves: {left} and {right}"
  | node left right =>
    s!"Complex tree"
  | leaf x =>
    s!"Single leaf: {x}"
```

## Advanced Type System Features

### Subtype

**Refinement types:**
```lean
def PositiveInt := { n : Int // n > 0 }

def makePositive (n : Int) (h : n > 0) : PositiveInt :=
  ⟨n, h⟩

def increment (p : PositiveInt) : PositiveInt :=
  ⟨p.val + 1, by omega⟩
```

### Quotient Types

**Equivalence classes:**
```lean
def IntMod (n : Nat) := Quot (fun a b : Int => (a - b) % n = 0)

def IntMod.mk (n : Nat) (a : Int) : IntMod n :=
  Quot.mk _ a

def IntMod.add {n : Nat} (a b : IntMod n) : IntMod n :=
  Quot.lift₂ (fun x y => IntMod.mk n (x + y)) sorry sorry a b
```
