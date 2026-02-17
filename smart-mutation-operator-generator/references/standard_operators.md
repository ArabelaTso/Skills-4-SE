# Standard Mutation Operators

This document describes standard mutation operators used in mutation testing.

## Arithmetic Operators

### AOR (Arithmetic Operator Replacement)

Replace arithmetic operators with other arithmetic operators.

**Mutations**:
- `+` → `-`, `*`, `/`, `%`
- `-` → `+`, `*`, `/`, `%`
- `*` → `+`, `-`, `/`, `%`
- `/` → `+`, `-`, `*`, `%`
- `%` → `+`, `-`, `*`, `/`

**Example**:
```python
# Original
result = a + b

# Mutants
result = a - b  # AOR
result = a * b  # AOR
result = a / b  # AOR
```

### UOI (Unary Operator Insertion)

Insert unary operators before variables.

**Mutations**:
- `x` → `-x`, `+x`, `~x`

**Example**:
```python
# Original
return value

# Mutants
return -value  # UOI
return +value  # UOI
```

### UOD (Unary Operator Deletion)

Remove unary operators.

**Mutations**:
- `-x` → `x`
- `+x` → `x`
- `~x` → `x`

## Relational Operators

### ROR (Relational Operator Replacement)

Replace relational operators.

**Mutations**:
- `>` → `>=`, `<`, `<=`, `==`, `!=`
- `>=` → `>`, `<`, `<=`, `==`, `!=`
- `<` → `>`, `>=`, `<=`, `==`, `!=`
- `<=` → `>`, `>=`, `<`, `==`, `!=`
- `==` → `>`, `>=`, `<`, `<=`, `!=`
- `!=` → `>`, `>=`, `<`, `<=`, `==`

**Example**:
```python
# Original
if x > 10:

# Mutants
if x >= 10:  # ROR
if x < 10:   # ROR
if x == 10:  # ROR
```

## Logical Operators

### LCR (Logical Connector Replacement)

Replace logical operators.

**Mutations**:
- `and` → `or`
- `or` → `and`
- `&&` → `||`
- `||` → `&&`

**Example**:
```python
# Original
if x > 0 and y > 0:

# Mutant
if x > 0 or y > 0:  # LCR
```

### LOI (Logical Operator Insertion)

Insert logical negation.

**Mutations**:
- `condition` → `not condition`

**Example**:
```python
# Original
if is_valid:

# Mutant
if not is_valid:  # LOI
```

### LOD (Logical Operator Deletion)

Remove logical negation.

**Mutations**:
- `not condition` → `condition`

## Constant Mutations

### CRP (Constant Replacement)

Replace constants with other values.

**Mutations**:
- `0` → `1`, `-1`
- `1` → `0`, `2`, `-1`
- `true` → `false`
- `false` → `true`
- `""` → `"mutant"`
- `null` → `new Object()`

**Example**:
```python
# Original
if count == 0:

# Mutants
if count == 1:   # CRP
if count == -1:  # CRP
```

### ABS (Absolute Value Insertion)

Insert absolute value function.

**Mutations**:
- `x` → `abs(x)`

**Example**:
```python
# Original
result = value

# Mutant
result = abs(value)  # ABS
```

## Statement Mutations

### SDL (Statement Deletion)

Delete statements.

**Mutations**:
- Remove entire statement
- Remove function call
- Remove assignment

**Example**:
```python
# Original
x = calculate()
process(x)
return x

# Mutants
# x = calculate()  # SDL - deleted
process(x)
return x
```

### SIR (Statement Insertion)

Insert return statements.

**Mutations**:
- Insert `return` before statement
- Insert `return null`
- Insert `return true/false`

**Example**:
```python
# Original
def process():
    validate()
    execute()

# Mutant
def process():
    return  # SIR - early return
    validate()
    execute()
```

## Control Flow Mutations

### COR (Conditional Operator Replacement)

Replace conditional operators.

**Mutations**:
- `if` → `if not`
- `while` → `if`
- `for` → (skip loop)

