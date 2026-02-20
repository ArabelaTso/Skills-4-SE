# Constraint Solving with Z3

Comprehensive guide to using Z3 theorem prover for symbolic execution.

## Table of Contents

1. [Z3 Basics](#z3-basics)
2. [Variable Types](#variable-types)
3. [Constraint Patterns](#constraint-patterns)
4. [Solving Techniques](#solving-techniques)
5. [Advanced Features](#advanced-features)

---

## Z3 Basics

### Installation

```bash
pip install z3-solver
```

### Basic Workflow

```python
from z3 import *

# 1. Create variables
x = Int('x')
y = Int('y')

# 2. Create solver
solver = Solver()

# 3. Add constraints
solver.add(x > 0)
solver.add(y < 10)
solver.add(x + y == 15)

# 4. Check satisfiability
if solver.check() == sat:
    model = solver.model()
    print(f"x = {model[x]}")
    print(f"y = {model[y]}")
else:
    print("Unsatisfiable")
```

---

## Variable Types

### Integer Variables

```python
x = Int('x')
y = Int('y')

solver = Solver()
solver.add(x + y == 10)
solver.add(x > y)

if solver.check() == sat:
    m = solver.model()
    print(f"x={m[x]}, y={m[y]}")  # e.g., x=6, y=4
```

### Real (Floating Point) Variables

```python
price = Real('price')
discount = Real('discount')

solver = Solver()
solver.add(price > 0)
solver.add(discount >= 0)
solver.add(discount <= price)
solver.add(price - discount == 50)

if solver.check() == sat:
    m = solver.model()
    print(f"price={m[price]}, discount={m[discount]}")
```

### Boolean Variables

```python
is_premium = Bool('is_premium')
has_coupon = Bool('has_coupon')

solver = Solver()
solver.add(Or(is_premium, has_coupon))  # At least one true
solver.add(Not(And(is_premium, has_coupon)))  # Not both

if solver.check() == sat:
    m = solver.model()
    print(f"is_premium={m[is_premium]}, has_coupon={m[has_coupon]}")
```

### String Variables

```python
username = String('username')
password = String('password')

solver = Solver()
solver.add(Length(username) >= 3)
solver.add(Length(password) >= 8)
solver.add(Contains(password, StringVal("@")))

if solver.check() == sat:
    m = solver.model()
    print(f"username={m[username]}, password={m[password]}")
```

### Array Variables

```python
arr = Array('arr', IntSort(), IntSort())  # int[] in Java
i = Int('i')

solver = Solver()
solver.add(arr[0] == 5)
solver.add(arr[1] == 10)
solver.add(Select(arr, i) == 10)  # arr[i] == 10

if solver.check() == sat:
    m = solver.model()
    print(f"i={m[i]}")  # i=1
```

---

## Constraint Patterns

### Range Constraints

```python
x = Int('x')

# Bounded range
solver.add(x >= 0)
solver.add(x <= 100)

# Or more concisely
solver.add(And(x >= 0, x <= 100))
```

### Conditional Constraints

```python
x = Int('x')
y = Int('y')
result = Int('result')

# If-then-else
solver.add(result == If(x > 0, y + 10, y - 10))

# Equivalent to:
# if x > 0:
#     result = y + 10
# else:
#     result = y - 10
```

### Multiple Paths

```python
x = Int('x')
output = Int('output')

# Path 1: x < 0
solver1 = Solver()
solver1.add(x < 0)
solver1.add(output == -x)

# Path 2: x >= 0
solver2 = Solver()
solver2.add(x >= 0)
solver2.add(output == x)
```

### Disjunctions (OR)

```python
x = Int('x')

# x is either negative or greater than 100
solver.add(Or(x < 0, x > 100))

# x is 5, 10, or 15
solver.add(Or(x == 5, x == 10, x == 15))
```

### Negations

```python
x = Int('x')

# x is NOT between 10 and 20
solver.add(Not(And(x >= 10, x <= 20)))

# Equivalent to: x < 10 OR x > 20
```

---

## Solving Techniques

### Basic Solving

```python
solver = Solver()
solver.add(x > 0)
solver.add(x < 10)

result = solver.check()
if result == sat:
    print("Satisfiable")
    model = solver.model()
    print(model)
elif result == unsat:
    print("Unsatisfiable")
else:
    print("Unknown")
```

### Multiple Solutions

```python
x = Int('x')
y = Int('y')

solver = Solver()
solver.add(x + y == 10)
solver.add(x > 0)
solver.add(y > 0)

solutions = []
for _ in range(5):  # Find 5 solutions
    if solver.check() == sat:
        m = solver.model()
        x_val = m[x].as_long()
        y_val = m[y].as_long()
        solutions.append((x_val, y_val))

        # Block this solution
        solver.add(Or(x != x_val, y != y_val))
    else:
        break

print(solutions)  # [(1,9), (2,8), (3,7), (4,6), (5,5)]
```

### Incremental Solving

```python
solver = Solver()

# Add permanent constraints
solver.add(x > 0)
solver.add(y > 0)

# Try different additional constraints
solver.push()  # Save state
solver.add(x + y == 10)
if solver.check() == sat:
    print(solver.model())
solver.pop()  # Restore state

solver.push()
solver.add(x + y == 20)
if solver.check() == sat:
    print(solver.model())
solver.pop()
```

### Unsatisfiable Core

Find minimal set of constraints that cause unsatisfiability.

```python
x = Int('x')

c1 = x > 10
c2 = x < 5
c3 = x >= 0

solver = Solver()
solver.add(c1)
solver.add(c2)
solver.add(c3)

if solver.check() == unsat:
    core = solver.unsat_core()
    print(f"Unsatisfiable core: {core}")
```

---

## Advanced Features

### Quantifiers

```python
x = Int('x')

# Universal quantification: ∀x. x > 0 → x^2 > 0
solver.add(ForAll([x], Implies(x > 0, x*x > 0)))

# Existential quantification: ∃x. x > 0 ∧ x < 10
solver.add(Exists([x], And(x > 0, x < 10)))
```

### Optimization

Find maximum/minimum values.

```python
from z3 import Optimize

x = Int('x')
y = Int('y')

opt = Optimize()
opt.add(x + y <= 10)
opt.add(x >= 0)
opt.add(y >= 0)

# Maximize x + y
opt.maximize(x + y)

if opt.check() == sat:
    m = opt.model()
    print(f"Optimal: x={m[x]}, y={m[y]}")
```

### Theories

**Bit-Vectors:**

```python
x = BitVec('x', 32)  # 32-bit integer
y = BitVec('y', 32)

solver = Solver()
solver.add(x + y == 0xFFFFFFFF)  # Check for overflow
```

**Arrays:**

```python
arr = Array('arr', IntSort(), IntSort())
i = Int('i')
j = Int('j')

solver.add(arr[i] > arr[j])
solver.add(i < j)
solver.add(i >= 0)
solver.add(j < 10)
```

---

## Complete Examples

### Example 1: Finding Division by Zero

```python
from z3 import *

def find_division_by_zero():
    """Find inputs that cause division by zero."""
    a = Int('a')
    b = Int('b')
    c = Int('c')

    # Code: result = a / (b - c)
    solver = Solver()

    # Error condition: denominator is zero
    solver.add(b - c == 0)

    # Additional constraints
    solver.add(a > 0)
    solver.add(b >= 0)
    solver.add(c >= 0)

    if solver.check() == sat:
        m = solver.model()
        print("ERROR: Division by zero possible!")
        print(f"  a={m[a]}, b={m[b]}, c={m[c]}")
        return True
    else:
        print("Safe: No division by zero")
        return False

find_division_by_zero()
# Output: ERROR: Division by zero possible!
#         a=1, b=5, c=5
```

### Example 2: Buffer Overflow Detection

```python
from z3 import *

def find_buffer_overflow():
    """Find array index that causes overflow."""
    arr_size = 10
    index = Int('index')
    value = Int('value')

    solver = Solver()

    # Error condition: index out of bounds
    solver.add(Or(index < 0, index >= arr_size))

    # Additional constraints from code
    solver.add(value > 0)
    solver.add(index == value - 1)

    if solver.check() == sat:
        m = solver.model()
        print("ERROR: Buffer overflow possible!")
        print(f"  index={m[index]}, value={m[value]}")
        return True
    else:
        print("Safe: No buffer overflow")
        return False

find_buffer_overflow()
```

### Example 3: Path Constraint Solving

```python
from z3 import *

def solve_path_constraints():
    """Solve constraints for all paths through code."""

    # Code:
    # if x > 0:
    #     if y > 10:
    #         result = x + y
    #     else:
    #         result = x - y
    # else:
    #     result = 0

    x = Int('x')
    y = Int('y')
    result = Int('result')

    paths = [
        ("Path 1: x>0, y>10", [x > 0, y > 10, result == x + y]),
        ("Path 2: x>0, y<=10", [x > 0, y <= 10, result == x - y]),
        ("Path 3: x<=0", [x <= 0, result == 0])
    ]

    for path_name, constraints in paths:
        solver = Solver()
        solver.add(constraints)

        if solver.check() == sat:
            m = solver.model()
            print(f"{path_name}")
            print(f"  x={m[x]}, y={m[y]}, result={m[result]}")
        else:
            print(f"{path_name}: Infeasible")

solve_path_constraints()
```

### Example 4: String Constraints

```python
from z3 import *

def validate_input():
    """Find inputs that satisfy validation rules."""
    username = String('username')
    password = String('password')

    solver = Solver()

    # Validation rules
    solver.add(Length(username) >= 3)
    solver.add(Length(username) <= 20)
    solver.add(Length(password) >= 8)
    solver.add(Contains(password, StringVal("@")))
    solver.add(Contains(password, StringVal("1")))

    if solver.check() == sat:
        m = solver.model()
        print("Valid input found:")
        print(f"  username={m[username]}")
        print(f"  password={m[password]}")

validate_input()
```

---

## Tips

1. **Start simple**: Begin with basic constraints, add complexity gradually
2. **Use appropriate types**: Int for integers, Real for floats, String for text
3. **Check satisfiability**: Always check if solver.check() == sat before accessing model
4. **Add bounds**: Constrain variables to reasonable ranges to speed up solving
5. **Incremental solving**: Use push/pop for trying different constraint sets
6. **Multiple solutions**: Block previous solutions to find alternatives
7. **Debugging**: Print constraints with `print(solver)` to see what you're solving
8. **Performance**: Simpler constraints solve faster; avoid unnecessary quantifiers

---

## Common Patterns

### Pattern: Explore All Branches

```python
def explore_branches(conditions):
    """Generate test inputs for all branch combinations."""
    for i, condition_set in enumerate(conditions):
        solver = Solver()
        solver.add(condition_set)

        if solver.check() == sat:
            print(f"Branch {i}: {solver.model()}")
```

### Pattern: Find Error Inputs

```python
def find_error(error_condition, context_constraints):
    """Find inputs that trigger an error."""
    solver = Solver()
    solver.add(error_condition)
    solver.add(context_constraints)

    if solver.check() == sat:
        return solver.model()
    return None
```

### Pattern: Verify Safety

```python
def verify_safe(safety_property, all_paths):
    """Verify safety property holds on all paths."""
    for path_constraints in all_paths:
        solver = Solver()
        solver.add(path_constraints)
        solver.add(Not(safety_property))  # Negate property

        if solver.check() == sat:
            print(f"VIOLATION: {solver.model()}")
            return False

    print("SAFE: Property holds on all paths")
    return True
```
