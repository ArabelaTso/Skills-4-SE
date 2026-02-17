# Instrumentation Guide

## Overview

This guide explains how to instrument programs to capture state snapshots at runtime. The instrumentation process varies by language but follows similar principles.

## Instrumentation Modes

### Manual Mode

Insert explicit snapshot markers at specific locations in your code.

**When to use:**
- You know exactly where you want to capture state
- You want fine-grained control over snapshot locations
- You want to minimize performance overhead

**How it works:**
- Add `__SNAPSHOT__("location")` markers in your code
- Run the instrumenter to replace markers with actual snapshot calls
- The instrumented code captures state at marked locations

### Automatic Mode

Automatically instrument all function/method entry and exit points.

**When to use:**
- You want comprehensive coverage of program execution
- You're exploring unfamiliar code
- You need to understand the full execution flow

**How it works:**
- The instrumenter analyzes your code structure
- Adds snapshot calls at function/method boundaries
- Captures state on entry and before each return

### Conditional Mode

Trigger snapshots based on runtime conditions.

**When to use:**
- You want to capture state only when specific conditions occur
- You're debugging intermittent issues
- You want to reduce snapshot volume

**How it works:**
- Add conditional logic around snapshot calls
- Snapshots only captured when conditions are met
- Can combine with manual or automatic modes

## Language-Specific Instructions

### Python

**Manual instrumentation:**

```python
def my_function(x, y):
    __SNAPSHOT__("my_function:start")

    result = x + y

    __SNAPSHOT__("my_function:before_return")
    return result
```

**Run instrumenter:**

```bash
# Manual mode (only __SNAPSHOT__ markers)
python scripts/instrument_python.py my_program.py --mode manual

# Automatic mode (all functions)
python scripts/instrument_python.py my_program.py --mode auto
```

**Run instrumented program:**

```bash
python my_program_instrumented.py
# Snapshots saved to snapshots.json
```

**Set custom output file:**

```bash
SNAPSHOT_OUTPUT=my_snapshots.json python my_program_instrumented.py
```

### C/C++

**Manual instrumentation:**

```c
#include <stdio.h>

int main() {
    int x = 10;
    int y = 20;

    __SNAPSHOT__("main:start");

    int result = x + y;

    __SNAPSHOT__("main:before_return");

    return 0;
}
```

**Run instrumenter:**

```bash
# Manual mode
python scripts/instrument_c.py my_program.c --mode manual

# Automatic mode
python scripts/instrument_c.py my_program.c --mode auto
```

**Compile and run:**

```bash
# Compile with snapshot runtime
gcc my_program_instrumented.c scripts/snapshot_runtime.c -o my_program -rdynamic

# Run
./my_program
# Snapshots saved to snapshots.json
```

**Set custom output file:**

```bash
SNAPSHOT_OUTPUT=my_snapshots.json ./my_program
```

### Java

**Manual instrumentation:**

```java
public class MyProgram {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;

        __SNAPSHOT__("main:start");

        int result = x + y;

        __SNAPSHOT__("main:before_return");
    }
}
```

**Run instrumenter:**

```bash
# Manual mode
python scripts/instrument_java.py MyProgram.java --mode manual

# Automatic mode
python scripts/instrument_java.py MyProgram.java --mode auto
```

**Compile and run:**

```bash
# Copy runtime to your source directory
cp scripts/SnapshotRuntime.java snapshot/

# Compile
javac snapshot/SnapshotRuntime.java
javac MyProgram_instrumented.java

# Run
java MyProgram_instrumented
# Snapshots saved to snapshots.json
```

**Set custom output file:**

```bash
SNAPSHOT_OUTPUT=my_snapshots.json java MyProgram_instrumented
```

## Best Practices

### Choosing Snapshot Locations

1. **Function boundaries** - Capture state at entry/exit to understand flow
2. **Before/after critical operations** - File I/O, network calls, database queries
3. **Loop iterations** - Understand how state evolves over iterations
4. **Conditional branches** - Capture state at decision points
5. **Error handling** - Capture state when errors occur

### Minimizing Overhead

1. **Use manual mode** when you know where to instrument
2. **Disable snapshots** in performance-critical sections
3. **Limit variable capture** to relevant variables only
4. **Use conditional snapshots** to reduce volume
5. **Clean up old snapshots** regularly

### Snapshot Naming Conventions

Use descriptive location names:

```
function_name:entry
function_name:exit
function_name:after_operation
function_name:error_path
module:function:line_description
```

## Controlling Snapshot Capture

### Python

```python
import snapshot_runtime

# Disable snapshots temporarily
snapshot_runtime.disable()

# Performance-critical code here

# Re-enable snapshots
snapshot_runtime.enable()

# Set custom output file
snapshot_runtime.set_output_file("custom.json")

# Manually save snapshots
snapshot_runtime.save_snapshots()
```

### C/C++

```c
#include "snapshot_runtime.h"

// Disable snapshots
snapshot_disable();

// Performance-critical code

// Re-enable snapshots
snapshot_enable();

// Manually finalize
snapshot_finalize();
```

### Java

```java
import snapshot.SnapshotRuntime;

// Disable snapshots
SnapshotRuntime.disable();

// Performance-critical code

// Re-enable snapshots
SnapshotRuntime.enable();

// Set custom output file
SnapshotRuntime.setOutputFile("custom.json");

// Manually save snapshots
SnapshotRuntime.saveSnapshots();
```

## Troubleshooting

### Snapshots not being captured

- Check that instrumentation completed successfully
- Verify runtime library is properly linked/imported
- Ensure snapshots are enabled (not disabled)
- Check file permissions for output file

### Large snapshot files

- Use manual mode instead of automatic
- Add conditional logic to filter snapshots
- Limit variable capture to essential data
- Increase snapshot granularity (fewer locations)

### Performance issues

- Disable snapshots in hot paths
- Use conditional snapshots
- Reduce variable serialization depth
- Consider sampling (capture every Nth snapshot)

### Compilation errors (C/C++)

- Ensure snapshot_runtime.h is in include path
- Link with snapshot_runtime.c or .o file
- Add `-rdynamic` flag for better stack traces
- Check for conflicting macro definitions
