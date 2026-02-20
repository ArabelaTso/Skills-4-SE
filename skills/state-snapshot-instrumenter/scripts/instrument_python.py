#!/usr/bin/env python3
"""
Instrument Python code to capture state snapshots at runtime.

Usage:
    python instrument_python.py <input_file> [--output <output_file>] [--mode <mode>]
"""

import ast
import argparse
import sys
from typing import List, Set


class SnapshotInstrumenter(ast.NodeTransformer):
    """AST transformer to add snapshot instrumentation."""

    def __init__(self, mode='manual', condition=None):
        self.mode = mode
        self.condition = condition
        self.snapshot_id = 0

    def _create_snapshot_call(self, location: str, snapshot_type: str = 'auto'):
        """Create AST node for snapshot call."""
        self.snapshot_id += 1
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__snapshot_runtime__', ctx=ast.Load()),
                    attr='capture_snapshot',
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=self.snapshot_id),
                    ast.Constant(value=location),
                    ast.Constant(value=snapshot_type),
                    ast.Call(
                        func=ast.Name(id='locals', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ),
                    ast.Call(
                        func=ast.Name(id='globals', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                ],
                keywords=[]
            )
        )

    def visit_FunctionDef(self, node):
        """Instrument function entry/exit if in auto mode."""
        self.generic_visit(node)

        if self.mode == 'auto':
            # Add snapshot at function entry
            entry_snapshot = self._create_snapshot_call(
                f"{node.name}:entry",
                'function_entry'
            )

            # Add snapshot before each return
            class ReturnInstrumenter(ast.NodeTransformer):
                def __init__(self, instrumenter):
                    self.instrumenter = instrumenter

                def visit_Return(self, ret_node):
                    snapshot = self.instrumenter._create_snapshot_call(
                        f"{node.name}:exit",
                        'function_exit'
                    )
                    # Return both snapshot and original return
                    return [snapshot, ret_node]

            return_instrumenter = ReturnInstrumenter(self)
            node.body = [entry_snapshot] + node.body
            node.body = [return_instrumenter.visit(stmt) if isinstance(stmt, ast.Return) else stmt
                        for stmt in node.body]
            # Flatten list (in case Return was replaced with list)
            new_body = []
            for stmt in node.body:
                if isinstance(stmt, list):
                    new_body.extend(stmt)
                else:
                    new_body.append(stmt)
            node.body = new_body

        return node

    def visit_Call(self, node):
        """Look for manual snapshot markers."""
        self.generic_visit(node)

        # Check for __SNAPSHOT__ marker
        if (isinstance(node.func, ast.Name) and
            node.func.id == '__SNAPSHOT__'):
            # Replace with actual snapshot call
            location = node.args[0].value if node.args else 'unknown'
            return self._create_snapshot_call(location, 'manual').value

        return node


def instrument_python_code(source_code: str, mode: str = 'manual') -> str:
    """Instrument Python source code with snapshot calls."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Syntax error in source code: {e}", file=sys.stderr)
        return source_code

    # Add import for snapshot runtime
    import_node = ast.Import(
        names=[ast.alias(name='snapshot_runtime', asname='__snapshot_runtime__')]
    )
    tree.body.insert(0, import_node)

    # Transform AST
    instrumenter = SnapshotInstrumenter(mode=mode)
    tree = instrumenter.visit(tree)
    ast.fix_missing_locations(tree)

    # Convert back to source
    try:
        import astor
        return astor.to_source(tree)
    except ImportError:
        # Fallback: use ast.unparse (Python 3.9+)
        try:
            return ast.unparse(tree)
        except AttributeError:
            print("Error: Need 'astor' package or Python 3.9+ for code generation", file=sys.stderr)
            print("Install with: pip install astor", file=sys.stderr)
            return source_code


def main():
    parser = argparse.ArgumentParser(description='Instrument Python code with state snapshots')
    parser.add_argument('input_file', help='Input Python file')
    parser.add_argument('--output', '-o', help='Output file (default: <input>_instrumented.py)')
    parser.add_argument('--mode', choices=['manual', 'auto'], default='manual',
                       help='Instrumentation mode: manual (only __SNAPSHOT__ markers) or auto (all functions)')
    parser.add_argument('--inplace', action='store_true', help='Modify file in place')

    args = parser.parse_args()

    # Read input file
    with open(args.input_file, 'r') as f:
        source_code = f.read()

    # Instrument code
    instrumented_code = instrument_python_code(source_code, mode=args.mode)

    # Determine output file
    if args.inplace:
        output_file = args.input_file
    elif args.output:
        output_file = args.output
    else:
        output_file = args.input_file.replace('.py', '_instrumented.py')

    # Write output
    with open(output_file, 'w') as f:
        f.write(instrumented_code)

    print(f"Instrumented code written to: {output_file}")


if __name__ == '__main__':
    main()
