#!/usr/bin/env python3
"""
contract_extractor.py - Extract contracts from program code

Extracts:
- Preconditions from docstrings and assertions
- Postconditions from docstrings and assertions
- Class invariants from docstrings
"""

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import re


class ContractExtractor(ast.NodeVisitor):
    """Extract contracts from Python code."""

    def __init__(self):
        self.contracts = {
            'classes': {},
            'functions':
        }
        self.current_class = None

    def visit_ClassDef(self, node):
        """Extract class contracts."""
        class_name = node.name
        self.current_class = class_name

        # Extract class invariants from docstring
        docstring = ast.get_docstring(node)
        invariants = self._extract_invariants(docstring) if docstring else []

        self.contracts['classes'][class_name] = {
            'invariants': invariants,
            'methods': {}
        }

        # Visit methods
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        """Extract function/method contracts."""
        func_name = node.name
        docstring = ast.get_docstring(node)

        # Extract preconditions and postconditions
        preconditions = self._extract_preconditions(docstring, node) if docstring else []
        postconditions = self._extract_postconditions(docstring, node) if docstring else []

        contract = {
            'preconditions': preconditions,
            'postconditions': postconditions
        }

        if self.current_class:
            self.contracts['classes'][self.current_class]['methods'][func_name] = contract
        else:
            self.contracts['functions'][func_name] = contract

    def _extract_invariants(self, docstring: str) -> List[str]:
        """Extract invariants from docstring."""
        invariants = []

        # Look for "Invariant:" section
        pattern = r'Invariant:\s*(.+?)(?:\n\n|\Z)'
        matches = re.findall(pattern, docstring, re.DOTALL | re.IGNORECASE)

        for match in matches:
            # Split by newlines and clean
            lines = [line.strip('- ').strip() for line in match.split('\n') if line.strip()]
            invariants.extend(lines)

        return invariants

    def _extract_preconditions(self, docstring: str, node: ast.FunctionDef) -> List[str]:
        """Extract preconditions from docstring and assertions."""
        preconditions = []

        # Extract from docstring
        pattern = r'Precondition:\s*(.+?)(?:\n\n|\Z)'
        matches = re.findall(pattern, docstring, re.DOTALL | re.IGNORECASE)

        for match in matches:
            lines = [line.strip('- ').strip() for line in match.split('\n') if line.strip()]
            preconditions.extend(lines)

        # Extract from assertions at start of function
        for stmt in node.body[:5]:  # Check first 5 statements
            if isinstance(stmt, ast.Assert):
                condition = ast.unparse(stmt.test)
                preconditions.append(condition)

        return preconditions

    def _extract_postconditions(self, docstring: str, node: ast.FunctionDef) -> List[str]:
        """Extract postconditions from docstring."""
        postconditions = []

        # Extract from docstring
        pattern = r'Postcondition:\s*(.+?)(?:\n\n|\Z)'
        matches = re.findall(pattern, docstring, re.DOTALL | re.IGNORECASE)

        for match in matches:
            lines = [line.strip('- ').strip() for line in match.split('\n') if line.strip()]
            postconditions.extend(lines)

        return postconditions


def extract_contracts(program_path: str) -> Dict:
    """Extract contracts from program."""
    path = Path(program_path)

    if not path.exists():
        raise FileNotFoundError(f"Program not found: {program_path}")

    # Read source code
    with open(path, 'r') as f:
        source = f.read()

    # Parse AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Error parsing {program_path}: {e}")
        return {'classes': {}, 'functions': {}}

    # Extract contracts
    extractor = ContractExtractor()
    extractor.visit(tree)

    return {
        'program': str(path),
        'contracts': extractor.contracts
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract contracts from program code'
    )
    parser.add_argument('--program', required=True,
                       help='Path to program file')
    parser.add_argument('--output', required=True,
                       help='Output JSON file for contracts')

    args = parser.parse_args()

    try:
        contracts = extract_contracts(args.program)

        # Save to file
        with open(args.output, 'w') as f:
            json.dump(contracts, f, indent=2)

        print(f"Contracts extracted from: {args.program}")
        print(f"Classes: {len(contracts['contracts']['classes'])}")
        print(f"Functions: {len(contracts['contracts']['functions'])}")
        print(f"Saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
