#!/usr/bin/env python3
"""
Analyze coverage data to identify code elements that can be safely removed.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple


def load_coverage_data(coverage_file: Path) -> Dict:
    """Load coverage data from JSON file."""
    with open(coverage_file) as f:
        return json.load(f)


def analyze_python_coverage(coverage_data: Dict) -> Dict[str, List[str]]:
    """Analyze Python coverage data (pytest-cov JSON format)."""
    results = {
        'uncovered_files': [],
        'partially_covered_files': [],
        'uncovered_lines_by_file': {},
        'coverage_summary': {}
    }

    files = coverage_data.get('files', {})

    for filepath, info in files.items():
        executed_lines = set(info.get('executed_lines', []))
        missing_lines = set(info.get('missing_lines', []))
        total_lines = len(executed_lines) + len(missing_lines)

        if total_lines == 0:
            continue

        coverage_pct = (len(executed_lines) / total_lines) * 100

        results['coverage_summary'][filepath] = {
            'coverage': coverage_pct,
            'executed': len(executed_lines),
            'missing': len(missing_lines),
            'total': total_lines
        }

        if coverage_pct == 0:
            results['uncovered_files'].append(filepath)
        elif coverage_pct < 100:
            results['partially_covered_files'].append(filepath)
            results['uncovered_lines_by_file'][filepath] = sorted(missing_lines)

    return results


def analyze_javascript_coverage(coverage_data: Dict) -> Dict[str, List[str]]:
    """Analyze JavaScript coverage data (Jest/Istanbul JSON format)."""
    results = {
        'uncovered_files': [],
        'partially_covered_files': [],
        'uncovered_lines_by_file': {},
        'coverage_summary': {}
    }

    for filepath, info in coverage_data.items():
        if filepath.startswith('jest-') or filepath == 'total':
            continue

        line_coverage = info.get('lines', {})
        covered = line_coverage.get('covered', 0)
        total = line_coverage.get('total', 0)

        if total == 0:
            continue

        coverage_pct = (covered / total) * 100

        results['coverage_summary'][filepath] = {
            'coverage': coverage_pct,
            'covered': covered,
            'total': total
        }

        if coverage_pct == 0:
            results['uncovered_files'].append(filepath)
        elif coverage_pct < 100:
            results['partially_covered_files'].append(filepath)

            # Extract uncovered line numbers
            line_details = info.get('statementMap', {})
            uncovered = []
            for line_num, count in info.get('s', {}).items():
                if count == 0 and line_num in line_details:
                    start_line = line_details[line_num]['start']['line']
                    uncovered.append(start_line)

            if uncovered:
                results['uncovered_lines_by_file'][filepath] = sorted(set(uncovered))

    return results


def generate_removal_candidates(analysis: Dict) -> List[Dict]:
    """Generate list of removal candidates with safety ratings."""
    candidates = []

    # Uncovered files - safest to remove
    for filepath in analysis['uncovered_files']:
        candidates.append({
            'type': 'file',
            'location': filepath,
            'safety': 'high',
            'reason': 'Zero coverage - file never executed by tests',
            'action': 'Remove entire file'
        })

    # Partially covered files - need manual review
    for filepath in analysis['partially_covered_files']:
        uncovered_lines = analysis['uncovered_lines_by_file'].get(filepath, [])
        if uncovered_lines:
            candidates.append({
                'type': 'lines',
                'location': filepath,
                'lines': uncovered_lines,
                'safety': 'medium',
                'reason': f'{len(uncovered_lines)} uncovered lines',
                'action': 'Review and remove uncovered functions/branches'
            })

    return candidates


def print_report(analysis: Dict, candidates: List[Dict]):
    """Print analysis report."""
    print("=" * 80)
    print("TEST-GUIDED DEBLOATING ANALYSIS REPORT")
    print("=" * 80)
    print()

    # Summary
    total_files = len(analysis['coverage_summary'])
    uncovered_files = len(analysis['uncovered_files'])
    partially_covered = len(analysis['partially_covered_files'])
    fully_covered = total_files - uncovered_files - partially_covered

    print(f"Total files analyzed: {total_files}")
    print(f"  Fully covered (100%): {fully_covered}")
    print(f"  Partially covered: {partially_covered}")
    print(f"  Uncovered (0%): {uncovered_files}")
    print()

    # Uncovered files
    if analysis['uncovered_files']:
        print("UNCOVERED FILES (Safe to remove):")
        print("-" * 80)
        for filepath in sorted(analysis['uncovered_files']):
            print(f"  ❌ {filepath}")
        print()

    # Partially covered files
    if analysis['partially_covered_files']:
        print("PARTIALLY COVERED FILES (Review required):")
        print("-" * 80)
        for filepath in sorted(analysis['partially_covered_files']):
            info = analysis['coverage_summary'][filepath]
            coverage = info['coverage']
            uncovered_lines = analysis['uncovered_lines_by_file'].get(filepath, [])
            print(f"  ⚠️  {filepath} ({coverage:.1f}% coverage)")
            if uncovered_lines:
                line_ranges = format_line_ranges(uncovered_lines)
                print(f"      Uncovered lines: {line_ranges}")
        print()

    # Removal candidates
    print("REMOVAL CANDIDATES:")
    print("-" * 80)
    high_safety = [c for c in candidates if c['safety'] == 'high']
    medium_safety = [c for c in candidates if c['safety'] == 'medium']

    if high_safety:
        print(f"\nHigh Safety ({len(high_safety)} candidates):")
        for candidate in high_safety:
            print(f"  🟢 {candidate['location']}")
            print(f"     Reason: {candidate['reason']}")
            print(f"     Action: {candidate['action']}")

    if medium_safety:
        print(f"\nMedium Safety ({len(medium_safety)} candidates - manual review needed):")
        for candidate in medium_safety:
            print(f"  🟡 {candidate['location']}")
            print(f"     Reason: {candidate['reason']}")
            print(f"     Action: {candidate['action']}")

    print()
    print("=" * 80)


def format_line_ranges(lines: List[int]) -> str:
    """Format line numbers into ranges (e.g., '1-5, 10, 15-20')."""
    if not lines:
        return ""

    ranges = []
    start = lines[0]
    end = lines[0]

    for line in lines[1:]:
        if line == end + 1:
            end = line
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = line
            end = line

    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ", ".join(ranges)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze test coverage to identify code for removal'
    )
    parser.add_argument(
        'coverage_file',
        type=Path,
        help='Path to coverage JSON file (coverage.json or coverage-final.json)'
    )
    parser.add_argument(
        '--format',
        choices=['python', 'javascript', 'auto'],
        default='auto',
        help='Coverage data format (default: auto-detect)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file for removal candidates JSON'
    )

    args = parser.parse_args()

    if not args.coverage_file.exists():
        print(f"Error: Coverage file not found: {args.coverage_file}", file=sys.stderr)
        return 1

    # Load coverage data
    coverage_data = load_coverage_data(args.coverage_file)

    # Auto-detect format
    format_type = args.format
    if format_type == 'auto':
        if 'files' in coverage_data:
            format_type = 'python'
        else:
            format_type = 'javascript'

    # Analyze coverage
    if format_type == 'python':
        analysis = analyze_python_coverage(coverage_data)
    else:
        analysis = analyze_javascript_coverage(coverage_data)

    # Generate removal candidates
    candidates = generate_removal_candidates(analysis)

    # Print report
    print_report(analysis, candidates)

    # Save candidates to file if requested
    if args.output:
        output_data = {
            'analysis': analysis,
            'candidates': candidates
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nDetailed analysis saved to: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
