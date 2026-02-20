#!/usr/bin/env python3
"""
Instrument C/C++ code to capture state snapshots at runtime.

Usage:
    python instrument_c.py <input_file> [--output <output_file>] [--mode <mode>]
"""

import re
import argparse
import sys
from typing import List, Tuple


class CInstrumenter:
    """Instrumenter for C/C++ code."""

    def __init__(self, mode='manual'):
        self.mode = mode
        self.snapshot_id = 0

    def _generate_snapshot_call(self, location: str, snapshot_type: str, variables: List[str] = None) -> str:
        """Generate C code for snapshot call."""
        self.snapshot_id += 1

        var_captures = ""
        if variables:
            for var in variables:
                var_captures += f'    snapshot_add_variable(&snapshot, "{var}", &{var}, sizeof({var}));\n'

        return f'''    // Snapshot {self.snapshot_id}: {location}
    {{
        Snapshot snapshot;
        snapshot_init(&snapshot, {self.snapshot_id}, "{location}", "{snapshot_type}");
{var_captures}        snapshot_capture(&snapshot);
        snapshot_free(&snapshot);
    }}
'''

    def instrument_manual(self, code: str) -> str:
        """Instrument code at manual markers (__SNAPSHOT__)."""
        # Find __SNAPSHOT__("location") markers
        pattern = r'__SNAPSHOT__\s*\(\s*"([^"]+)"\s*\)\s*;'

        def replace_marker(match):
            location = match.group(1)
            return self._generate_snapshot_call(location, 'manual')

        return re.sub(pattern, replace_marker, code)

    def instrument_functions(self, code: str) -> str:
        """Instrument all function entry/exit points."""
        # Simple regex-based function detection (not perfect but works for many cases)
        # Pattern: return_type function_name(params) {
        func_pattern = r'(\w+\s+\*?\s*\w+\s*\([^)]*\)\s*)\{'

        def add_entry_snapshot(match):
            func_decl = match.group(1)
            # Extract function name
            name_match = re.search(r'\b(\w+)\s*\(', func_decl)
            if name_match:
                func_name = name_match.group(1)
                snapshot_call = self._generate_snapshot_call(f"{func_name}:entry", 'function_entry')
                return func_decl + '{\n' + snapshot_call
            return match.group(0)

        instrumented = re.sub(func_pattern, add_entry_snapshot, code)

        # Add snapshots before return statements
        return_pattern = r'(\s+)(return\s+[^;]+;)'

        def add_exit_snapshot(match):
            indent = match.group(1)
            return_stmt = match.group(2)
            snapshot_call = self._generate_snapshot_call("function:exit", 'function_exit')
            return indent + snapshot_call + indent + return_stmt

        instrumented = re.sub(return_pattern, add_exit_snapshot, instrumented)

        return instrumented

    def add_includes(self, code: str) -> str:
        """Add necessary includes for snapshot runtime."""
        includes = '#include "snapshot_runtime.h"\n'

        # Add after existing includes or at the beginning
        if '#include' in code:
            # Find last include
            last_include = 0
            for match in re.finditer(r'#include\s+[<"][^>"]+[>"]', code):
                last_include = match.end()
            return code[:last_include] + '\n' + includes + code[last_include:]
        else:
            return includes + '\n' + code

    def instrument(self, code: str) -> str:
        """Main instrumentation entry point."""
        # Add includes
        code = self.add_includes(code)

        # Instrument based on mode
        if self.mode == 'manual':
            code = self.instrument_manual(code)
        elif self.mode == 'auto':
            code = self.instrument_manual(code)  # Still handle manual markers
            code = self.instrument_functions(code)

        return code


def main():
    parser = argparse.ArgumentParser(description='Instrument C/C++ code with state snapshots')
    parser.add_argument('input_file', help='Input C/C++ file')
    parser.add_argument('--output', '-o', help='Output file (default: <input>_instrumented.c)')
    parser.add_argument('--mode', choices=['manual', 'auto'], default='manual',
                       help='Instrumentation mode: manual (only __SNAPSHOT__ markers) or auto (all functions)')
    parser.add_argument('--inplace', action='store_true', help='Modify file in place')

    args = parser.parse_args()

    # Read input file
    with open(args.input_file, 'r') as f:
        source_code = f.read()

    # Instrument code
    instrumenter = CInstrumenter(mode=args.mode)
    instrumented_code = instrumenter.instrument(source_code)

    # Determine output file
    if args.inplace:
        output_file = args.input_file
    elif args.output:
        output_file = args.output
    else:
        # Preserve extension
        if args.input_file.endswith('.cpp') or args.input_file.endswith('.cc'):
            output_file = args.input_file.replace('.cpp', '_instrumented.cpp').replace('.cc', '_instrumented.cc')
        else:
            output_file = args.input_file.replace('.c', '_instrumented.c')

    # Write output
    with open(output_file, 'w') as f:
        f.write(instrumented_code)

    print(f"Instrumented code written to: {output_file}")
    print(f"\nNote: You need to compile with snapshot_runtime.c and link appropriately.")


if __name__ == '__main__':
    main()
