#!/usr/bin/env python3
"""
Analyze code to generate customized mutation operators.
"""

import ast
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class MutationOperatorGenerator:
    """Generate customized mutation operators for a codebase."""

    def __init__(self):
        self.operators = defaultdict(list)
        self.code_patterns = {
            'arithmetic_ops': set(),
            'comparison_ops': set(),
            'logical_ops': set(),
            'constants': set(),
            'function_calls': set(),
            'data_types': set(),
            'api_calls': set(),
        }

    def analyze_file(self, filepath: Path) -> None:
        """Analyze a Python file to identify mutation opportunities."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(filepath))

            self._analyze_tree(tree)
        except Exception as e:
            print(f"Warning: Could not analyze {filepath}: {e}", file=sys.stderr)

    def _analyze_tree(self, tree: ast.AST) -> None:
        """Analyze AST to identify patterns."""
        for node in ast.walk(tree):
            # Arithmetic operators
            if isinstance(node, ast.BinOp):
                op_type = type(node.op).__name__
                self.code_patterns['arithmetic_ops'].add(op_type)
                self._add_operator('AOR', f'Replace {op_type} with other arithmetic operators')

            # Comparison operators
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    op_type = type(op).__name__
                    self.code_patterns['comparison_ops'].add(op_type)
                self._add_operator('ROR', 'Replace relational operators')

            # Logical operators
            elif isinstance(node, ast.BoolOp):
                op_type = type(node.op).__name__
                self.code_patterns['logical_ops'].add(op_type)
                self._add_operator('LCR', 'Replace logical connectors (and/or)')

            # Constants
            elif isinstance(node, ast.Constant):
                value = node.value
                if isinstance(value, (int, float)):
                    self.code_patterns['constants'].add(f'numeric:{value}')
                    self._add_operator('CRP', f'Replace constant {value}')
                elif isinstance(value, bool):
                    self.code_patterns['constants'].add(f'bool:{value}')
                    self._add_operator('CRP', f'Replace boolean {value}')
                elif isinstance(value, str):
                    self.code_patterns['constants'].add('string')
                    self._add_operator('STR', 'Replace string values')

            # Function calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    self.code_patterns['function_calls'].add(func_name)

                    # API calls (common patterns)
                    if any(api in func_name.lower() for api in ['request', 'get', 'post', 'fetch', 'query']):
                        self.code_patterns['api_calls'].add(func_name)
                        self._add_operator('API', f'Modify API call {func_name}')

                    # Database calls
                    if any(db in func_name.lower() for db in ['save', 'delete', 'update', 'insert', 'select']):
                        self._add_operator('DB', f'Modify database operation {func_name}')

                    self._add_operator('FCR', f'Modify function call {func_name}')

            # Return statements
            elif isinstance(node, ast.Return):
                self._add_operator('RVR', 'Replace return values')

            # Exception handling
            elif isinstance(node, ast.ExceptHandler):
                self._add_operator('EXS', 'Modify exception handling')

            # Assignments
            elif isinstance(node, ast.Assign):
                self._add_operator('ASG', 'Modify assignments')

            # If statements
            elif isinstance(node, ast.If):
                self._add_operator('COR', 'Negate conditionals')

            # Loops
            elif isinstance(node, (ast.For, ast.While)):
                self._add_operator('LOOP', 'Modify loop behavior')

    def _add_operator(self, op_code: str, description: str) -> None:
        """Add a mutation operator."""
        if description not in [op['description'] for op in self.operators[op_code]]:
            self.operators[op_code].append({
                'code': op_code,
                'description': description,
                'priority': self._calculate_priority(op_code)
            })

    def _calculate_priority(self, op_code: str) -> str:
        """Calculate operator priority based on effectiveness."""
        high_priority = ['ROR', 'LCR', 'CRP', 'SDL', 'COR']
        medium_priority = ['AOR', 'FCR', 'RVR', 'API', 'DB']

        if op_code in high_priority:
            return 'high'
        elif op_code in medium_priority:
            return 'medium'
        else:
            return 'low'

    def generate_report(self) -> Dict:
        """Generate mutation operator report."""
        report = {
            'summary': {
                'total_operators': sum(len(ops) for ops in self.operators.values()),
                'operator_types': len(self.operators),
                'code_patterns': {
                    k: len(v) for k, v in self.code_patterns.items()
                }
            },
            'operators': {},
            'recommendations': []
        }

        # Group operators by priority
        for op_code, ops in self.operators.items():
            for op in ops:
                priority = op['priority']
                if priority not in report['operators']:
                    report['operators'][priority] = []
                report['operators'][priority].append(op)

        # Generate recommendations
        report['recommendations'] = self._generate_recommendations()

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for mutation testing."""
        recommendations = []

        # Check for arithmetic operations
        if self.code_patterns['arithmetic_ops']:
            recommendations.append(
                "Focus on arithmetic operator mutations (AOR) - found multiple arithmetic operations"
            )

        # Check for comparisons
        if self.code_patterns['comparison_ops']:
            recommendations.append(
                "Prioritize relational operator mutations (ROR) - found comparison operations"
            )

        # Check for API calls
        if self.code_patterns['api_calls']:
            recommendations.append(
                "Test API call mutations - found external API interactions"
            )

        # Check for constants
        if len(self.code_patterns['constants']) > 10:
            recommendations.append(
                "Consider constant replacement mutations (CRP) - found many constants"
            )

        # Check for logical operations
        if self.code_patterns['logical_ops']:
            recommendations.append(
                "Apply logical connector mutations (LCR) - found boolean logic"
            )

        return recommendations


