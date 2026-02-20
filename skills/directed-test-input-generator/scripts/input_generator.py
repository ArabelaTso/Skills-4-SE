#!/usr/bin/env python3
"""
Test Input Generator - Generates test inputs to satisfy specific path conditions.
"""

from typing import Any, Dict, List, Set, Optional
from dataclasses import dataclass
import random


@dataclass
class InputConstraint:
    """Represents a constraint on an input parameter."""
    param_name: str
    param_type: type
    constraints: List[str]  # List of constraint expressions


class TestInputGenerator:
    """Generates test inputs that satisfy path conditions."""

    def __init__(self):
        self.random = random.Random()

    def generate_for_path(self, constraints: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Generate test inputs that satisfy the given constraints.

        Args:
            constraints: Dictionary mapping parameter names to their constraints

        Returns:
            Dictionary mapping parameter names to generated values
        """
        inputs = {}
        for param_name, param_constraints in constraints.items():
            inputs[param_name] = self._generate_value(param_name, param_constraints)
        return inputs

    def _generate_value(self, param_name: str, constraints: List[Any]) -> Any:
        """Generate a value satisfying the given constraints."""
        if not constraints:
            return self._generate_default_value(param_name)

        # Analyze constraints to determine value
        for constraint in constraints:
            constraint_str = str(constraint)

            # Parse comparison constraints
            if " == " in constraint_str:
                _, value = constraint_str.split(" == ", 1)
                return self._parse_value(value.strip())

            elif " != " in constraint_str:
                _, value = constraint_str.split(" != ", 1)
                # Generate something different
                parsed = self._parse_value(value.strip())
                return self._generate_different_value(parsed)

            elif " < " in constraint_str:
                _, value = constraint_str.split(" < ", 1)
                upper_bound = self._parse_numeric(value.strip())
                return upper_bound - 1 if isinstance(upper_bound, int) else upper_bound - 0.1

            elif " > " in constraint_str:
                _, value = constraint_str.split(" > ", 1)
                lower_bound = self._parse_numeric(value.strip())
                return lower_bound + 1 if isinstance(lower_bound, int) else lower_bound + 0.1

            elif " <= " in constraint_str:
                _, value = constraint_str.split(" <= ", 1)
                upper_bound = self._parse_numeric(value.strip())
                return upper_bound

            elif " >= " in constraint_str:
                _, value = constraint_str.split(" >= ", 1)
                lower_bound = self._parse_numeric(value.strip())
                return lower_bound

            elif "isinstance" in constraint_str or "callable" in constraint_str:
                # Type constraints
                if "str" in constraint_str:
                    return "test_string"
                elif "int" in constraint_str:
                    return 42
                elif "list" in constraint_str:
                    return []
                elif "dict" in constraint_str:
                    return {}

        return self._generate_default_value(param_name)

    def _parse_value(self, value_str: str) -> Any:
        """Parse a string value into appropriate Python type."""
        value_str = value_str.strip().strip("'\"")

        # Try to parse as number
        try:
            if "." in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass

        # Check for boolean
        if value_str.lower() == "true":
            return True
        elif value_str.lower() == "false":
            return False

        # Return as string
        return value_str

    def _parse_numeric(self, value_str: str) -> float:
        """Parse a numeric value."""
        try:
            return float(value_str)
        except ValueError:
            return 0

    def _generate_different_value(self, reference_value: Any) -> Any:
        """Generate a value different from the reference."""
        if isinstance(reference_value, bool):
            return not reference_value
        elif isinstance(reference_value, int):
            return reference_value + 1
        elif isinstance(reference_value, float):
            return reference_value + 1.0
        elif isinstance(reference_value, str):
            return reference_value + "_different"
        elif isinstance(reference_value, list):
            return reference_value + [1]
        else:
            return None

    def _generate_default_value(self, param_name: str) -> Any:
        """Generate a default value based on parameter name heuristics."""
        name_lower = param_name.lower()

        # Heuristics based on common naming patterns
        if "age" in name_lower:
            return self.random.randint(18, 80)
        elif "count" in name_lower or "num" in name_lower:
            return self.random.randint(0, 100)
        elif "price" in name_lower or "cost" in name_lower:
            return round(self.random.uniform(0, 1000), 2)
        elif "name" in name_lower:
            return "test_name"
        elif "email" in name_lower:
            return "test@example.com"
        elif "is_" in name_lower or name_lower.startswith("has_"):
            return self.random.choice([True, False])
        elif "id" in name_lower:
            return self.random.randint(1, 10000)
        elif "country" in name_lower:
            return self.random.choice(["US", "UK", "CA", "AU"])
        else:
            return None


class EdgeCaseGenerator:
    """Generates edge case and boundary value test inputs."""

    @staticmethod
    def generate_edge_cases(param_type: type) -> List[Any]:
        """Generate edge case values for a given type."""
        edge_cases = []

        if param_type == int:
            edge_cases = [
                0,
                -1,
                1,
                -2147483648,  # Min int32
                2147483647,   # Max int32
                -9223372036854775808,  # Min int64
                9223372036854775807,   # Max int64
            ]
        elif param_type == float:
            edge_cases = [
                0.0,
                -0.0,
                1.0,
                -1.0,
                float('inf'),
                float('-inf'),
                float('nan'),
            ]
        elif param_type == str:
            edge_cases = [
                "",
                " ",
                "a",
                "A" * 1000,  # Long string
                "\n\t\r",    # Whitespace
                "unicode: 你好",
                "special: !@#$%^&*()",
            ]
        elif param_type == list:
            edge_cases = [
                [],
                [None],
                [1],
                list(range(1000)),  # Large list
            ]
        elif param_type == dict:
            edge_cases = [
                {},
                {None: None},
                {"key": "value"},
            ]
        elif param_type == bool:
            edge_cases = [True, False]

        return edge_cases

    @staticmethod
    def generate_boundary_values(operator: str, value: Any) -> List[Any]:
        """Generate boundary values based on a comparison operator."""
        boundary_values = []

        if operator in ["<", "<="]:
            # Values around upper boundary
            if isinstance(value, int):
                boundary_values = [value - 2, value - 1, value, value + 1]
            elif isinstance(value, float):
                boundary_values = [value - 1.0, value - 0.1, value, value + 0.1]

        elif operator in [">", ">="]:
            # Values around lower boundary
            if isinstance(value, int):
                boundary_values = [value - 1, value, value + 1, value + 2]
            elif isinstance(value, float):
                boundary_values = [value - 0.1, value, value + 0.1, value + 1.0]

        elif operator == "==":
            boundary_values = [value]

        elif operator == "!=":
            if isinstance(value, int):
                boundary_values = [value - 1, value + 1]
            elif isinstance(value, str):
                boundary_values = [value + "_diff", ""]
            elif isinstance(value, bool):
                boundary_values = [not value]

        return boundary_values


def generate_test_suite(paths: List[Any]) -> Dict[int, Dict[str, Any]]:
    """
    Generate a complete test suite covering all paths.

    Args:
        paths: List of CodePath objects from path_analyzer

    Returns:
        Dictionary mapping path IDs to generated test inputs
    """
    generator = TestInputGenerator()
    test_suite = {}

    for path in paths:
        constraints = path.get_constraints()
        test_inputs = generator.generate_for_path(constraints)
        test_suite[path.path_id] = {
            "inputs": test_inputs,
            "description": path.description,
            "target_line": path.target_line
        }

    return test_suite


if __name__ == "__main__":
    # Example usage
    from path_analyzer import analyze_code_paths

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
    test_suite = generate_test_suite(paths)

    print("\nGenerated Test Suite:\n")
    for path_id, test_data in test_suite.items():
        print(f"Path #{path_id}: {test_data['description']}")
        print(f"  Inputs: {test_data['inputs']}")
        print()
