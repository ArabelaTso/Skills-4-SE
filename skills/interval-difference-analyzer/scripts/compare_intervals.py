#!/usr/bin/env python3
"""
compare_intervals.py - Compare intervals between two program versions

Identifies:
- Added intervals (new variables)
- Removed intervals (deleted variables)
- Modified intervals (changed bounds)
- Behavioral implications
- Testing recommendations
"""

import argparse
import json
import sys
from typing import Dict, List, Set


class IntervalComparator:
    """Compare intervals between two program versions."""

    def __init__(self, old_file: str, new_file: str):
        self.old_file = old_file
        self.new_file = new_file

    def load_intervals(self, file_path: str) -> Dict:
        """Load intervals from JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def compare(self) -> Dict:
        """Compare intervals and generate report."""
        print(f"Loading old intervals from {self.old_file}...")
        old_data = self.load_intervals(self.old_file)
        old_intervals = old_data.get('intervals', {})

        print(f"Loading new intervals from {self.new_file}...")
        new_data = self.load_intervals(self.new_file)
        new_intervals = new_data.get('intervals', {})

        print(f"Comparing {len(old_intervals)} vs {len(new_intervals)} intervals...")

        # Identify differences
        old_vars = set(old_intervals.keys())
        new_vars = set(new_intervals.keys())

        added_vars = new_vars - old_vars
        removed_vars = old_vars - new_vars
        common_vars = old_vars & new_vars

        differences = []

        # Check added intervals
        for var in added_vars:
            differences.append({
                'type': 'added',
                'variable': var,
                'new_interval': new_intervals[var]['range'],
                'severity': self._assess_severity_added(new_intervals[var]),
                'implications': self._get_implications_added(var, new_intervals[var]),
                'testing_priority': 'medium'
            })

        # Check removed intervals
        for var in removed_vars:
            differences.append({
                'type': 'removed',
                'variable': var,
                'old_interval': old_intervals[var]['range'],
                'severity': 'low',
                'implications': ['Variable removed or renamed'],
                'testing_priority': 'low'
            })

        # Check modified intervals
        for var in common_vars:
            old_int = old_intervals[var]
            new_int = new_intervals[var]

            if old_int['min'] != new_int['min'] or old_int['max'] != new_int['max']:
                diff = self._analyze_modification(var, old_int, new_int)
                differences.append(diff)

        # Generate summary
        summary = {
            'old_version': old_data.get('program', 'unknown'),
            'new_version': new_data.get('program', 'unknown'),
            'total_intervals_old': len(old_intervals),
            'total_intervals_new': len(new_intervals),
            'added_intervals': len(added_vars),
            'removed_intervals': len(removed_vars),
            'modified_intervals': sum(1 for d in differences if d['type'] == 'modified'),
            'unchanged_intervals': len(common_vars) - sum(1 for d in differences if d['type'] == 'modified')
        }

        # Generate recommendations
        recommendations = self._generate_recommendations(differences)

        return {
            'summary': summary,
            'differences': differences,
            'recommendations': recommendations
        }

    def _assess_severity_added(self, interval: Dict) -> str:
        """Assess severity of added interval."""
        min_val = interval['min']
        max_val = interval['max']

        # Check for potential issues
        if min_val < 0:
            return 'high'  # Negative values may cause issues
        elif max_val > 1000000:
            return 'medium'  # Large values may cause overflow
        else:
            return 'low'

    def _get_implications_added(self, var: str, interval: Dict) -> List[str]:
        """Get implications of added interval."""
        implications = ['New variable introduced']

        min_val = interval['min']
        max_val = interval['max']

        if min_val < 0:
            implications.append('Accepts negative values')
        if max_val > 1000000:
            implications.append('Large values possible - check for overflow')

        return implications

    def _analyze_modification(self, var: str, old_int: Dict, new_int: Dict) -> Dict:
        """Analyze modified interval."""
        old_min, old_max = old_int['min'], old_int['max']
        new_min, new_max = new_int['min'], new_int['max']

        # Determine type of modification
        widened = new_min < old_min or new_max > old_max
        narrowed = new_min > old_min or new_max < old_max

        # Assess severity
        severity = self._assess_modification_severity(old_int, new_int, widened, narrowed)

        # Get implications
        implications = self._get_modification_implications(
            var, old_min, old_max, new_min, new_max, widened, narrowed
        )

        # Generate test suggestions
        suggested_tests = self._generate_test_values(old_int, new_int)

        # Determine testing priority
        testing_priority = 'critical' if severity == 'critical' else \
                          'high' if severity == 'high' else \
                          'medium' if widened else 'low'

        return {
            'type': 'modified',
            'variable': var,
            'old_interval': old_int['range'],
            'new_interval': new_int['range'],
            'change': 'widened' if widened else 'narrowed' if narrowed else 'shifted',
            'severity': severity,
            'implications': implications,
            'testing_priority': testing_priority,
            'suggested_tests': suggested_tests
        }

    def _assess_modification_severity(self, old_int: Dict, new_int: Dict,
                                      widened: bool, narrowed: bool) -> str:
        """Assess severity of interval modification."""
        old_min, old_max = old_int['min'], old_int['max']
        new_min, new_max = new_int['min'], new_int['max']

        # Critical: Negative index possible
        if old_min >= 0 and new_min < 0:
            return 'critical'

        # Critical: Overflow risk (assuming int32)
        if new_max > 2147483647 and old_max <= 2147483647:
            return 'critical'

        # High: Significant widening
        if widened:
            old_range = old_max - old_min
            new_range = new_max - new_min
            if new_range > old_range * 2:
                return 'high'

        # Medium: Moderate changes
        if widened or (new_min < old_min or new_max > old_max):
            return 'medium'

        # Low: Narrowing (generally safer)
        return 'low'

    def _get_modification_implications(self, var: str, old_min: float, old_max: float,
                                      new_min: float, new_max: float,
                                      widened: bool, narrowed: bool) -> List[str]:
        """Get implications of interval modification."""
        implications = []

        if new_min < old_min:
            implications.append(f'Lower bound decreased: {old_min} → {new_min}')
            if old_min >= 0 and new_min < 0:
                implications.append('WARNING: Now accepts negative values')

        if new_max > old_max:
            implications.append(f'Upper bound increased: {old_max} → {new_max}')
            if new_max > 2147483647:
                implications.append('WARNING: Potential overflow (exceeds int32)')

        if widened:
            implications.append('Accepts wider range of values')
            implications.append('May accept previously invalid inputs')

        if narrowed:
            implications.append('Accepts narrower range of values')
            implications.append('More restrictive - generally safer')

        return implications

    def _generate_test_values(self, old_int: Dict, new_int: Dict) -> List:
        """Generate test values for modified interval."""
        old_min, old_max = old_int['min'], old_int['max']
        new_min, new_max = new_int['min'], new_int['max']

        test_values = []

        # Test new boundaries
        if new_min < old_min:
            test_values.extend([new_min, new_min + 1, old_min - 1])

        if new_max > old_max:
            test_values.extend([old_max + 1, (old_max + new_max) // 2, new_max - 1, new_max])

        # Always test boundaries
        test_values.extend([new_min, new_max])

        # Remove duplicates and sort
        test_values = sorted(list(set(test_values)))

        return test_values

    def _generate_recommendations(self, differences: List[Dict]) -> List[str]:
        """Generate testing recommendations."""
        recommendations = []

        critical_count = sum(1 for d in differences if d.get('severity') == 'critical')
        high_count = sum(1 for d in differences if d.get('severity') == 'high')
        modified_count = sum(1 for d in differences if d['type'] == 'modified')

        if critical_count > 0:
            recommendations.append(
                f'CRITICAL: {critical_count} interval(s) with critical changes - test immediately'
            )

        if high_count > 0:
            recommendations.append(
                f'Test {high_count} high-severity interval change(s) with boundary values'
            )

        if modified_count > 0:
            recommendations.append(
                f'Review {modified_count} modified interval(s) for correctness'
            )

        recommendations.append('Generate tests for all modified interval boundaries')
        recommendations.append('Verify no overflow/underflow in calculations')

        return recommendations

    def print_report(self, report: Dict):
        """Print comparison report to console."""
        print("\n" + "="*80)
        print("INTERVAL DIFFERENCE REPORT")
        print("="*80)

        summary = report['summary']
        print(f"\nOld version: {summary['old_version']}")
        print(f"New version: {summary['new_version']}")
        print(f"\nTotal intervals (old): {summary['total_intervals_old']}")
        print(f"Total intervals (new): {summary['total_intervals_new']}")
        print(f"Added: {summary['added_intervals']}")
        print(f"Removed: {summary['removed_intervals']}")
        print(f"Modified: {summary['modified_intervals']}")
        print(f"Unchanged: {summary['unchanged_intervals']}")

        # Print critical differences
        critical = [d for d in report['differences'] if d.get('severity') == 'critical']
        if critical:
            print("\n" + "="*80)
            print("CRITICAL DIFFERENCES")
            print("="*80)
            for diff in critical:
                print(f"\n✗ {diff['variable']}")
                print(f"  Type: {diff['type']}")
                if diff['type'] == 'modified':
                    print(f"  Old: {diff['old_interval']}")
                    print(f"  New: {diff['new_interval']}")
                print(f"  Implications:")
                for imp in diff['implications']:
                    print(f"    - {imp}")

        # Print recommendations
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare intervals between two program versions'
    )
    parser.add_argument('--old', required=True,
                       help='Old intervals JSON file')
    parser.add_argument('--new', required=True,
                       help='New intervals JSON file')
    parser.add_argument('--output', required=True,
                       help='Output file for comparison report')

    args = parser.parse_args()

    try:
        comparator = IntervalComparator(args.old, args.new)
        report = comparator.compare()
        comparator.print_report(report)

        # Save report
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to: {args.output}")

        # Exit with error if critical differences found
        critical_count = sum(1 for d in report['differences']
                           if d.get('severity') == 'critical')
        if critical_count > 0:
            print(f"\n⚠ Found {critical_count} critical difference(s)")
            sys.exit(1)
        else:
            print("\n✓ Comparison complete")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
