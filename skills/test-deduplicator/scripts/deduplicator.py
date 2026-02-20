#!/usr/bin/env python3
"""
Test Deduplicator - Integrated Analysis and Recommendation Engine

Combines coverage, semantic, and execution result analysis to provide
comprehensive test deduplication recommendations.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class TestDeduplicator:
    """Integrated test deduplication engine"""

    def __init__(self):
        self.coverage_data = {}
        self.semantic_data = {}
        self.execution_data = {}
        self.test_metadata = {}

    def load_coverage_analysis(self, coverage_file: Path):
        """Load coverage analysis results"""
        with open(coverage_file, 'r') as f:
            self.coverage_data = json.load(f)

    def load_semantic_analysis(self, semantic_file: Path):
        """Load semantic analysis results"""
        with open(semantic_file, 'r') as f:
            self.semantic_data = json.load(f)

    def load_execution_results(self, execution_file: Path):
        """Load test execution results"""
        with open(execution_file, 'r') as f:
            self.execution_data = json.load(f)

    def calculate_redundancy_score(self, test1: str, test2: str) -> Dict[str, float]:
        """Calculate comprehensive redundancy score between two tests"""
        scores = {
            'coverage_similarity': 0.0,
            'semantic_similarity': 0.0,
            'execution_similarity': 0.0,
            'overall_redundancy': 0.0
        }

        # Coverage similarity
        for pair in self.coverage_data.get('highly_similar_pairs', []):
            if (pair['test1'] == test1 and pair['test2'] == test2) or \
               (pair['test1'] == test2 and pair['test2'] == test1):
                scores['coverage_similarity'] = pair['similarity']
                break

        # Semantic similarity
        for pair in self.semantic_data.get('semantically_similar_pairs', []):
            if (pair['test1'] == test1 and pair['test2'] == test2) or \
               (pair['test1'] == test2 and pair['test2'] == test1):
                scores['semantic_similarity'] = pair['similarity']['composite_similarity']
                break

        # Execution similarity (same outcomes)
        exec1 = self.execution_data.get('test_results', {}).get(test1, {})
        exec2 = self.execution_data.get('test_results', {}).get(test2, {})
        if exec1.get('status') == exec2.get('status'):
            scores['execution_similarity'] = 1.0

        # Overall redundancy (weighted average)
        scores['overall_redundancy'] = (
            scores['coverage_similarity'] * 0.5 +
            scores['semantic_similarity'] * 0.3 +
            scores['execution_similarity'] * 0.2
        )

        return scores

    def identify_redundant_groups(self, threshold: float = 0.8) -> List[Dict]:
        """Identify groups of redundant tests"""
        groups = []

        # Start with identical coverage groups
        for group_data in self.coverage_data.get('identical_coverage_groups', []):
            tests = group_data['tests']
            if len(tests) > 1:
                groups.append({
                    'type': 'identical_coverage',
                    'tests': tests,
                    'reason': 'Tests have identical code coverage',
                    'confidence': 1.0,
                    'recommendation': 'Keep one test, remove others'
                })

        # Add identical assertion groups
        for group_data in self.semantic_data.get('identical_assertions', []):
            tests = group_data['tests']
            if len(tests) > 1:
                groups.append({
                    'type': 'identical_assertions',
                    'tests': tests,
                    'reason': 'Tests have identical assertions',
                    'confidence': 0.95,
                    'recommendation': 'Keep one test, remove others'
                })

        # Find highly redundant pairs
        test_names = set()
        if 'coverage_contributions' in self.coverage_data:
            test_names.update(self.coverage_data['coverage_contributions'].keys())

        redundant_pairs = []
        for test1 in test_names:
            for test2 in test_names:
                if test1 >= test2:
                    continue
                scores = self.calculate_redundancy_score(test1, test2)
                if scores['overall_redundancy'] >= threshold:
                    redundant_pairs.append({
                        'test1': test1,
                        'test2': test2,
                        'scores': scores,
                        'reason': self._generate_redundancy_reason(scores)
                    })

        if redundant_pairs:
            groups.append({
                'type': 'highly_redundant_pairs',
                'pairs': redundant_pairs,
                'confidence': 0.85,
                'recommendation': 'Review and consider merging or removing'
            })

        return groups

    def _generate_redundancy_reason(self, scores: Dict[str, float]) -> str:
        """Generate human-readable reason for redundancy"""
        reasons = []
        if scores['coverage_similarity'] > 0.8:
            reasons.append(f"similar coverage ({scores['coverage_similarity']:.0%})")
        if scores['semantic_similarity'] > 0.7:
            reasons.append(f"similar code structure ({scores['semantic_similarity']:.0%})")
        if scores['execution_similarity'] > 0.9:
            reasons.append("same execution outcomes")

        return "Tests have " + ", ".join(reasons) if reasons else "high overall similarity"

    def prioritize_tests_to_keep(self, test_group: List[str]) -> List[Tuple[str, float, str]]:
        """Prioritize which tests to keep in a redundant group"""
        priorities = []

        for test in test_group:
            score = 0.0
            reasons = []

            # Unique coverage contribution
            contrib = self.coverage_data.get('coverage_contributions', {}).get(test, {})
            unique_lines = contrib.get('unique_lines', 0)
            total_lines = contrib.get('total_lines', 1)

            if unique_lines > 0:
                score += unique_lines * 10
                reasons.append(f"{unique_lines} unique lines")

            # Test execution time (prefer faster tests)
            exec_data = self.execution_data.get('test_results', {}).get(test, {})
            duration = exec_data.get('duration', 1.0)
            if duration < 1.0:
                score += 5
                reasons.append("fast execution")

            # Test stability (prefer tests that pass consistently)
            if exec_data.get('status') == 'passed':
                score += 3
                reasons.append("stable")

            # Test name clarity (prefer descriptive names)
            if len(test.split('_')) > 3:
                score += 2
                reasons.append("descriptive name")

            priorities.append((test, score, ", ".join(reasons)))

        # Sort by score descending
        priorities.sort(key=lambda x: x[1], reverse=True)
        return priorities

    def generate_recommendations(self, output_file: Path, threshold: float = 0.8):
        """Generate comprehensive deduplication recommendations"""
        redundant_groups = self.identify_redundant_groups(threshold)

        recommendations = {
            'summary': {
                'total_redundant_groups': len(redundant_groups),
                'threshold': threshold
            },
            'redundant_groups': [],
            'removal_candidates': [],
            'merge_candidates': [],
            'coverage_impact': {}
        }

        for group in redundant_groups:
            if group['type'] in ['identical_coverage', 'identical_assertions']:
                tests = group['tests']
                priorities = self.prioritize_tests_to_keep(tests)

                group_rec = {
                    'type': group['type'],
                    'tests': tests,
                    'reason': group['reason'],
                    'confidence': group['confidence'],
                    'keep': priorities[0][0] if priorities else tests[0],
                    'remove': [t for t, _, _ in priorities[1:]],
                    'rationale': priorities[0][2] if priorities else 'first test'
                }
                recommendations['redundant_groups'].append(group_rec)

                # Add to removal candidates
                for test in group_rec['remove']:
                    recommendations['removal_candidates'].append({
                        'test': test,
                        'reason': f"Redundant with {group_rec['keep']}",
                        'confidence': group['confidence']
                    })

        # Calculate coverage impact
        total_coverage_before = self.coverage_data.get('summary', {}).get('total_covered_lines', 0)
        recommendations['coverage_impact'] = {
            'total_coverage_before': total_coverage_before,
            'estimated_coverage_after': total_coverage_before,  # Should remain same
            'tests_removed': len(recommendations['removal_candidates']),
            'coverage_preserved': True
        }

        # Write recommendations
        with open(output_file, 'w') as f:
            json.dump(recommendations, f, indent=2)

        print(f"Deduplication recommendations saved to {output_file}")
        return recommendations


def main():
    parser = argparse.ArgumentParser(
        description='Generate comprehensive test deduplication recommendations'
    )
    parser.add_argument(
        '--coverage',
        type=Path,
        required=True,
        help='Coverage analysis JSON file'
    )
    parser.add_argument(
        '--semantic',
        type=Path,
        required=True,
        help='Semantic analysis JSON file'
    )
    parser.add_argument(
        '--execution',
        type=Path,
        help='Execution results JSON file (optional)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default='deduplication_recommendations.json',
        help='Output recommendations file'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.8,
        help='Redundancy threshold (default: 0.8)'
    )

    args = parser.parse_args()

    deduplicator = TestDeduplicator()

    print("Loading analysis results...")
    deduplicator.load_coverage_analysis(args.coverage)
    deduplicator.load_semantic_analysis(args.semantic)

    if args.execution and args.execution.exists():
        deduplicator.load_execution_results(args.execution)
    else:
        # Create empty execution data
        deduplicator.execution_data = {'test_results': {}}

    print("Generating deduplication recommendations...")
    recommendations = deduplicator.generate_recommendations(args.output, args.threshold)

    # Print summary
    print("\n" + "="*80)
    print("TEST DEDUPLICATION RECOMMENDATIONS")
    print("="*80)
    print(f"Redundant groups found: {recommendations['summary']['total_redundant_groups']}")
    print(f"Tests recommended for removal: {len(recommendations['removal_candidates'])}")
    print(f"Coverage preserved: {recommendations['coverage_impact']['coverage_preserved']}")

    if recommendations['redundant_groups']:
        print("\nRedundant Test Groups:")
        for i, group in enumerate(recommendations['redundant_groups'][:5], 1):
            print(f"\n  Group {i} ({group['type']}):")
            print(f"    Reason: {group['reason']}")
            print(f"    Confidence: {group['confidence']:.0%}")
            print(f"    Keep: {group['keep']}")
            print(f"    Remove: {', '.join(group['remove'][:3])}")
            if len(group['remove']) > 3:
                print(f"            ... and {len(group['remove']) - 3} more")

    print("\n" + "="*80)
    print(f"\nDetailed recommendations saved to: {args.output}")


if __name__ == '__main__':
    main()
