---
name: trace-collection-assistant
description: Collect, normalize, and structure execution traces from instrumented programs (strace, ltrace) into JSON format for downstream analysis. Use when working with system call traces, library call traces, or execution logs that need to be analyzed for debugging, test case reproduction, or verification. Supports parsing strace/ltrace output, filtering noise, extracting debug information, and preparing traces for bug analysis or reproduction workflows.
---

# Trace Collection Assistant

## Overview

This skill helps collect, normalize, and structure execution traces produced by instrumented programs (strace, ltrace), making them suitable for downstream analysis such as debugging, reproduction, or verification. It converts raw trace output into structured JSON format and provides tools for filtering, cleaning, and extracting relevant information.

## Quick Start

### Basic Workflow

1. **Parse raw traces** - Convert strace/ltrace output to JSON
2. **Filter and clean** - Remove noise and focus on relevant calls
3. **Extract debug info** - Identify errors, file operations, network activity

### Example: Debugging with strace

```bash
# 1. Capture trace
strace -o trace.txt python buggy_program.py

# 2. Parse to JSON
python scripts/parse_strace.py trace.txt -o trace.json --pretty

# 3. Extract errors
python scripts/extract_debug_info.py trace.json --category errors --pretty

# 4. Filter to relevant operations
python scripts/filter_trace.py trace.json --error-only --remove-noise -o filtered.json --pretty
```

### Example: Analyzing library calls with ltrace

```bash
# 1. Capture trace
ltrace -o trace.txt ./program

# 2. Parse to JSON
python scripts/parse_ltrace.py trace.txt -o trace.json --pretty

# 3. Analyze specific functions
python scripts/filter_trace.py trace.json --include-calls "malloc,free,strlen" --pretty
```

## Core Operations

### 1. Parsing Traces

Convert raw trace output to normalized JSON format.

**For strace:**
```bash
python scripts/parse_strace.py <input_file> [--output <output_file>] [--pretty]
```

**For ltrace:**
```bash
python scripts/parse_ltrace.py <input_file> [--output <output_file>] [--pretty]
```

Both parsers produce the same normalized JSON structure (see `references/json_schema.md` for details).

### 2. Filtering Traces

Remove noise and focus on relevant operations.

**Common filtering operations:**

```bash
# Show only errors
python scripts/filter_trace.py trace.json --error-only --pretty

# Remove common noise syscalls
python scripts/filter_trace.py trace.json --remove-noise --pretty

# Include specific calls
python scripts/filter_trace.py trace.json --include-calls "open,read,write,close" --pretty

# Exclude specific calls
python scripts/filter_trace.py trace.json --exclude-calls "gettimeofday,clock_gettime" --pretty

# Filter by argument pattern
python scripts/filter_trace.py trace.json --arg-pattern "config.json" --pretty

# Combine filters
python scripts/filter_trace.py trace.json --error-only --remove-noise --arg-pattern "/etc" -o filtered.json --pretty
```

### 3. Extracting Debug Information

Extract structured information for specific analysis tasks.

**Extract all debug info:**
```bash
python scripts/extract_debug_info.py trace.json --pretty
```

**Extract specific categories:**
```bash
# File operations only
python scripts/extract_debug_info.py trace.json --category file --pretty

# Network operations only
python scripts/extract_debug_info.py trace.json --category network --pretty

# Process operations only
python scripts/extract_debug_info.py trace.json --category process --pretty

# Errors only
python scripts/extract_debug_info.py trace.json --category errors --pretty
```

## Use Cases

### Bug Debugging

When debugging a failing program:

1. Parse the trace to JSON
2. Extract all errors to identify failure points
3. Filter to relevant operations around the error
4. Analyze file/network/process operations for root cause

See `references/analysis_guide.md` for detailed debugging patterns.

### Test Case Reproduction

When reproducing a bug:

1. Parse the trace from the failing execution
2. Extract file operations to identify input dependencies
3. Filter to the minimal sequence of operations
4. Use the structured trace to reconstruct the execution environment

See `references/analysis_guide.md` for reproduction workflows.

## Reference Documentation

- **`references/trace_formats.md`** - Detailed documentation on strace and ltrace output formats, common syscalls, error codes
- **`references/json_schema.md`** - Schema for normalized JSON output format
- **`references/analysis_guide.md`** - Comprehensive guide on using traces for debugging and reproduction, including common patterns

## Output Format

All tools produce JSON output following the normalized schema:

```json
{
  "trace_type": "strace",
  "source_file": "trace.txt",
  "total_calls": 1234,
  "traces": [
    {
      "syscall": "open",
      "arguments": ["\"/etc/passwd\"", "O_RDONLY"],
      "return_value": "3",
      "line_number": 42,
      "raw_line": "open(\"/etc/passwd\", O_RDONLY) = 3"
    }
  ]
}
```

See `assets/schema_template.json` for the complete JSON schema definition.

## Tips

- Use `--pretty` flag for human-readable JSON output
- Use `--remove-noise` to filter out common irrelevant syscalls
- Combine multiple filters for focused analysis
- Check `references/analysis_guide.md` for common debugging patterns
- The `line_number` field preserves execution order for sequence analysis
