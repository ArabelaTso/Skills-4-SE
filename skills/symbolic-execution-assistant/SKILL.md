---
name: symbolic-execution-assistant
description: >
  Performs symbolic execution to detect potential errors by exploring execution paths, solving
  path constraints, and generating test inputs. Use when you need to analyze code for bugs like
  null dereferences, division by zero, buffer overflows, or assertion violations. Also use to
  generate test inputs that exercise different code paths, find edge cases, or explore all
  reachable program states. Supports Python, Java, and C/C++ through manual symbolic execution
  techniques and integration with tools like KLEE, angr, Z3, and Symbolic PathFinder.
---

# Symbolic Execution Assistant

Perform symbolic execution analysis to detect errors and generate test inputs by exploring program paths with symbolic variables.

## What is Symbolic Execution?

Symbolic execution executes code with **symbolic values** (representing any possible value) instead of concrete values. This allows exploring multiple execution paths simultaneously and detecting errors that might only occur with specific inputs.

**Key Concepts:**
- **Symbolic variables**: Variables with unknown values (e.g., α, β instead of 5, 10)
- **Path constraints**: Conditions accumulated along each execution path
- **Path explosion**: Number of paths grows exponentially with branches
- **Constraint solver**: Tool (like Z3) that finds concrete values satisfying constraints

## Workflow

### Step 1: Identify the Function to Analyze

Select the function and determine what to analyze for.

**Questions to ask:**
- What bugs might this function have? (null refs, div by zero, overflows, assertions)
- What inputs could trigger errors?
- Which execution paths are critical?
- Are there complex conditionals that need exploration?

**Example:**

```python
def calculate_discount(price, customer_type):
    """Calculate discount based on customer type."""
    if customer_type == "premium":
        discount = price * 0.2
    elif customer_type == "regular":
        discount = price * 0.1
    else:
        discount = 0

    final_price = price - discount
    return final_price
```

**Analysis goals:**
- Explore all three branches (premium, regular, other)
- Check for potential arithmetic errors
- Generate test inputs for each path

### Step 2: Set Up Symbolic Variables

Replace concrete inputs with symbolic variables.

**Manual Symbolic Execution:**

```
Input: price = α (symbolic), customer_type = β (symbolic)
Initial constraints: α ∈ ℝ, β ∈ String
Initial state: { price: α, customer_type: β }
```

**Using Python with Z3:**

```python
from z3 import *

# Create symbolic variables
price = Real('price')
customer_type = String('customer_type')

# Create solver
solver = Solver()
```

**Using Java with Symbolic PathFinder (SPF):**

```java
// Annotate symbolic inputs
public static void calculate_discount(double price, String customer_type) {
    // SPF will make these symbolic via configuration
}
```

**Using C with KLEE:**

```c
#include <klee/klee.h>

int main() {
    float price;
    char customer_type[20];

    klee_make_symbolic(&price, sizeof(price), "price");
    klee_make_symbolic(customer_type, sizeof(customer_type), "customer_type");

    calculate_discount(price, customer_type);
    return 0;
}
```

### Step 3: Execute Symbolically and Build Path Tree

Trace through code, tracking constraints for each branch.

**Manual Execution Example:**

```
State 0: { price: α, customer_type: β }
Path constraint: (none)

Branch 1: customer_type == "premium"
  State 1a: { discount: α * 0.2, final_price: α - (α * 0.2) }
  Path constraint: β = "premium"

Branch 2: customer_type == "regular"
  State 1b: { discount: α * 0.1, final_price: α - (α * 0.1) }
  Path constraint: β ≠ "premium" ∧ β = "regular"

Branch 3: else
  State 1c: { discount: 0, final_price: α }
  Path constraint: β ≠ "premium" ∧ β ≠ "regular"
```

**Path Tree Visualization:**

```
                    [Initial State]
                     price = α
                  customer_type = β
                         |
        +----------------+----------------+
        |                |                |
  β = "premium"    β = "regular"      else
        |                |                |
  discount=α*0.2   discount=α*0.1    discount=0
  Path 1           Path 2            Path 3
```

For detailed path tree construction techniques, see [references/path_exploration.md](references/path_exploration.md).

### Step 4: Identify Error Conditions

Look for states where errors could occur.

**Common Error Patterns:**

