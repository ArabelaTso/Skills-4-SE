#!/usr/bin/env python3
"""
Compare test results between two versions to detect regressions.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import difflib


class RegressionChecker:
    """Check for regressions between two test runs."""

    def __init__(self, tolerance=1e-6):
        self.tolerance = tolerance
        self.regressions = []
        self.improvements = []
        self.unchanged = []

    def compare_test_results(self, old_results: Dict, new_results: Dict) -> Dict:
        """Compare test results from old and new versions."""
        report = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'improvements': [],
            'unchanged': 0
        }

        all_tests = set(old_results.keys()) | set(new_results.keys())

        for test_name in all_tests:
            old_result = old_results.get(test_name)
            new_result = new_results.get(test_name)

            # Test missing in new version
            if old_result and not new_result:
                report['critical'].append({
                    'test': test_name,
                    'type': 'missing_test',
                    'message': 'Test exists in old version but missing in new version',
                    'old': 'exists',
                    'new': 'missing'
                })
                continue

            # New test added
            if not old_result and new_result:
                report['improvements'].append({
                    'test': test_name,
                    'type': 'new_test',
                    'message': 'New test added in new version'
                })
                continue

            # Compare test outcomes
            regression = self._compare_test_outcome(test_name, old_result, new_result)
            if regression:
                severity = regression['severity']
                if severity in report:
                    report[severity].append(regression)
            else:
                report['unchanged'] += 1

        return report

    def _compare_test_outcome(self, test_name: str, old: Dict, new: Dict) -> Dict:
        """Compare a single test outcome."""
        old_passed = old.get('passed', False)
        new_passed = new.get('passed', False)

        # Test now fails
        if old_passed and not new_passed:
            return {
                'test': test_name,
                'type': 'test_failure',
                'severity': 'critical',
                'message': 'Test passed in old version but fails in new version',
                'old': 'PASS',
                'new': 'FAIL',
                'error': new.get('error', 'Unknown error')
            }

        # Test now passes (improvement)
        if not old_passed and new_passed:
            self.improvements.append({
                'test': test_name,
                'type': 'test_fix',
                'message': 'Test failed in old version but passes in new version'
            })
            return None

        # Both pass - compare outputs
        if old_passed and new_passed:
            return self._compare_outputs(test_name, old, new)

        # Both fail - compare errors
        if not old_passed and not new_passed:
            return self._compare_errors(test_name, old, new)

        return None

    def _compare_outputs(self, test_name: str, old: Dict, new: Dict) -> Dict:
        """Compare test outputs when both pass."""
        old_output = old.get('output')
        new_output = new.get('output')

        if old_output is None or new_output is None:
            return None

        # Try different comparison strategies
        if self._exact_match(old_output, new_output):
            return None

        if self._approx_match(old_output, new_output):
            return None

        # Outputs differ
        diff = self._generate_diff(old_output, new_output)

        return {
            'test': test_name,
            'type': 'output_regression',
            'severity': 'high',
            'message': 'Test passes but output differs between versions',
            'old': str(old_output)[:200],
            'new': str(new_output)[:200],
            'diff': diff
        }

    def _compare_errors(self, test_name: str, old: Dict, new: Dict) -> Dict:
        """Compare errors when both fail."""
        old_error = old.get('error', '')
        new_error = new.get('error', '')

        old_type = old.get('error_type', '')
        new_type = new.get('error_type', '')

        # Different exception types
        if old_type != new_type:
            return {
                'test': test_name,
                'type': 'exception_regression',
                'severity': 'medium',
                'message': 'Test fails with different exception type',
                'old': old_type,
                'new': new_type
            }

        # Different error messages
        if old_error != new_error:
            return {
                'test': test_name,
                'type': 'error_message_change',
                'severity': 'low',
                'message': 'Test fails with different error message',
                'old': old_error[:200],
                'new': new_error[:200]
            }

        return None

    def _exact_match(self, old: Any, new: Any) -> bool:
        """Check if outputs match exactly."""
        return old == new

    def _approx_match(self, old: Any, new: Any) -> bool:
        """Check if outputs match approximately (for floats)."""
        try:
            if isinstance(old, (int, float)) and isinstance(new, (int, float)):
                return abs(old - new) < self.tolerance
        except:
            pass
        return False

    def _generate_diff(self, old: Any, new: Any) -> str:
        """Generate diff between outputs."""
        old_str = str(old).splitlines()
        new_str = str(new).splitlines()

        diff = difflib.unified_diff(
            old_str,
            new_str,
            fromfile='old',
            tofile='new',
            lineterm=''
        )

        return '\n'.join(list(diff)[:20])  # Limit to 20 lines


def load_test_results(filepath: Path) -> Dict:
    """Load test results from JSON file."""
    with open(filepath) as f:
        data = json.load(f)

    # Normalize to common format
    results = {}

    # Handle pytest-json format
    if 'tests' in data:
        for test in data['tests']:
            test_name = test.get('nodeid', test.get('name'))
            results[test_name] = {
                'passed': test.get('outcome') == 'passed',
                'output': test.get('call', {}).get('stdout'),
                'error': test.get('call', {}).get('longrepr'),
                'error_type': test.get('call', {}).get('excinfo', {}).get('type')
            }

    # Handle Jest format
    elif 'testResults' in data:
        for test_file in data['testResults']:
            for test in test_file.get('assertionResults', []):
                test_name = f"{test_file['name']}::{test['title']}"
                results[test_name] = {
                    'passed': test['status'] == 'passed',
                    'error': '\n'.join(test.get('failureMessages', []))
                }

    # Generic format
    else:
        results = data

    return results


def print_report(report: Dict):
    """Print regression report."""
    print("=" * 80)
    print("REGRESSION CONSISTENCY CHECK REPORT")
    print("=" * 80)
    print()

    total_issues = sum(len(report[k]) for k in ['critical', 'high', 'medium', 'low'])

    if total_issues == 0:
        print("✅ No regressions detected!")
        print(f"   {report['unchanged']} tests unchanged")
        if report['improvements']:
            print(f"   {len(report['improvements'])} improvements found")
        print()
        return

    print(f"⚠️  {total_issues} potential regressions detected")
    print(f"   {report['unchanged']} tests unchanged")
    if report['improvements']:
        print(f"   {len(report['improvements'])} improvements found")
    print()

    # Critical regressions
    if report['critical']:
        print("🔴 CRITICAL REGRESSIONS ({})".format(len(report['critical'])))
        print("-" * 80)
        for issue in report['critical']:
            print(f"\n  Test: {issue['test']}")
            print(f"  Type: {issue['type']}")
            print(f"  Issue: {issue['message']}")
            if 'old' in issue and 'new' in issue:
                print(f"  Old: {issue['old']}")
                print(f"  New: {issue['new']}")
            if 'error' in issue:
                print(f"  Error: {issue['error']}")
        print()

    # High severity
    if report['high']:
        print("🟠 HIGH SEVERITY REGRESSIONS ({})".format(len(report['high'])))
        print("-" * 80)
        for issue in report['high'][:5]:  # Show first 5
            print(f"\n  Test: {issue['test']}")
            print(f"  Type: {issue['type']}")
            print(f"  Issue: {issue['message']}")
            if 'diff' in issue:
                print(f"  Diff:\n{issue['diff']}")
        if len(report['high']) > 5:
            print(f"\n  ... and {len(report['high']) - 5} more")
        print()

    # Medium severity
    if report['medium']:
        print("🟡 MEDIUM SEVERITY REGRESSIONS ({})".format(len(report['medium'])))
        print("-" * 80)
        for issue in report['medium'][:3]:
            print(f"\n  Test: {issue['test']}")
            print(f"  Issue: {issue['message']}")
        if len(report['medium']) > 3:
            print(f"\n  ... and {len(report['medium']) - 3} more")
        print()

    # Low severity
    if report['low']:
        print("🔵 LOW SEVERITY CHANGES ({})".format(len(report['low'])))
        print("-" * 80)
        print(f"  {len(report['low'])} minor changes detected")
        print()

    # Improvements
    if report['improvements']:
        print("✅ IMPROVEMENTS ({})".format(len(report['improvements'])))
        print("-" * 80)
        for improvement in report['improvements'][:3]:
            print(f"  • {improvement['test']}: {improvement['message']}")
        if len(report['improvements']) > 3:
            print(f"  ... and {len(report['improvements']) - 3} more")
        print()

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Check for regressions between two test runs'
    )
    parser.add_argument(
        'old_results',
        type=Path,
        help='Test results from old version (JSON)'
    )
    parser.add_argument(
        'new_results',
        type=Path,
        help='Test results from new version (JSON)'
    )
    parser.add_argument(
        '--tolerance',
        type=float,
        default=1e-6,
        help='Tolerance for floating point comparison'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file for detailed report (JSON)'
    )

    args = parser.parse_args()

    if not args.old_results.exists():
        print(f"Error: Old results file not found: {args.old_results}", file=sys.stderr)
        return 1

    if not args.new_results.exists():
        print(f"Error: New results file not found: {args.new_results}", file=sys.stderr)
        return 1

    # Load results
    old_results = load_test_results(args.old_results)
    new_results = load_test_results(args.new_results)

    # Compare
    checker = RegressionChecker(tolerance=args.tolerance)
    report = checker.compare_test_results(old_results, new_results)

    # Print report
    print_report(report)

    # Save detailed report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nDetailed report saved to: {args.output}")

    # Exit code: 0 if no regressions, 1 if regressions found
    total_issues = sum(len(report[k]) for k in ['critical', 'high', 'medium'])
    return 1 if total_issues > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
