---
name: reproduction-trace-instrumenter
description: Instruments programs to capture execution traces specifically for reproducing reported bugs, enabling consistent replay and diagnosis of failures. Use this skill when you need to reproduce a bug, capture execution traces for debugging, instrument code to record program behavior, generate replay scripts for bug reproduction, diagnose hard-to-reproduce failures, or perform deterministic replay of program execution. Triggers when users ask to instrument code for tracing, capture execution traces, reproduce bugs, generate replay scripts, or enable deterministic debugging.
---

# Reproduction Trace Instrumenter

## Overview

This skill instruments source code to capture detailed execution traces for bug reproduction. It records function calls, variable values, control flow, and program state, then generates replay scripts to deterministically reproduce the bug for diagnosis.

## Workflow

### 1. Identify the Bug Context

Before instrumentation, understand:
- What is the bug or failure being investigated?
- Which code paths are likely involved?
- What inputs trigger the bug?
- Is the bug deterministic or intermittent?

### 2. Instrument the Code

Use the appropriate instrumenter for your language:

#### Python Instrumentation

```bash
python scripts/python_instrumenter.py <source_file.py> -o <instrumented_file.py>
```

**Options:**
- `--no-functions`: Disable function call tracing
- `--no-variables`: Disable variable assignment tracing
- `--no-control-flow`: Disable control flow tracing
- `--exclude <patterns>`: Exclude functions matching patterns (e.g., `__init__` `test_*`)

**Example:**
```bash
# Full instrumentation
python scripts/python_instrumenter.py app.py -o app_instrumented.py

# Minimal instrumentation (functions only)
python scripts/python_instrumenter.py app.py -o app_instrumented.py --no-variables --no-control-flow

# Exclude test functions
python scripts/python_instrumenter.py app.py -o app_instrumented.py --exclude test_ __
```

### 3. Run the Instrumented Code

Execute the instrumented program with the inputs that trigger the bug:

```bash
python app_instrumented.py
```

The execution trace will be automatically saved to `trace.json` when the program exits.

**Trace Output:**
- `trace.json`: Complete execution trace with all recorded events
- Console output: Summary of trace recording

### 4. Analyze the Trace

Generate a human-readable summary:

```bash
python scripts/replay_generator.py trace.json --summary
```

This shows:
- Total number of events
- Event type distribution
- Function call sequence
- Maximum call depth

### 5. Generate Replay Script

Create a replay script to reproduce the bug:

```bash
python scripts/replay_generator.py trace.json -o replay.py
```

Run the replay script:

```bash
python replay.py
```

The replay script executes the same sequence of operations, allowing you to:
- Reproduce the bug consistently
- Add breakpoints at specific steps
- Modify values to test hypotheses
- Understand the execution flow

## Configuration

Use the trace configuration template to customize instrumentation:

```bash
cp assets/trace_config_template.json trace_config.json
# Edit trace_config.json as needed
```

**Key Configuration Options:**

**Instrumentation Level:**
- `trace_functions`: Record function entry/exit
- `trace_variables`: Record variable assignments
- `trace_control_flow`: Record if/else, loops
- `trace_exceptions`: Record exception handling

**Filtering:**
- `exclude_patterns`: Function name patterns to skip
- `exclude_modules`: Modules to skip entirely
- `max_string_length`: Truncate long strings
- `max_call_depth`: Limit trace depth

**Performance:**
- `buffer_size`: Events to buffer before writing
- `async_write`: Write traces asynchronously
- `max_trace_size_mb`: Maximum trace file size

## Instrumentation Levels

Choose the appropriate level based on your needs:

### Minimal (Functions Only)
```bash
python scripts/python_instrumenter.py app.py -o app_inst.py --no-variables --no-control-flow
```
- **Overhead**: 5-15%
- **Use when**: You need to understand call sequence only
- **Trace size**: Small

### Standard (Functions + Variables)
```bash
python scripts/python_instrumenter.py app.py -o app_inst.py --no-control-flow
```
- **Overhead**: 20-50%
- **Use when**: You need to track state changes
- **Trace size**: Medium

### Full (Everything)
```bash
python scripts/python_instrumenter.py app.py -o app_inst.py
```
- **Overhead**: 50-200%
- **Use when**: You need complete execution details
- **Trace size**: Large

## Common Use Cases

