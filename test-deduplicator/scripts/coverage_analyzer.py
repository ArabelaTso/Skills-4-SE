#!/usr/bin/env python3
"""
Test Deduplicator - Coverage-Based Analysis

Analyzes test coverage to identify tests with overlapping or identical coverage patterns.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import subprocess


class CoverageAnalyzer:
    """Analyzes test coverage to find redundant tests"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.test_coverage = {}  # test_name -> set of covered lines
        self.coverage_data = {}

    def run_coverage_for_test(self, test_command: str, test_name: str) -> Set[Tuple[str, int]]:
        """Run a single test with coverage and return covered lines"""
        try:
            # Run test with coverage
            result = subprocess.run(
                test_command.split(),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            # Parse coverage data (assuming coverage.py JSON format)
            coverage_file = self.repo_path / '.coverage'
            if coverage_file.exists():
                # Convert to JSON format
                subprocess.run(
                    ['coverage', 'json', '-o', 'coverage.json'],
                    cwd=self.repo_path,
                    capture_output=True
                )

                with open(self.repo_path / 'coverage.json', 'r') as f:
                    data = json.load(f)

                covered_lines = set()
                for file_path, file_data in data.get('files', {}).items():
                    executed_lines = file_data.get('executed_lines', [])
                    for line in executed_lines:
                        covered_lines.add((file_path, line))

                return covered_lines

        except Exception as e:
            print(f"Error running coverage for {test_name}: {e}", file=sys.stderr)

        return set()

    def load_coverage_data(self, coverage_file: Path):
        """Load pre-computed coverage data from JSON file"""
        with open(coverage_file, 'r') as f:
            data = json.load(f)

        self.coverage_data = data
        for test_name, test_data in data.items():
            covered_lines = set()
            for file_path, lines in test_data.get('coverage', {}).items():
                for line in lines:
                    covered_lines.add((file_path, line))
            self.test_coverage[test_name] = covered_lines

    def calculate_coverage_similarity(self, test1: str, test2: str) -> float:
        """Calculate Jaccard similarity between two tests' coverage"""
        cov1 = self.test_coverage.get(test1, set())
        cov2 = self.test_coverage.get(test2, set())

        if not cov1 and not cov2:
            return 0.0

        intersection = len(cov1 & cov2)
        union = len(cov1 | cov2)

        return intersection / union if union > 0 else 0.0

    def find_subsumed_tests(self) -> List[Tuple[str, str, float]]:
        """Find tests where one test's coverage is a subset of another"""
        subsumed = []

        test_names = list(self.test_coverage.keys())
        for i, test1 in enumerate(test_names):
            for test2 in test_names[i+1:]:
                cov1 = self.test_coverage[test1]
                cov2 = self.test_coverage[test2]

                # Check if test1 is subsumed by test2
                if cov1.issubset(cov2) and cov1:
                    overlap = len(cov1) / len(cov2) if cov2 else 0
                    subsumed.append((test1, test2, overlap))

                # Check if test2 is subsumed by test1
                elif cov2.issubset(cov1) and cov2:
                    overlap = len(cov2) / len(cov1) if cov1 else 0
                    subsumed.append((test2, test1, overlap))

        return subsumed

    def find_identical_coverage(self, threshold: float = 1.0) -> List[List[str]]:
        """Find groups of tests with identical or near-identical coverage"""
        groups = []
        processed = set()

        test_names = list(self.test_coverage.keys())
        for i, test1 in enumerate(test_names):
            if test1 in processed:
                continue

            group = [test1]
            for test2 in test_names[i+1:]:
                if test2 in processed:
                    continue

                similarity = self.calculate_coverage_similarity(test1, test2)
                if similarity >= threshold:
                    group.append(test2)
                    processed.add(test2)

            if len(group) > 1:
                groups.append(group)
                processed.add(test1)

        return groups

    def find_highly_similar_tests(self, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
        """Find pairs of tests with high coverage similarity"""
        similar_pairs = []

        test_names = list(self.test_coverage.keys())
        for i, test1 in enumerate(test_names):
            for test2 in test_names[i+1:]:
                similarity = self.calculate_coverage_similarity(test1, test2)
                if similarity >= threshold:
                    similar_pairs.append((test1, test2, similarity))

        # Sort by similarity descending
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        return similar_pairs

    def calculate_coverage_contribution(self, test_name: str, all_tests: List[str]) -> int:
        """Calculate unique lines covered by this test"""
        test_cov = self.test_coverage.get(test_name, set())
        other_tests = [t for t in all_tests if t != test_name]

        # Union of all other tests' coverage
        other_coverage = set()
        for other_test in other_tests:
            other_coverage.update(self.test_coverage.get(other_test, set()))

        # Unique contribution
        unique_lines = test_cov - other_coverage
        return len(unique_lines)

    def generate_report(self, output_file: Path):
        """Generate deduplication report"""
        report = {
            'summary': {
                'total_tests': len(self.test_coverage),
                'total_covered_lines': len(set().union(*self.test_coverage.values())) if self.test_coverage else 0
            },
            'identical_coverage_groups': [],
            'subsumed_tests': [],
            'highly_similar_pairs': [],
            'coverage_contributions': {}
        }

        # Find identical coverage groups
        identical_groups = self.find_identical_coverage(threshold=1.0)
        for group in identical_groups:
            report['identical_coverage_groups'].append({
                'tests': group,
                'count': len(group),
                'covered_lines': len(self.test_coverage[group[0]])
            })

        # Find subsumed tests
        subsumed = self.find_subsumed_tests()
        for test1, test2, overlap in subsumed:
            report['subsumed_tests'].append({
                'subsumed_test': test1,
                'subsuming_test': test2,
                'overlap_ratio': overlap
            })

        # Find highly similar tests
        similar_pairs = self.find_highly_similar_tests(threshold=0.8)
        for test1, test2, similarity in similar_pairs[:20]:  # Top 20
            report['highly_similar_pairs'].append({
                'test1': test1,
                'test2': test2,
                'similarity': similarity
            })

        # Calculate coverage contributions
        all_tests = list(self.test_coverage.keys())
        for test_name in all_tests:
            contribution = self.calculate_coverage_contribution(test_name, all_tests)
            report['coverage_contributions'][test_name] = {
                'unique_lines': contribution,
                'total_lines': len(self.test_coverage[test_name])
            }

        # Write report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Coverage analysis report saved to {output_file}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Analyze test coverage to identify redundant tests'
    )
    parser.add_argument(
        'coverage_file',
        type=Path,
        help='JSON file containing coverage data for each test'
    )
    parser.add_argument(
        '--repo',
        type=Path,
        default='.',
        help='Repository path (default: current directory)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default='coverage_analysis.json',
        help='Output report file (default: coverage_analysis.json)'
    )
    parser.add_argument(
        '--similarity-threshold',
        type=float,
        default=0.8,
        help='Similarity threshold for finding similar tests (default: 0.8)'
    )

    args = parser.parse_args()

    if not args.coverage_file.exists():
        print(f"Error: Coverage file {args.coverage_file} not found", file=sys.stderr)
        sys.exit(1)

    analyzer = CoverageAnalyzer(args.repo)
    analyzer.load_coverage_data(args.coverage_file)

    print(f"Loaded coverage data for {len(analyzer.test_coverage)} tests")
    print(f"Analyzing test redundancy...")

    report = analyzer.generate_report(args.output)

    # Print summary
    print("\n" + "="*80)
    print("COVERAGE-BASED DEDUPLICATION ANALYSIS")
    print("="*80)
    print(f"Total tests: {report['summary']['total_tests']}")
    print(f"Total covered lines: {report['summary']['total_covered_lines']}")
    print(f"\nIdentical coverage groups: {len(report['identical_coverage_groups'])}")
    print(f"Subsumed tests: {len(report['subsumed_tests'])}")
    print(f"Highly similar pairs: {len(report['highly_similar_pairs'])}")

    if report['identical_coverage_groups']:
        print("\nIdentical Coverage Groups:")
        for i, group in enumerate(report['identical_coverage_groups'][:5], 1):
            print(f"  Group {i}: {group['count']} tests with identical coverage")
            for test in group['tests'][:3]:
                print(f"    - {test}")
            if len(group['tests']) > 3:
                print(f"    ... and {len(group['tests']) - 3} more")

    if report['subsumed_tests']:
        print("\nSubsumed Tests (can be removed):")
        for item in report['subsumed_tests'][:5]:
            print(f"  {item['subsumed_test']} is subsumed by {item['subsuming_test']}")

    print("\n" + "="*80)


if __name__ == '__main__':
    main()