| Error Type | Check For | Example Constraint |
|------------|-----------|-------------------|
| Division by zero | denominator == 0 | x / y where y = 0 |
| Null dereference | variable == null | obj.method() where obj = null |
| Buffer overflow | index >= array.length | arr[i] where i ≥ len(arr) |
| Assertion violation | assertion condition false | assert x > 0 where x ≤ 0 |
| Integer overflow | result > MAX_INT | a + b > 2³¹-1 |
| Negative array index | index < 0 | arr[i] where i < 0 |

**Example with Division by Zero:**

```python
def safe_divide(a, b):
    if b != 0:
        return a / b
    else:
        return None
```

**Symbolic execution:**
```
State 0: { a: α, b: β }

Branch 1: b != 0
  Path constraint: β ≠ 0
  Result: α / β (safe)

Branch 2: b == 0
  Path constraint: β = 0
  Result: None (safe)

ERROR CHECK: Division by zero?
  Constraint: β = 0 AND execution reaches "a / b"
  Result: NO (the if-check prevents it)
```

**Example with Null Dereference:**

```java
public int getLength(String str) {
    if (str != null) {
        return str.length();
    }
    return 0;
}
```

**Symbolic execution:**
```
State 0: { str: α }

Branch 1: str != null
  Path constraint: α ≠ null
  Result: α.length() (safe)

Branch 2: str == null
  Path constraint: α = null
  Result: 0 (safe)

ERROR CHECK: Null dereference?
  Constraint: α = null AND execution reaches str.length()
  Result: NO (protected by null check)
```

### Step 5: Solve Constraints for Test Inputs

Use constraint solver to find concrete values that exercise each path or trigger errors.

**Manual Constraint Solving:**

For simple constraints, solve manually:
```
Path 1 constraint: β = "premium"
Solution: price = 100, customer_type = "premium"

Path 2 constraint: β ≠ "premium" ∧ β = "regular"
Solution: price = 100, customer_type = "regular"

Path 3 constraint: β ≠ "premium" ∧ β ≠ "regular"
Solution: price = 100, customer_type = "guest"
```

**Using Z3 Solver (Python):**

```python
from z3 import *

# Define symbolic variables
price = Real('price')
customer_type = String('customer_type')

# Solve for Path 1: premium customer
solver = Solver()
solver.add(customer_type == StringVal("premium"))
solver.add(price > 0)  # Add reasonable constraints

if solver.check() == sat:
    model = solver.model()
    print(f"Test input for Path 1: price={model[price]}, customer_type={model[customer_type]}")

# Solve for Path 2: regular customer
solver2 = Solver()
solver2.add(customer_type == StringVal("regular"))
solver2.add(price > 0)

if solver2.check() == sat:
    model = solver2.model()
    print(f"Test input for Path 2: price={model[price]}, customer_type={model[customer_type]}")
```

**Using Z3 for Error Detection:**

```python
# Check for division by zero
a = Int('a')
b = Int('b')

solver = Solver()
solver.add(b == 0)  # Error condition: divisor is zero
solver.add(a > 0)   # Additional context

if solver.check() == sat:
    model = solver.model()
    print(f"ERROR: Division by zero possible with a={model[a]}, b={model[b]}")
```

For comprehensive constraint solving techniques, see [references/constraint_solving.md](references/constraint_solving.md).

### Step 6: Generate Test Cases

Convert solved constraints into executable test cases.

**Test Case Template:**

```python
import pytest

class TestCalculateDiscount:
    # Path 1: Premium customer
    def test_premium_customer(self):
        """Test premium customer path."""
        # Generated from constraint: customer_type = "premium"
        result = calculate_discount(100, "premium")
        assert result == 80  # 100 - 20% discount

    # Path 2: Regular customer
    def test_regular_customer(self):
        """Test regular customer path."""
        # Generated from constraint: customer_type = "regular"
        result = calculate_discount(100, "regular")
        assert result == 90  # 100 - 10% discount

    # Path 3: Other customer type
    def test_other_customer(self):
        """Test other customer type path."""
        # Generated from constraint: customer_type ∉ {"premium", "regular"}
        result = calculate_discount(100, "guest")
        assert result == 100  # No discount
```

**Java Test Cases:**

```java
import org.junit.Test;
import static org.junit.Assert.*;

public class TestCalculateDiscount {
    @Test
    public void testPremiumCustomer() {
        // Path 1: Premium customer
        double result = calculateDiscount(100.0, "premium");
        assertEquals(80.0, result, 0.01);
    }

    @Test
    public void testRegularCustomer() {
        // Path 2: Regular customer
        double result = calculateDiscount(100.0, "regular");
        assertEquals(90.0, result, 0.01);
    }

    @Test
    public void testOtherCustomer() {
        // Path 3: Other customer
        double result = calculateDiscount(100.0, "guest");
        assertEquals(100.0, result, 0.01);
    }
}
```

