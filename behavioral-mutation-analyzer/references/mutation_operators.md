# Mutation Operators Reference

## Overview

Mutation operators are transformations applied to source code to create mutants. Understanding each operator helps identify what tests are needed to kill the resulting mutants.

## Arithmetic Operators

### Binary Arithmetic Replacement

**Operator:** Replace arithmetic operators with alternatives

**Mutations:**
- `+` → `-`, `*`, `/`, `%`
- `-` → `+`, `*`, `/`, `%`
- `*` → `+`, `-`, `/`, `%`
- `/` → `+`, `-`, `*`, `%`
- `%` → `+`, `-`, `*`, `/`

**Example:**
```java
// Original
int result = a + b;

// Mutants
int result = a - b;  // Subtraction
int result = a * b;  // Multiplication
int result = a / b;  // Division
int result = a % b;  // Modulo
```

**Test Strategy:**
- Verify exact numeric results
- Use inputs where operations produce different results
- Example: `a=5, b=3` → `+`=8, `-`=2, `*`=15, `/`=1, `%`=2

### Unary Arithmetic Replacement

**Operator:** Change or remove unary operators

**Mutations:**
- `+x` → `-x`
- `-x` → `+x`
- `++x` → `--x`, `x`
- `--x` → `++x`, `x`
- `x++` → `x--`, `x`
- `x--` → `x++`, `x`

**Example:**
```python
# Original
value = -amount

# Mutant
value = +amount  # Sign flip
```

**Test Strategy:**
- Test with positive and negative values
- Verify sign correctness
- Check increment/decrement effects

## Relational Operators

### Relational Operator Replacement

**Operator:** Replace comparison operators

**Mutations:**
- `>` → `>=`, `<`, `<=`, `==`, `!=`
- `>=` → `>`, `<`, `<=`, `==`, `!=`
- `<` → `<=`, `>`, `>=`, `==`, `!=`
- `<=` → `<`, `>`, `>=`, `==`, `!=`
- `==` → `!=`, `<=`, `>=`
- `!=` → `==`, `<`, `>`

**Example:**
```javascript
// Original
if (age > 18) {
    return true;
}

// Mutants
if (age >= 18) { ... }  // Boundary change
if (age < 18) { ... }   // Negation
if (age == 18) { ... }  // Equality
```

**Test Strategy:**
- Test boundary values (18, 19, 17)
- Verify exact boundary behavior
- Test both sides of condition

### Conditional Boundary Mutation

**Operator:** Adjust boundary conditions

**Mutations:**
- `<` ↔ `<=`
- `>` ↔ `>=`

**Example:**
```java
// Original
if (score < 100) {
    return "Pass";
}

// Mutant
if (score <= 100) {
    return "Pass";
}
```

**Test Strategy:**
- Test exact boundary value (100)
- Test values on both sides (99, 101)
- Verify off-by-one correctness

## Logical Operators

### Logical Operator Replacement

**Operator:** Replace logical operators

**Mutations:**
- `&&` → `||`, `==`, `!=`
- `||` → `&&`, `==`, `!=`
- `&` → `|`, `^`
- `|` → `&`, `^`
- `^` → `&`, `|`

**Example:**
```python
# Original
if (is_valid and is_active):
    process()

# Mutants
if (is_valid or is_active):   # OR instead of AND
if (is_valid == is_active):   # Equality
```

**Test Strategy:**
- Test all boolean combinations (T/T, T/F, F/T, F/F)
- Verify correct logical behavior
- Use truth tables

### Negation Operator

**Operator:** Insert or remove negation

**Mutations:**
- `!x` → `x`
- `x` → `!x`
- `~x` → `x` (bitwise)

**Example:**
```java
// Original
if (isEnabled) {
    start();
}

// Mutant
if (!isEnabled) {
    start();
}
```

**Test Strategy:**
- Test both true and false cases
- Verify behavior matches expectation
- Check negation logic

## Conditional Mutations

### Conditional Expression Mutation

**Operator:** Modify conditional expressions

**Mutations:**
- `if (condition)` → `if (true)`, `if (false)`
- Ternary: `a ? b : c` → `true ? b : c`, `false ? b : c`, `a ? c : b`

**Example:**
```javascript
// Original
const result = x > 0 ? positive() : negative();

// Mutants
const result = true ? positive() : negative();  // Always positive
const result = false ? positive() : negative(); // Always negative
const result = x > 0 ? negative() : positive(); // Swapped branches
```

**Test Strategy:**
- Test both branches
- Verify correct branch taken
- Check branch return values

### Remove Conditionals

**Operator:** Remove conditional checks

**Mutations:**
- Remove `if` statement, keep body
- Remove `else` branch
- Remove entire conditional

**Example:**
```python
# Original
if (user is not None):
    user.update()

# Mutant (condition removed)
user.update()  # Will crash if user is None
```

**Test Strategy:**
- Test with null/None values
- Verify guard conditions work
- Check error handling

## Return Value Mutations

### Return Value Replacement

**Operator:** Change return values

**Mutations:**
- `return x` → `return null`, `return 0`, `return true`, `return false`, `return ""`
- `return true` → `return false`
- `return false` → `return true`
- `return x` → `return x + 1`, `return x - 1`

**Example:**
```java
// Original
public boolean isValid() {
    return checkCondition();
}

// Mutants
public boolean isValid() {
    return true;   // Always valid
}

public boolean isValid() {
    return false;  // Always invalid
}
```

**Test Strategy:**
- Assert exact return values
- Don't just check type or truthiness
- Verify all return paths

