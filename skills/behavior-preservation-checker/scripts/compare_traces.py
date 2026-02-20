#!/usr/bin/env python3
"""
compare_traces.py - Compare execution traces between two versions

Identifies differences in:
- Function call sequences
- Argument values
- Return values
- Execution paths
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


class TraceComparator:
    """Compare execution traces between original and migrated versions."""

    def __init__(self, original_file: str, migrated_file: str):
        self.original_file = original_file
        self.migrated_file = migrated_file

    def load_traces(self, file_path: str) -> List[Dict]:
        """Load traces from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data.get('traces', [])

    def compare_traces(self) -> Dict:
        """Compare traces and identify differences."""
        print(f"Loading original traces from {self.original_file}...")
        original_traces = self.load_traces(self.original_file)

        print(f"Loading migrated traces from {self.migrated_file}...")
        migrated_traces = self.load_traces(self.migrated_file)

        print(f"Comparing {len(original_traces)} vs {len(migrated_traces)} traces...")

        comparison = {
            'summary': {
                'original_calls': len(original_traces),
                'migrated_calls': len(migrated_traces),
                'call_count_difference': len(migrated_traces) - len(original_traces)
            },
            'differences': [],
            'sequence_similarity': 0.0
        }

        # Compare call sequences
        orig_sequence = [t['function'] for t in original_traces]
        mig_sequence = [t['function'] for t in migrated_traces]

        matcher = SequenceMatcher(None, orig_sequence, mig_sequence)
        comparison['sequence_similarity'] = matcher.ratio()

        # Compare individual calls
        max_len = max(len(original_traces), len(migrated_traces))

        for i in range(max_len):
            orig_trace = original_traces[i] if i < len(original_traces) else None
            mig_trace = migrated_traces[i] if i < len(migrated_traces) else None

            if orig_trace and mig_trace:
                diff = self._compare_single_trace(orig_trace, mig_trace, i)
                if diff:
                    comparison['differences'].append(diff)
            elif orig_trace:
                comparison['differences'].append({
                    'index': i,
                    'type': 'missing_in_migrated',
                    'function': orig_trace['function'],
                    'severity': 'high'
                })
            else:
                comparison['differences'].append({
                    'index': i,
                    'type': 'extra_in_migrated',
                    'function': mig_trace['function'],
                    'severity': 'medium'
                })

        comparison['summary']['total_differences'] = len(comparison['differences'])

        return comparison

    def _compare_single_trace(self, orig: Dict, mig: Dict, index: int) -> Dict:
        """Compare a single trace entry."""
        differences = []

        # Compare function names
        if orig['function'] != mig['function']:
            return {
                'index': index,
                'type': 'function_mismatch',
                'original_function': orig['function'],
                'migrated_function': mig['function'],
                'severity': 'critical'
            }

        # Compare arguments
        if orig.get('args') != mig.get('args'):
            differences.append('args')

        if orig.get('kwargs') != mig.get('kwargs'):
            differences.append('kwargs')

        # Compare return values
        if orig.get('return_value') != mig.get('return_value'):
            differences.append('return_value')

        # Compare status
        if orig.get('status') != mig.get('status'):
            differences.append('status')

        if differences:
            return {
                'index': index,
                'type': 'value_mismatch',
                'function': orig['function'],
                'differences': differences,
                'original': {
                    'args': orig.get('args'),
                    'return_value': orig.get('return_value'),
                    'status': orig.get('status')
                },
                'migrated': {
                    'args': mig.get('args'),
                    'return_value': mig.get('return_value'),
                    'status': mig.get('status')
                },
                'severity': 'high' if 'return_value' in differences else 'medium'
            }

        return None

    def print_report(self, comparison: Dict):
        """Print comparison report to console."""
        print("\n" + "="*80)
        print("EXECUTION TRACE COMPARISON")
        print("="*80)

        summary = comparison['summary']
        print(f"\nOriginal calls: {summary['original_calls']}")
        print(f"Migrated calls: {summary['migrated_calls']}")
        print(f"Call count difference: {summary['call_count_difference']}")
        print(f"Sequence similarity: {comparison['sequence_similarity']:.1%}")
        print(f"Total differences: {summary['total_differences']}")

        # Print critical differences
        critical = [d for d in comparison['differences'] if d.get('severity') == 'critical']
        if critical:
            print("\n" + "="*80)
            print("CRITICAL DIFFERENCES")
            print("="*80)
            for diff in critical[:10]:
                print(f"\nCall #{diff['index']}:")
                print(f"  Type: {diff['type']}")
                if diff['type'] == 'function_mismatch':
                    print(f"  Original: {diff['original_function']}")
                    print(f"  Migrated: {diff['migrated_function']}")

        # Print value mismatches
        value_mismatches = [d for d in comparison['differences']
                           if d.get('type') == 'value_mismatch']
        if value_mismatches:
            print("\n" + "="*80)
            print("VALUE MISMATCHES")
            print("="*80)
            for diff in value_mismatches[:5]:
                print(f"\nCall #{diff['index']}: {diff['function']}")
                print(f"  Differences: {', '.join(diff['differences'])}")
                if 'return_value' in diff['differences']:
                    print(f"  Original return: {diff['original']['return_value']}")
                    print(f"  Migrated return: {diff['migrated']['return_value']}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare execution traces between original and migrated versions'
    )
    parser.add_argument('original', help='Original trace file (JSON)')
    parser.add_argument('migrated', help='Migrated trace file (JSON)')
    parser.add_argument('--output', help='Output file for comparison report (JSON)')
    parser.add_argument('--fail-on-difference', action='store_true',
                       help='Exit with error code if differences found')

    args = parser.parse_args()

    try:
        comparator = TraceComparator(args.original, args.migrated)
        comparison = comparator.compare_traces()
        comparator.print_report(comparison)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(comparison, f, indent=2)
            print(f"\nComparison report saved to: {args.output}")

        # Exit with error if differences found
        if args.fail_on_difference and comparison['summary']['total_differences'] > 0:
            print(f"\n✗ Found {comparison['summary']['total_differences']} difference(s)")
            sys.exit(1)
        else:
            print("\n✓ Trace comparison complete")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
