#!/usr/bin/env python3
"""
Validate temporal logic formula syntax.
Supports LTL, CTL, and basic well-formedness checks.
"""

import re
import sys
from typing import Tuple, List

class TemporalLogicValidator:
    """Validator for temporal logic formulas."""

    # LTL operators
    LTL_UNARY = {'G', 'F', 'X', '!', '~'}
    LTL_BINARY = {'U', 'R', 'W', '->', '<->', '&&', '||', '&', '|', 'and', 'or', 'imply'}

    # CTL operators
    CTL_PATH = {'A', 'E'}
    CTL_TEMPORAL = {'G', 'F', 'X', 'U'}

    # SPIN syntax
    SPIN_ALWAYS = {'[]'}
    SPIN_EVENTUALLY = {'<>'}

    def __init__(self, logic_type='LTL'):
        """
        Initialize validator.

        Args:
            logic_type: 'LTL', 'CTL', or 'SPIN'
        """
        self.logic_type = logic_type.upper()
        self.errors = []
        self.warnings = []

    def validate(self, formula: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a temporal logic formula.

        Args:
            formula: The formula string to validate

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        if not formula or not formula.strip():
            self.errors.append("Empty formula")
            return False, self.errors, self.warnings

        formula = formula.strip()

        # Check balanced parentheses
        if not self._check_balanced_parens(formula):
            self.errors.append("Unbalanced parentheses")

        # Check for invalid characters
        if not self._check_valid_chars(formula):
            self.errors.append("Invalid characters in formula")

        # Logic-specific validation
        if self.logic_type == 'LTL':
            self._validate_ltl(formula)
        elif self.logic_type == 'CTL':
            self._validate_ctl(formula)
        elif self.logic_type == 'SPIN':
            self._validate_spin(formula)

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_balanced_parens(self, formula: str) -> bool:
        """Check if parentheses are balanced."""
        count = 0
        for char in formula:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count < 0:
                return False
        return count == 0

    def _check_valid_chars(self, formula: str) -> bool:
        """Check for valid characters."""
        # Allow alphanumeric, operators, parentheses, spaces, underscores
        valid_pattern = r'^[a-zA-Z0-9_\s()\[\]<>!~&|GFXURAWES\->,]+$'
        return bool(re.match(valid_pattern, formula))

    def _validate_ltl(self, formula: str):
        """Validate LTL formula."""
        # Check for CTL path quantifiers (not allowed in LTL)
        if re.search(r'\b[AE]\s*[GFXU]', formula):
            self.errors.append("LTL formulas cannot contain CTL path quantifiers (A, E)")

        # Check for proper operator usage
        if re.search(r'[GFXU]\s*[GFXU]', formula):
            self.warnings.append("Consecutive temporal operators - ensure this is intentional")

        # Check for common mistakes
        if 'GF' in formula.replace(' ', ''):
            self.warnings.append("GF pattern detected - this means 'infinitely often'")
        if 'FG' in formula.replace(' ', ''):
            self.warnings.append("FG pattern detected - this means 'eventually forever'")

    def _validate_ctl(self, formula: str):
        """Validate CTL formula."""
        # Check that temporal operators are preceded by path quantifiers
        temporal_without_path = re.findall(r'(?<![AE])\s*([GFXU])\s*[a-zA-Z(]', formula)
        if temporal_without_path:
            self.errors.append(f"CTL temporal operators must be preceded by path quantifiers (A or E)")

        # Check for valid CTL patterns
        valid_ctl_patterns = ['AG', 'EG', 'AF', 'EF', 'AX', 'EX', 'AU', 'EU']
        found_patterns = re.findall(r'[AE][GFXU]', formula)

        for pattern in found_patterns:
            if pattern not in valid_ctl_patterns:
                self.warnings.append(f"Unusual CTL pattern: {pattern}")

    def _validate_spin(self, formula: str):
        """Validate SPIN (Promela) formula."""
        # Convert SPIN syntax to standard LTL for validation
        converted = formula.replace('[]', 'G').replace('<>', 'F')
        self._validate_ltl(converted)

        # Check for SPIN-specific syntax
        if '[]' in formula and 'G' in formula:
            self.warnings.append("Mixed SPIN ([]) and standard (G) syntax")
        if '<>' in formula and 'F' in formula:
            self.warnings.append("Mixed SPIN (<>) and standard (F) syntax")

def main():
    """Command-line interface for formula validation."""
    if len(sys.argv) < 2:
        print("Usage: python validate_formula.py <formula> [logic_type]")
        print("  logic_type: LTL (default), CTL, or SPIN")
        sys.exit(1)

    formula = sys.argv[1]
    logic_type = sys.argv[2] if len(sys.argv) > 2 else 'LTL'

    validator = TemporalLogicValidator(logic_type)
    is_valid, errors, warnings = validator.validate(formula)

    print(f"Formula: {formula}")
    print(f"Logic Type: {logic_type}")
    print(f"Valid: {is_valid}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  ❌ {error}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")

    if is_valid and not warnings:
        print("\n✅ Formula is valid!")

    sys.exit(0 if is_valid else 1)

if __name__ == '__main__':
    main()