### Void Method Call Removal

**Operator:** Remove calls to void methods

**Mutations:**
- Remove method call that returns void
- Remove statement with side effects

**Example:**
```python
# Original
def process():
    validate_input()
    save_to_database()
    send_notification()

# Mutant (save_to_database removed)
def process():
    validate_input()
    # save_to_database()  # Removed
    send_notification()
```

**Test Strategy:**
- Verify side effects occurred
- Check database state
- Verify external interactions

## Assignment Mutations

### Assignment Operator Replacement

**Operator:** Change assignment operators

**Mutations:**
- `+=` → `-=`, `*=`, `/=`, `=`
- `-=` → `+=`, `*=`, `/=`, `=`
- `*=` → `+=`, `-=`, `/=`, `=`
- `/=` → `+=`, `-=`, `*=`, `=`

**Example:**
```javascript
// Original
counter += 1;

// Mutants
counter -= 1;  // Decrement instead
counter = 1;   // Assignment instead
```

**Test Strategy:**
- Verify accumulated values
- Check state after multiple operations
- Test compound assignment effects

### Remove Assignment

**Operator:** Remove variable assignments

**Mutations:**
- Remove assignment statement
- Keep right-hand side if it has side effects

**Example:**
```java
// Original
int total = calculateSum();

// Mutant
calculateSum();  // Assignment removed, call kept
```

**Test Strategy:**
- Verify variable has correct value
- Check that assignment happened
- Test variable usage downstream

## Constant Mutations

### Inline Constant Mutation

**Operator:** Modify constant values

**Mutations:**
- Numeric: `n` → `n+1`, `n-1`, `0`, `1`, `-1`
- Boolean: `true` ↔ `false`
- String: `"text"` → `""`, `null`
- Null: `null` → `new Object()`

**Example:**
```python
# Original
MAX_RETRIES = 3

# Mutants
MAX_RETRIES = 4   # Increment
MAX_RETRIES = 2   # Decrement
MAX_RETRIES = 0   # Zero
```

**Test Strategy:**
- Test with exact expected constants
- Verify magic numbers
- Check boundary values

## Statement Mutations

### Statement Deletion

**Operator:** Remove statements

**Mutations:**
- Remove non-void method calls
- Remove assignments
- Remove control flow statements

**Example:**
```java
// Original
public void process() {
    validate();
    transform();
    save();
}

// Mutant (transform removed)
public void process() {
    validate();
    // transform();  // Deleted
    save();
}
```

**Test Strategy:**
- Verify all steps executed
- Check intermediate state
- Test end-to-end behavior

### Statement Swap

**Operator:** Swap adjacent statements

**Mutations:**
- Swap order of independent statements

**Example:**
```python
# Original
x = calculate_x()
y = calculate_y()

# Mutant
y = calculate_y()
x = calculate_x()
```

**Test Strategy:**
- Verify order-dependent behavior
- Check for dependencies between statements
- Test state at each step

## Constructor Mutations

### Constructor Call Mutation

**Operator:** Modify constructor calls

**Mutations:**
- `new Object()` → `null`
- Change constructor arguments

**Example:**
```java
// Original
User user = new User(name, email);

// Mutant
User user = null;
```

**Test Strategy:**
- Verify object creation
- Check null handling
- Test constructor parameters

## Exception Mutations

### Exception Handler Removal

**Operator:** Remove exception handling

**Mutations:**
- Remove try-catch blocks
- Remove throw statements
- Change exception types

**Example:**
```javascript
// Original
try {
    riskyOperation();
} catch (error) {
    handleError(error);
}

// Mutant (catch removed)
riskyOperation();  // Exception propagates
```

**Test Strategy:**
- Verify exception handling
- Test error cases
- Check error recovery

## Language-Specific Operators

### Java-Specific

**Inline Constant Mutation:**
- `0` → `1`, `-1`
- `1` → `0`, `2`
- Empty string → non-empty

**Member Variable Mutation:**
- Change field access
- Modify visibility

### Python-Specific

**Decorator Removal:**
- Remove `@decorator`

**Slice Mutation:**
- `list[1:]` → `list[2:]`, `list[0:]`

### JavaScript-Specific

**Arrow Function Mutation:**
- `() => expr` → `() => undefined`

**Optional Chaining:**
- `obj?.prop` → `obj.prop`

### C/C++-Specific

**Pointer Mutation:**
- `*ptr` → `ptr`
- `&var` → `var`

**Bitwise Operators:**
- `<<` → `>>`
- `&` → `|`, `^`

## Mutation Operator Selection

**High-value operators** (kill these first):
1. Relational operators (boundary bugs common)
2. Return value mutations (direct output impact)
3. Logical operators (boolean logic errors)
4. Conditional mutations (control flow critical)

**Medium-value operators:**
1. Arithmetic operators
2. Assignment mutations
3. Statement deletions

**Low-value operators** (often equivalent):
1. Constant increments (may not change behavior)
2. Statement swaps (if independent)
3. Some unary operators

## Equivalent Mutant Patterns

Common patterns that produce equivalent mutants:

**Mathematical identities:**
- `x * 1` → `x`
- `x + 0` → `x`
- `x - 0` → `x`

**Logical identities:**
- `x && true` → `x`
- `x || false` → `x`

**Redundant operations:**
- Multiple assignments to same value
- Dead code mutations

**Commutative operations:**
- `a + b` → `b + a`
- `a * b` → `b * a`
- `a == b` → `b == a`
