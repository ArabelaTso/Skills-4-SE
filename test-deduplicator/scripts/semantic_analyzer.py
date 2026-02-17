#!/usr/bin/env python3
"""
Test Deduplicator - Semantic Similarity Analysis

Analyzes test code and assertions for semantic similarity to identify redundant tests.
"""

import ast
import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import difflib


class TestSemanticAnalyzer:
    """Analyzes semantic similarity between tests"""

    def __init__(self):
        self.test_data = {}  # test_name -> test metadata
        self.test_assertions = {}  # test_name -> list of assertions
        self.test_calls = {}  # test_name -> list of function calls

    def parse_test_file(self, file_path: Path) -> Dict[str, Dict]:
        """Parse a test file and extract test metadata"""
        with open(file_path, 'r') as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return {}

        tests = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_info = self._analyze_test_function(node, file_path)
                test_name = f"{file_path.stem}::{node.name}"
                tests[test_name] = test_info
                self.test_data[test_name] = test_info

        return tests

    def _analyze_test_function(self, node: ast.FunctionDef, file_path: Path) -> Dict:
        """Analyze a single test function"""
        assertions = []
        function_calls = []
        variables = set()

        for child in ast.walk(node):
            # Extract assertions
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in ['assertEqual', 'assertEquals', 'assertTrue',
                                          'assertFalse', 'assertIn', 'assertNotIn',
                                          'assertIsNone', 'assertIsNotNone', 'assertRaises']:
                        assertions.append(ast.unparse(child))
                elif isinstance(child.func, ast.Name) and child.func.id == 'assert':
                    assertions.append(ast.unparse(child))

                # Extract function calls
                if isinstance(child.func, ast.Name):
                    function_calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    function_calls.append(child.func.attr)

            # Extract variable names
            if isinstance(child, ast.Name):
                variables.add(child.id)

        return {
            'file': str(file_path),
            'name': node.name,
            'line': node.lineno,
            'assertions': assertions,
            'function_calls': function_calls,
            'variables': list(variables),
            'source': ast.unparse(node)
        }

    def calculate_assertion_similarity(self, test1: str, test2: str) -> float:
        """Calculate similarity based on assertions"""
        assertions1 = set(self.test_data.get(test1, {}).get('assertions', []))
        assertions2 = set(self.test_data.get(test2, {}).get('assertions', []))

        if not assertions1 and not assertions2:
            return 0.0

        intersection = len(assertions1 & assertions2)
        union = len(assertions1 | assertions2)

        return intersection / union if union > 0 else 0.0

    def calculate_call_similarity(self, test1: str, test2: str) -> float:
        """Calculate similarity based on function calls"""
        calls1 = self.test_data.get(test1, {}).get('function_calls', [])
        calls2 = self.test_data.get(test2, {}).get('function_calls', [])

        if not calls1 and not calls2:
            return 0.0

        # Use sequence matching for ordered calls
        matcher = difflib.SequenceMatcher(None, calls1, calls2)
        return matcher.ratio()

    def calculate_source_similarity(self, test1: str, test2: str) -> float:
        """Calculate similarity based on source code"""
        source1 = self.test_data.get(test1, {}).get('source', '')
        source2 = self.test_data.get(test2, {}).get('source', '')

        if not source1 and not source2:
            return 0.0

        matcher = difflib.SequenceMatcher(None, source1, source2)
        return matcher.ratio()

    def calculate_composite_similarity(self, test1: str, test2: str) -> Dict[str, float]:
        """Calculate composite similarity score"""
        assertion_sim = self.calculate_assertion_similarity(test1, test2)
        call_sim = self.calculate_call_similarity(test1, test2)
        source_sim = self.calculate_source_similarity(test1, test2)

        # Weighted average
        composite = (assertion_sim * 0.4 + call_sim * 0.3 + source_sim * 0.3)

        return {
            'assertion_similarity': assertion_sim,
            'call_similarity': call_sim,
            'source_similarity': source_sim,
            'composite_similarity': composite
        }

    def find_semantically_similar_tests(self, threshold: float = 0.7) -> List[Tuple[str, str, Dict]]:
        """Find pairs of semantically similar tests"""
        similar_pairs = []

        test_names = list(self.test_data.keys())
        for i, test1 in enumerate(test_names):
            for test2 in test_names[i+1:]:
                similarity = self.calculate_composite_similarity(test1, test2)
                if similarity['composite_similarity'] >= threshold:
                    similar_pairs.append((test1, test2, similarity))

        # Sort by composite similarity
        similar_pairs.sort(key=lambda x: x[2]['composite_similarity'], reverse=True)
        return similar_pairs

    def find_identical_assertions(self) -> List[List[str]]:
        """Find tests with identical assertion sets"""
        assertion_groups = defaultdict(list)

        for test_name, test_info in self.test_data.items():
            assertions = tuple(sorted(test_info.get('assertions', [])))
            if assertions:
                assertion_groups[assertions].append(test_name)

        # Return groups with more than one test
        return [tests for tests in assertion_groups.values() if len(tests) > 1]

    def analyze_test_patterns(self) -> Dict[str, List[str]]:
        """Group tests by common patterns"""
        patterns = defaultdict(list)

        for test_name, test_info in self.test_data.items():
            # Pattern: number of assertions
            num_assertions = len(test_info.get('assertions', []))
            patterns[f'assertions_{num_assertions}'].append(test_name)

            # Pattern: tested functions
            calls = test_info.get('function_calls', [])
            if calls:
                main_call = calls[0] if calls else 'unknown'
                patterns[f'tests_{main_call}'].append(test_name)

        return dict(patterns)

    def generate_report(self, output_file: Path, similarity_threshold: float = 0.7):
        """Generate semantic similarity report"""
        report = {
            'summary': {
                'total_tests': len(self.test_data),
                'similarity_threshold': similarity_threshold
            },
            'identical_assertions': [],
            'semantically_similar_pairs': [],
            'test_patterns': {}
        }

        # Find tests with identical assertions
        identical_groups = self.find_identical_assertions()
        for group in identical_groups:
            report['identical_assertions'].append({
                'tests': group,
                'count': len(group),
                'assertions': self.test_data[group[0]].get('assertions', [])
            })

        # Find semantically similar tests
        similar_pairs = self.find_semantically_similar_tests(threshold=similarity_threshold)
        for test1, test2, similarity in similar_pairs:
            report['semantically_similar_pairs'].append({
                'test1': test1,
                'test2': test2,
                'similarity': similarity
            })

        # Analyze patterns
        report['test_patterns'] = self.analyze_test_patterns()

        # Write report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Semantic analysis report saved to {output_file}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Analyze semantic similarity between tests'
    )
    parser.add_argument(
        'test_files',
        nargs='+',
        type=Path,
        help='Test files to analyze'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default='semantic_analysis.json',
        help='Output report file (default: semantic_analysis.json)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.7,
        help='Similarity threshold (default: 0.7)'
    )

    args = parser.parse_args()

    analyzer = TestSemanticAnalyzer()

    # Parse all test files
    print("Parsing test files...")
    for test_file in args.test_files:
        if test_file.exists():
            analyzer.parse_test_file(test_file)
        else:
            print(f"Warning: {test_file} not found")

    print(f"Analyzed {len(analyzer.test_data)} tests")
    print("Finding semantically similar tests...")

    report = analyzer.generate_report(args.output, args.threshold)

    # Print summary
    print("\n" + "="*80)
    print("SEMANTIC SIMILARITY ANALYSIS")
    print("="*80)
    print(f"Total tests: {report['summary']['total_tests']}")
    print(f"Similarity threshold: {report['summary']['similarity_threshold']}")
    print(f"\nTests with identical assertions: {len(report['identical_assertions'])} groups")
    print(f"Semantically similar pairs: {len(report['semantically_similar_pairs'])}")

    if report['identical_assertions']:
        print("\nIdentical Assertion Groups:")
        for i, group in enumerate(report['identical_assertions'][:5], 1):
            print(f"  Group {i}: {group['count']} tests")
            for test in group['tests'][:3]:
                print(f"    - {test}")

    if report['semantically_similar_pairs']:
        print("\nTop Semantically Similar Pairs:")
        for i, pair in enumerate(report['semantically_similar_pairs'][:5], 1):
            sim = pair['similarity']['composite_similarity']
            print(f"  {i}. {pair['test1']} <-> {pair['test2']}")
            print(f"     Similarity: {sim:.2f}")

    print("\n" + "="*80)


if __name__ == '__main__':
    main()
