---
name: code-instrumentation-generator
description: "Automatically instruments source code to collect runtime information such as function calls, branch decisions, variable values, and execution traces while preserving original program semantics. Use when users need to: (1) Add logging or tracing to code for debugging, (2) Collect runtime execution data for analysis, (3) Monitor function calls and control flow, (4) Track variable values during execution, (5) Generate execution traces for testing or profiling. Supports Python, Java, JavaScript, and C/C++ with configurable instrumentation levels."
---

# Code Instrumentation Generator

Automatically instrument source code to collect runtime information while preserving program semantics.

## Workflow

Follow these steps to instrument code:

### 1. Analyze the Source Code

Understand the code structure and identify instrumentation points:

- **Language detection**: Identify the programming language
- **Code structure**: Parse functions, classes, branches, loops
- **Entry/exit points**: Locate function boundaries
- **Control flow**: Identify branches (if/else, switch, loops)
- **Variable scope**: Understand variable declarations and usage

### 2. Determine Instrumentation Strategy

Choose appropriate instrumentation based on requirements:

**Instrumentation levels:**
- **Function-level**: Entry/exit of functions with parameters and return values
- **Branch-level**: Execution of conditional branches (if/else, switch cases)
- **Statement-level**: Individual statement execution
- **Variable-level**: Variable assignments and value changes

**Configuration options:**
- Enable/disable specific instrumentation types
- Filter by function names or file patterns
- Set verbosity level
- Choose output format (logs, JSON, CSV)

### 3. Insert Instrumentation Code

Add instrumentation hooks at identified points:

**Function instrumentation:**
- Insert entry hook at function start
- Capture function name, parameters, timestamp
- Insert exit hook before returns
- Capture return value, execution time

**Branch instrumentation:**
- Insert hooks at branch conditions
- Record which branch was taken
- Track branch coverage

**Variable instrumentation:**
- Insert hooks after variable assignments
- Capture variable name and value
- Track value changes over time

### 4. Ensure Semantic Preservation

Verify that instrumentation doesn't change program behavior:

- **No side effects**: Instrumentation code doesn't modify program state
- **Exception safety**: Instrumentation handles exceptions properly
- **Performance**: Minimal overhead added
- **Thread safety**: Instrumentation is safe in concurrent code

### 5. Generate Output

Provide instrumented code and documentation:

- **Instrumented source code**: Modified code with instrumentation
- **Probe description**: Documentation of inserted instrumentation points
- **Configuration file**: Settings to enable/disable instrumentation
- **Usage instructions**: How to run and collect data

## Language-Specific Patterns

### Python

```python
# Original code
def calculate_sum(a, b):
    result = a + b
    return result

# Instrumented code
import logging
logging.basicConfig(level=logging.INFO)

def calculate_sum(a, b):
    # Function entry instrumentation
    logging.info(f"ENTER calculate_sum(a={a}, b={b})")

    result = a + b
    # Variable instrumentation
    logging.info(f"VAR result={result}")

    # Function exit instrumentation
    logging.info(f"EXIT calculate_sum() -> {result}")
    return result
```

### Java

```java
// Original code
public int calculateSum(int a, int b) {
    int result = a + b;
    return result;
}

// Instrumented code
public int calculateSum(int a, int b) {
    // Function entry instrumentation
    System.out.println("ENTER calculateSum(a=" + a + ", b=" + b + ")");

    int result = a + b;
    // Variable instrumentation
    System.out.println("VAR result=" + result);

    // Function exit instrumentation
    System.out.println("EXIT calculateSum() -> " + result);
    return result;
}
```

### JavaScript

```javascript
// Original code
function calculateSum(a, b) {
    const result = a + b;
    return result;
}

// Instrumented code
function calculateSum(a, b) {
    // Function entry instrumentation
    console.log(`ENTER calculateSum(a=${a}, b=${b})`);

    const result = a + b;
    // Variable instrumentation
    console.log(`VAR result=${result}`);

    // Function exit instrumentation
    console.log(`EXIT calculateSum() -> ${result}`);
    return result;
}
```

### C/C++

```c
// Original code
int calculate_sum(int a, int b) {
    int result = a + b;
    return result;
}

// Instrumented code
#include <stdio.h>

int calculate_sum(int a, int b) {
    // Function entry instrumentation
    printf("ENTER calculate_sum(a=%d, b=%d)\n", a, b);

    int result = a + b;
    // Variable instrumentation
    printf("VAR result=%d\n", result);

    // Function exit instrumentation
    printf("EXIT calculate_sum() -> %d\n", result);
    return result;
}
```

