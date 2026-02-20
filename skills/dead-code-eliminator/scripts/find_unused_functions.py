#!/usr/bin/env python3
"""
Find unused functions and methods in Python codebase.
Uses AST analysis to identify functions that are never called.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Set, Dict, List, Tuple


class FunctionCollector(ast.NodeVisitor):
    """Collect all function and method definitions."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.functions: List[Tuple[str, int]] = []

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        # Skip private/magic methods and test functions
        if not node.name.startswith('_') and not node.name.startswith('test_'):
            self.functions.append((node.name, node.lineno))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition."""
        if not node.name.startswith('_') and not node.name.startswith('test_'):
            self.functions.append((node.name, node.lineno))
        self.generic_visit(node)


class FunctionCallCollector(ast.NodeVisitor):
    """Collect all function calls."""

    def __init__(self):
        self.calls: Set[str] = set()

    def visit_Call(self, node):
        """Visit function call."""
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        self.generic_visit(node)


def analyze_file(filepath: Path) -> Tuple[List[Tuple[str, int]], Set[str]]:
    """Analyze a Python file for function definitions and calls."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))

        # Collect function definitions
        func_collector = FunctionCollector(str(filepath))
        func_collector.visit(tree)

        # Collect function calls
        call_collector = FunctionCallCollector()
        call_collector.visit(tree)

        return func_collector.functions, call_collector.calls

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return [], set()


def find_unused_functions(directory: str, exclude_dirs: List[str] = None) -> Dict[str, List[Tuple[str, int]]]:
    """
    Find unused functions in a Python codebase.

    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude (e.g., ['tests', 'venv'])

    Returns:
        Dictionary mapping file paths to lists of (function_name, line_number) tuples
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '.venv', 'env', '__pycache__', '.git', 'node_modules', 'tests', 'test']

    root = Path(directory)
    all_functions: Dict[str, List[Tuple[str, int]]] = {}
    all_calls: Set[str] = set()

    # Collect all function definitions and calls
    for py_file in root.rglob('*.py'):
        # Skip excluded directories
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        functions, calls = analyze_file(py_file)

        if functions:
            all_functions[str(py_file)] = functions

        all_calls.update(calls)

    # Find unused functions
    unused: Dict[str, List[Tuple[str, int]]] = {}

    for filepath, functions in all_functions.items():
        unused_in_file = [(name, line) for name, line in functions if name not in all_calls]
        if unused_in_file:
            unused[filepath] = unused_in_file

    return unused


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python find_unused_functions.py <directory> [exclude_dir1,exclude_dir2,...]")
        sys.exit(1)

    directory = sys.argv[1]
    exclude_dirs = sys.argv[2].split(',') if len(sys.argv) > 2 else None

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Scanning {directory} for unused functions...\n")

    unused = find_unused_functions(directory, exclude_dirs)

    if not unused:
        print("✅ No unused functions found!")
        return

    print(f"Found {sum(len(funcs) for funcs in unused.values())} unused functions:\n")

    for filepath in sorted(unused.keys()):
        print(f"\n{filepath}:")
        for func_name, line_num in sorted(unused[filepath], key=lambda x: x[1]):
            print(f"  Line {line_num}: {func_name}()")


if __name__ == '__main__':
    main()
