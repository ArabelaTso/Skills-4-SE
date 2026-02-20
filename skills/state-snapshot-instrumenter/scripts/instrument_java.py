#!/usr/bin/env python3
"""
Instrument Java code to capture state snapshots at runtime.

Usage:
    python instrument_java.py <input_file> [--output <output_file>] [--mode <mode>]
"""

import re
import argparse
import sys
from typing import List


class JavaInstrumenter:
    """Instrumenter for Java code."""

    def __init__(self, mode='manual'):
        self.mode = mode
        self.snapshot_id = 0

    def _generate_snapshot_call(self, location: str, snapshot_type: str) -> str:
        """Generate Java code for snapshot call."""
        self.snapshot_id += 1
        return f'''        // Snapshot {self.snapshot_id}: {location}
        SnapshotRuntime.captureSnapshot({self.snapshot_id}, "{location}", "{snapshot_type}");
'''

    def instrument_manual(self, code: str) -> str:
        """Instrument code at manual markers (__SNAPSHOT__)."""
        # Find __SNAPSHOT__("location") markers
        pattern = r'__SNAPSHOT__\s*\(\s*"([^"]+)"\s*\)\s*;'

        def replace_marker(match):
            location = match.group(1)
            return self._generate_snapshot_call(location, 'manual')

        return re.sub(pattern, replace_marker, code)

    def instrument_methods(self, code: str) -> str:
        """Instrument all method entry/exit points."""
        # Pattern for method declarations
        # Simplified pattern - matches: modifiers returnType methodName(params) {
        method_pattern = r'((?:public|private|protected|static|final|synchronized|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*)\{'

        def add_entry_snapshot(match):
            method_decl = match.group(1)
            method_name = match.group(2)
            snapshot_call = self._generate_snapshot_call(f"{method_name}:entry", 'method_entry')
            return method_decl + '{\n' + snapshot_call

        instrumented = re.sub(method_pattern, add_entry_snapshot, code)

        # Add snapshots before return statements
        return_pattern = r'(\s+)(return\s+[^;]+;)'

        def add_exit_snapshot(match):
            indent = match.group(1)
            return_stmt = match.group(2)
            snapshot_call = self._generate_snapshot_call("method:exit", 'method_exit')
            return indent + snapshot_call + indent + return_stmt

        instrumented = re.sub(return_pattern, add_exit_snapshot, instrumented)

        return instrumented

    def add_import(self, code: str) -> str:
        """Add import for snapshot runtime."""
        import_stmt = 'import snapshot.SnapshotRuntime;\n'

        # Add after package declaration or at the beginning
        if 'package ' in code:
            # Find package declaration
            package_match = re.search(r'package\s+[\w.]+\s*;', code)
            if package_match:
                pos = package_match.end()
                return code[:pos] + '\n\n' + import_stmt + code[pos:]

        # Add after existing imports or at the beginning
        if 'import ' in code:
            # Find last import
            last_import = 0
            for match in re.finditer(r'import\s+[\w.*]+\s*;', code):
                last_import = match.end()
            return code[:last_import] + '\n' + import_stmt + code[last_import:]
        else:
            return import_stmt + '\n' + code

    def instrument(self, code: str) -> str:
        """Main instrumentation entry point."""
        # Add import
        code = self.add_import(code)

        # Instrument based on mode
        if self.mode == 'manual':
            code = self.instrument_manual(code)
        elif self.mode == 'auto':
            code = self.instrument_manual(code)  # Still handle manual markers
            code = self.instrument_methods(code)

        return code


def main():
    parser = argparse.ArgumentParser(description='Instrument Java code with state snapshots')
    parser.add_argument('input_file', help='Input Java file')
    parser.add_argument('--output', '-o', help='Output file (default: <input>_instrumented.java)')
    parser.add_argument('--mode', choices=['manual', 'auto'], default='manual',
                       help='Instrumentation mode: manual (only __SNAPSHOT__ markers) or auto (all methods)')
    parser.add_argument('--inplace', action='store_true', help='Modify file in place')

    args = parser.parse_args()

    # Read input file
    with open(args.input_file, 'r') as f:
        source_code = f.read()

    # Instrument code
    instrumenter = JavaInstrumenter(mode=args.mode)
    instrumented_code = instrumenter.instrument(source_code)

    # Determine output file
    if args.inplace:
        output_file = args.input_file
    elif args.output:
        output_file = args.output
    else:
        output_file = args.input_file.replace('.java', '_instrumented.java')

    # Write output
    with open(output_file, 'w') as f:
        f.write(instrumented_code)

    print(f"Instrumented code written to: {output_file}")
    print(f"\nNote: You need to include SnapshotRuntime.java in your project.")


if __name__ == '__main__':
    main()