### Step 7: Report Findings

Document discovered paths, errors, and generated tests.

**Report Template:**

```markdown
# Symbolic Execution Report: calculate_discount

## Function Analyzed
`calculate_discount(price, customer_type)`

## Paths Discovered
- **Path 1**: Premium customer (customer_type = "premium")
  - Constraint: β = "premium"
  - Behavior: 20% discount applied
  - Test input: price=100, customer_type="premium"

- **Path 2**: Regular customer (customer_type = "regular")
  - Constraint: β ≠ "premium" ∧ β = "regular"
  - Behavior: 10% discount applied
  - Test input: price=100, customer_type="regular"

- **Path 3**: Other customer types
  - Constraint: β ∉ {"premium", "regular"}
  - Behavior: No discount
  - Test input: price=100, customer_type="guest"

## Errors Detected
None. All paths are safe.

## Generated Test Cases
3 test cases generated (see test_calculate_discount.py)

## Coverage
- Branch coverage: 100% (all 3 branches)
- Path coverage: 100% (all 3 paths)

## Recommendations
- Consider validating customer_type against known values
- Add explicit error handling for negative prices
```

## Symbolic Execution Tools

### Python Tools

**Z3 Theorem Prover:**
```bash
pip install z3-solver
```

**angr (Binary Analysis Framework):**
```bash
pip install angr
```

**Crosshair (Symbolic Testing):**
```bash
pip install crosshair-tool
```

### Java Tools

**Symbolic PathFinder (SPF):**
- Extension of Java PathFinder
- Symbolic execution for Java bytecode
- Configuration via .jpf files

**JDart:**
- Dynamic symbolic execution for Java
- Integrates with DART framework

### C/C++ Tools

**KLEE:**
```bash
# Uses LLVM bitcode
clang -emit-llvm -c program.c -o program.bc
klee program.bc
```

**Symbolic Execution Engine (SEE):**
- Symbolic execution for C programs
- Built on top of LLVM

For detailed tool setup and usage, see [references/tool_integration.md](references/tool_integration.md).

## Handling Path Explosion

Path explosion occurs when the number of paths grows exponentially.

**Mitigation Strategies:**

1. **Bounded Execution**: Limit search depth
   ```python
   # Limit loop iterations
   for i in range(min(len(array), 10)):  # Max 10 iterations
       process(array[i])
   ```

2. **Path Pruning**: Eliminate infeasible paths early
   ```python
   if not is_feasible(path_constraint):
       prune_path()
   ```

3. **State Merging**: Combine similar states
   ```python
   # Merge states with same program counter
   if state1.pc == state2.pc:
       merged_state = merge(state1, state2)
   ```

4. **Selective Exploration**: Focus on critical paths
   ```python
   # Prioritize paths with error conditions
   if contains_error_check(path):
       explore_first(path)
   ```

5. **Concolic Execution**: Mix concrete and symbolic execution
   ```python
   # Start with concrete value, switch to symbolic when needed
   x = 5  # Concrete initially
   if complex_condition(x):
       x = make_symbolic(x)  # Switch to symbolic
   ```

## Tips

1. **Start small**: Analyze simple functions before complex ones
2. **Focus on critical code**: Prioritize security-sensitive or error-prone code
3. **Use tools when possible**: Manual symbolic execution is labor-intensive
4. **Set time limits**: Path explosion can make analysis impractical
5. **Combine techniques**: Use both manual analysis and automated tools
6. **Validate generated tests**: Ensure tests actually run and make sense
7. **Document assumptions**: Note any simplifications or constraints

## Common Use Cases

**1. Bug Detection**
- Find null pointer dereferences
- Detect division by zero
- Identify buffer overflows
- Catch assertion violations

**2. Test Generation**
- Generate inputs for full path coverage
- Create edge case tests
- Produce regression test suites

**3. Security Analysis**
- Find exploitable vulnerabilities
- Detect integer overflows
- Identify injection points

**4. Equivalence Checking**
- Verify refactored code behaves identically
- Check optimization correctness

## References

For detailed information on specific topics:
- [references/path_exploration.md](references/path_exploration.md) - Path tree construction and exploration strategies
- [references/constraint_solving.md](references/constraint_solving.md) - Z3 solver usage and constraint patterns
- [references/tool_integration.md](references/tool_integration.md) - Setup and usage of KLEE, angr, SPF, and other tools
