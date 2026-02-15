#!/usr/bin/env python3
"""
Extract test case documentation from Python test files.
Analyzes test functions to generate structured documentation.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a test case extracted from code."""
    name: str
    file_path: str
    line_number: int
    class_name: Optional[str]
    docstring: Optional[str]
    test_type: str  # 'unit', 'integration', 'e2e', 'other'
    tags: List[str]


class TestExtractor(ast.NodeVisitor):
    """Extract test cases from Python AST."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.test_cases: List[TestCase] = []
        self.current_class = None

    def visit_ClassDef(self, node):
        """Visit test class definition."""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        """Visit function definition and extract test cases."""
        if node.name.startswith('test_'):
            # Extract docstring
            docstring = ast.get_docstring(node)

            # Determine test type from name or decorators
            test_type = self._determine_test_type(node)

            # Extract tags from decorators
            tags = self._extract_tags(node)

            test_case = TestCase(
                name=node.name,
                file_path=self.filepath,
                line_number=node.lineno,
                class_name=self.current_class,
                docstring=docstring,
                test_type=test_type,
                tags=tags
            )

            self.test_cases.append(test_case)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async test functions."""
        if node.name.startswith('test_'):
            self.visit_FunctionDef(node)

    def _determine_test_type(self, node) -> str:
        """Determine test type from name or decorators."""
        name_lower = node.name.lower()

        if 'integration' in name_lower or 'e2e' in name_lower:
            return 'integration'
        elif 'unit' in name_lower:
            return 'unit'

        # Check decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id in ['integration_test', 'e2e_test']:
                    return 'integration'
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ['integration', 'e2e']:
                    return 'integration'

        return 'unit'  # Default to unit test

    def _extract_tags(self, node) -> List[str]:
        """Extract tags from decorators like @pytest.mark.tag."""
        tags = []

        for decorator in node.decorator_list:
            # pytest.mark.tag format
            if isinstance(decorator, ast.Attribute):
                if isinstance(decorator.value, ast.Attribute):
                    if decorator.value.attr == 'mark':
                        tags.append(decorator.attr)
            # @slow, @skip, etc.
            elif isinstance(decorator, ast.Name):
                if decorator.id in ['slow', 'skip', 'skipif', 'parametrize']:
                    tags.append(decorator.id)

        return tags


def extract_tests_from_file(filepath: Path) -> List[TestCase]:
    """Extract test cases from a Python test file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))

        extractor = TestExtractor(str(filepath))
        extractor.visit(tree)

        return extractor.test_cases

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return []


def extract_tests_from_directory(directory: str, exclude_dirs: List[str] = None) -> Dict[str, List[TestCase]]:
    """
    Extract test cases from all test files in a directory.

    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude

    Returns:
        Dictionary mapping file paths to lists of TestCase instances
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '.venv', 'env', '__pycache__', '.git', 'node_modules']

    root = Path(directory)
    tests_by_file: Dict[str, List[TestCase]] = {}

    # Find test files
    test_files = []
    for pattern in ['**/test_*.py', '**/*_test.py', '**/tests.py']:
        test_files.extend(root.glob(pattern))

    # Remove duplicates
    test_files = list(set(test_files))

    for test_file in sorted(test_files):
        # Skip excluded directories
        if any(excluded in test_file.parts for excluded in exclude_dirs):
            continue

        test_cases = extract_tests_from_file(test_file)

        if test_cases:
            tests_by_file[str(test_file)] = test_cases

    return tests_by_file


def generate_summary_stats(tests_by_file: Dict[str, List[TestCase]]) -> Dict[str, int]:
    """Generate summary statistics about tests."""
    stats = {
        'total_files': len(tests_by_file),
        'total_tests': 0,
        'unit_tests': 0,
        'integration_tests': 0,
        'tests_with_docstrings': 0,
        'tests_without_docstrings': 0,
    }

    for test_cases in tests_by_file.values():
        stats['total_tests'] += len(test_cases)
        for test in test_cases:
            if test.test_type == 'unit':
                stats['unit_tests'] += 1
            elif test.test_type == 'integration':
                stats['integration_tests'] += 1

            if test.docstring:
                stats['tests_with_docstrings'] += 1
            else:
                stats['tests_without_docstrings'] += 1

    return stats


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python extract_tests.py <directory> [exclude_dir1,exclude_dir2,...]")
        sys.exit(1)

    directory = sys.argv[1]
    exclude_dirs = sys.argv[2].split(',') if len(sys.argv) > 2 else None

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Extracting test cases from {directory}...\n")

    tests_by_file = extract_tests_from_directory(directory, exclude_dirs)

    if not tests_by_file:
        print("No test files found!")
        return

    stats = generate_summary_stats(tests_by_file)

    print("Summary:")
    print(f"  Test files: {stats['total_files']}")
    print(f"  Total tests: {stats['total_tests']}")
    print(f"  Unit tests: {stats['unit_tests']}")
    print(f"  Integration tests: {stats['integration_tests']}")
    print(f"  Tests with documentation: {stats['tests_with_docstrings']}")
    print(f"  Tests without documentation: {stats['tests_without_docstrings']}")
    print()

    # Show sample tests
    print("Sample test cases:")
    print("=" * 80)

    for file_path in sorted(tests_by_file.keys())[:3]:  # Show first 3 files
        test_cases = tests_by_file[file_path]
        print(f"\n{file_path}")
        print("-" * 80)

        for test in test_cases[:5]:  # Show first 5 tests per file
            print(f"\n  {test.name} (line {test.line_number})")
            if test.class_name:
                print(f"    Class: {test.class_name}")
            print(f"    Type: {test.test_type}")
            if test.tags:
                print(f"    Tags: {', '.join(test.tags)}")
            if test.docstring:
                # Show first line of docstring
                first_line = test.docstring.split('\n')[0]
                print(f"    Doc: {first_line}")
            else:
                print(f"    Doc: [No documentation]")

        if len(test_cases) > 5:
            print(f"\n  ... and {len(test_cases) - 5} more tests")


if __name__ == '__main__':
    main()