**Example**:
```python
# Original
while condition:
    process()

# Mutant
if condition:  # COR
    process()
```

### BCR (Break/Continue Replacement)

Replace break/continue statements.

**Mutations**:
- `break` → `continue`
- `continue` → `break`

## Object-Oriented Mutations

### IHI (Hiding Variable Insertion)

Insert `this` or `self` qualifier.

**Mutations**:
- `variable` → `this.variable`
- `variable` → `self.variable`

### IHD (Hiding Variable Deletion)

Remove `this` or `self` qualifier.

**Mutations**:
- `this.variable` → `variable`
- `self.variable` → `variable`

### IOD (Overriding Method Deletion)

Delete overriding method.

**Mutations**:
- Remove method override, use parent implementation

### IOP (Overridden Method Call)

Change method call to parent.

**Mutations**:
- `method()` → `super.method()`

## Exception Handling Mutations

### EXS (Exception Swallowing)

Remove exception handling.

**Mutations**:
- Remove `try-catch` block
- Remove `catch` clause

**Example**:
```python
# Original
try:
    risky_operation()
except Exception:
    handle_error()

# Mutant
risky_operation()  # EXS - removed try-catch
```

### ETR (Exception Type Replacement)

Replace exception types.

**Mutations**:
- `ValueError` → `Exception`
- `FileNotFoundError` → `IOError`

## Collection Mutations

### CIR (Collection Item Replacement)

Replace collection items.

**Mutations**:
- `list[0]` → `list[1]`
- `list[-1]` → `list[0]`

**Example**:
```python
# Original
first = items[0]

# Mutant
first = items[1]  # CIR
```

### CER (Collection Empty Replacement)

Replace with empty collection.

**Mutations**:
- `[1, 2, 3]` → `[]`
- `{a: 1}` → `{}`

## String Mutations

### STR (String Replacement)

Replace string values.

**Mutations**:
- `"text"` → `""`
- `"text"` → `"mutant"`

**Example**:
```python
# Original
message = "Hello"

# Mutants
message = ""        # STR
message = "mutant"  # STR
```

## Function Call Mutations

### FCR (Function Call Replacement)

Replace function calls.

**Mutations**:
- `func(x)` → `func()`
- `func(x, y)` → `func(x)`
- `func(x)` → `func(x, x)`

**Example**:
```python
# Original
result = calculate(a, b)

# Mutants
result = calculate(a)     # FCR
result = calculate(a, a)  # FCR
```

### FCM (Function Call Modification)

Modify function arguments.

**Mutations**:
- `func(x)` → `func(None)`
- `func(x)` → `func(0)`

## Return Value Mutations

### RVR (Return Value Replacement)

Replace return values.

**Mutations**:
- `return x` → `return None`
- `return x` → `return 0`
- `return x` → `return True/False`

**Example**:
```python
# Original
def get_value():
    return result

# Mutants
def get_value():
    return None   # RVR

def get_value():
    return 0      # RVR
```

## Assignment Mutations

### ABS (Assignment Replacement)

Replace assignment operators.

**Mutations**:
- `=` → `+=`, `-=`, `*=`, `/=`
- `+=` → `=`, `-=`

**Example**:
```python
# Original
count = count + 1

# Mutant
count += 1  # ABS
```

## Mutation Operator Selection

### High-Value Operators

These operators typically find real bugs:
- ROR (relational operators)
- LCR (logical connectors)
- CRP (constants)
- SDL (statement deletion)

### Medium-Value Operators

Useful but may generate equivalent mutants:
- AOR (arithmetic operators)
- FCR (function calls)
- RVR (return values)

### Low-Value Operators

Often generate trivial or equivalent mutants:
- UOI/UOD (unary operators)
- STR (string replacement)
- IHI/IHD (hiding variables)

## Equivalent Mutants

Some mutations don't change program behavior:

**Example**:
```python
# Original
x = a + 0

# Mutant (equivalent)
x = a - 0  # Still equals a
```

**Common equivalent mutants**:
- `x + 0` → `x - 0`
- `x * 1` → `x / 1`
- `if True:` → `if not False:`
