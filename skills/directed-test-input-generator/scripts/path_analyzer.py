#!/usr/bin/env python3
"""
Code Path Analyzer - Extracts control flow paths and constraints from Python code.
"""

import ast
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass


@dataclass
class PathCondition:
    """Represents a condition that must be satisfied to reach a code path."""
    variable: str
    operator: str
    value: Any
    negated: bool = False

    def __str__(self):
        op = self.operator
        if self.negated:
            if op == "==":
                op = "!="
            elif op == "!=":
                op = "=="
            elif op == "<":
                op = ">="
            elif op == ">":
                op = "<="
            elif op == "<=":
                op = ">"
            elif op == ">=":
                op = "<"
        return f"{self.variable} {op} {self.value}"


@dataclass
class CodePath:
    """Represents a specific execution path through the code."""
    path_id: int
    conditions: List[PathCondition]
    target_line: int
    description: str

    def get_constraints(self) -> Dict[str, List[PathCondition]]:
        """Group constraints by variable."""
        constraints = {}
        for condition in self.conditions:
            if condition.variable not in constraints:
                constraints[condition.variable] = []
            constraints[condition.variable].append(condition)
        return constraints


class PathAnalyzer(ast.NodeVisitor):
    """Analyzes Python AST to extract code paths and their conditions."""

    def __init__(self):
        self.paths: List[CodePath] = []
        self.current_conditions: List[PathCondition] = []
        self.path_counter = 0

    def visit_If(self, node: ast.If):
        """Extract conditions from if statements."""
        # Extract condition
        conditions = self._extract_conditions(node.test, negated=False)

        # Visit if branch with positive condition
        self.current_conditions.extend(conditions)
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, (ast.Return, ast.Raise)):
                self._record_path(stmt.lineno, "if branch")
        self.current_conditions = self.current_conditions[:-len(conditions)]

        # Visit else branch with negated condition
        if node.orelse:
            negated_conditions = [
                PathCondition(c.variable, c.operator, c.value, not c.negated)
                for c in conditions
            ]
            self.current_conditions.extend(negated_conditions)
            for stmt in node.orelse:
                self.visit(stmt)
                if isinstance(stmt, (ast.Return, ast.Raise)):
                    self._record_path(stmt.lineno, "else branch")
            self.current_conditions = self.current_conditions[:-len(negated_conditions)]

    def visit_For(self, node: ast.For):
        """Handle for loops."""
        # Record path for loop body
        for stmt in node.body:
            self.visit(stmt)

    def visit_While(self, node: ast.While):
        """Handle while loops."""
        conditions = self._extract_conditions(node.test, negated=False)
        self.current_conditions.extend(conditions)
        for stmt in node.body:
            self.visit(stmt)
        self.current_conditions = self.current_conditions[:-len(conditions)]

    def visit_Try(self, node: ast.Try):
        """Handle try-except blocks."""
        # Visit try body
        for stmt in node.body:
            self.visit(stmt)

        # Visit exception handlers
        for handler in node.handlers:
            if handler.type:
                exc_type = self._get_name(handler.type)
                desc = f"exception handler ({exc_type})"
            else:
                desc = "exception handler (all)"

            for stmt in handler.body:
                self.visit(stmt)
                if isinstance(stmt, (ast.Return, ast.Raise)):
                    self._record_path(stmt.lineno, desc)

    def _extract_conditions(self, test_node: ast.AST, negated: bool) -> List[PathCondition]:
        """Extract path conditions from a test expression."""
        conditions = []

        if isinstance(test_node, ast.Compare):
            left = self._get_name(test_node.left)
            for op, comparator in zip(test_node.ops, test_node.comparators):
                operator = self._get_operator(op)
                value = self._get_value(comparator)
                conditions.append(PathCondition(left, operator, value, negated))

        elif isinstance(test_node, ast.UnaryOp) and isinstance(test_node.op, ast.Not):
            # Handle 'not' operator
            conditions.extend(self._extract_conditions(test_node.operand, not negated))

        elif isinstance(test_node, ast.BoolOp):
            # Handle 'and'/'or' operators
            for value in test_node.values:
                conditions.extend(self._extract_conditions(value, negated))

        elif isinstance(test_node, ast.Call):
            # Handle function calls (e.g., isinstance, callable)
            func_name = self._get_name(test_node.func)
            if test_node.args:
                arg_name = self._get_name(test_node.args[0])
                conditions.append(PathCondition(arg_name, func_name, True, negated))

        elif isinstance(test_node, ast.Name):
            # Handle boolean variables
            var_name = test_node.id
            conditions.append(PathCondition(var_name, "==", True, negated))

        return conditions

    def _get_operator(self, op: ast.AST) -> str:
        """Convert AST operator to string."""
        op_map = {
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.Is: "is",
            ast.IsNot: "is not",
            ast.In: "in",
            ast.NotIn: "not in",
        }
        return op_map.get(type(op), "unknown")

    def _get_name(self, node: ast.AST) -> str:
        """Extract variable/attribute name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[...]"
        return "unknown"

    def _get_value(self, node: ast.AST) -> Any:
        """Extract constant value from AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.List):
            return [self._get_value(elt) for elt in node.elts]
        return "unknown"

    def _record_path(self, line_number: int, description: str):
        """Record a code path with its conditions."""
        path = CodePath(
            path_id=self.path_counter,
            conditions=list(self.current_conditions),
            target_line=line_number,
            description=description
        )
        self.paths.append(path)
        self.path_counter += 1


def analyze_code_paths(source_code: str) -> List[CodePath]:
    """
    Analyze Python source code and extract all code paths with their conditions.

    Args:
        source_code: Python source code as a string

    Returns:
        List of CodePath objects representing different execution paths
    """
    tree = ast.parse(source_code)
    analyzer = PathAnalyzer()
    analyzer.visit(tree)
    return analyzer.paths


def print_paths(paths: List[CodePath]):
    """Pretty print extracted code paths."""
    print(f"\nFound {len(paths)} code paths:\n")
    for path in paths:
        print(f"Path #{path.path_id}: {path.description} (line {path.target_line})")
        print("  Conditions:")
        for condition in path.conditions:
            print(f"    - {condition}")
        print()


if __name__ == "__main__":
    # Example usage
    example_code = """
def validate_user(age, is_premium, country):
    if age < 18:
        raise ValueError("Too young")

    if age > 65:
        return "senior_discount"

    if is_premium and country == "US":
        return "premium_us"
    elif is_premium:
        return "premium_intl"
    else:
        return "standard"
"""

    paths = analyze_code_paths(example_code)
    print_paths(paths)
