#!/usr/bin/env python3
"""
Main validator for comparing API behavior between two Python library versions.

Usage:
    python validate.py <old_version_path> <new_version_path> [--output <report.json>]
"""

import argparse
import ast
import inspect
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
import importlib.util


class APIValidator:
    """Validates API consistency between two Python library versions."""

    def __init__(self, old_path: Path, new_path: Path):
        self.old_path = old_path
        self.new_path = new_path
        self.differences = []
        self.breaking_changes = []
        self.warnings = []

    def validate(self) -> Dict[str, Any]:
        """Run complete validation."""
        print("=== API Behavior Consistency Validator ===\n")

        # Extract APIs from both versions
        print("Analyzing old version...")
        old_api = self._extract_api(self.old_path)

        print("Analyzing new version...")
        new_api = self._extract_api(self.new_path)

        # Compare APIs
        print("\nComparing APIs...")
        self._compare_apis(old_api, new_api)

        # Generate report
        report = self._generate_report(old_api, new_api)

        return report

    def _extract_api(self, path: Path) -> Dict[str, Any]:
        """Extract API definitions from Python code."""
        api = {
            'classes': {},
            'functions': {},
            'constants': {}
        }

        for py_file in path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        api['classes'][node.name] = self._analyze_class(node)
                    elif isinstance(node, ast.FunctionDef):
                        if not node.name.startswith('_'):
                            api['functions'][node.name] = self._analyze_function(node)

            except Exception as e:
                print(f"Warning: Could not parse {py_file}: {e}")

        return api

    def _analyze_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Analyze a class definition."""
        methods = {}

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods[item.name] = self._analyze_function(item)

        return {
            'name': node.name,
            'methods': methods,
            'bases': [self._get_name(base) for base in node.bases]
        }

    def _analyze_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Analyze a function definition."""
        params = []

        for arg in node.args.args:
            param_info = {
                'name': arg.arg,
                'annotation': self._get_annotation(arg.annotation)
            }
            params.append(param_info)

        return {
            'name': node.name,
            'parameters': params,
            'return_type': self._get_annotation(node.returns),
            'decorators': [self._get_name(d) for d in node.decorator_list]
        }

    def _get_annotation(self, node) -> str:
        """Get type annotation as string."""
        if node is None:
            return None
        return ast.unparse(node) if hasattr(ast, 'unparse') else 'Any'

    def _get_name(self, node) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def _compare_apis(self, old_api: Dict, new_api: Dict):
        """Compare two API definitions."""
        # Compare functions
        self._compare_functions(old_api['functions'], new_api['functions'])

        # Compare classes
        self._compare_classes(old_api['classes'], new_api['classes'])

    def _compare_functions(self, old_funcs: Dict, new_funcs: Dict):
        """Compare function signatures."""
        # Check for removed functions
        for name in old_funcs:
            if name not in new_funcs:
                self.breaking_changes.append({
                    'type': 'function_removed',
                    'name': name,
                    'severity': 'breaking',
                    'message': f"Function '{name}' was removed"
                })

        # Check for modified functions
        for name in old_funcs:
            if name in new_funcs:
                self._compare_function_signatures(name, old_funcs[name], new_funcs[name])

        # Check for new functions
        for name in new_funcs:
            if name not in old_funcs:
                self.differences.append({
                    'type': 'function_added',
                    'name': name,
                    'severity': 'info',
                    'message': f"New function '{name}' was added"
                })

    def _compare_function_signatures(self, name: str, old_func: Dict, new_func: Dict):
        """Compare function signatures in detail."""
        old_params = {p['name']: p for p in old_func['parameters']}
        new_params = {p['name']: p for p in new_func['parameters']}

        # Check for removed parameters
        for param_name in old_params:
            if param_name not in new_params:
                self.breaking_changes.append({
                    'type': 'parameter_removed',
                    'function': name,
                    'parameter': param_name,
                    'severity': 'breaking',
                    'message': f"Parameter '{param_name}' removed from '{name}'"
                })

        # Check for parameter type changes
        for param_name in old_params:
            if param_name in new_params:
                old_type = old_params[param_name]['annotation']
                new_type = new_params[param_name]['annotation']

                if old_type != new_type:
                    self.warnings.append({
                        'type': 'parameter_type_changed',
                        'function': name,
                        'parameter': param_name,
                        'old_type': old_type,
                        'new_type': new_type,
                        'severity': 'warning',
                        'message': f"Parameter '{param_name}' type changed in '{name}': {old_type} -> {new_type}"
                    })

        # Check return type changes
        if old_func['return_type'] != new_func['return_type']:
            self.warnings.append({
                'type': 'return_type_changed',
                'function': name,
                'old_type': old_func['return_type'],
                'new_type': new_func['return_type'],
                'severity': 'warning',
                'message': f"Return type changed in '{name}': {old_func['return_type']} -> {new_func['return_type']}"
            })

    def _compare_classes(self, old_classes: Dict, new_classes: Dict):
        """Compare class definitions."""
        # Check for removed classes
        for name in old_classes:
            if name not in new_classes:
                self.breaking_changes.append({
                    'type': 'class_removed',
                    'name': name,
                    'severity': 'breaking',
                    'message': f"Class '{name}' was removed"
                })

        # Check for modified classes
        for name in old_classes:
            if name in new_classes:
                self._compare_class_methods(name, old_classes[name], new_classes[name])

    def _compare_class_methods(self, class_name: str, old_class: Dict, new_class: Dict):
        """Compare methods in a class."""
        old_methods = old_class['methods']
        new_methods = new_class['methods']

        # Check for removed methods
        for method_name in old_methods:
            if method_name not in new_methods:
                self.breaking_changes.append({
                    'type': 'method_removed',
                    'class': class_name,
                    'method': method_name,
                    'severity': 'breaking',
                    'message': f"Method '{class_name}.{method_name}' was removed"
                })

    def _generate_report(self, old_api: Dict, new_api: Dict) -> Dict[str, Any]:
        """Generate validation report."""
        report = {
            'summary': {
                'breaking_changes': len(self.breaking_changes),
                'warnings': len(self.warnings),
                'info': len(self.differences),
                'total_issues': len(self.breaking_changes) + len(self.warnings) + len(self.differences)
            },
            'breaking_changes': self.breaking_changes,
            'warnings': self.warnings,
            'differences': self.differences,
            'old_api_summary': {
                'classes': len(old_api['classes']),
                'functions': len(old_api['functions'])
            },
            'new_api_summary': {
                'classes': len(new_api['classes']),
                'functions': len(new_api['functions'])
            }
        }

        return report


def main():
    parser = argparse.ArgumentParser(description='Python API Consistency Validator')
    parser.add_argument('old_version', help='Path to old version')
    parser.add_argument('new_version', help='Path to new version')
    parser.add_argument('--output', '-o', default='api_validation_report.json',
                       help='Output report file')

    args = parser.parse_args()

    validator = APIValidator(Path(args.old_version), Path(args.new_version))
    report = validator.validate()

    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)

    # Print summary
    print(f"\n=== Validation Summary ===")
    print(f"Breaking changes: {report['summary']['breaking_changes']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Info: {report['summary']['info']}")
    print(f"\nReport saved to: {args.output}")

    # Exit with error if breaking changes found
    sys.exit(1 if report['summary']['breaking_changes'] > 0 else 0)


if __name__ == '__main__':
    main()
