#!/usr/bin/env python3
"""
Semantic SZZ Analyzer - Main script for identifying bug-introducing commits
using semantic analysis to reduce false positives.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from semantic_analyzer import SemanticAnalyzer


class SemanticSZZ:
    def __init__(self, repo_path: str, threshold: float = 0.7):
        self.repo_path = Path(repo_path)
        self.threshold = threshold
        self.analyzer = SemanticAnalyzer(threshold)

    def get_changed_lines(self, commit_hash: str) -> Dict[str, List[Tuple[int, int]]]:
        """Extract changed line ranges from a commit."""
        cmd = ['git', '-C', str(self.repo_path), 'show', '--unified=0',
               '--no-prefix', commit_hash]
        result = subprocess.run(cmd, capture_output=True, text=True)

        changed_lines = {}
        current_file = None

        for line in result.stdout.split('\n'):
            if line.startswith('---') or line.startswith('+++'):
                if line.startswith('+++'):
                    current_file = line[4:].strip()
                    if current_file != '/dev/null':
                        changed_lines[current_file] = []
            elif line.startswith('@@'):
                # Parse @@ -start,count +start,count @@
                parts = line.split('@@')[1].strip().split()
                if len(parts) >= 2:
                    # Extract the + side (new file)
                    plus_part = parts[1] if parts[1].startswith('+') else parts[0]
                    if ',' in plus_part:
                        start, count = plus_part[1:].split(',')
                        start, count = int(start), int(count)
                    else:
                        start = int(plus_part[1:])
                        count = 1

                    if current_file and current_file in changed_lines:
                        changed_lines[current_file].append((start, start + count - 1))

        return changed_lines

    def find_candidate_commits(self, file_path: str, line_ranges: List[Tuple[int, int]],
                               fix_commit: str) -> List[str]:
        """Use git blame to find commits that last modified the given lines."""
        candidates = set()

        for start, end in line_ranges:
            cmd = ['git', '-C', str(self.repo_path), 'blame', '-L',
                   f'{start},{end}', f'{fix_commit}^', '--', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)

            for line in result.stdout.split('\n'):
                if line.strip():
                    # Extract commit hash (first field)
                    commit = line.split()[0]
                    if commit.startswith('^'):
                        commit = commit[1:]
                    candidates.add(commit)

        return list(candidates)

    def analyze_fix_commit(self, fix_commit: str, explain: bool = False) -> Dict:
        """Main analysis function for a bug-fix commit."""
        print(f"Analyzing fix commit: {fix_commit}")

        # Step 1: Get changed lines from fix commit
        changed_lines = self.get_changed_lines(fix_commit)
        print(f"Found changes in {len(changed_lines)} files")

        # Step 2: Find candidate commits for each file
        all_candidates = {}
        for file_path, line_ranges in changed_lines.items():
            candidates = self.find_candidate_commits(file_path, line_ranges, fix_commit)
            all_candidates[file_path] = candidates
            print(f"  {file_path}: {len(candidates)} candidate commits")

        # Step 3: Apply semantic analysis
        bug_introducing_commits = []

        for file_path, candidates in all_candidates.items():
            for candidate in candidates:
                print(f"Analyzing candidate: {candidate}")

                # Get file content at candidate and fix commits
                result = self.analyzer.analyze_commit_pair(
                    self.repo_path, file_path, candidate, fix_commit
                )

                if result['is_bug_introducing']:
                    result['file'] = file_path
                    result['commit'] = candidate
                    bug_introducing_commits.append(result)

        # Step 4: Rank by confidence
        bug_introducing_commits.sort(key=lambda x: x['confidence'], reverse=True)

        output = {
            'fix_commit': fix_commit,
            'files_analyzed': len(changed_lines),
            'candidates_analyzed': sum(len(c) for c in all_candidates.values()),
            'bug_introducing_commits': bug_introducing_commits
        }

        return output


def main():
    parser = argparse.ArgumentParser(
        description='Semantic SZZ: Identify bug-introducing commits with semantic analysis'
    )
    parser.add_argument('--repo', required=True, help='Path to git repository')
    parser.add_argument('--fix-commit', required=True, help='Bug-fix commit hash')
    parser.add_argument('--threshold', type=float, default=0.7,
                       help='Semantic similarity threshold (default: 0.7)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--explain', action='store_true',
                       help='Generate detailed explanations')

    args = parser.parse_args()

    # Validate repository
    if not Path(args.repo).is_dir():
        print(f"Error: Repository path does not exist: {args.repo}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    szz = SemanticSZZ(args.repo, args.threshold)
    results = szz.analyze_fix_commit(args.fix_commit, args.explain)

    # Output results
    output_json = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"\nResults written to: {args.output}")
    else:
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        print(output_json)

    # Summary
    print(f"\nSummary:")
    print(f"  Fix commit: {results['fix_commit']}")
    print(f"  Files analyzed: {results['files_analyzed']}")
    print(f"  Candidates analyzed: {results['candidates_analyzed']}")
    print(f"  Bug-introducing commits found: {len(results['bug_introducing_commits'])}")

    for bic in results['bug_introducing_commits']:
        print(f"\n  Commit: {bic['commit']}")
        print(f"    File: {bic['file']}")
        print(f"    Confidence: {bic['confidence']:.2f}")
        print(f"    Change type: {bic['semantic_change_type']}")


if __name__ == '__main__':
    main()
