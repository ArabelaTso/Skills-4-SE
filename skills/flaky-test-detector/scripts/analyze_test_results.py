#!/usr/bin/env python3
"""
Analyze test execution history to identify flaky tests.

This script analyzes test results from multiple runs to identify tests
that have inconsistent pass/fail behavior, indicating flakiness.

Usage:
    python analyze_test_results.py <test_results_file>

Input format (JSON):
    [
        {
            "test_name": "test_example",
            "status": "passed",  # or "failed"
            "timestamp": "2024-01-01T10:00:00",
            "duration": 1.23
        },
        ...
    ]

Output:
    - List of flaky tests with statistics
    - Flakiness score (0-1, higher = more flaky)
    - Pass/fail pattern
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple


def analyze_test_results(results: List[Dict]) -> Dict:
    """
    Analyze test results to identify flaky tests.

    Args:
        results: List of test result dictionaries

    Returns:
        Dictionary mapping test names to flakiness statistics
    """
    test_stats = defaultdict(lambda: {
        'total_runs': 0,
        'passes': 0,
        'failures': 0,
        'results': [],
        'durations': []
    })

    # Aggregate results by test name
    for result in results:
        test_name = result['test_name']
        status = result['status']
        duration = result.get('duration', 0)

        test_stats[test_name]['total_runs'] += 1
        test_stats[test_name]['results'].append(status)
        test_stats[test_name]['durations'].append(duration)

        if status == 'passed':
            test_stats[test_name]['passes'] += 1
        else:
            test_stats[test_name]['failures'] += 1

    # Calculate flakiness metrics
    flaky_tests = {}
    for test_name, stats in test_stats.items():
        if stats['total_runs'] < 2:
            continue  # Need multiple runs to detect flakiness

        # Calculate flakiness score
        pass_rate = stats['passes'] / stats['total_runs']

        # Flaky if pass rate is between 10% and 90%
        if 0.1 < pass_rate < 0.9:
            flakiness_score = 1 - abs(pass_rate - 0.5) * 2

            # Check for alternating pattern
            has_alternating = has_alternating_pattern(stats['results'])

            # Calculate duration variance
            duration_variance = calculate_variance(stats['durations'])

            flaky_tests[test_name] = {
                'total_runs': stats['total_runs'],
                'passes': stats['passes'],
                'failures': stats['failures'],
                'pass_rate': pass_rate,
                'flakiness_score': flakiness_score,
                'has_alternating_pattern': has_alternating,
                'duration_variance': duration_variance,
                'pattern': ''.join(['P' if r == 'passed' else 'F' for r in stats['results'][-10:]])
            }

    return flaky_tests


def has_alternating_pattern(results: List[str]) -> bool:
    """Check if results show alternating pass/fail pattern."""
    if len(results) < 3:
        return False

    alternations = 0
    for i in range(len(results) - 1):
        if results[i] != results[i + 1]:
            alternations += 1

    # Consider alternating if more than 50% of transitions are changes
    return alternations / (len(results) - 1) > 0.5


def calculate_variance(values: List[float]) -> float:
    """Calculate variance of duration values."""
    if len(values) < 2:
        return 0.0

    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance


def print_flaky_tests(flaky_tests: Dict):
    """Print flaky test report."""
    if not flaky_tests:
        print("No flaky tests detected!")
        return

    print(f"\n{'='*80}")
    print(f"FLAKY TEST REPORT - {len(flaky_tests)} flaky tests detected")
    print(f"{'='*80}\n")

    # Sort by flakiness score (highest first)
    sorted_tests = sorted(
        flaky_tests.items(),
        key=lambda x: x[1]['flakiness_score'],
        reverse=True
    )

    for test_name, stats in sorted_tests:
        print(f"Test: {test_name}")
        print(f"  Flakiness Score: {stats['flakiness_score']:.2f}")
        print(f"  Pass Rate: {stats['pass_rate']:.1%} ({stats['passes']}/{stats['total_runs']})")
        print(f"  Pattern (last 10): {stats['pattern']}")
        print(f"  Alternating: {'Yes' if stats['has_alternating_pattern'] else 'No'}")
        print(f"  Duration Variance: {stats['duration_variance']:.3f}s²")
        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_test_results.py <test_results_file>")
        sys.exit(1)

    results_file = sys.argv[1]

    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{results_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{results_file}'")
        sys.exit(1)

    flaky_tests = analyze_test_results(results)
    print_flaky_tests(flaky_tests)

    # Exit with error code if flaky tests found
    sys.exit(1 if flaky_tests else 0)


if __name__ == '__main__':
    main()