### Use Case 1: Intermittent Bug Reproduction
```
User: "I have a bug that only happens sometimes. Help me capture what's happening."
→ Instrument with full tracing
→ Run multiple times until bug occurs
→ Analyze the trace from the failing run
→ Generate replay script to reproduce consistently
```

### Use Case 2: Understanding Complex Control Flow
```
User: "I don't understand why this function returns the wrong value."
→ Instrument with functions + variables
→ Run with problematic input
→ Review trace to see variable values at each step
→ Identify where the logic goes wrong
```

### Use Case 3: Debugging Production Issues
```
User: "Users report a crash but I can't reproduce it locally."
→ Instrument production code (minimal level for performance)
→ Deploy and wait for crash
→ Retrieve trace.json from crashed instance
→ Generate replay script to reproduce locally
```

### Use Case 4: Regression Testing
```
User: "I fixed a bug. How do I ensure it doesn't come back?"
→ Capture trace of the bug before fix
→ Generate replay script
→ Use replay script as regression test
→ Run after each code change
```

## Trace Format

Traces are stored in JSON format with the following structure:

```json
{
  "traces": [
    {
      "seq": 1,
      "timestamp": "2024-01-15T10:30:45.123",
      "type": "function_entry",
      "depth": 0,
      "data": {
        "function": "calculate_total",
        "arguments": {"price": 100, "tax_rate": 0.08}
      }
    },
    {
      "seq": 2,
      "timestamp": "2024-01-15T10:30:45.125",
      "type": "variable_assignment",
      "depth": 1,
      "data": {
        "variable": "tax",
        "value": 8.0,
        "type": "float"
      }
    }
  ],
  "metadata": {
    "total_events": 2,
    "max_depth": 1
  }
}
```

## Best Practices

1. **Start Minimal**: Begin with function-level tracing, add detail as needed

2. **Focus on Bug Area**: Use `--exclude` to skip irrelevant code paths

3. **Test Instrumentation**: Verify instrumented code behaves the same as original

4. **Manage Trace Size**: Use filtering to keep traces manageable

5. **Validate Replay**: Ensure replay script reproduces the bug consistently

6. **Clean Up**: Remove instrumentation before committing code

## Limitations

1. **Observer Effect**: Instrumentation may change timing and behavior
   - Minimize by using lower instrumentation levels
   - Be aware of race conditions in concurrent code

2. **Performance Overhead**: Instrumented code runs slower
   - Use sampling or selective instrumentation for performance-critical code

3. **Trace Size**: Full traces can be very large
   - Apply filtering and size limits
   - Focus on specific code regions

4. **Non-Determinism**: Some bugs involve external factors
   - Record external inputs (network, file system, time)
   - Use deterministic mode in configuration

5. **Language Support**: Currently supports Python only
   - See references/instrumentation_techniques.md for other languages

## Advanced Topics

### Custom Instrumentation

Modify `scripts/python_instrumenter.py` to add custom tracing:
- Trace specific function arguments
- Record custom metrics
- Add conditional breakpoints
- Integrate with logging frameworks

### Multi-Process Tracing

For programs with multiple processes:
- Instrument each process separately
- Use process ID in trace filenames
- Merge traces for analysis

### Distributed System Tracing

For distributed systems:
- Add correlation IDs to trace events
- Synchronize timestamps across nodes
- Use distributed tracing tools (Jaeger, Zipkin)

## Resources

### scripts/python_instrumenter.py
AST-based Python code instrumenter that:
- Parses Python source code
- Inserts tracing calls at key points
- Generates instrumented code with embedded trace runtime
- Supports configurable instrumentation levels

### scripts/replay_generator.py
Trace replay script generator that:
- Reads execution traces from JSON
- Generates executable Python replay scripts
- Provides trace summaries and statistics
- Enables deterministic bug reproduction

### references/instrumentation_techniques.md
Comprehensive guide covering:
- Instrumentation approaches (source, bytecode, dynamic)
- What to trace and how to filter
- Trace reduction strategies
- Deterministic replay techniques
- Language-specific considerations
- Performance optimization
- Best practices and common pitfalls

Read this reference when you need deeper understanding of instrumentation theory, want to implement instrumenters for other languages, or need to optimize trace performance.

### assets/trace_config_template.json
Configuration template for customizing:
- Instrumentation levels
- Filtering rules
- Performance settings
- Replay options

Copy and modify this template to create custom trace configurations for specific use cases.
