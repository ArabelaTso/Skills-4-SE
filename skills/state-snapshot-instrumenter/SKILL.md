---
name: state-snapshot-instrumenter
description: Instrument programs (Python, C/C++, Java) to capture snapshots of key program states at runtime, including variables, memory, and call stacks. Use when you need to debug complex issues, reproduce test cases, prepare traces for formal verification, or analyze program execution. Supports manual instrumentation points, automatic function/method instrumentation, and conditional triggers. Outputs structured JSON snapshots for debugging, replay, and verification workflows.
---

# State Snapshot Instrumenter

## Overview

This skill instruments programs to capture snapshots of key program states at runtime. Snapshots include variable values, memory state, call stacks, and execution context, saved in structured JSON format for analysis, debugging, reproduction, and verification.

## Quick Start

### Basic Workflow

1. **Add snapshot markers** to your code (manual mode) or use automatic instrumentation
2. **Run the instrumenter** to generate instrumented code
3. **Execute the instrumented program** to capture snapshots
4. **Analyze snapshots** to understand program behavior

### Example: Python

```bash
# 1. Add markers to your code
# def my_function(x):
#     __SNAPSHOT__("my_function:start")
#     result = x * 2
#     __SNAPSHOT__("my_function:end")
#     return result

# 2. Instrument the code
python scripts/instrument_python.py my_program.py --mode manual

# 3. Run instrumented program
python my_program_instrumented.py
# Snapshots saved to snapshots.json

# 4. Analyze snapshots
python scripts/analyze_snapshots.py snapshots.json --list
```

### Example: C/C++

```bash
# 1. Add markers to your code
# int main() {
#     __SNAPSHOT__("main:start");
#     int x = 10;
#     __SNAPSHOT__("main:end");
#     return 0;
# }

# 2. Instrument the code
python scripts/instrument_c.py program.c --mode manual

# 3. Compile with runtime
gcc program_instrumented.c scripts/snapshot_runtime.c -o program -rdynamic

# 4. Run and analyze
./program
python scripts/analyze_snapshots.py snapshots.json --list
```

### Example: Java

```bash
# 1. Add markers to your code
# public static void main(String[] args) {
#     __SNAPSHOT__("main:start");
#     int x = 10;
#     __SNAPSHOT__("main:end");
# }

# 2. Instrument the code
python scripts/instrument_java.py Program.java --mode manual

# 3. Compile and run
cp scripts/SnapshotRuntime.java snapshot/
javac snapshot/SnapshotRuntime.java
javac Program_instrumented.java
java Program_instrumented

# 4. Analyze
python scripts/analyze_snapshots.py snapshots.json --list
```

## Instrumentation Modes

### Manual Mode (Recommended for Targeted Debugging)

Add explicit `__SNAPSHOT__("location")` markers at specific points in your code.

**Python:**
```python
def process_data(items):
    __SNAPSHOT__("process_data:entry")

    result = []
    for item in items:
        __SNAPSHOT__("loop_iteration")
        result.append(item * 2)

    __SNAPSHOT__("process_data:exit")
    return result
```

**C/C++:**
```c
int calculate(int x, int y) {
    __SNAPSHOT__("calculate:entry");

    int result = x + y;

    __SNAPSHOT__("calculate:exit");
    return result;
}
```

**Java:**
```java
public int calculate(int x, int y) {
    __SNAPSHOT__("calculate:entry");

    int result = x + y;

    __SNAPSHOT__("calculate:exit");
    return result;
}
```

**Instrument:**
```bash
python scripts/instrument_python.py file.py --mode manual
python scripts/instrument_c.py file.c --mode manual
python scripts/instrument_java.py file.java --mode manual
```

### Automatic Mode (Comprehensive Coverage)

Automatically instrument all function/method entry and exit points.

```bash
python scripts/instrument_python.py file.py --mode auto
python scripts/instrument_c.py file.c --mode auto
python scripts/instrument_java.py file.java --mode auto
```

This captures state at every function boundary without manual markers.

## Core Operations

### 1. Instrumentation

**Python:**
```bash
# Manual mode
python scripts/instrument_python.py input.py --mode manual -o output.py

# Automatic mode
python scripts/instrument_python.py input.py --mode auto -o output.py

# In-place modification
python scripts/instrument_python.py input.py --mode manual --inplace
```

