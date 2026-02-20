#!/usr/bin/env python3
"""
Detect design smells in source code.

Analyzes code for coupling, cohesion, and other design quality issues.

Usage:
    python detect_smells.py <file_or_directory> [--format text|json]
"""

import ast
import sys
import json
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class DesignSmell:
    """Represents a detected design smell."""
    file_path: str
    line_number: int
    smell_type: str
    severity: str  # 'critical', 'major', 'minor'
    description: str
    suggestion: str


class PythonDesignAnalyzer(ast.NodeVisitor):
    """Analyze Python code for design smells."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.smells: List[DesignSmell] = []
        self.imports: Set[str] = set()
        self.classes: Dict[str, ast.ClassDef] = {}
        self.functions: Dict[str, ast.FunctionDef] = {}

    def visit_Import(self, node: ast.Import):
        """Track imports for coupling analysis."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports for coupling analysis."""
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Analyze class design."""
        self.classes[node.name] = node

        # Check God Class (too many methods/attributes)
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        attributes = self._count_attributes(node)

        if len(methods) > 20:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="God Class",
                severity="critical",
                description=f"Class '{node.name}' has {len(methods)} methods (threshold: 20)",
                suggestion="Split into multiple smaller, focused classes"
            ))

        if attributes > 15:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="God Class",
                severity="major",
                description=f"Class '{node.name}' has {attributes} attributes (threshold: 15)",
                suggestion="Consider splitting class or using composition"
            ))

        # Check for low cohesion
        cohesion_score = self._calculate_cohesion(node)
        if cohesion_score < 0.3 and len(methods) > 5:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="Low Cohesion",
                severity="major",
                description=f"Class '{node.name}' has low cohesion (score: {cohesion_score:.2f})",
                suggestion="Group related methods/attributes or split class"
            ))

        # Check Feature Envy (methods accessing other objects more than self)
        for method in methods:
            if isinstance(method, ast.FunctionDef):
                self._check_feature_envy(node.name, method)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Analyze function design."""
        self.functions[node.name] = node

        # Check Long Method
        num_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
        if num_lines > 50:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="Long Method",
                severity="major",
                description=f"Method '{node.name}' has {num_lines} lines (threshold: 50)",
                suggestion="Extract smaller methods or refactor"
            ))

        # Check Long Parameter List
        params = len(node.args.args)
        if params > 5:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="Long Parameter List",
                severity="minor",
                description=f"Method '{node.name}' has {params} parameters (threshold: 5)",
                suggestion="Use parameter object or builder pattern"
            ))

        # Check Cyclomatic Complexity
        complexity = self._calculate_complexity(node)
        if complexity > 10:
            self.smells.append(DesignSmell(
                file_path=self.file_path,
                line_number=node.lineno,
                smell_type="High Complexity",
                severity="major",
                description=f"Method '{node.name}' has complexity {complexity} (threshold: 10)",
                suggestion="Simplify logic or extract methods"
            ))

        self.generic_visit(node)

    def _count_attributes(self, class_node: ast.ClassDef) -> int:
        """Count instance attributes in a class."""
        attributes = set()
        for node in ast.walk(class_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'self':
                            attributes.add(target.attr)
        return len(attributes)

    def _calculate_cohesion(self, class_node: ast.ClassDef) -> float:
        """Calculate LCOM (Lack of Cohesion of Methods) for a class."""
        methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
        if len(methods) < 2:
            return 1.0

        # Track which attributes each method uses
        method_attrs = []
        all_attrs = set()

        for method in methods:
            attrs = set()
            for node in ast.walk(method):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                    if node.value.id == 'self':
                        attrs.add(node.attr)
                        all_attrs.add(node.attr)
            method_attrs.append(attrs)

        if not all_attrs:
            return 1.0

        # Calculate cohesion: how many methods share attributes
        shared_pairs = 0
        total_pairs = 0

        for i, attrs1 in enumerate(method_attrs):
            for attrs2 in method_attrs[i+1:]:
                total_pairs += 1
                if attrs1 & attrs2:  # Intersection
                    shared_pairs += 1

        return shared_pairs / total_pairs if total_pairs > 0 else 1.0

    def _check_feature_envy(self, class_name: str, method: ast.FunctionDef):
        """Check if method accesses other objects more than self."""
        self_access = 0
        other_access = defaultdict(int)

        for node in ast.walk(method):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    if node.value.id == 'self':
                        self_access += 1
                    else:
                        other_access[node.value.id] += 1

        # If method accesses another object significantly more than self
        for obj, count in other_access.items():
            if count > self_access * 2 and count > 3:
                self.smells.append(DesignSmell(
                    file_path=self.file_path,
                    line_number=method.lineno,
                    smell_type="Feature Envy",
                    severity="minor",
                    description=f"Method '{method.name}' accesses '{obj}' more than 'self'",
                    suggestion=f"Consider moving method to '{obj}' class"
                ))

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity


def analyze_file(file_path: str) -> List[DesignSmell]:
    """Analyze a single Python file for design smells."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code, filename=file_path)
        analyzer = PythonDesignAnalyzer(file_path, source_code)
        analyzer.visit(tree)

        # Check module-level coupling
        if len(analyzer.imports) > 20:
            analyzer.smells.append(DesignSmell(
                file_path=file_path,
                line_number=1,
                smell_type="High Coupling",
                severity="major",
                description=f"Module has {len(analyzer.imports)} imports (threshold: 20)",
                suggestion="Reduce dependencies or split module"
            ))

        return analyzer.smells

    except SyntaxError:
        return []
    except Exception as e:
        print(f"Warning: Could not analyze {file_path}: {e}", file=sys.stderr)
        return []


def analyze_directory(directory: str) -> List[DesignSmell]:
    """Analyze all Python files in a directory."""
    all_smells = []

    for py_file in Path(directory).rglob('*.py'):
        smells = analyze_file(str(py_file))
        all_smells.extend(smells)

    return all_smells


def format_report(smells: List[DesignSmell], format_type: str = 'text') -> str:
    """Format design smells as a report."""
    if format_type == 'json':
        return json.dumps([asdict(s) for s in smells], indent=2)

    if not smells:
        return "✅ No design smells detected!"

    # Group by severity
    critical = [s for s in smells if s.severity == 'critical']
    major = [s for s in smells if s.severity == 'major']
    minor = [s for s in smells if s.severity == 'minor']

    output = []
    output.append(f"Found {len(smells)} design smell(s): {len(critical)} critical, {len(major)} major, {len(minor)} minor\n")

    if critical:
        output.append("CRITICAL ISSUES:")
        for smell in critical:
            output.append(f"  🔴 {smell.file_path}:{smell.line_number} - {smell.smell_type}")
            output.append(f"     {smell.description}")
            output.append(f"     💡 {smell.suggestion}")
            output.append("")

    if major:
        output.append("MAJOR ISSUES:")
        for smell in major:
            output.append(f"  🟠 {smell.file_path}:{smell.line_number} - {smell.smell_type}")
            output.append(f"     {smell.description}")
            output.append(f"     💡 {smell.suggestion}")
            output.append("")

    if minor:
        output.append("MINOR ISSUES:")
        for smell in minor:
            output.append(f"  🟡 {smell.file_path}:{smell.line_number} - {smell.smell_type}")
            output.append(f"     {smell.description}")
            output.append(f"     💡 {smell.suggestion}")
            output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python detect_smells.py <file_or_directory> [--format text|json]")
        sys.exit(1)

    path = sys.argv[1]
    format_type = 'text'

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--format' and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1]

    # Analyze file or directory
    if Path(path).is_file():
        smells = analyze_file(path)
    elif Path(path).is_dir():
        smells = analyze_directory(path)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    # Output report
    print(format_report(smells, format_type))

    # Exit with warning if critical issues found
    critical = [s for s in smells if s.severity == 'critical']
    sys.exit(1 if critical else 0)


if __name__ == '__main__':
    main()
