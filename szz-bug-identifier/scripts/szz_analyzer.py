#!/usr/bin/env python3
"""
SZZ Bug-Introducing Commit Identifier

Identifies bug-introducing commits using SZZ-style analysis based on bug-fixing
commits, commit history, and code blame information.
"""

import subprocess
import sys
import re
import argparse
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import json


@dataclass
class CandidateCommit:
    """Represents a candidate bug-introducing commit"""
    commit_hash: str
    author: str
    date: str
    message: str
    modified_lines: List[int]
    confidence_score: float
    reasons: List[str]


class SZZAnalyzer:
    """Performs SZZ analysis to identify bug-introducing commits"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.false_positive_patterns = [
            r'^\s*$',  # Empty lines
            r'^\s*[{}]\s*$',  # Braces only
            r'^\s*import\s+',  # Import statements
            r'^\s*from\s+.*\s+import\s+',  # From imports
            r'^\s*#',  # Comments
            r'^\s*//',  # C-style comments
            r'^\s*/\*',  # Multi-line comment start
            r'^\s*\*',  # Multi-line comment continuation
            r'^\s*\*/',  # Multi-line comment end
        ]

        self.refactoring_keywords = [
            'refactor', 'rename', 'format', 'style', 'cleanup',
            'reorganize', 'restructure', 'reformat', 'whitespace'
        ]

    def run_git_command(self, command: List[str]) -> str:
        """Execute a git command and return output"""
        try:
            result = subprocess.run(
                ['git', '-C', self.repo_path] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}", file=sys.stderr)
            print(f"stderr: {e.stderr}", file=sys.stderr)
            sys.exit(1)

    def get_commit_info(self, commit_hash: str) -> Dict[str, str]:
        """Get detailed information about a commit"""
        output = self.run_git_command([
            'show', '--no-patch', '--format=%H%n%an%n%ad%n%s%n%b',
            commit_hash
        ])
        lines = output.strip().split('\n')
        return {
            'hash': lines[0] if len(lines) > 0 else '',
            'author': lines[1] if len(lines) > 1 else '',
            'date': lines[2] if len(lines) > 2 else '',
            'subject': lines[3] if len(lines) > 3 else '',
            'body': '\n'.join(lines[4:]) if len(lines) > 4 else ''
        }

    def get_modified_files(self, commit_hash: str) -> List[str]:
        """Get list of files modified in a commit"""
        output = self.run_git_command(['diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash])
        return [f.strip() for f in output.strip().split('\n') if f.strip()]

    def get_deleted_lines(self, commit_hash: str, file_path: str) -> List[Tuple[int, str]]:
        """Get deleted lines from a file in a commit (line_number, content)"""
        output = self.run_git_command([
            'show', f'{commit_hash}^:{file_path}'
        ])

        diff_output = self.run_git_command([
            'diff', f'{commit_hash}^', commit_hash, '--', file_path
        ])

        deleted_lines = []
        current_line = 0

        for line in diff_output.split('\n'):
            if line.startswith('@@'):
                # Parse hunk header: @@ -start,count +start,count @@
                match = re.match(r'@@ -(\d+),?\d* \+\d+,?\d* @@', line)
                if match:
                    current_line = int(match.group(1))
            elif line.startswith('-') and not line.startswith('---'):
                deleted_lines.append((current_line, line[1:]))
                current_line += 1
            elif not line.startswith('+'):
                current_line += 1

        return deleted_lines

    def is_false_positive_line(self, line_content: str) -> bool:
        """Check if a line is likely a false positive (formatting, comments, etc.)"""
        for pattern in self.false_positive_patterns:
            if re.match(pattern, line_content):
                return True
        return False

    def is_refactoring_commit(self, commit_message: str) -> bool:
        """Check if commit message suggests refactoring/formatting"""
        message_lower = commit_message.lower()
        return any(keyword in message_lower for keyword in self.refactoring_keywords)

    def blame_line(self, file_path: str, line_number: int, before_commit: str) -> Dict[str, str]:
        """Use git blame to find the commit that introduced a line"""
        try:
            output = self.run_git_command([
                'blame', '-L', f'{line_number},{line_number}',
                '--porcelain', f'{before_commit}^', '--', file_path
            ])

            lines = output.split('\n')
            if lines:
                commit_hash = lines[0].split()[0]
                return self.get_commit_info(commit_hash)
        except:
            return None

        return None

    def analyze_bug_fix(self, fix_commit_hash: str) -> List[CandidateCommit]:
        """Analyze a bug-fixing commit to find bug-introducing commits"""
        print(f"Analyzing bug-fixing commit: {fix_commit_hash}")

        fix_info = self.get_commit_info(fix_commit_hash)
        print(f"Fix commit: {fix_info['subject']}")

        modified_files = self.get_modified_files(fix_commit_hash)
        print(f"Modified files: {len(modified_files)}")

        candidates = defaultdict(lambda: {
            'info': None,
            'lines': [],
            'reasons': [],
            'is_refactoring': False
        })

        for file_path in modified_files:
            print(f"\nAnalyzing file: {file_path}")
            deleted_lines = self.get_deleted_lines(fix_commit_hash, file_path)
            print(f"  Deleted lines: {len(deleted_lines)}")

            for line_num, line_content in deleted_lines:
                # Skip false positive lines
                if self.is_false_positive_line(line_content):
                    continue

                # Blame the line to find who introduced it
                blame_info = self.blame_line(file_path, line_num, fix_commit_hash)

                if blame_info and blame_info['hash'] != fix_commit_hash:
                    commit_hash = blame_info['hash']
                    candidates[commit_hash]['info'] = blame_info
                    candidates[commit_hash]['lines'].append((file_path, line_num, line_content))

                    # Check if it's a refactoring commit
                    if self.is_refactoring_commit(blame_info['subject']):
                        candidates[commit_hash]['is_refactoring'] = True
                        candidates[commit_hash]['reasons'].append('Refactoring commit (lower confidence)')

        # Convert to CandidateCommit objects and calculate confidence scores
        result = []
        for commit_hash, data in candidates.items():
            if data['info']:
                # Calculate confidence score
                confidence = 1.0
                reasons = []

                # Reduce confidence for refactoring commits
                if data['is_refactoring']:
                    confidence *= 0.3
                    reasons.append('Commit message suggests refactoring/formatting')

                # Increase confidence based on number of lines
                num_lines = len(data['lines'])
                if num_lines > 5:
                    confidence *= 1.2
                    reasons.append(f'Multiple lines modified ({num_lines} lines)')
                elif num_lines == 1:
                    confidence *= 0.8
                    reasons.append('Only one line modified')

                # Add general reason
                reasons.append(f'Introduced {num_lines} line(s) that were removed in the fix')

                result.append(CandidateCommit(
                    commit_hash=commit_hash,
                    author=data['info']['author'],
                    date=data['info']['date'],
                    message=data['info']['subject'],
                    modified_lines=[line_num for _, line_num, _ in data['lines']],
                    confidence_score=min(confidence, 1.0),
                    reasons=reasons
                ))

        # Sort by confidence score (descending)
        result.sort(key=lambda x: x.confidence_score, reverse=True)

        return result


def main():
    parser = argparse.ArgumentParser(
        description='Identify bug-introducing commits using SZZ analysis'
    )
    parser.add_argument(
        'fix_commit',
        help='The bug-fixing commit hash'
    )
    parser.add_argument(
        '--repo',
        default='.',
        help='Path to git repository (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Number of top candidates to show (default: 10)'
    )

    args = parser.parse_args()

    analyzer = SZZAnalyzer(args.repo)
    candidates = analyzer.analyze_bug_fix(args.fix_commit)

    if args.json:
        # JSON output
        output = []
        for candidate in candidates[:args.top]:
            output.append({
                'commit_hash': candidate.commit_hash,
                'author': candidate.author,
                'date': candidate.date,
                'message': candidate.message,
                'confidence_score': candidate.confidence_score,
                'reasons': candidate.reasons
            })
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print("\n" + "="*80)
        print("BUG-INTRODUCING COMMIT CANDIDATES")
        print("="*80)

        for i, candidate in enumerate(candidates[:args.top], 1):
            print(f"\n#{i} - Confidence: {candidate.confidence_score:.2f}")
            print(f"Commit: {candidate.commit_hash[:8]}")
            print(f"Author: {candidate.author}")
            print(f"Date: {candidate.date}")
            print(f"Message: {candidate.message}")
            print(f"Reasons:")
            for reason in candidate.reasons:
                print(f"  - {reason}")

        if not candidates:
            print("\nNo bug-introducing commit candidates found.")

        print("\n" + "="*80)


if __name__ == '__main__':
    main()