**C/C++:**
```bash
# Instrument
python scripts/instrument_c.py input.c --mode manual -o output.c

# Compile with runtime
gcc output.c scripts/snapshot_runtime.c -o program -rdynamic

# Run with custom output file
SNAPSHOT_OUTPUT=my_snapshots.json ./program
```

**Java:**
```bash
# Instrument
python scripts/instrument_java.py Input.java --mode manual -o Output.java

# Setup runtime
cp scripts/SnapshotRuntime.java snapshot/
javac snapshot/SnapshotRuntime.java

# Compile and run
javac Output.java
SNAPSHOT_OUTPUT=my_snapshots.json java Output
```

### 2. Snapshot Analysis

**List all snapshots:**
```bash
python scripts/analyze_snapshots.py snapshots.json --list
```

**Show detailed snapshot:**
```bash
python scripts/analyze_snapshots.py snapshots.json --show 5
```

**View execution timeline:**
```bash
python scripts/analyze_snapshots.py snapshots.json --timeline
```

**Track variable changes:**
```bash
python scripts/analyze_snapshots.py snapshots.json --track-var "user_id"
```

**Compare two snapshots:**
```bash
python scripts/analyze_snapshots.py snapshots.json --compare 10 20
```

**Filter snapshots:**
```bash
# By location
python scripts/analyze_snapshots.py snapshots.json --filter-location "main"

# By type
python scripts/analyze_snapshots.py snapshots.json --filter-type "function_entry"
```

### 3. Runtime Control

**Python:**
```python
import snapshot_runtime

# Disable snapshots temporarily
snapshot_runtime.disable()
# ... performance-critical code ...
snapshot_runtime.enable()

# Set custom output file
snapshot_runtime.set_output_file("custom.json")

# Manually save snapshots
snapshot_runtime.save_snapshots()
```

**C/C++:**
```c
#include "snapshot_runtime.h"

snapshot_disable();
// ... performance-critical code ...
snapshot_enable();

snapshot_finalize();  // Manually save
```

**Java:**
```java
import snapshot.SnapshotRuntime;

SnapshotRuntime.disable();
// ... performance-critical code ...
SnapshotRuntime.enable();

SnapshotRuntime.setOutputFile("custom.json");
SnapshotRuntime.saveSnapshots();
```

## Use Cases

### Bug Debugging

Capture comprehensive state to understand complex bugs:

1. Instrument with automatic mode for full coverage
2. Run to reproduce the bug
3. Analyze snapshots to identify failure point
4. Track variable changes to understand root cause

See `references/use_cases.md` for detailed debugging workflows.

### Test Case Reproduction

Extract exact inputs and state to reproduce failures:

1. Instrument with manual snapshots at key points
2. Capture failing execution
3. Extract input dependencies from snapshots
4. Reconstruct minimal test case

See `references/use_cases.md` for reproduction workflows.

### Formal Verification

Generate execution traces for verification tools:

1. Instrument function boundaries
2. Collect execution traces
3. Extract invariants and contracts
4. Feed to verification tools

See `references/use_cases.md` for verification workflows.

## Reference Documentation

- **`references/instrumentation_guide.md`** - Comprehensive guide on instrumenting programs, including language-specific instructions, best practices, and troubleshooting
- **`references/snapshot_format.md`** - Complete specification of the JSON snapshot format, including language-specific variations and serialization rules
- **`references/use_cases.md`** - Detailed workflows for debugging, reproduction, verification, performance analysis, and concurrency debugging

## Example Programs

Example instrumented programs are provided in `assets/`:
- `example_python.py` - Python example with manual snapshots
- `example_c.c` - C example with manual snapshots
- `example_java.java` - Java example with manual snapshots

## Output Format

All snapshots are saved in unified JSON format:

```json
{
  "format_version": "1.0",
  "language": "python",
  "total_snapshots": 5,
  "snapshots": [
    {
      "snapshot_id": 1,
      "timestamp": "2026-02-17T19:30:45",
      "location": "main:start",
      "type": "manual",
      "call_stack": [...],
      "local_variables": {...}
    }
  ]
}
```

See `assets/snapshot_schema.json` for the complete JSON schema.

## Tips

- Use manual mode for targeted debugging to minimize overhead
- Use automatic mode for comprehensive execution understanding
- Disable snapshots in performance-critical sections
- Use descriptive location names (e.g., "function:entry", "after_operation")
- Set custom output files with `SNAPSHOT_OUTPUT` environment variable
- Analyze snapshots incrementally as you debug
- Compare snapshots to identify when state becomes incorrect
- Track key variables through execution to understand data flow
