# Trace Analysis Guide

## Using Traces for Bug Debugging

### 1. Identify Error Points

Start by extracting all errors from the trace:

```bash
python extract_debug_info.py trace.json --category errors --pretty
```

This shows all failed system calls with their error codes, helping pinpoint where things went wrong.

### 2. Analyze File Operations

Many bugs involve file I/O issues:

```bash
python extract_debug_info.py trace.json --category file --pretty
```

Look for:
- Failed `open()` calls (file not found, permission denied)
- Mismatched open/close pairs (resource leaks)
- Read/write errors
- Unexpected file access patterns

### 3. Check Network Operations

For network-related bugs:

```bash
python extract_debug_info.py trace.json --category network --pretty
```

Look for:
- Connection failures (`connect()` returning errors)
- Socket creation issues
- Send/receive errors
- Timeout patterns

### 4. Examine Process Behavior

For process/threading issues:

```bash
python extract_debug_info.py trace.json --category process --pretty
```

Look for:
- Failed `execve()` calls
- Unexpected exit codes
- Fork/clone patterns

### 5. Filter Noise

Remove irrelevant syscalls to focus on the problem:

```bash
python filter_trace.py trace.json --remove-noise --error-only --pretty
```

This shows only failed calls, excluding common noise.

## Using Traces for Test Case Reproduction

### 1. Capture Complete Execution Context

When collecting traces for reproduction, ensure you capture:
- All file operations (to understand required input files)
- Environment variables (via `getenv` calls)
- Command-line arguments (via `execve` arguments)
- Network interactions (to mock external dependencies)

### 2. Identify Minimal Reproduction Path

Filter the trace to the essential operations:

```bash
# Focus on specific file or pattern
python filter_trace.py trace.json --arg-pattern "target_file.txt" --pretty

# Focus on specific syscalls
python filter_trace.py trace.json --include-calls "open,read,write" --pretty
```

### 3. Extract Input Dependencies

Look at file operations to identify required inputs:

```bash
python extract_debug_info.py trace.json --category file --pretty | grep "open"
```

This shows all files the program tried to access.

### 4. Reconstruct Execution Sequence

The normalized JSON preserves execution order via `line_number`. Use this to:
- Understand the sequence of operations leading to a bug
- Identify the exact point where behavior diverges from expected
- Create a minimal test case that reproduces the issue

### Example Workflow

```bash
# 1. Parse the trace
python parse_strace.py failing_test.strace -o trace.json --pretty

# 2. Extract errors
python extract_debug_info.py trace.json --category errors -o errors.json --pretty

# 3. Filter to relevant operations
python filter_trace.py trace.json --error-only --remove-noise -o filtered.json --pretty

# 4. Analyze file dependencies
python extract_debug_info.py filtered.json --category file -o file_ops.json --pretty
```

Now you have:
- `errors.json`: All failures
- `filtered.json`: Focused trace without noise
- `file_ops.json`: File dependencies

Use these to construct a minimal reproduction test case.

## Common Debugging Patterns

### Pattern 1: File Not Found

```json
{
  "syscall": "open",
  "arguments": ["\"/path/to/file\"", "O_RDONLY"],
  "return_value": "-1 ENOENT"
}
```

**Action**: Check if file exists, verify path is correct, check working directory.

### Pattern 2: Permission Denied

```json
{
  "syscall": "open",
  "arguments": ["\"/etc/shadow\"", "O_RDONLY"],
  "return_value": "-1 EACCES"
}
```

**Action**: Check file permissions, verify user has access rights.

### Pattern 3: Connection Refused

```json
{
  "syscall": "connect",
  "arguments": ["3", "{sa_family=AF_INET, sin_port=htons(8080), ...}"],
  "return_value": "-1 ECONNREFUSED"
}
```

**Action**: Check if server is running, verify port number, check firewall rules.

### Pattern 4: Resource Leak

```json
// Many open() calls without corresponding close()
{"syscall": "open", "return_value": "3", "line_number": 10},
{"syscall": "open", "return_value": "4", "line_number": 20},
{"syscall": "open", "return_value": "5", "line_number": 30}
// No close() calls
```

**Action**: Ensure all opened file descriptors are properly closed.