def print_report(report: Dict) -> None:
    """Print mutation operator report."""
    print("=" * 80)
    print("SMART MUTATION OPERATOR GENERATOR REPORT")
    print("=" * 80)
    print()

    # Summary
    summary = report['summary']
    print(f"Total Mutation Operators: {summary['total_operators']}")
    print(f"Operator Types: {summary['operator_types']}")
    print()

    print("Code Patterns Detected:")
    for pattern, count in summary['code_patterns'].items():
        if count > 0:
            print(f"  - {pattern}: {count}")
    print()

    # Operators by priority
    for priority in ['high', 'medium', 'low']:
        if priority in report['operators']:
            ops = report['operators'][priority]
            icon = {'high': '🔴', 'medium': '🟡', 'low': '🔵'}[priority]
            print(f"{icon} {priority.upper()} PRIORITY OPERATORS ({len(ops)})")
            print("-" * 80)

            # Group by operator code
            by_code = defaultdict(list)
            for op in ops:
                by_code[op['code']].append(op)

            for code, ops_list in sorted(by_code.items()):
                print(f"\n  {code}:")
                for op in ops_list[:3]:  # Show first 3
                    print(f"    • {op['description']}")
                if len(ops_list) > 3:
                    print(f"    ... and {len(ops_list) - 3} more")
            print()

    # Recommendations
    if report['recommendations']:
        print("💡 RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")
        print()

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Generate customized mutation operators for a codebase'
    )
    parser.add_argument(
        'path',
        type=Path,
        help='Path to repository or file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file for JSON report'
    )
    parser.add_argument(
        '--language',
        default='python',
        choices=['python'],
        help='Programming language (currently only Python supported)'
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        return 1

    # Collect files
    if args.path.is_file():
        files = [args.path]
    else:
        files = list(args.path.rglob('*.py'))

    if not files:
        print("Error: No Python files found", file=sys.stderr)
        return 1

    print(f"Analyzing {len(files)} files...")

    # Analyze files
    generator = MutationOperatorGenerator()
    for filepath in files:
        generator.analyze_file(filepath)

    # Generate report
    report = generator.generate_report()

    # Print report
    print_report(report)

    # Save JSON report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nDetailed report saved to: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
