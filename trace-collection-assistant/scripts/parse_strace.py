#!/usr/bin/env python3
"""
Parse strace output and convert to normalized JSON format.

Usage:
    python parse_strace.py <strace_file> [--output <output_file>]
"""

import re
import json
import sys
import argparse
from typing import List, Dict, Any, Optional


def parse_strace_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a single strace output line into structured format."""
    line = line.strip()
    if not line or line.startswith('---') or line.startswith('+++'):
        return None

    # Pattern: syscall(args) = return_value
    # Example: open("/etc/passwd", O_RDONLY) = 3
    match = re.match(r'^(\w+)\((.*?)\)\s*=\s*(.+?)(?:\s+(.+))?$', line)
    if not match:
        return None

    syscall, args_str, return_value, extra = match.groups()

    # Parse arguments
    args = []
    if args_str:
        # Simple argument splitting (handles basic cases)
        current_arg = ""
        depth = 0
        in_string = False
        escape = False

        for char in args_str:
            if escape:
                current_arg += char
                escape = False
                continue

            if char == '\\':
                escape = True
                current_arg += char
                continue

            if char == '"' and not escape:
                in_string = not in_string
                current_arg += char
                continue

            if in_string:
                current_arg += char
                continue

            if char in '([{':
                depth += 1
            elif char in ')]}':
                depth -= 1

            if char == ',' and depth == 0:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char

        if current_arg:
            args.append(current_arg.strip())

    return {
        "syscall": syscall,
        "arguments": args,
        "return_value": return_value.strip(),
        "extra_info": extra.strip() if extra else None
    }


def parse_strace_file(filepath: str) -> List[Dict[str, Any]]:
    """Parse entire strace output file."""
    traces = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            parsed = parse_strace_line(line)
            if parsed:
                parsed['line_number'] = line_num
                parsed['raw_line'] = line.strip()
                traces.append(parsed)

    return traces


def main():
    parser = argparse.ArgumentParser(description='Parse strace output to JSON')
    parser.add_argument('input_file', help='Input strace file')
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')

    args = parser.parse_args()

    traces = parse_strace_file(args.input_file)

    output_data = {
        "trace_type": "strace",
        "source_file": args.input_file,
        "total_calls": len(traces),
        "traces": traces
    }

    indent = 2 if args.pretty else None
    json_output = json.dumps(output_data, indent=indent)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
        print(f"Parsed {len(traces)} system calls to {args.output}")
    else:
        print(json_output)


if __name__ == '__main__':
    main()
