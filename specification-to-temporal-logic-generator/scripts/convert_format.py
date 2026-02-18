#!/usr/bin/env python3
"""
Convert temporal logic formulas between different tool formats.
Supports: LTL, CTL, SPIN, NuSMV, Uppaal, TLA+, Maude
"""

import sys
import re
from typing import Dict, Tuple

class FormulaConverter:
    """Convert temporal logic formulas between different formats."""

    def __init__(self):
        """Initialize converter with syntax mappings."""
        # Operator mappings: source -> target
        self.conversions = {
            'SPIN_to_LTL': {
                r'\[\]': 'G',
                r'<>': 'F',
            },
            'LTL_to_SPIN': {
                r'\bG\b': '[]',
                r'\bF\b': '<>',
            },
            'LTL_to_NuSMV_LTL': {
                r'&&': '&',
                r'\|\|': '|',
                r'!': '!',
            },
            'LTL_to_NuSMV_CTL': {
                r'\bG\b': 'AG',
                r'\bF\b': 'AF',
                r'\bX\b': 'AX',
                r'&&': '&',
                r'\|\|': '|',
            },
            'CTL_to_Uppaal': {
                r'\bAG\b': 'A[]',
                r'\bEG\b': 'E[]',
                r'\bAF\b': 'A<>',
                r'\bEF\b': 'E<>',
                r'\bAX\b': 'A<>',  # Uppaal doesn't have direct AX
                r'\bEX\b': 'E<>',  # Uppaal doesn't have direct EX
                r'->': 'imply',
                r'!': 'not ',
                r'&&': 'and',
                r'\|\|': 'or',
            },
            'LTL_to_TLA': {
                r'\bG\b': '[]',
                r'\bF\b': '<>',
                r'->': '=>',
                r'&&': '/\\',
                r'\|\|': '\\/',
                r'!': '~',
            },
            'LTL_to_Maude': {
                r'\bX\b': 'O',
                r'->': '->',
                r'&&': '/\\',
                r'\|\|': '\\/',
                r'!': '~',
            },
        }

    def convert(self, formula: str, source_format: str, target_format: str) -> Tuple[str, str]:
        """
        Convert formula from source format to target format.

        Args:
            formula: The formula to convert
            source_format: Source format (LTL, CTL, SPIN, etc.)
            target_format: Target format (LTL, CTL, SPIN, NuSMV, Uppaal, TLA+, Maude)

        Returns:
            Tuple of (converted_formula, notes)
        """
        source = source_format.upper()
        target = target_format.upper()
        notes = []

        # Handle special cases
        if source == target:
            return formula, "No conversion needed (same format)"

        # Normalize source format
        if source == 'SPIN':
            formula = self._apply_conversions(formula, 'SPIN_to_LTL')
            source = 'LTL'
            notes.append("Converted from SPIN to LTL syntax")

        # Convert to target format
        conversion_key = f"{source}_to_{target}"

        if target == 'NUSMV':
            # NuSMV supports both LTL and CTL
            if source == 'LTL':
                formula = self._apply_conversions(formula, 'LTL_to_NuSMV_LTL')
                notes.append("Converted to NuSMV LTL syntax (use LTLSPEC)")
            elif source == 'CTL':
                notes.append("Use SPEC for CTL formulas in NuSMV")
        elif target == 'SPIN':
            if source == 'LTL':
                formula = self._apply_conversions(formula, 'LTL_to_SPIN')
                notes.append("Converted to SPIN syntax")
        elif target == 'UPPAAL':
            if source == 'CTL':
                formula = self._apply_conversions(formula, 'CTL_to_Uppaal')
                notes.append("Converted to Uppaal TCTL syntax")
            else:
                notes.append("Warning: Uppaal primarily uses CTL-like syntax")
        elif target == 'TLA+' or target == 'TLA':
            if source == 'LTL':
                formula = self._apply_conversions(formula, 'LTL_to_TLA')
                notes.append("Converted to TLA+ syntax")
        elif target == 'MAUDE':
            if source == 'LTL':
                formula = self._apply_conversions(formula, 'LTL_to_Maude')
                notes.append("Converted to Maude LTL syntax")
        else:
            notes.append(f"Warning: Direct conversion from {source} to {target} may not be fully supported")

        # Add semantic notes
        if source == 'LTL' and target in ['CTL', 'UPPAAL']:
            notes.append("Note: LTL formulas converted to CTL assume universal path quantification (A)")
        if source == 'CTL' and target == 'LTL':
            notes.append("Warning: CTL path quantifiers (A/E) are lost in LTL conversion")

        return formula, "; ".join(notes) if notes else "Conversion complete"

    def _apply_conversions(self, formula: str, conversion_key: str) -> str:
        """Apply a set of regex conversions to a formula."""
        if conversion_key not in self.conversions:
            return formula

        result = formula
        for pattern, replacement in self.conversions[conversion_key].items():
            result = re.sub(pattern, replacement, result)

        return result

    def get_supported_formats(self) -> list:
        """Get list of supported formats."""
        return ['LTL', 'CTL', 'SPIN', 'NuSMV', 'Uppaal', 'TLA+', 'Maude']

def main():
    """Command-line interface for formula conversion."""
    if len(sys.argv) < 4:
        print("Usage: python convert_format.py <formula> <source_format> <target_format>")
        print("\nSupported formats: LTL, CTL, SPIN, NuSMV, Uppaal, TLA+, Maude")
        print("\nExample:")
        print("  python convert_format.py 'G(request -> F response)' LTL SPIN")
        sys.exit(1)

    formula = sys.argv[1]
    source_format = sys.argv[2]
    target_format = sys.argv[3]

    converter = FormulaConverter()
    converted, notes = converter.convert(formula, source_format, target_format)

    print(f"Original ({source_format}): {formula}")
    print(f"Converted ({target_format}): {converted}")
    if notes:
        print(f"\nNotes: {notes}")

if __name__ == '__main__':
    main()
