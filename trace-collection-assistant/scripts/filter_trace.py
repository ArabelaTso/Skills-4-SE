#!/usr/bin/env python3
"""
Filter and clean normalized trace JSON data.

Usage:
    python filter_trace.py <input_json> [options]
"""

import json
import argparse
import re
from typing import List, Dict, Any, Set


def filter_by_calls(traces: List[Dict], include: Set[str] = None, exclude: Set[str] = None) -> List[Dict]:
    """Filter traces by syscall/function names."""
    filtered = []
    for trace in traces:
        call_name = trace.get('syscall') or trace.get('function')

        if exclude and call_name in exclude:
            continue

        if include and call_name not in include:
            continue

        filtered.append(trace)

    return filtered


def filter_by_return_value(traces: List[Dict], pattern: str = None, error_only: bool = False) -> List[Dict]:
    """Filter traces by return value."""
    filtered = []
    for trace in traces:
        return_val = trace.get('return_value', '')

        if error_only and not return_val.startswith('-'):
            continue

        if pattern and not re.search(pattern, return_val):
            continue

        filtered.append(trace)

    return filtered


def filter_by_arguments(traces: List[Dict], pattern: str) -> List[Dict]:
    """Filter traces by argument content."""
    filtered = []
    for trace in traces:
        args = trace.get('arguments', [])
        args_str = ' '.join(str(arg) for arg in args)

        if re.search(pattern, args_str):
            filtered.append(trace)

    return filtered


def remove_noise(traces: List[Dict]) -> List[Dict]:
    """Remove common noise syscalls that are rarely relevant for debugging."""
    noise_calls = {
        'gettimeofday', 'clock_gettime', 'getpid', 'getuid', 'getgid',
        'geteuid', 'getegid', 'getppid', 'arch_prctl', 'set_tid_address',
        'set_robust_list', 'rt_sigaction', 'rt_sigprocmask', 'prlimit64'
    }

    return [t for t in traces if (t.get('syscall') or t.get('function')) not in noise_calls]


def main():
    parser = argparse.ArgumentParser(description='Filter and clean trace JSON data')
    parser.add_argument('input_file', help='Input JSON file')
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)')
    parser.add_argument('--include-calls', help='Comma-separated list of calls to include')
    parser.add_argument('--exclude-calls', help='Comma-separated list of calls to exclude')
    parser.add_argument('--error-only', action='store_true', help='Only show failed calls')
    parser.add_argument('--return-pattern', help='Regex pattern for return values')
    parser.add_argument('--arg-pattern', help='Regex pattern for arguments')
    parser.add_argument('--remove-noise', action='store_true', help='Remove common noise syscalls')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')

    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        data = json.load(f)

    traces = data.get('traces', [])

    # Apply filters
    if args.include_calls:
        include_set = set(args.include_calls.split(','))
        traces = filter_by_calls(traces, include=include_set)

    if args.exclude_calls:
        exclude_set = set(args.exclude_calls.split(','))
        traces = filter_by_calls(traces, exclude=exclude_set)

    if args.error_only or args.return_pattern:
        traces = filter_by_return_value(traces, args.return_pattern, args.error_only)

    if args.arg_pattern:
        traces = filter_by_arguments(traces, args.arg_pattern)

    if args.remove_noise:
        traces = remove_noise(traces)

    # Update data
    data['traces'] = traces
    data['total_calls'] = len(traces)
    data['filtered'] = True

    indent = 2 if args.pretty else None
    json_output = json.dumps(data, indent=indent)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
        print(f"Filtered to {len(traces)} calls, saved to {args.output}")
    else:
        print(json_output)


if __name__ == '__main__':
    main()
