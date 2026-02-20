# Normalized JSON Schema

## Top-Level Structure

```json
{
  "trace_type": "strace|ltrace",
  "source_file": "path/to/original/trace/file",
  "total_calls": 1234,
  "filtered": false,
  "traces": [...]
}
```

### Fields

- `trace_type`: Type of trace ("strace" or "ltrace")
- `source_file`: Original trace file path
- `total_calls`: Number of trace entries
- `filtered`: Whether filtering has been applied (optional)
- `traces`: Array of trace entries

## Trace Entry Structure

### strace Entry

```json
{
  "syscall": "open",
  "arguments": ["\"/etc/passwd\"", "O_RDONLY"],
  "return_value": "3",
  "extra_info": null,
  "line_number": 42,
  "raw_line": "open(\"/etc/passwd\", O_RDONLY) = 3"
}
```

### ltrace Entry

```json
{
  "function": "strlen",
  "arguments": ["\"hello\""],
  "return_value": "5",
  "timing": "0.000123",
  "line_number": 15,
  "raw_line": "strlen(\"hello\") = 5 <0.000123>"
}
```

### Common Fields

- `syscall` / `function`: Name of the system call or library function
- `arguments`: Array of argument strings (as they appear in trace)
- `return_value`: Return value as string
- `line_number`: Line number in original trace file
- `raw_line`: Original unmodified line from trace file

### Optional Fields

- `extra_info`: Additional information from strace (e.g., error messages)
- `timing`: Execution time from ltrace (when available)

## Debug Info Structure

When using `extract_debug_info.py`, the output follows this structure:

```json
{
  "source_file": "path/to/trace.json",
  "trace_type": "strace",
  "total_calls": 1234,
  "file_operations": {
    "open": [...],
    "read": [...],
    "write": [...],
    "close": [...],
    "errors": [...]
  },
  "network_operations": {
    "socket": [...],
    "connect": [...],
    "errors": [...]
  },
  "process_operations": {
    "fork": [...],
    "execve": [...],
    "exit": [...]
  },
  "errors": [
    {
      "call": "open",
      "error": "-1 ENOENT",
      "line": 42,
      "arguments": ["\"/missing/file\"", "O_RDONLY"]
    }
  ]
}
```

This structured format makes it easy to:
- Identify all errors at a glance
- Track file descriptor lifecycle
- Analyze network connection patterns
- Understand process creation/termination
