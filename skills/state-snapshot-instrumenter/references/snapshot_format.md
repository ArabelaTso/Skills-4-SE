# Snapshot Format Specification

## JSON Structure

All snapshots are saved in a unified JSON format regardless of source language.

## Top-Level Structure

```json
{
  "format_version": "1.0",
  "language": "python|c|java",
  "total_snapshots": 42,
  "snapshots": [...]
}
```

### Fields

- `format_version`: Version of the snapshot format (currently "1.0")
- `language`: Source language of the instrumented program
- `total_snapshots`: Total number of snapshots captured
- `snapshots`: Array of snapshot objects

## Snapshot Object Structure

### Common Fields (All Languages)

```json
{
  "snapshot_id": 1,
  "timestamp": "2026-02-17T19:30:45",
  "location": "function_name:entry",
  "type": "manual|function_entry|function_exit|method_entry|method_exit",
  "call_stack": [...],
  "variables": {...}
}
```

#### Field Descriptions

- `snapshot_id`: Unique identifier for this snapshot (integer)
- `timestamp`: ISO 8601 timestamp when snapshot was captured
- `location`: Descriptive location string (e.g., "main:start", "process_data:line_42")
- `type`: Type of snapshot
  - `manual`: Explicitly placed by developer
  - `function_entry`: Automatic capture at function entry
  - `function_exit`: Automatic capture at function exit
  - `method_entry`: Automatic capture at method entry (Java)
  - `method_exit`: Automatic capture at method exit (Java)
- `call_stack`: Array of stack frames (format varies by language)
- `variables`: Object containing captured variables

## Language-Specific Formats

### Python Snapshots

```json
{
  "snapshot_id": 1,
  "timestamp": "2026-02-17T19:30:45.123456",
  "location": "calculate:entry",
  "type": "function_entry",
  "call_stack": [
    {
      "function": "calculate",
      "filename": "/path/to/file.py",
      "lineno": 42
    },
    {
      "function": "main",
      "filename": "/path/to/file.py",
      "lineno": 100
    }
  ],
  "local_variables": {
    "x": 10,
    "y": 20,
    "name": "test",
    "data": [1, 2, 3],
    "obj": {
      "__type__": "MyClass",
      "__attributes__": {
        "field1": "value1",
        "field2": 42
      }
    }
  },
  "thread_id": null
}
```

**Python-specific features:**
- `local_variables`: Dictionary of local variable names and values
- Variables are serialized to JSON-compatible types
- Objects include `__type__` and `__attributes__` or `__repr__`
- Collections are limited to 100 items
- `thread_id`: Thread identifier (if threading is used)

### C/C++ Snapshots

```json
{
  "snapshot_id": 1,
  "timestamp": "2026-02-17T19:30:45",
  "location": "main:start",
  "type": "manual",
  "call_stack": [
    "./program(main+0x1a) [0x400567]",
    "/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0) [0x7f8b9c123830]",
    "./program(_start+0x29) [0x400489]"
  ],
  "variables": {
    "x": {
      "size": 4,
      "data": "0a000000"
    },
    "y": {
      "size": 4,
      "data": "14000000"
    },
    "buffer": {
      "size": 256,
      "data": "48656c6c6f20576f726c64..."
    }
  }
}
```

**C/C++-specific features:**
- `call_stack`: Array of strings from `backtrace_symbols()`
- `variables`: Each variable has `size` (bytes) and `data` (hex string)
- Data is raw memory dump (first 64 bytes)
- Stack traces include addresses and offsets

### Java Snapshots

```json
{
  "snapshot_id": 1,
  "timestamp": "2026-02-17T19:30:45",
  "location": "calculate:entry",
  "type": "method_entry",
  "call_stack": [
    "com.example.MyClass.calculate(MyClass.java:42)",
    "com.example.MyClass.main(MyClass.java:100)",
    "java.base/java.lang.Thread.run(Thread.java:829)"
  ],
  "variables": {
    "x": 10,
    "y": 20,
    "name": "test",
    "list": [1, 2, 3, 4, 5],
    "map": {
      "key1": "value1",
      "key2": "value2"
    },
    "obj": {
      "__type__": "com.example.MyObject",
      "__repr__": "MyObject@1a2b3c4d"
    }
  }
}
```

**Java-specific features:**
- `call_stack`: Array of formatted stack trace strings
- `variables`: Serialized Java objects
- Primitives and strings are preserved
- Collections are limited to 100 items
- Objects include `__type__` (fully qualified class name) and `__repr__` (toString)

## Variable Serialization Rules

### Primitive Types

Serialized directly:
- Integers: `42`
- Floats: `3.14`
- Booleans: `true`, `false`
- Strings: `"hello"`
- Null: `null`

### Collections

Arrays and lists:
```json
[1, 2, 3, 4, 5]
```

Dictionaries and maps:
```json
{
  "key1": "value1",
  "key2": 42
}
```

**Size limits:** Collections are truncated to 100 items maximum.

### Objects

Custom objects are serialized with type information:

```json
{
  "__type__": "ClassName",
  "__attributes__": {
    "field1": "value",
    "field2": 42
  }
}
```

Or with string representation:

```json
{
  "__type__": "ClassName",
  "__repr__": "ClassName(field1=value, field2=42)"
}
```

### Binary Data (C/C++)

Raw memory as hexadecimal string:

```json
{
  "size": 16,
  "data": "0a0000001400000048656c6c6f"
}
```

## Schema Validation

A JSON Schema is provided in `assets/snapshot_schema.json` for validation.

Validate snapshots:

```bash
# Using jsonschema (Python)
pip install jsonschema
python -c "
import json
import jsonschema

with open('snapshots.json') as f:
    data = json.load(f)
with open('assets/snapshot_schema.json') as f:
    schema = json.load(f)

jsonschema.validate(data, schema)
print('Valid!')
"
```

## Extending the Format

To add custom fields to snapshots:

1. Add fields to the snapshot object in your runtime
2. Ensure fields are JSON-serializable
3. Document the extension
4. Consider backward compatibility

Example custom field:

```json
{
  "snapshot_id": 1,
  "timestamp": "2026-02-17T19:30:45",
  "location": "main:start",
  "type": "manual",
  "custom_metric": 42.5,
  "custom_tag": "important",
  ...
}
```
