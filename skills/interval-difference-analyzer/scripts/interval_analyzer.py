#!/usr/bin/env python3
"""
interval_analyzer.py - Extract interval information from programs

Supports multiple analysis methods:
- Static analysis: Infer intervals from code structure
- Dynamic analysis: Observe intervals from test execution
- Hybrid: Combine both approaches

Outputs interval database in JSON format.
"""

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict


class IntervalAnalyzer:
    """Analyze program to extract variable intervals."""

    def __init__(self, program_path: str):
        self.program_path = Path(program_path)
        self.intervals = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf')})
        self.functions = {}

    def analyze_static(self) -> Dict:
        """Perform static interval analysis."""
        print(f"Analyzing {self.program_path} statically...")

        # Read and parse program
        with open(self.program_path, 'r') as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"Error parsing {self.program_path}: {e}")
            return {}

        # Analyze AST
        self._analyze_ast(tree)

        return self._format_intervals()

    def _analyze_ast(self, tree: ast.AST):
        """Analyze AST to extract intervals."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._analyze_function(node)
            elif isinstance(node, ast.Assign):
                self._analyze_assignment(node)

    def _analyze_function(self, node: ast.FunctionDef):
        """Analyze function to extract parameter and return intervals."""
        func_name = node.name
        self.functions[func_name] = {
            'parameters': [],
            'returns': []
        }

        # Analyze parameters
        for arg in node.args.args:
            param_name = arg.arg
            self.functions[func_name]['parameters'].append(param_name)

            # Try to infer interval from type hints or docstring
            interval = self._infer_parameter_interval(node, param_name)
            if interval:
                var_key = f"{func_name}.{param_name}"
                self.intervals[var_key] = interval

        # Analyze return statements
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value:
                self._analyze_expression(child.value, func_name)

    def _infer_parameter_interval(self, func_node: ast.FunctionDef, param_name: str) -> Optional[Dict]:
        """Infer parameter interval from docstring or annotations."""
        # Check docstring for interval hints
        docstring = ast.get_docstring(func_node)
        if docstring:
            # Look for patterns like "param_name: [min, max]"
            import re
            pattern = rf"{param_name}:\s*\[(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\]"
            match = re.search(pattern, docstring)
            if match:
                return {
                    'min': float(match.group(1)),
                    'max': float(match.group(2))
                }

        return None

    def _analyze_assignment(self, node: ast.Assign):
        """Analyze assignment to extract intervals."""
        if isinstance(node.value, ast.Constant):
            # Direct constant assignment
            value = node.value.value
            if isinstance(value, (int, float)):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        self._update_interval(var_name, value, value)

        elif isinstance(node.value, ast.BinOp):
            # Binary operation
            self._analyze_binop(node.value)

    def _analyze_expression(self, node: ast.AST, context: str = ""):
        """Analyze expression to extract intervals."""
        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, (int, float)):
                return {'min': value, 'max': value}

        elif isinstance(node, ast.BinOp):
            return self._analyze_binop(node)

        elif isinstance(node, ast.Name):
            var_key = f"{context}.{node.id}" if context else node.id
            return self.intervals.get(var_key)

        return None

    def _analyze_binop(self, node: ast.BinOp) -> Optional[Dict]:
        """Analyze binary operation to compute result interval."""
        left_interval = self._analyze_expression(node.left)
        right_interval = self._analyze_expression(node.right)

        if not left_interval or not right_interval:
            return None

        # Compute result interval based on operation
        if isinstance(node.op, ast.Add):
            return {
                'min': left_interval['min'] + right_interval['min'],
                'max': left_interval['max'] + right_interval['max']
            }
        elif isinstance(node.op, ast.Sub):
            return {
                'min': left_interval['min'] - right_interval['max'],
                'max': left_interval['max'] - right_interval['min']
            }
        elif isinstance(node.op, ast.Mult):
            products = [
                left_interval['min'] * right_interval['min'],
                left_interval['min'] * right_interval['max'],
                left_interval['max'] * right_interval['min'],
                left_interval['max'] * right_interval['max']
            ]
            return {
                'min': min(products),
                'max': max(products)
            }
        elif isinstance(node.op, ast.Div):
            # Avoid division by zero
            if right_interval['min'] <= 0 <= right_interval['max']:
                return None  # Potential division by zero

            quotients = [
                left_interval['min'] / right_interval['min'],
                left_interval['min'] / right_interval['max'],
                left_interval['max'] / right_interval['min'],
                left_interval['max'] / right_interval['max']
            ]
            return {
                'min': min(quotients),
                'max': max(quotients)
            }

        return None

    def _update_interval(self, var_name: str, min_val: float, max_val: float):
        """Update interval for a variable."""
        self.intervals[var_name]['min'] = min(self.intervals[var_name]['min'], min_val)
        self.intervals[var_name]['max'] = max(self.intervals[var_name]['max'], max_val)

    def _format_intervals(self) -> Dict:
        """Format intervals for output."""
        result = {
            'program': str(self.program_path),
            'intervals': {}
        }

        for var_name, interval in self.intervals.items():
            if interval['min'] != float('inf') and interval['max'] != float('-inf'):
                result['intervals'][var_name] = {
                    'min': interval['min'],
                    'max': interval['max'],
                    'range': f"[{interval['min']}, {interval['max']}]"
                }

        return result

    def save_intervals(self, output_path: str):
        """Save intervals to JSON file."""
        intervals = self.analyze_static()

        with open(output_path, 'w') as f:
            json.dump(intervals, f, indent=2)

        print(f"Intervals saved to: {output_path}")
        print(f"Total intervals extracted: {len(intervals['intervals'])}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract interval information from programs'
    )
    parser.add_argument('--program', required=True,
                       help='Path to program file')
    parser.add_argument('--output', required=True,
                       help='Output JSON file for intervals')
    parser.add_argument('--method', choices=['static', 'dynamic', 'hybrid'],
                       default='static',
                       help='Analysis method (default: static)')

    args = parser.parse_args()

    try:
        analyzer = IntervalAnalyzer(args.program)

        if args.method == 'static':
            analyzer.save_intervals(args.output)
        elif args.method == 'dynamic':
            print("Dynamic analysis not yet implemented")
            sys.exit(1)
        elif args.method == 'hybrid':
            print("Hybrid analysis not yet implemented")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
