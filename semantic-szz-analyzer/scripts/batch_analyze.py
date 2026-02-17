#!/usr/bin/env python3
"""
Batch Analyzer - Process multiple bug-fix commits in batch mode.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List
from semantic_szz import SemanticSZZ


def read_fixes_file(file_path: str) -> List[str]:
    """Read bug-fix commit hashes from a file (one per line)."""
    with open(file_path, 'r') as f:
        commits = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return commits


def batch_analyze(repo_path: str, fix_commits: List[str],
                  threshold: float = 0.7, output_dir: str = None) -> Dict:
    """Analyze multiple bug-fix commits."""
    szz = SemanticSZZ(repo_path, threshold)

    all_results = {
        'repository': repo_path,
        'threshold': threshold,
        'total_fixes': len(fix_commits),
        'results': []
    }

    for i, fix_commit in enumerate(fix_commits, 1):
        print(f"\n{'='*80}")
        print(f"Processing {i}/{len(fix_commits)}: {fix_commit}")
        print('='*80)

        try:
            result = szz.analyze_fix_commit(fix_commit, explain=True)
            all_results['results'].append(result)

            # Save individual result if output directory specified
            if output_dir:
                output_path = Path(output_dir) / f"{fix_commit}.json"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)

        except Exception as e:
            print(f"Error processing {fix_commit}: {e}", file=sys.stderr)
            all_results['results'].append({
                'fix_commit': fix_commit,
                'error': str(e)
            })

    return all_results


def generate_summary(results: Dict) -> str:
    """Generate summary statistics from batch results."""
    total_fixes = results['total_fixes']
    successful = sum(1 for r in results['results'] if 'error' not in r)
    failed = total_fixes - successful

    total_bics = sum(len(r.get('bug_introducing_commits', []))
                     for r in results['results'] if 'error' not in r)

    avg_bics = total_bics / successful if successful > 0 else 0

    summary = f"""
Batch Analysis Summary
{'='*80}
Repository: {results['repository']}
Threshold: {results['threshold']}

Fixes Analyzed: {total_fixes}
  Successful: {successful}
  Failed: {failed}

Bug-Introducing Commits Found: {total_bics}
  Average per fix: {avg_bics:.2f}

Top Bug-Introducing Commits:
"""

    # Collect all BICs with their frequency
    bic_frequency = {}
    for result in results['results']:
        if 'error' not in result:
            for bic in result.get('bug_introducing_commits', []):
                commit = bic['commit']
                if commit not in bic_frequency:
                    bic_frequency[commit] = {
                        'count': 0,
                        'avg_confidence': 0.0,
                        'files': set()
                    }
                bic_frequency[commit]['count'] += 1
                bic_frequency[commit]['avg_confidence'] += bic['confidence']
                bic_frequency[commit]['files'].add(bic.get('file', 'unknown'))

    # Calculate averages and sort by frequency
    for commit, data in bic_frequency.items():
        data['avg_confidence'] /= data['count']
        data['files'] = list(data['files'])

    sorted_bics = sorted(bic_frequency.items(),
                        key=lambda x: x[1]['count'],
                        reverse=True)[:10]

    for commit, data in sorted_bics:
        summary += f"\n  {commit[:8]}: {data['count']} fixes, "
        summary += f"confidence: {data['avg_confidence']:.2f}, "
        summary += f"files: {len(data['files'])}"

    return summary


def main():
    parser = argparse.ArgumentParser(
        description='Batch analysis of multiple bug-fix commits'
    )
    parser.add_argument('--repo', required=True, help='Path to git repository')
    parser.add_argument('--fixes-file', required=True,
                       help='File containing bug-fix commit hashes (one per line)')
    parser.add_argument('--threshold', type=float, default=0.7,
                       help='Semantic similarity threshold (default: 0.7)')
    parser.add_argument('--output', help='Output JSON file for combined results')
    parser.add_argument('--output-dir', help='Directory for individual result files')

    args = parser.parse_args()

    # Validate inputs
    if not Path(args.repo).is_dir():
        print(f"Error: Repository path does not exist: {args.repo}", file=sys.stderr)
        sys.exit(1)

    if not Path(args.fixes_file).is_file():
        print(f"Error: Fixes file does not exist: {args.fixes_file}", file=sys.stderr)
        sys.exit(1)

    # Read fix commits
    fix_commits = read_fixes_file(args.fixes_file)
    print(f"Loaded {len(fix_commits)} bug-fix commits from {args.fixes_file}")

    # Run batch analysis
    results = batch_analyze(args.repo, fix_commits, args.threshold, args.output_dir)

    # Save combined results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nCombined results written to: {args.output}")

    # Print summary
    summary = generate_summary(results)
    print(summary)

    # Save summary
    if args.output:
        summary_path = Path(args.output).with_suffix('.summary.txt')
        with open(summary_path, 'w') as f:
            f.write(summary)
        print(f"Summary written to: {summary_path}")


if __name__ == '__main__':
    main()
