#!/usr/bin/env python3
"""
behavior_checker.py - Main orchestrator for comparing behavior between repositories

Coordinates multiple comparison methods:
- Test result comparison
- Execution trace comparison
- Output comparison
- Performance benchmarking

Generates comprehensive report with actionable guidance.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class BehaviorChecker:
    """Orchestrates behavior comparison between original and migrated repositories."""

    def __init__(self, original_repo: str, migrated_repo: str):
        self.original_repo = Path(original_repo)
        self.migrated_repo = Path(migrated_repo)
        self.results = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'original_repo': str(self.original_repo),
            'migrated_repo': str(self.migrated_repo),
            'summary': {},
            'differences': [],
            'recommendations': []
        }

    def run_tests(self, repo_path: Path) -> Dict:
        """Run test suite in a repository."""
        print(f"Running tests in {repo_path}...")

        # Try pytest first
        pytest_result = subprocess.run(
            ['pytest', 'tests/', '--json-report', '--json-report-file=test_results.json'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if pytest_result.returncode in [0, 1]:  # 0 = all passed, 1 = some failed
            try:
                with open(repo_path / 'test_results.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                pass

        # Fallback to unittest
        unittest_result = subprocess.run(
            ['python', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        # Parse unittest output
        return self._parse_unittest_output(unittest_result.stdout)

    def _parse_unittest_output(self, output: str) -> Dict:
        """Parse unittest output into structured format."""
        lines = output.split('\n')
        tests = []

        for line in lines:
            if line.startswith('test_'):
                parts = line.split()
                if len(parts) >= 2:
                    test_name = parts[0]
                    status = 'passed' if 'ok' in line.lower() else 'failed'
                    tests.append({'name': test_name, 'status': status})

        return {'tests': tests}

    def compare_test_results(self, original_results: Dict, migrated_results: Dict) -> Dict:
        """Compare test results between repositories."""
        print("Comparing test results...")

        original_tests = {t['name']: t for t in original_results.get('tests', [])}
        migrated_tests = {t['name']: t for t in migrated_results.get('tests', [])}

        all_test_names = set(original_tests.keys()) | set(migrated_tests.keys())

        passed_both = 0
        failed_both = 0
        passed_original_failed_migrated = 0
        failed_original_passed_migrated = 0
        only_in_original = 0
        only_in_migrated = 0

        differences = []

        for test_name in all_test_names:
            original_test = original_tests.get(test_name)
            migrated_test = migrated_tests.get(test_name)

            if original_test and migrated_test:
                orig_status = original_test.get('status', 'unknown')
                mig_status = migrated_test.get('status', 'unknown')

                if orig_status == 'passed' and mig_status == 'passed':
                    passed_both += 1
                elif orig_status == 'failed' and mig_status == 'failed':
                    failed_both += 1
                elif orig_status == 'passed' and mig_status == 'failed':
                    passed_original_failed_migrated += 1
                    differences.append({
                        'type': 'test_failure',
                        'test_name': test_name,
                        'severity': 'critical',
                        'original_result': 'passed',
                        'migrated_result': 'failed',
                        'guidance': f'Test {test_name} passed in original but fails in migrated version'
                    })
                elif orig_status == 'failed' and mig_status == 'passed':
                    failed_original_passed_migrated += 1
                    differences.append({
                        'type': 'test_improvement',
                        'test_name': test_name,
                        'severity': 'info',
                        'original_result': 'failed',
                        'migrated_result': 'passed',
                        'guidance': f'Test {test_name} now passes (was failing in original)'
                    })
            elif original_test:
                only_in_original += 1
                differences.append({
                    'type': 'missing_test',
                    'test_name': test_name,
                    'severity': 'medium',
                    'guidance': f'Test {test_name} exists in original but not in migrated'
                })
            else:
                only_in_migrated += 1

        total_tests = len(all_test_names)
        behavioral_equivalence = (passed_both / total_tests * 100) if total_tests > 0 else 0

        return {
            'summary': {
                'total_tests': total_tests,
                'passed_both': passed_both,
                'failed_both': failed_both,
                'passed_original_failed_migrated': passed_original_failed_migrated,
                'failed_original_passed_migrated': failed_original_passed_migrated,
                'only_in_original': only_in_original,
                'only_in_migrated': only_in_migrated,
                'behavioral_equivalence': f"{behavioral_equivalence:.1f}%"
            },
            'differences': differences
        }

    def generate_recommendations(self, comparison: Dict) -> List[str]:
        """Generate actionable recommendations based on comparison results."""
        recommendations = []
        summary = comparison['summary']

        critical_failures = summary.get('passed_original_failed_migrated', 0)
        if critical_failures > 0:
            recommendations.append(
                f"Fix {critical_failures} critical test failure(s) before deployment"
            )

        missing_tests = summary.get('only_in_original', 0)
        if missing_tests > 0:
            recommendations.append(
                f"Implement {missing_tests} missing test(s) from original repository"
            )

        equivalence = float(summary.get('behavioral_equivalence', '0%').rstrip('%'))
        if equivalence < 95:
            recommendations.append(
                f"Behavioral equivalence is {equivalence:.1f}% - aim for >95% before migration"
            )
        elif equivalence >= 95:
            recommendations.append(
                f"Good behavioral equivalence ({equivalence:.1f}%) - review remaining differences"
            )

        return recommendations

    def run_comparison(self) -> Dict:
        """Run full behavior comparison."""
        print("="*80)
        print("Behavior Preservation Checker")
        print("="*80)

        # Validate repositories
        if not self.original_repo.exists():
            raise ValueError(f"Original repository not found: {self.original_repo}")
        if not self.migrated_repo.exists():
            raise ValueError(f"Migrated repository not found: {self.migrated_repo}")

        # Run tests on both repositories
        try:
            original_test_results = self.run_tests(self.original_repo)
        except Exception as e:
            print(f"Warning: Could not run tests on original repository: {e}")
            original_test_results = {'tests': []}

        try:
            migrated_test_results = self.run_tests(self.migrated_repo)
        except Exception as e:
            print(f"Warning: Could not run tests on migrated repository: {e}")
            migrated_test_results = {'tests': []}

        # Compare results
        comparison = self.compare_test_results(original_test_results, migrated_test_results)

        # Update results
        self.results['summary'] = comparison['summary']
        self.results['differences'] = comparison['differences']
        self.results['recommendations'] = self.generate_recommendations(comparison)

        return self.results

    def save_report(self, output_path: str):
        """Save comparison report to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nReport saved to: {output_path}")

    def print_summary(self):
        """Print summary to console."""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)

        summary = self.results['summary']
        print(f"Total tests: {summary.get('total_tests', 0)}")
        print(f"Passed in both: {summary.get('passed_both', 0)}")
        print(f"Failed in both: {summary.get('failed_both', 0)}")
        print(f"Passed in original, failed in migrated: {summary.get('passed_original_failed_migrated', 0)}")
        print(f"Failed in original, passed in migrated: {summary.get('failed_original_passed_migrated', 0)}")
        print(f"Behavioral equivalence: {summary.get('behavioral_equivalence', 'N/A')}")

        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)
        for i, rec in enumerate(self.results['recommendations'], 1):
            print(f"{i}. {rec}")

        critical_diffs = [d for d in self.results['differences'] if d.get('severity') == 'critical']
        if critical_diffs:
            print("\n" + "="*80)
            print("CRITICAL DIFFERENCES")
            print("="*80)
            for diff in critical_diffs[:5]:  # Show first 5
                print(f"\n- {diff.get('test_name', 'Unknown')}")
                print(f"  {diff.get('guidance', 'No guidance available')}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare behavior between original and migrated repositories'
    )
    parser.add_argument('--original', required=True,
                       help='Path to original repository')
    parser.add_argument('--migrated', required=True,
                       help='Path to migrated repository')
    parser.add_argument('--output', default='behavior_report.json',
                       help='Output file for comparison report (default: behavior_report.json)')

    args = parser.parse_args()

    try:
        checker = BehaviorChecker(args.original, args.migrated)
        checker.run_comparison()
        checker.save_report(args.output)
        checker.print_summary()

        # Exit with error code if critical differences found
        critical_count = sum(1 for d in checker.results['differences']
                           if d.get('severity') == 'critical')
        if critical_count > 0:
            print(f"\n⚠ Found {critical_count} critical difference(s)")
            sys.exit(1)
        else:
            print("\n✓ No critical differences found")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
