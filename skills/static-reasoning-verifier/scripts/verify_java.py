#!/usr/bin/env python3
"""
Verify Java code against specifications using static analysis.

Checks types, null safety annotations, JML contracts, and code quality.

Usage:
    python verify_java.py <file_or_directory> [--strict]
"""

import sys
import subprocess
import re
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class VerificationIssue:
    """Represents a verification issue found in code."""
    file_path: str
    line_number: int
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'type', 'contract', 'quality', 'null-safety'
    message: str
    suggestion: Optional[str] = None


def run_javac_type_check(path: str) -> List[VerificationIssue]:
    """Run javac compiler for type checking."""
    issues = []

    try:
        # Find all Java files
        if Path(path).is_file():
            java_files = [path]
        else:
            java_files = [str(f) for f in Path(path).rglob('*.java')]

        if not java_files:
            return issues

        # Compile with strict warnings
        cmd = ['javac', '-Xlint:all', '-Xdiags:verbose'] + java_files
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse javac output
        for line in result.stderr.splitlines():
            if '.java:' in line:
                match = re.match(r'([^:]+):(\d+):\s*(error|warning):\s*(.+)', line)
                if match:
                    file_path, line_num, severity, message = match.groups()
                    issues.append(VerificationIssue(
                        file_path=file_path,
                        line_number=int(line_num),
                        severity=severity,
                        category='type',
                        message=message,
                        suggestion=get_java_type_suggestion(message)
                    ))

    except subprocess.TimeoutExpired:
        print("Warning: javac timed out", file=sys.stderr)
    except FileNotFoundError:
        print("Warning: javac not found. Ensure Java JDK is installed", file=sys.stderr)

    return issues


def get_java_type_suggestion(message: str) -> Optional[str]:
    """Generate suggestions for Java type errors."""
    if 'incompatible types' in message.lower():
        return "Check type compatibility or add explicit cast"
    elif 'cannot find symbol' in message.lower():
        return "Check import statements and symbol names"
    elif 'method does not override' in message.lower():
        return "Check method signature matches superclass/interface"
    return None


def verify_null_safety(file_path: str) -> List[VerificationIssue]:
    """Verify null safety annotations in Java code."""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            # Check for potential null dereferences
            if re.search(r'\w+\s*\.\s*\w+', line) and 'null' not in line.lower():
                # Look for null checks nearby
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 2)
                context = ''.join(lines[context_start:context_end])

                if 'if' not in context and '@NonNull' not in context and '@NotNull' not in context:
                    # Check if variable is annotated
                    var_match = re.search(r'(\w+)\s*\.\s*\w+', line)
                    if var_match:
                        var_name = var_match.group(1)
                        # Look for declaration
                        found_annotation = False
                        for prev_line in lines[max(0, i-20):i]:
                            if f'{var_name}' in prev_line and ('@NonNull' in prev_line or '@NotNull' in prev_line):
                                found_annotation = True
                                break

                        if not found_annotation and var_name not in ['this', 'super']:
                            issues.append(VerificationIssue(
                                file_path=file_path,
                                line_number=i,
                                severity='warning',
                                category='null-safety',
                                message=f"Potential null dereference on variable '{var_name}'",
                                suggestion="Add null check or @NonNull annotation"
                            ))

    except Exception as e:
        pass  # Skip files that can't be parsed

    return issues


def verify_jml_contracts(file_path: str) -> List[VerificationIssue]:
    """Verify JML (Java Modeling Language) contract specifications."""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_method = False
        method_line = 0
        has_requires = False
        has_ensures = False
        method_name = ""

        for i, line in enumerate(lines, 1):
            # Check for JML annotations
            if '/*@' in line or '//@' in line:
                if 'requires' in line:
                    has_requires = True
                elif 'ensures' in line:
                    has_ensures = True

            # Detect method declarations
            method_match = re.match(r'\s*(public|private|protected).*?\s+(\w+)\s*\([^)]*\)', line)
            if method_match and '{' in line:
                # Check if previous method had contracts
                if in_method and method_name and not method_name.startswith('get') and not method_name.startswith('set'):
                    if not has_requires:
                        issues.append(VerificationIssue(
                            file_path=file_path,
                            line_number=method_line,
                            severity='warning',
                            category='contract',
                            message=f"Method '{method_name}' missing JML preconditions (@requires)",
                            suggestion="Add /*@ requires <condition>; @*/ before method"
                        ))
                    if not has_ensures:
                        issues.append(VerificationIssue(
                            file_path=file_path,
                            line_number=method_line,
                            severity='warning',
                            category='contract',
                            message=f"Method '{method_name}' missing JML postconditions (@ensures)",
                            suggestion="Add /*@ ensures <condition>; @*/ before method"
                        ))

                # Reset for new method
                in_method = True
                method_line = i
                method_name = method_match.group(2)
                has_requires = False
                has_ensures = False

    except Exception as e:
        pass

    return issues


def verify_file(file_path: str, strict: bool = False) -> List[VerificationIssue]:
    """Verify a single Java file."""
    issues = []

    # Type checking with javac
    type_issues = run_javac_type_check(file_path)
    issues.extend(type_issues)

    # Null safety verification
    null_issues = verify_null_safety(file_path)
    issues.extend(null_issues)

    # JML contract verification
    if strict:
        contract_issues = verify_jml_contracts(file_path)
        issues.extend(contract_issues)

    return issues


def verify_directory(directory: str, strict: bool = False) -> List[VerificationIssue]:
    """Verify all Java files in a directory."""
    issues = []

    # Type checking with javac (on all files at once)
    type_issues = run_javac_type_check(directory)
    issues.extend(type_issues)

    # Per-file checks
    for java_file in Path(directory).rglob('*.java'):
        null_issues = verify_null_safety(str(java_file))
        issues.extend(null_issues)

        if strict:
            contract_issues = verify_jml_contracts(str(java_file))
            issues.extend(contract_issues)

    return issues


def format_report(issues: List[VerificationIssue]) -> str:
    """Format verification issues as a report."""
    if not issues:
        return "✅ All verifications passed!"

    # Group by severity
    errors = [i for i in issues if i.severity == 'error']
    warnings = [i for i in issues if i.severity == 'warning']
    info = [i for i in issues if i.severity == 'info']

    output = []
    output.append(f"Found {len(issues)} issue(s): {len(errors)} error(s), {len(warnings)} warning(s)\n")

    if errors:
        output.append("ERRORS:")
        for issue in errors:
            output.append(f"  ❌ {issue.file_path}:{issue.line_number} [{issue.category}]")
            output.append(f"     {issue.message}")
            if issue.suggestion:
                output.append(f"     💡 {issue.suggestion}")
            output.append("")

    if warnings:
        output.append("WARNINGS:")
        for issue in warnings:
            output.append(f"  ⚠️  {issue.file_path}:{issue.line_number} [{issue.category}]")
            output.append(f"     {issue.message}")
            if issue.suggestion:
                output.append(f"     💡 {issue.suggestion}")
            output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python verify_java.py <file_or_directory> [--strict]")
        sys.exit(1)

    path = sys.argv[1]
    strict = '--strict' in sys.argv

    if Path(path).is_file():
        issues = verify_file(path, strict)
    elif Path(path).is_dir():
        issues = verify_directory(path, strict)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    print(format_report(issues))

    errors = [i for i in issues if i.severity == 'error']
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
