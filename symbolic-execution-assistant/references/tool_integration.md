# Symbolic Execution Tool Integration

Setup and usage guides for popular symbolic execution tools.

## Table of Contents

1. [KLEE (C/C++)](#klee-cc)
2. [angr (Python/Binary)](#angr-pythonbinary)
3. [Symbolic PathFinder (Java)](#symbolic-pathfinder-java)
4. [Z3 (Constraint Solver)](#z3-constraint-solver)
5. [Crosshair (Python)](#crosshair-python)

---

## KLEE (C/C++)

### Overview

KLEE is a symbolic execution engine for LLVM bitcode. It can automatically generate test cases that achieve high code coverage.

### Installation

```bash
# Install dependencies
sudo apt-get install build-essential curl libcap-dev git cmake \
  libncurses5-dev python3-minimal python3-pip unzip libtcmalloc-minimal4 \
  libgoogle-perftools-dev libsqlite3-dev doxygen

# Install LLVM
sudo apt-get install llvm-13 llvm-13-dev llvm-13-tools

# Build KLEE
git clone https://github.com/klee/klee.git
cd klee
mkdir build
cd build
cmake ..
make
sudo make install
```

### Basic Usage

**1. Write code with symbolic inputs:**

```c
// example.c
#include <klee/klee.h>

int get_sign(int x) {
    if (x == 0)
        return 0;
    if (x < 0)
        return -1;
    else
        return 1;
}

int main() {
    int x;
    klee_make_symbolic(&x, sizeof(x), "x");
    return get_sign(x);
}
```

**2. Compile to LLVM bitcode:**

```bash
clang -I /path/to/klee/include -emit-llvm -c -g example.c -o example.bc
```

**3. Run KLEE:**

```bash
klee example.bc
```

**4. View results:**

```bash
# KLEE generates test cases in klee-out-N/
ls klee-last/

# View test inputs
ktest-tool klee-last/test000001.ktest

# Statistics
klee-stats klee-last/
```

### Advanced Options

```bash
# Set time limit
klee --max-time=60s example.bc

# Set memory limit
klee --max-memory=1024 example.bc

# Generate only failing tests
klee --emit-all-errors example.bc

# Use optimization
klee --optimize example.bc

# Limit solver time
klee --max-solver-time=5s example.bc
```

### Example: Finding Buffer Overflow

```c
#include <klee/klee.h>
#include <assert.h>

void process_array(int arr[], int size, int index) {
    // Potential buffer overflow
    int value = arr[index];
    assert(value >= 0);
}

int main() {
    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int index;

    klee_make_symbolic(&index, sizeof(index), "index");

    // Add assumption: index should be in valid range (but may not be)
    klee_assume(index >= -5);
    klee_assume(index <= 15);

    process_array(arr, 10, index);
    return 0;
}
```

**Run:**

```bash
clang -I /path/to/klee/include -emit-llvm -c -g overflow.c -o overflow.bc
klee overflow.bc
```

**KLEE will find:**
- Test cases where index < 0 (negative index)
- Test cases where index >= 10 (buffer overflow)

---

## angr (Python/Binary)

### Overview

angr is a Python framework for analyzing binaries. It supports symbolic execution, control flow analysis, and vulnerability finding.

### Installation

```bash
pip install angr
```

### Basic Usage

**1. Load binary:**

```python
import angr

# Load binary
project = angr.Project('./binary')

# Create initial state
state = project.factory.entry_state()

# Create simulation manager
simgr = project.factory.simulation_manager(state)
```

**2. Explore paths:**

```python
# Explore until finding target address
target_addr = 0x400600
simgr.explore(find=target_addr)

# Check if target was found
if simgr.found:
    found_state = simgr.found[0]
    print(f"Found target! Input: {found_state.posix.dumps(0)}")
```

**3. Symbolic execution:**

```python
import angr
import claripy

# Create project
project = angr.Project('./binary', auto_load_libs=False)

# Create symbolic input
flag = claripy.BVS('flag', 8 * 32)  # 32 bytes

# Create initial state with symbolic stdin
state = project.factory.entry_state(stdin=flag)

# Add constraints (e.g., printable ASCII)
for byte in flag.chop(8):
    state.solver.add(byte >= 0x20)
    state.solver.add(byte <= 0x7e)

# Create simulation manager
simgr = project.factory.simulation_manager(state)

# Explore
simgr.explore(find=lambda s: b"SUCCESS" in s.posix.dumps(1))

if simgr.found:
    solution = simgr.found[0].solver.eval(flag, cast_to=bytes)
    print(f"Solution: {solution}")
```

### Example: Finding Correct Password

```python
import angr
import claripy

def find_password(binary_path):
    # Load binary
    project = angr.Project(binary_path, auto_load_libs=False)

    # Create symbolic password (max 20 bytes)
    password = claripy.BVS('password', 8 * 20)

    # Initial state with symbolic stdin
    state = project.factory.entry_state(stdin=password)

    # Constrain to printable ASCII
    for byte in password.chop(8):
        state.solver.add(claripy.And(byte >= 0x20, byte <= 0x7e))

    # Simulation manager
    simgr = project.factory.simulation_manager(state)

    # Explore until "Correct!" message
    simgr.explore(find=lambda s: b"Correct!" in s.posix.dumps(1),
                  avoid=lambda s: b"Wrong!" in s.posix.dumps(1))

    if simgr.found:
        found = simgr.found[0]
        password_solution = found.solver.eval(password, cast_to=bytes)
        print(f"Password: {password_solution.decode().strip()}")
    else:
        print("No solution found")

find_password('./password_checker')
```

### Hook Functions

```python
import angr

project = angr.Project('./binary')

# Hook a function to replace its implementation
@project.hook(0x400500)
def custom_malloc(state):
    # Custom malloc implementation
    size = state.solver.eval(state.regs.rdi)
    addr = state.heap.allocate(size)
    state.regs.rax = addr

# Or use angr's built-in hooks
project.hook_symbol('printf', angr.SIM_PROCEDURES['libc']['printf']())
```

---

## Symbolic PathFinder (Java)

### Overview

Symbolic PathFinder (SPF) extends Java PathFinder with symbolic execution capabilities for Java programs.

### Installation

**1. Install JPF core:**

```bash
git clone https://github.com/javapathfinder/jpf-core.git
cd jpf-core
./gradlew build
```

**2. Install SPF:**

```bash
git clone https://github.com/SymbolicPathFinder/jpf-symbc.git
cd jpf-symbc
./gradlew build
```

**3. Configure site.properties:**

```properties
# ~/.jpf/site.properties
jpf-core = /path/to/jpf-core
jpf-symbc = /path/to/jpf-symbc
```

### Basic Usage

**1. Write Java code:**

```java
public class Example {
    public static int compute(int x, int y) {
        int result;
        if (x > y) {
            result = x + y;
        } else {
            result = x - y;
        }
        return result;
    }

    public static void main(String[] args) {
        int x = Debug.makeSymbolicInteger("x");
        int y = Debug.makeSymbolicInteger("y");
        int result = compute(x, y);
    }
}
```

**2. Create JPF configuration (.jpf file):**

```properties
# example.jpf
target = Example
classpath = ${jpf-symbc}/build/examples
sourcepath = ${jpf-symbc}/src/examples

symbolic.method = Example.compute(sym#sym)
symbolic.min_int = -100
symbolic.max_int = 100

listener = gov.nasa.jpf.symbc.SymbolicListener
```

**3. Run SPF:**

```bash
jpf example.jpf
```

### Example: Finding Null Pointer Exception

```java
public class NullCheck {
    public static int getLength(String str) {
        if (str != null) {
            return str.length();
        }
        return 0;
    }

    public static void main(String[] args) {
        String str = Debug.makeSymbolicString("str");
        int length = getLength(str);
        Debug.printSymbolicConstraints();
    }
}
```

**Configuration:**

```properties
target = NullCheck
symbolic.method = NullCheck.getLength(sym)
symbolic.string_dp = choco

listener = gov.nasa.jpf.symbc.SymbolicListener
```

---

## Z3 (Constraint Solver)

See [constraint_solving.md](constraint_solving.md) for comprehensive Z3 usage.

### Quick Reference

```python
from z3 import *

# Create solver
solver = Solver()

# Add constraints
x = Int('x')
solver.add(x > 0)
solver.add(x < 10)

# Solve
if solver.check() == sat:
    print(solver.model())
```

---

## Crosshair (Python)

### Overview

Crosshair uses symbolic execution to test Python functions.

### Installation

```bash
pip install crosshair-tool
```

### Basic Usage

**1. Add assertions to code:**

```python
def divide(a: int, b: int) -> float:
    """
    Divide two numbers.

    pre: b != 0
    post: _ * b == a
    """
    return a / b
```

**2. Run Crosshair:**

```bash
crosshair check mymodule.py
```

**3. Watch mode (continuous checking):**

```bash
crosshair watch mymodule.py
```

### Example: Finding Bugs

```python
def process_list(items: list) -> int:
    """
    Process a list and return the first positive item.

    pre: len(items) > 0
    post: _ > 0
    """
    for item in items:
        if item > 0:
            return item
    return 0  # BUG: violates postcondition if no positive items
```

**Crosshair will find:**
```
AssertionError: postcondition failed
Counterexample: items = [0]
```

### Preconditions and Postconditions

```python
def search(arr: list[int], target: int) -> int:
    """
    Binary search.

    pre: all(arr[i] <= arr[i+1] for i in range(len(arr)-1))  # Sorted
    post: _ == -1 or arr[_] == target
    """
    # Implementation
    ...
```

---

## Tool Comparison

| Tool | Language | Strength | Limitation |
|------|----------|----------|------------|
| KLEE | C/C++ | High coverage, finds deep bugs | Requires LLVM bitcode |
| angr | Binary | Works on binaries, no source needed | Slower than source-based tools |
| SPF | Java | Integrated with Java ecosystem | Setup complexity |
| Z3 | Any (manual) | Precise constraint solving | Requires manual analysis |
| Crosshair | Python | Easy to use, Pythonic | Limited to Python |

---

## General Tips

1. **Start with simple tools**: Z3 for manual analysis, Crosshair for Python
2. **Use KLEE for C**: Best coverage and bug-finding for C programs
3. **angr for binaries**: When source code unavailable
4. **SPF for Java**: Integrates well with Java testing frameworks
5. **Combine tools**: Use Z3 for constraint solving alongside other tools
6. **Set limits**: Time and memory limits prevent infinite exploration
7. **Focus exploration**: Target specific functions or code sections
8. **Validate results**: Always verify tool-generated test cases
