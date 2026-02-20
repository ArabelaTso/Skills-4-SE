#!/usr/bin/env python3
"""
Extract debugging-relevant information from normalized trace JSON.

Usage:
    python extract_debug_info.py <input_json> [options]
"""

import json
import argparse
from typing import List, Dict, Any
from collections import defaultdict


def extract_file_operations(traces: List[Dict]) -> Dict[str, Any]:
    """Extract file operation patterns."""
    file_ops = {
        'open': [],
        'read': [],
        'write': [],
        'close': [],
        'errors': []
    }

    for trace in traces:
        syscall = trace.get('syscall', '')
        args = trace.get('arguments', [])
        ret_val = trace.get('return_value', '')

        if syscall in ['open', 'openat']:
            filename = args[0] if args else 'unknown'
            file_ops['open'].append({
                'file': filename,
                'return': ret_val,
                'line': trace.get('line_number')
            })
            if ret_val.startswith('-'):
                file_ops['errors'].append({
                    'operation': 'open',
                    'file': filename,
                    'error': ret_val,
                    'line': trace.get('line_number')
                })

        elif syscall in ['read', 'pread64']:
            fd = args[0] if args else 'unknown'
            file_ops['read'].append({
                'fd': fd,
                'return': ret_val,
                'line': trace.get('line_number')
            })

        elif syscall in ['write', 'pwrite64']:
            fd = args[0] if args else 'unknown'
            file_ops['write'].append({
                'fd': fd,
                'return': ret_val,
                'line': trace.get('line_number')
            })

        elif syscall == 'close':
            fd = args[0] if args else 'unknown'
            file_ops['close'].append({
                'fd': fd,
                'return': ret_val,
                'line': trace.get('line_number')
            })

    return file_ops


def extract_network_operations(traces: List[Dict]) -> Dict[str, Any]:
    """Extract network operation patterns."""
    net_ops = {
        'socket': [],
        'connect': [],
        'bind': [],
        'listen': [],
        'accept': [],
        'send': [],
        'recv': [],
        'errors': []
    }

    for trace in traces:
        syscall = trace.get('syscall', '')
        ret_val = trace.get('return_value', '')

        if syscall in net_ops:
            net_ops[syscall].append({
                'return': ret_val,
                'line': trace.get('line_number'),
                'args': trace.get('arguments', [])
            })

            if ret_val.startswith('-'):
                net_ops['errors'].append({
                    'operation': syscall,
                    'error': ret_val,
                    'line': trace.get('line_number')
                })

    return net_ops


def extract_process_operations(traces: List[Dict]) -> Dict[str, Any]:
    """Extract process/thread operations."""
    proc_ops = {
        'fork': [],
        'clone': [],
        'execve': [],
        'exit': [],
        'errors': []
    }

    for trace in traces:
        syscall = trace.get('syscall', '')
        ret_val = trace.get('return_value', '')

        if syscall in ['fork', 'vfork']:
            proc_ops['fork'].append({
                'return': ret_val,
                'line': trace.get('line_number')
            })

        elif syscall == 'clone':
            proc_ops['clone'].append({
                'return': ret_val,
                'line': trace.get('line_number'),
                'args': trace.get('arguments', [])
            })

        elif syscall == 'execve':
            args = trace.get('arguments', [])
            proc_ops['execve'].append({
                'program': args[0] if args else 'unknown',
                'return': ret_val,
                'line': trace.get('line_number')
            })

            if ret_val.startswith('-'):
                proc_ops['errors'].append({
                    'operation': 'execve',
                    'program': args[0] if args else 'unknown',
                    'error': ret_val,
                    'line': trace.get('line_number')
                })

        elif syscall in ['exit', 'exit_group']:
            proc_ops['exit'].append({
                'code': trace.get('arguments', ['unknown'])[0],
                'line': trace.get('line_number')
            })

    return proc_ops


def extract_error_summary(traces: List[Dict]) -> List[Dict[str, Any]]:
    """Extract all errors from traces."""
    errors = []

    for trace in traces:
        ret_val = trace.get('return_value', '')
        if ret_val.startswith('-'):
            errors.append({
                'call': trace.get('syscall') or trace.get('function'),
                'error': ret_val,
                'line': trace.get('line_number'),
                'arguments': trace.get('arguments', [])
            })

    return errors


def main():
    parser = argparse.ArgumentParser(description='Extract debugging info from trace JSON')
    parser.add_argument('input_file', help='Input JSON file')
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)')
    parser.add_argument('--category', choices=['file', 'network', 'process', 'errors', 'all'],
                       default='all', help='Category of information to extract')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')

    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        data = json.load(f)

    traces = data.get('traces', [])

    debug_info = {
        'source_file': data.get('source_file'),
        'trace_type': data.get('trace_type'),
        'total_calls': len(traces)
    }

    if args.category in ['file', 'all']:
        debug_info['file_operations'] = extract_file_operations(traces)

    if args.category in ['network', 'all']:
        debug_info['network_operations'] = extract_network_operations(traces)

    if args.category in ['process', 'all']:
        debug_info['process_operations'] = extract_process_operations(traces)

    if args.category in ['errors', 'all']:
        debug_info['errors'] = extract_error_summary(traces)

    indent = 2 if args.pretty else None
    json_output = json.dumps(debug_info, indent=indent)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
        print(f"Extracted debug info to {args.output}")
    else:
        print(json_output)


if __name__ == '__main__':
    main()