## Branch Instrumentation Example

```python
# Original code
def check_value(x):
    if x > 0:
        return "positive"
    else:
        return "non-positive"

# Instrumented code
def check_value(x):
    logging.info(f"ENTER check_value(x={x})")

    # Branch instrumentation
    if x > 0:
        logging.info("BRANCH if(x > 0) -> TRUE")
        result = "positive"
    else:
        logging.info("BRANCH if(x > 0) -> FALSE")
        result = "non-positive"

    logging.info(f"EXIT check_value() -> {result}")
    return result
```

## Configuration-Based Instrumentation

Generate a configuration file to control instrumentation:

```python
# instrumentation_config.py
INSTRUMENTATION_ENABLED = True
INSTRUMENT_FUNCTIONS = True
INSTRUMENT_BRANCHES = True
INSTRUMENT_VARIABLES = False
LOG_LEVEL = "INFO"
OUTPUT_FORMAT = "text"  # or "json", "csv"

# Instrumented code with configuration
import instrumentation_config as config

def calculate_sum(a, b):
    if config.INSTRUMENT_FUNCTIONS:
        logging.info(f"ENTER calculate_sum(a={a}, b={b})")

    result = a + b

    if config.INSTRUMENT_VARIABLES:
        logging.info(f"VAR result={result}")

    if config.INSTRUMENT_FUNCTIONS:
        logging.info(f"EXIT calculate_sum() -> {result}")

    return result
```

## Output Format

### Probe Description Document

```markdown
## Instrumentation Report

**File**: calculator.py
**Instrumentation Date**: 2024-02-17
**Configuration**: Function-level + Branch-level

### Instrumented Functions

1. **calculate_sum(a, b)**
   - Entry probe: Line 3
   - Exit probe: Line 8
   - Captures: Parameters (a, b), return value

2. **check_value(x)**
   - Entry probe: Line 11
   - Branch probe: Line 14 (if x > 0)
   - Exit probe: Line 19
   - Captures: Parameter (x), branch decision, return value

### Instrumentation Statistics
- Total functions instrumented: 2
- Total branches instrumented: 1
- Total variables instrumented: 0
- Estimated overhead: <5%

### Usage
Run the instrumented code normally. Instrumentation output will be written to:
- Console (stdout)
- Log file: instrumentation.log (if configured)
```

## Best Practices

1. **Minimize overhead**: Only instrument what's necessary
2. **Use conditional compilation**: Allow disabling instrumentation in production
3. **Handle exceptions**: Ensure instrumentation doesn't crash the program
4. **Preserve semantics**: Never modify program logic
5. **Thread-safe logging**: Use thread-safe logging mechanisms
6. **Structured output**: Use consistent format for easy parsing
7. **Timestamp everything**: Include timestamps for temporal analysis

## Advanced Features

### Selective Instrumentation

```python
# Only instrument specific functions
INSTRUMENTED_FUNCTIONS = ["calculate_sum", "process_data"]

def should_instrument(func_name):
    return func_name in INSTRUMENTED_FUNCTIONS

# Apply instrumentation conditionally
if should_instrument("calculate_sum"):
    # Add instrumentation
    pass
```

### Performance Monitoring

```python
import time

def calculate_sum(a, b):
    start_time = time.time()
    logging.info(f"ENTER calculate_sum(a={a}, b={b})")

    result = a + b

    elapsed = time.time() - start_time
    logging.info(f"EXIT calculate_sum() -> {result} [time={elapsed:.6f}s]")
    return result
```

### JSON Output Format

```python
import json
import time

def calculate_sum(a, b):
    entry_event = {
        "type": "function_entry",
        "function": "calculate_sum",
        "params": {"a": a, "b": b},
        "timestamp": time.time()
    }
    print(json.dumps(entry_event))

    result = a + b

    exit_event = {
        "type": "function_exit",
        "function": "calculate_sum",
        "return_value": result,
        "timestamp": time.time()
    }
    print(json.dumps(exit_event))

    return result
```

## Constraints

- **Preserve semantics**: Never change program behavior
- **Minimal overhead**: Keep instrumentation lightweight
- **No side effects**: Instrumentation shouldn't modify program state
- **Exception safety**: Handle errors gracefully
- **Configurable**: Allow enabling/disabling instrumentation
