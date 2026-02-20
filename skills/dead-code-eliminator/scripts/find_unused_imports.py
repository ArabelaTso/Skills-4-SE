#!/usr/bin/env python3
"""
Find unused imports in Python files.
Uses AST analysis to identify imports that are never used.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Set, List, Tuple


class ImportCollector(ast.NodeVisitor):
    """Collect all imports."""

    def __init__(self):
        self.imports: List[Tuple[str, int, str]] = []  # (name, line, type)

    def visit_Import(self, node):
        """Visit import statement."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.append((name, node.lineno, 'import'))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visit from...import statement."""
        for alias in node.names:
            if alias.name == '*':
                continue  # Skip wildcard imports
            name = alias.asname if alias.asname else alias.name
            self.imports.append((name, node.lineno, 'from'))
        self.generic_visit(node)


class NameUsageCollector(ast.NodeVisitor):
    """Collect all name usages."""

    def __init__(self, imported_names: Set[str]):
        self.imported_names = imported_names
        self.used_names: Set[str] = set()

    def visit_Name(self, node):
        """Visit name reference."""
        if node.id in self.imported_names:
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Visit attribute access."""
        if isinstance(node.value, ast.Name) and node.value.id in self.imported_names:
            self.used_names.add(node.value.id)
        self.generic_visit(node)


def find_unused_imports(filepath: Path) -> List[Tuple[str, int]]:
    """
    Find unused imports in a Python file.

    Args:
        filepath: Path to Python file

    Returns:
        List of (import_name, line_number) tuples for unused imports
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content, filename=str(filepath))

        # Collect imports
        import_collector = ImportCollector()
        import_collector.visit(tree)

        if not import_collector.imports:
            return []

        # Get all imported names
        imported_names = {name for name, _, _ in import_collector.imports}

        # Collect name usages
        usage_collector = NameUsageCollector(imported_names)
        usage_collector.visit(tree)

        # Find unused imports
        unused = []
        for name, line, import_type in import_collector.imports:
            if name not in usage_collector.used_names:
                unused.append((name, line))

        return unused

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return []


def scan_directory(directory: str, exclude_dirs: List[str] = None):
    """
    Scan directory for unused imports.

    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '.venv', 'env', '__pycache__', '.git', 'node_modules']

    root = Path(directory)
    total_unused = 0
    files_with_unused = 0

    for py_file in sorted(root.rglob('*.py')):
        # Skip excluded directories
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        unused = find_unused_imports(py_file)

        if unused:
            files_with_unused += 1
            print(f"\n{py_file}:")
            for name, line in sorted(unused, key=lambda x: x[1]):
                print(f"  Line {line}: {name}")
                total_unused += 1

    return total_unused, files_with_unused


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python find_unused_imports.py <file_or_directory> [exclude_dir1,exclude_dir2,...]")
        sys.exit(1)

    path = sys.argv[1]
    exclude_dirs = sys.argv[2].split(',') if len(sys.argv) > 2 else None

    if os.path.isfile(path):
        # Single file
        unused = find_unused_imports(Path(path))
        if unused:
            print(f"\n{path}:")
            for name, line in sorted(unused, key=lambda x: x[1]):
                print(f"  Line {line}: {name}")
            print(f"\nFound {len(unused)} unused imports")
        else:
            print("✅ No unused imports found!")

    elif os.path.isdir(path):
        # Directory
        print(f"Scanning {path} for unused imports...\n")
        total, files = scan_directory(path, exclude_dirs)

        if total == 0:
            print("\n✅ No unused imports found!")
        else:
            print(f"\n\nFound {total} unused imports in {files} files")

    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
