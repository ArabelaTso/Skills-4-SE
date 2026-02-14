#!/usr/bin/env python3
"""
Detect code smells in Python code using AST analysis.
Focuses on code quality and design smells.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CodeSmell:
    """Represents a detected code smell."""
    smell_type: str
    severity: str  # 'high', 'medium', 'low'
    file_path: str
    line_number: int
    name: str
    description: str
    recommendation: str


class SmellDetector(ast.NodeVisitor):
    """Detect various code smells in Python code."""

    def __init__(self, filepath: str, max_function_length: int = 50, max_params: int = 5):
        self.filepath = filepath
        self.max_function_length = max_function_length
        self.max_params = max_params
        self.smells: List[CodeSmell] = []
        self.current_class = None

    def visit_FunctionDef(self, node):
        """Check functions for code smells."""
        # Long method
        function_length = self._count_lines(node)
        if function_length > self.max_function_length:
            self.smells.append(CodeSmell(
                smell_type="Long Method",
                severity="medium",
                file_path=self.filepath,
                line_number=node.lineno,
                name=node.name,
                description=f"Function has {function_length} lines (limit: {self.max_function_length})",
                recommendation="Break down into smaller, focused functions"
            ))

        # Too many parameters
        param_count = len(node.args.args) + len(node.args.kwonlyargs)
        if param_count > self.max_params:
            self.smells.append(CodeSmell(
                smell_type="Too Many Parameters",
                severity="medium",
                file_path=self.filepath,
                line_number=node.lineno,
                name=node.name,
                description=f"Function has {param_count} parameters (limit: {self.max_params})",
                recommendation="Consider using parameter objects or builder pattern"
            ))

        # Check for magic numbers
        self._check_magic_numbers(node)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Check async functions."""
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        """Check classes for code smells."""
        old_class = self.current_class
        self.current_class = node.name

        # Large class (too many methods)
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        if len(methods) > 15:
            self.smells.append(CodeSmell(
                smell_type="Large Class",
                severity="high",
                file_path=self.filepath,
                line_number=node.lineno,
                name=node.name,
                description=f"Class has {len(methods)} methods (recommended max: 15)",
                recommendation="Split into multiple classes with single responsibilities"
            ))

        # God class (too many responsibilities)
        if len(methods) > 20:
            self.smells.append(CodeSmell(
                smell_type="God Class",
                severity="high",
                file_path=self.filepath,
                line_number=node.lineno,
                name=node.name,
                description=f"Class has {len(methods)} methods and likely too many responsibilities",
                recommendation="Apply Single Responsibility Principle - split into focused classes"
            ))

        self.generic_visit(node)
        self.current_class = old_class

    def _count_lines(self, node) -> int:
        """Count non-empty lines in a function."""
        if not hasattr(node, 'body'):
            return 0

        min_line = node.lineno
        max_line = node.lineno

        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                max_line = max(max_line, child.lineno)

        return max_line - min_line + 1

    def _check_magic_numbers(self, node):
        """Check for magic numbers in function."""
        for child in ast.walk(node):
            if isinstance(child, ast.Num):
                # Skip common acceptable numbers
                if child.n not in [0, 1, -1, 2, 10, 100, 1000]:
                    self.smells.append(CodeSmell(
                        smell_type="Magic Number",
                        severity="low",
                        file_path=self.filepath,
                        line_number=child.lineno,
                        name=node.name if hasattr(node, 'name') else 'unknown',
                        description=f"Magic number {child.n} found",
                        recommendation="Replace with named constant"
                    ))


def analyze_file(filepath: Path, max_function_length: int = 50, max_params: int = 5) -> List[CodeSmell]:
    """Analyze a Python file for code smells."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))

        detector = SmellDetector(str(filepath), max_function_length, max_params)
        detector.visit(tree)

        return detector.smells

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return []


def detect_smells(directory: str, exclude_dirs: List[str] = None) -> Dict[str, List[CodeSmell]]:
    """
    Detect code smells in a Python codebase.

    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude

    Returns:
        Dictionary mapping smell types to lists of CodeSmell instances
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '.venv', 'env', '__pycache__', '.git', 'node_modules']

    root = Path(directory)
    all_smells: List[CodeSmell] = []

    for py_file in root.rglob('*.py'):
        # Skip excluded directories
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        smells = analyze_file(py_file)
        all_smells.extend(smells)

    # Group by smell type
    smells_by_type: Dict[str, List[CodeSmell]] = {}
    for smell in all_smells:
        if smell.smell_type not in smells_by_type:
            smells_by_type[smell.smell_type] = []
        smells_by_type[smell.smell_type].append(smell)

    return smells_by_type


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python detect_smells.py <directory> [exclude_dir1,exclude_dir2,...]")
        sys.exit(1)

    directory = sys.argv[1]
    exclude_dirs = sys.argv[2].split(',') if len(sys.argv) > 2 else None

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Scanning {directory} for code smells...\n")

    smells_by_type = detect_smells(directory, exclude_dirs)

    if not smells_by_type:
        print("✅ No code smells detected!")
        return

    total_smells = sum(len(smells) for smells in smells_by_type.values())
    print(f"Found {total_smells} code smells:\n")

    severity_order = {'high': 0, 'medium': 1, 'low': 2}

    for smell_type in sorted(smells_by_type.keys()):
        smells = sorted(smells_by_type[smell_type], key=lambda s: (severity_order[s.severity], s.file_path, s.line_number))

        print(f"\n{smell_type} ({len(smells)} occurrences):")
        print("=" * 60)

        for smell in smells[:5]:  # Show first 5 of each type
            severity_icon = "🔴" if smell.severity == "high" else "🟡" if smell.severity == "medium" else "🔵"
            print(f"{severity_icon} {smell.file_path}:{smell.line_number}")
            print(f"   {smell.name}: {smell.description}")
            print(f"   → {smell.recommendation}")
            print()

        if len(smells) > 5:
            print(f"   ... and {len(smells) - 5} more")


if __name__ == '__main__':
    main()
