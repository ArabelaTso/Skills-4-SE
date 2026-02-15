#!/usr/bin/env python3
"""
Verify Python code against type annotations and contracts.

Uses mypy for type checking and validates design-by-contract annotations.

Usage:
    python verify_python.py <file_or_directory> [--strict]
"""

import sys
import subprocess
import ast
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class VerificationIssue:
    """Represents a verification issue found in code."""
    file_path: str
    line_number: int
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'type', 'contract', 'quality'
    message: str
    suggestion: Optional[str] = None


def run_mypy(path: str, strict: bool = False) -> List[VerificationIssue]:
    """Run mypy type checker on Python code."""
    issues = []

    cmd = ['mypy', path]
    if strict:
        cmd.extend(['--strict', '--disallow-untyped-defs'])
    else:
        cmd.extend(['--check-untyped-defs'])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse mypy output
        for line in result.stdout.splitlines():
            if ':' in line:
                match = re.match(r'([^:]+):(\d+):.*?:\s*(error|warning|note):\s*(.+)', line)
                if match:
                    file_path, line_num, severity, message = match.groups()
                    issues.append(VerificationIssue(
                        file_path=file_path,
                        line_number=int(line_num),
                        severity=severity,
                        category='type',
                        message=message,
                        suggestion=get_type_suggestion(message)
                    ))

    except subprocess.TimeoutExpired:
        print("Warning: mypy timed out", file=sys.stderr)
    except FileNotFoundError:
        print("Warning: mypy not found. Install with: pip install mypy", file=sys.stderr)

    return issues


def get_type_suggestion(message: str) -> Optional[str]:
    """Generate suggestions for type errors."""
    if 'incompatible type' in message.lower():
        return "Add explicit type annotation or cast"
    elif 'has no attribute' in message.lower():
        return "Check attribute name or add type annotation"
    elif 'missing return' in message.lower():
        return "Add return statement or specify return type as None"
    elif 'argument' in message.lower() and 'has incompatible type' in message.lower():
        return "Check argument type matches function signature"
    return None


class ContractVerifier(ast.NodeVisitor):
    """Verify design-by-contract annotations in Python code."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.issues: List[VerificationIssue] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Check function contracts (preconditions, postconditions)."""
        # Check for contract decorators
        has_requires = False
        has_ensures = False

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == 'requires':
                    has_requires = True
                elif decorator.id == 'ensures':
                    has_ensures = True

        # Check docstring for contract specifications
        docstring = ast.get_docstring(node)
        if docstring:
            self._check_docstring_contracts(node, docstring)

        # Check for assertions as contracts
        self._check_function_assertions(node)

        self.generic_visit(node)

    def _check_docstring_contracts(self, node: ast.FunctionDef, docstring: str):
        """Check for contract specifications in docstrings."""
        # Look for Requires/Ensures sections
        has_requires = 'Requires:' in docstring or 'Precondition:' in docstring
        has_ensures = 'Ensures:' in docstring or 'Postcondition:' in docstring

        # If function has parameters, should have preconditions
        if node.args.args and not has_requires:
            self.issues.append(VerificationIssue(
                file_path=self.file_path,
                line_number=node.lineno,
                severity='warning',
                category='contract',
                message=f"Function '{node.name}' has parameters but no preconditions specified",
                suggestion="Add 'Requires:' section in docstring or @requires decorator"
            ))

        # If function returns non-None, should have postconditions
        if node.returns and not has_ensures:
            self.issues.append(VerificationIssue(
                file_path=self.file_path,
                line_number=node.lineno,
                severity='warning',
                category='contract',
                message=f"Function '{node.name}' returns value but no postconditions specified",
                suggestion="Add 'Ensures:' section in docstring or @ensures decorator"
            ))

    def _check_function_assertions(self, node: ast.FunctionDef):
        """Check for assertion-based contracts."""
        body = node.body

        # Skip docstring
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
            body = body[1:]

        # Check for precondition assertions at start
        precondition_count = 0
        for stmt in body:
            if isinstance(stmt, ast.Assert):
                precondition_count += 1
            else:
                break

        # Check for postcondition assertions at end
        postcondition_count = 0
        for stmt in reversed(body):
            if isinstance(stmt, ast.Assert):
                postcondition_count += 1
            elif isinstance(stmt, ast.Return):
                # Assertion before return is postcondition
                continue
            else:
                break


def verify_contracts(file_path: str) -> List[VerificationIssue]:
    """Verify design-by-contract specifications in Python code."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code, filename=file_path)
        verifier = ContractVerifier(file_path, source_code)
        verifier.visit(tree)

        return verifier.issues

    except SyntaxError as e:
        return [VerificationIssue(
            file_path=file_path,
            line_number=e.lineno or 0,
            severity='error',
            category='quality',
            message=f"Syntax error: {e.msg}"
        )]
    except Exception as e:
        return [VerificationIssue(
            file_path=file_path,
            line_number=0,
            severity='error',
            category='quality',
            message=f"Failed to parse file: {str(e)}"
        )]


def verify_file(file_path: str, strict: bool = False) -> List[VerificationIssue]:
    """Verify a single Python file."""
    issues = []

    # Type checking with mypy
    type_issues = run_mypy(file_path, strict)
    issues.extend(type_issues)

    # Contract verification
    contract_issues = verify_contracts(file_path)
    issues.extend(contract_issues)

    return issues


def verify_directory(directory: str, strict: bool = False) -> List[VerificationIssue]:
    """Verify all Python files in a directory."""
    issues = []

    # Run mypy on entire directory (more efficient)
    type_issues = run_mypy(directory, strict)
    issues.extend(type_issues)

    # Contract verification per file
    for py_file in Path(directory).rglob('*.py'):
        contract_issues = verify_contracts(str(py_file))
        issues.extend(contract_issues)

    return issues


def format_report(issues: List[VerificationIssue]) -> str:
    """Format verification issues as a report."""
    if not issues:
        return "✅ All verifications passed!"

    # Group by severity
    errors = [i for i in issues if i.severity == 'error']
    warnings = [i for i in issues if i.severity == 'warning']
    info = [i for i in issues if i.severity in ('info', 'note')]

    output = []
    output.append(f"Found {len(issues)} issue(s): {len(errors)} error(s), {len(warnings)} warning(s), {len(info)} info\n")

    # Report errors first
    if errors:
        output.append("ERRORS:")
        for issue in errors:
            output.append(f"  ❌ {issue.file_path}:{issue.line_number} [{issue.category}]")
            output.append(f"     {issue.message}")
            if issue.suggestion:
                output.append(f"     💡 {issue.suggestion}")
            output.append("")

    # Then warnings
    if warnings:
        output.append("WARNINGS:")
        for issue in warnings:
            output.append(f"  ⚠️  {issue.file_path}:{issue.line_number} [{issue.category}]")
            output.append(f"     {issue.message}")
            if issue.suggestion:
                output.append(f"     💡 {issue.suggestion}")
            output.append("")

    # Then info
    if info:
        output.append("INFO:")
        for issue in info:
            output.append(f"  ℹ️  {issue.file_path}:{issue.line_number} [{issue.category}]")
            output.append(f"     {issue.message}")
            output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python verify_python.py <file_or_directory> [--strict]")
        sys.exit(1)

    path = sys.argv[1]
    strict = '--strict' in sys.argv

    # Verify file or directory
    if Path(path).is_file():
        issues = verify_file(path, strict)
    elif Path(path).is_dir():
        issues = verify_directory(path, strict)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    # Output report
    print(format_report(issues))

    # Exit with error code if errors found
    errors = [i for i in issues if i.severity == 'error']
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
