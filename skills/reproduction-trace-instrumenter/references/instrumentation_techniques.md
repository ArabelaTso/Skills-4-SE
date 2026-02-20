# Instrumentation Techniques Reference

## Overview

This document provides detailed information on code instrumentation techniques for capturing execution traces to reproduce bugs.

## Instrumentation Approaches

### 1. Source Code Instrumentation

Modify source code directly by inserting tracing statements.

**Advantages:**
- Language-agnostic approach
- Full control over what to trace
- No runtime overhead when tracing is disabled

**Disadvantages:**
- Requires source code access
- May alter program behavior
- Needs recompilation

**Implementation Methods:**
- AST (Abstract Syntax Tree) transformation
- Text-based code injection
- Preprocessor directives

### 2. Bytecode Instrumentation

Modify compiled bytecode to add tracing logic.

**Advantages:**
- No source code modification needed
- Can instrument third-party libraries
- Transparent to developers

**Disadvantages:**
- Language-specific (JVM, Python bytecode, etc.)
- More complex implementation
- Potential compatibility issues

**Common Tools:**
- Java: ASM, Javassist, ByteBuddy
- Python: sys.settrace(), bytecode manipulation
- .NET: Mono.Cecil, IL weaving

### 3. Dynamic Instrumentation

Inject tracing code at runtime without modifying files.

**Advantages:**
- No code modification required
- Can enable/disable dynamically
- Works with production binaries

**Disadvantages:**
- Higher runtime overhead
- Platform-specific
- May require special permissions

**Common Tools:**
- DTrace, SystemTap (Linux)
- Frida (cross-platform)
- Pin, DynamoRIO (binary instrumentation)

## What to Trace

### Function Calls

**Essential Information:**
- Function name
- Entry timestamp
- Arguments (names and values)
- Return value
- Exit timestamp
- Call stack depth

**Example Trace Entry:**
```json
{
  "type": "function_entry",
  "function": "calculate_discount",
  "timestamp": "2024-01-15T10:30:45.123",
  "arguments": {
    "price": 100.0,
    "discount_rate": 0.15
  },
  "depth": 2
}
```

### Variable Assignments

**Essential Information:**
- Variable name
- Assigned value
- Data type
- Scope (local/global)
- Line number

**Filtering Strategy:**
- Skip temporary variables
- Skip loop counters (unless relevant)
- Focus on domain-specific variables
- Limit string/collection sizes

### Control Flow

**Essential Information:**
- Branch type (if/else, switch, loop)
- Condition evaluation result
- Branch taken
- Iteration count (for loops)

**Example:**
```json
{
  "type": "control_flow",
  "branch": "if",
  "condition": "user.age >= 18",
  "result": true,
  "line": 42
}
```

### Exception Handling

**Essential Information:**
- Exception type
- Exception message
- Stack trace
- Caught/uncaught status
- Handler location

## Trace Reduction Strategies

### 1. Selective Instrumentation

Only instrument code paths relevant to the bug.

**Techniques:**
- Instrument specific modules/packages
- Focus on recently changed code
- Exclude standard library calls
- Use call stack filtering

### 2. Sampling

Record only a subset of events.

**Strategies:**
- Time-based sampling (every N milliseconds)
- Event-based sampling (every Nth call)
- Adaptive sampling (increase rate near bug)

### 3. Data Filtering

Limit the amount of data captured per event.

**Techniques:**
- Truncate large strings
- Summarize collections (length only)
- Skip redundant values
- Use hash values for large objects

### 4. Compression

Reduce trace file size.

**Methods:**
- Delta encoding (store changes only)
- Reference deduplication
- Binary format instead of JSON
- Stream compression (gzip, zstd)

## Deterministic Replay Considerations

### Sources of Non-Determinism

1. **Concurrency**
   - Thread scheduling
   - Race conditions
   - Lock ordering

2. **External Input**
   - User input
   - Network responses
   - File system state
   - System time

3. **Random Number Generation**
   - Unseeded RNGs
   - System entropy

4. **Memory Addresses**
   - ASLR (Address Space Layout Randomization)
   - Pointer values
   - Hash table ordering

### Making Execution Deterministic

**Record External Inputs:**
```json
{
  "type": "external_input",
  "source": "stdin",
  "value": "user input text",
  "timestamp": "2024-01-15T10:30:45.123"
}
```

**Record Thread Scheduling:**
```json
{
  "type": "thread_switch",
  "from_thread": "thread-1",
  "to_thread": "thread-2",
  "timestamp": "2024-01-15T10:30:45.124"
}
```

**Seed Random Number Generators:**
```python
import random
random.seed(12345)  # Fixed seed for replay
```

## Performance Optimization

### Minimize Overhead

1. **Buffered Writing**
   - Write traces to memory buffer
   - Flush periodically to disk
   - Use async I/O

2. **Lazy Serialization**
   - Defer JSON encoding
   - Use binary formats
   - Compress on-the-fly

3. **Conditional Tracing**
   - Enable only when needed
   - Use environment variables
   - Implement trace levels

### Overhead Benchmarks

Typical overhead by instrumentation level:

- **Minimal** (function calls only): 5-15%
- **Medium** (+ variables): 20-50%
- **Full** (+ control flow): 50-200%
- **Verbose** (+ all data): 200-500%

## Language-Specific Considerations

### Python

- Use `sys.settrace()` for lightweight tracing
- AST transformation for source instrumentation
- `inspect` module for runtime introspection
- Consider GIL impact on multithreaded programs

### Java

- Use AspectJ for aspect-oriented instrumentation
- Java agents for bytecode manipulation
- JVM TI for native instrumentation
- Consider JIT compilation effects

### JavaScript/Node.js

- Use Babel plugins for transpilation
- Proxy objects for property access tracing
- V8 profiler API for performance data
- Consider async/await complexity

### C/C++

- Compiler instrumentation flags (-finstrument-functions)
- LD_PRELOAD for library interposition
- GDB scripting for debugging
- Consider optimization level impact

## Best Practices

1. **Start Minimal**: Begin with function-level tracing, add detail as needed

2. **Focus on Bug Area**: Instrument code paths related to the bug report

3. **Validate Instrumentation**: Ensure instrumented code behaves identically

4. **Test Replay**: Verify traces can reproduce the bug consistently

5. **Document Assumptions**: Note any non-deterministic elements

6. **Version Control**: Track instrumentation configuration with code

7. **Clean Up**: Remove instrumentation before production deployment

## Common Pitfalls

1. **Observer Effect**: Instrumentation changes program behavior
   - Solution: Minimize overhead, use sampling

2. **Trace Explosion**: Too much data to analyze
   - Solution: Apply filtering, use selective instrumentation

3. **Incomplete Traces**: Missing critical events
   - Solution: Ensure all relevant code paths are instrumented

4. **Non-Deterministic Replay**: Cannot reproduce bug
   - Solution: Record all external inputs and timing

5. **Performance Degradation**: Program too slow to use
   - Solution: Use adaptive instrumentation, optimize trace writing
