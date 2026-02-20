#!/usr/bin/env python3
"""
RTL Equivalence Checker - Main script for comparing two RTL designs.
Supports Verilog and tool-agnostic formal verification approach.
"""

import sys
import os
import argparse
from pathlib import Path
from rtl_parser import RTLParser
from equivalence_analyzer import EquivalenceAnalyzer
from counterexample_generator import CounterexampleGenerator


def check_equivalence(rtl_a_path, rtl_b_path, options):
    """
    Check equivalence between two RTL designs.

    Args:
        rtl_a_path: Path to RTL version A
        rtl_b_path: Path to RTL version B
        options: Dictionary of checking options

    Returns:
        Dictionary containing equivalence results
    """
    print("=" * 70)
    print("RTL EQUIVALENCE CHECKING")
    print("=" * 70)
    print(f"Version A: {rtl_a_path}")
    print(f"Version B: {rtl_b_path}")
    print()

    # Parse RTL designs
    print("[1/5] Parsing RTL designs...")
    parser = RTLParser()

    design_a = parser.parse(rtl_a_path)
    design_b = parser.parse(rtl_b_path)

    if not design_a or not design_b:
        return {
            'equivalent': False,
            'error': 'Failed to parse one or both RTL designs',
            'details': None
        }

    print(f"  Version A: {design_a['module_name']} ({len(design_a['ports'])} ports, {len(design_a['signals'])} signals)")
    print(f"  Version B: {design_b['module_name']} ({len(design_b['ports'])} ports, {len(design_b['signals'])} signals)")
    print()

    # Align interfaces and state variables
    print("[2/5] Aligning interfaces and state variables...")
    analyzer = EquivalenceAnalyzer(design_a, design_b, options)

    alignment = analyzer.align_designs()

    if not alignment['success']:
        return {
            'equivalent': False,
            'error': 'Interface mismatch',
            'details': alignment
        }

    print(f"  Matched ports: {len(alignment['matched_ports'])}")
    print(f"  Matched state elements: {len(alignment['matched_state'])}")
    if alignment['unmatched_a']:
        print(f"  Unmatched in A: {', '.join(alignment['unmatched_a'])}")
    if alignment['unmatched_b']:
        print(f"  Unmatched in B: {', '.join(alignment['unmatched_b'])}")
    print()

    # Identify differences
    print("[3/5] Analyzing behavioral differences...")
    differences = analyzer.find_differences()

    print(f"  Cosmetic differences: {len(differences['cosmetic'])}")
    print(f"  Semantic differences: {len(differences['semantic'])}")
    print()

    # Determine equivalence
    print("[4/5] Determining equivalence...")

    if not differences['semantic']:
        print("  ✓ Designs are functionally EQUIVALENT")
        print()

        result = {
            'equivalent': True,
            'alignment': alignment,
            'cosmetic_differences': differences['cosmetic'],
            'explanation': 'The two RTL designs are functionally equivalent. All differences are cosmetic (naming, formatting, or structurally equivalent refactoring).'
        }
    else:
        print("  ✗ Designs are NOT equivalent")
        print()

        # Generate counterexample
        print("[5/5] Generating counterexample...")
        cex_gen = CounterexampleGenerator(design_a, design_b, alignment, differences)
        counterexample = cex_gen.generate()

        if counterexample:
            print(f"  Found counterexample with {len(counterexample['trace'])} cycles")
        print()

        result = {
            'equivalent': False,
            'alignment': alignment,
            'semantic_differences': differences['semantic'],
            'cosmetic_differences': differences['cosmetic'],
            'counterexample': counterexample,
            'explanation': analyzer.explain_differences(differences['semantic'])
        }

    return result


def format_output(result, output_file=None):
    """Format and display equivalence checking results."""
    lines = []

    lines.append("=" * 70)
    lines.append("EQUIVALENCE CHECKING RESULTS")
    lines.append("=" * 70)
    lines.append("")

    # Verdict
    if result.get('error'):
        lines.append(f"ERROR: {result['error']}")
        lines.append("")
        return '\n'.join(lines)

    verdict = "EQUIVALENT" if result['equivalent'] else "NOT EQUIVALENT"
    lines.append(f"Verdict: {verdict}")
    lines.append("")

    # Explanation
    lines.append("Explanation:")
    lines.append("-" * 70)
    lines.append(result['explanation'])
    lines.append("")

    # Cosmetic differences
    if result.get('cosmetic_differences'):
        lines.append("Cosmetic Differences (non-functional):")
        lines.append("-" * 70)
        for diff in result['cosmetic_differences']:
            lines.append(f"  - {diff['type']}: {diff['description']}")
        lines.append("")

    # Semantic differences
    if not result['equivalent'] and result.get('semantic_differences'):
        lines.append("Semantic Differences (functional):")
        lines.append("-" * 70)
        for diff in result['semantic_differences']:
            lines.append(f"  - {diff['type']}: {diff['description']}")
            if diff.get('location'):
                lines.append(f"    Location: {diff['location']}")
        lines.append("")

    # Counterexample
    if not result['equivalent'] and result.get('counterexample'):
        cex = result['counterexample']
        lines.append("Counterexample Trace:")
        lines.append("-" * 70)
        lines.append(f"Length: {len(cex['trace'])} cycles")
        lines.append("")

        for i, cycle in enumerate(cex['trace']):
            lines.append(f"Cycle {i}:")
            lines.append(f"  Inputs: {cycle['inputs']}")
            lines.append(f"  Output A: {cycle['output_a']}")
            lines.append(f"  Output B: {cycle['output_b']}")
            if cycle.get('mismatch'):
                lines.append(f"  MISMATCH: {cycle['mismatch']}")
            lines.append("")

    lines.append("=" * 70)

    output = '\n'.join(lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"Results written to: {output_file}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description='Check functional equivalence between two RTL designs'
    )
    parser.add_argument('rtl_a', help='Path to RTL version A (Verilog)')
    parser.add_argument('rtl_b', help='Path to RTL version B (Verilog)')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('--clock', help='Clock signal name (default: clk)')
    parser.add_argument('--reset', help='Reset signal name (default: rst)')
    parser.add_argument('--reset-active', choices=['high', 'low'],
                       default='low', help='Reset active level (default: low)')
    parser.add_argument('--ignore-names', action='store_true',
                       help='Ignore signal name differences')
    parser.add_argument('--max-depth', type=int, default=100,
                       help='Maximum trace depth for counterexample (default: 100)')

    args = parser.parse_args()

    options = {
        'clock': args.clock or 'clk',
        'reset': args.reset or 'rst',
        'reset_active': args.reset_active,
        'ignore_names': args.ignore_names,
        'max_depth': args.max_depth
    }

    # Check equivalence
    result = check_equivalence(args.rtl_a, args.rtl_b, options)

    # Format and display results
    output = format_output(result, args.output)
    print(output)

    # Exit with appropriate code
    sys.exit(0 if result.get('equivalent') else 1)


if __name__ == '__main__':
    main()
