#!/usr/bin/env python3
"""
compare_test_results.py - Compare test results from two test runs

Supports multiple test result formats:
- pytest JSON reports
- JUnit XML
- unittest output
- Custom JSON format
"""

import argparse
import json
import sys
from typing import Dict, List, Set
from pathlib import Path


class TestResultComparator:
    """Compare test results between two test runs."""

    def __init__(self, original_file: str, migrated_file: str):
        self.original_file = original_file
        self.migrated_file = migrated_file

    def load_results(self, file_path: str) -> Dict:
        """Load test results from file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Test results file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        # Normalize to common format
        return self._normalize_format(data)

    def _normalize_format(self, data: Dict) -> Dict:
        """Normalize different test result formats to common structure."""
        # Detect format and normalize
        if 'tests' in data and isinstance(data['tests'], list):
            # Already in normalized format
            return data

        if 'report' in data:
            # pytest-json-report format
            return self._normalize_pytest_json(data)

        # Assume custom format
        return data

    def _normalize_pytest_json(self, data: Dict) -> Dict:
        """Normalize pytest JSON report format."""
        tests = []
        report = data.get('report', {})

        for test in report.get('tests', []):
            tests.append({
                'name': test.get('nodeid', 'unknown'),
                'status': 'passed' if test.get('outcome') == 'passed' else 'failed',
                'duration': test.get('duration', 0),
                'error': test.get('call', {}).get('longrepr') if test.get('outcome') == 'failed' else None
            })

        return {
            'tests': tests,
            'summary': report.get('summary', {})
        }

    def compare(self) -> Dict:
        """Compare test results and generate report."""
        print(f"Loading original results from {self.original_file}...")
        original = self.load_results(self.original_file)

        print(f"Loading migrated results from {self.migrated_file}...")
        migrated = self.load_results(self.migrated_file)

        original_tests = {t['name']: t for t in original.get('tests', [])}
        migrated_tests = {t['name']: t for t in migrated.get('tests', [])}

        all_tests = set(original_tests.keys()) | set(migrated_tests.keys())

        comparison = {
            'total_tests': len(all_tests),
            'categories': {
                'passed_both': [],
                'failed_both': [],
                'passed_original_failed_migrated': [],
                'failed_original_passed_migrated': [],
                'only_in_original': [],
                'only_in_migrated': []
            },
            'differences': []
        }

        for test_name in sorted(all_tests):
            orig = original_tests.get(test_name)
            mig = migrated_tests.get(test_name)

            if orig and mig:
                orig_status = orig['status']
                mig_status = mig['status']

                if orig_status == 'passed' and mig_status == 'passed':
                    comparison['categories']['passed_both'].append(test_name)
                elif orig_status == 'failed' and mig_status == 'failed':
                    comparison['categories']['failed_both'].append(test_name)
                elif orig_status == 'passed' and mig_status == 'failed':
                    comparison['categories']['passed_original_failed_migrated'].append(test_name)
                    comparison['differences'].append({
                        'test': test_name,
                        'type': 'regression',
                        'original': 'passed',
                        'migrated': 'failed',
                        'error': mig.get('error', 'No error message')
                    })
                elif orig_status == 'failed' and mig_status == 'passed':
                    comparison['categories']['failed_original_passed_migrated'].append(test_name)
                    comparison['differences'].append({
                        'test': test_name,
                        'type': 'improvement',
                        'original': 'failed',
                        'migrated': 'passed'
                    })
            elif orig:
                comparison['categories']['only_in_original'].append(test_name)
                comparison['differences'].append({
                    'test': test_name,
                    'type': 'missing_in_migrated',
                    'original': orig['status'],
                    'migrated': 'not_found'
                })
            else:
                comparison['categories']['only_in_migrated'].append(test_name)

        # Calculate summary statistics
        comparison['summary'] = {
            'passed_both': len(comparison['categories']['passed_both']),
            'failed_both': len(comparison['categories']['failed_both']),
            'regressions': len(comparison['categories']['passed_original_failed_migrated']),
            'improvements': len(comparison['categories']['failed_original_passed_migrated']),
            'missing_in_migrated': len(comparison['categories']['only_in_original']),
            'new_in_migrated': len(comparison['categories']['only_in_migrated'])
        }

        total = comparison['total_tests']
        passed_both = comparison['summary']['passed_both']
        equivalence = (passed_both / total * 100) if total > 0 else 0
        comparison['summary']['behavioral_equivalence'] = f"{equivalence:.1f}%"

        return comparison

    def print_report(self, comparison: Dict):
        """Print comparison report to console."""
        print("\n" + "="*80)
        print("TEST COMPARISON REPORT")
        print("="*80)

        summary = comparison['summary']
        print(f"\nTotal tests: {comparison['total_tests']}")
        print(f"Passed in both: {summary['passed_both']}")
        print(f"Failed in both: {summary['failed_both']}")
        print(f"Regressions (passed → failed): {summary['regressions']}")
        print(f"Improvements (failed → passed): {summary['improvements']}")
        print(f"Missing in migrated: {summary['missing_in_migrated']}")
        print(f"New in migrated: {summary['new_in_migrated']}")
        print(f"\nBehavioral equivalence: {summary['behavioral_equivalence']}")

        # Print regressions
        regressions = [d for d in comparison['differences'] if d['type'] == 'regression']
        if regressions:
            print("\n" + "="*80)
            print("REGRESSIONS (Critical)")
            print("="*80)
            for reg in regressions[:10]:  # Show first 10
                print(f"\n✗ {reg['test']}")
                if reg.get('error'):
                    error_lines = reg['error'].split('\n')[:3]
                    for line in error_lines:
                        print(f"  {line}")

        # Print improvements
        improvements = [d for d in comparison['differences'] if d['type'] == 'improvement']
        if improvements:
            print("\n" + "="*80)
            print("IMPROVEMENTS")
            print("="*80)
            for imp in improvements[:5]:
                print(f"✓ {imp['test']}")

        # Print missing tests
        missing = [d for d in comparison['differences'] if d['type'] == 'missing_in_migrated']
        if missing:
            print("\n" + "="*80)
            print("MISSING TESTS")
            print("="*80)
            for miss in missing[:5]:
                print(f"⚠ {miss['test']}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare test results between original and migrated versions'
    )
    parser.add_argument('original', help='Original test results file (JSON)')
    parser.add_argument('migrated', help='Migrated test results file (JSON)')
    parser.add_argument('--output', help='Output file for comparison report (JSON)')
    parser.add_argument('--fail-on-regression', action='store_true',
                       help='Exit with error code if regressions found')

    args = parser.parse_args()

    try:
        comparator = TestResultComparator(args.original, args.migrated)
        comparison = comparator.compare()
        comparator.print_report(comparison)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(comparison, f, indent=2)
            print(f"\nComparison report saved to: {args.output}")

        # Exit with error if regressions found
        if args.fail_on_regression and comparison['summary']['regressions'] > 0:
            print(f"\n✗ Found {comparison['summary']['regressions']} regression(s)")
            sys.exit(1)
        else:
            print("\n✓ Comparison complete")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
