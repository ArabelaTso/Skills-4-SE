#!/usr/bin/env python3
"""
Analyze test failures and categorize them to guide migration fixes.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class TestFailureAnalyzer:
    """Analyze test output to categorize failures."""

    def __init__(self):
        self.categories = {
            'import_errors': [],
            'api_signature_errors': [],
            'type_errors': [],
            'behavior_changes': [],
            'configuration_errors': [],
            'deprecation_warnings': [],
            'other_errors': []
        }

    def analyze_pytest_output(self, output: str) -> Dict[str, List[Dict]]:
        """Analyze pytest output."""
        lines = output.split('\n')
        current_test = None
        current_error = []
        in_error = False

        for line in lines:
            # Detect test name
            test_match = re.match(r'^(.*?)::(.*?)\s+', line)
            if test_match:
                if current_test and current_error:
                    self._categorize_error(current_test, '\n'.join(current_error))
                current_test = f"{test_match.group(1)}::{test_match.group(2)}"
                current_error = []
                in_error = False

            # Detect error section
            if 'FAILED' in line or 'ERROR' in line:
                in_error = True
            elif line.startswith('=') or line.startswith('_'):
                in_error = False

            if in_error:
                current_error.append(line)

        # Process last error
        if current_test and current_error:
            self._categorize_error(current_test, '\n'.join(current_error))

        return self.categories

    def analyze_jest_output(self, output: str) -> Dict[str, List[Dict]]:
        """Analyze Jest output."""
        lines = output.split('\n')
        current_test = None
        current_error = []

        for line in lines:
            # Detect test name
            if '●' in line and '›' in line:
                if current_test and current_error:
                    self._categorize_error(current_test, '\n'.join(current_error))
                current_test = line.strip('● ').strip()
                current_error = []
            elif current_test and line.strip():
                current_error.append(line)

        # Process last error
        if current_test and current_error:
            self._categorize_error(current_test, '\n'.join(current_error))

        return self.categories

    def _categorize_error(self, test_name: str, error_text: str):
        """Categorize a single error."""
        error_lower = error_text.lower()

        error_info = {
            'test': test_name,
            'error': error_text[:500]  # Truncate long errors
        }

        # Import errors
        if any(keyword in error_lower for keyword in [
            'importerror', 'modulenotfounderror', 'cannot find module',
            'cannot import', 'no module named'
        ]):
            self.categories['import_errors'].append(error_info)

        # API signature errors
        elif any(keyword in error_lower for keyword in [
            'unexpected keyword argument', 'missing required argument',
            'takes', 'positional argument', 'got an unexpected keyword'
        ]):
            self.categories['api_signature_errors'].append(error_info)

        # Type errors
        elif any(keyword in error_lower for keyword in [
            'typeerror', 'type error', 'expected type', 'is not assignable'
        ]):
            self.categories['type_errors'].append(error_info)

        # Configuration errors
        elif any(keyword in error_lower for keyword in [
            'configurationerror', 'invalid configuration', 'config',
            'settings', 'environment'
        ]):
            self.categories['configuration_errors'].append(error_info)

        # Deprecation warnings
        elif any(keyword in error_lower for keyword in [
            'deprecationwarning', 'deprecated', 'will be removed'
        ]):
            self.categories['deprecation_warnings'].append(error_info)

        # Behavior changes (assertion failures)
        elif any(keyword in error_lower for keyword in [
            'assertionerror', 'assert', 'expected', 'actual',
            'to equal', 'to be', 'received'
        ]):
            self.categories['behavior_changes'].append(error_info)

        # Other errors
        else:
            self.categories['other_errors'].append(error_info)


def print_analysis_report(categories: Dict[str, List[Dict]]):
    """Print categorized failure report."""
    print("=" * 80)
    print("TEST FAILURE ANALYSIS REPORT")
    print("=" * 80)
    print()

    total_failures = sum(len(errors) for errors in categories.values())
    print(f"Total failures analyzed: {total_failures}")
    print()

    # Priority order for fixing
    priority_order = [
        ('import_errors', 'Import/Module Errors', '🔴', 'CRITICAL - Fix first'),
        ('api_signature_errors', 'API Signature Errors', '🟠', 'HIGH - Fix second'),
        ('type_errors', 'Type Errors', '🟡', 'MEDIUM'),
        ('configuration_errors', 'Configuration Errors', '🟡', 'MEDIUM'),
        ('behavior_changes', 'Behavior Changes', '🟢', 'Review carefully'),
        ('deprecation_warnings', 'Deprecation Warnings', '🔵', 'Fix when possible'),
        ('other_errors', 'Other Errors', '⚪', 'Investigate')
    ]

    for category_key, category_name, icon, priority in priority_order:
        errors = categories[category_key]
        if not errors:
            continue

        print(f"{icon} {category_name} ({len(errors)} failures) - {priority}")
        print("-" * 80)

        # Show first 3 examples
        for i, error in enumerate(errors[:3], 1):
            print(f"\n  Example {i}: {error['test']}")
            # Show first 2 lines of error
            error_lines = error['error'].split('\n')[:2]
            for line in error_lines:
                if line.strip():
                    print(f"    {line.strip()[:100]}")

        if len(errors) > 3:
            print(f"\n  ... and {len(errors) - 3} more")

        print()

    # Recommendations
    print("=" * 80)
    print("RECOMMENDED FIX ORDER")
    print("=" * 80)
    print()

    if categories['import_errors']:
        print("1. Fix import errors first (blocks other tests)")
        print("   - Update import statements")
        print("   - Check for renamed/moved modules")
        print("   - Install missing dependencies")
        print()

    if categories['api_signature_errors']:
        print("2. Fix API signature errors")
        print("   - Update function calls")
        print("   - Check migration guide for parameter changes")
        print("   - Use IDE refactoring tools")
        print()

    if categories['type_errors']:
        print("3. Fix type errors")
        print("   - Update type annotations")
        print("   - Add type conversions")
        print("   - Check for stricter type checking")
        print()

    if categories['configuration_errors']:
        print("4. Fix configuration errors")
        print("   - Update config files")
        print("   - Check for renamed settings")
        print("   - Set explicit defaults")
        print()

    if categories['behavior_changes']:
        print("5. Review behavior changes carefully")
        print("   - Read migration guide")
        print("   - Understand new behavior")
        print("   - Update code to match new semantics")
        print("   - DO NOT modify tests unless behavior change is intentional")
        print()

    if categories['deprecation_warnings']:
        print("6. Address deprecation warnings")
        print("   - Update to new APIs")
        print("   - Plan for future compatibility")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Analyze test failures to guide migration'
    )
    parser.add_argument(
        'test_output',
        type=Path,
        help='Path to test output file'
    )
    parser.add_argument(
        '--format',
        choices=['pytest', 'jest', 'auto'],
        default='auto',
        help='Test framework format (default: auto-detect)'
    )

    args = parser.parse_args()

    if not args.test_output.exists():
        print(f"Error: Test output file not found: {args.test_output}", file=sys.stderr)
        return 1

    # Read test output
    with open(args.test_output) as f:
        output = f.read()

    # Auto-detect format
    format_type = args.format
    if format_type == 'auto':
        if 'FAILED' in output and '::' in output:
            format_type = 'pytest'
        elif '●' in output and 'FAIL' in output:
            format_type = 'jest'
        else:
            format_type = 'pytest'  # Default

    # Analyze failures
    analyzer = TestFailureAnalyzer()
    if format_type == 'pytest':
        categories = analyzer.analyze_pytest_output(output)
    else:
        categories = analyzer.analyze_jest_output(output)

    # Print report
    print_analysis_report(categories)

    return 0


if __name__ == '__main__':
    sys.exit(main())
