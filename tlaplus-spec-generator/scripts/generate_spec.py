#!/usr/bin/env python3
"""
Main script for generating TLA+ specifications from source code.
Supports C/C++ and Python programs, particularly for distributed systems.
"""

import sys
import os
import argparse
from pathlib import Path
from program_analyzer import ProgramAnalyzer
from tlaplus_generator import TLAPlusGenerator


def detect_language(file_path):
    """Detect programming language from file extension."""
    ext = Path(file_path).suffix.lower()
    lang_map = {
        '.c': 'c',
        '.h': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.py': 'python'
    }
    return lang_map.get(ext, 'unknown')


def generate_spec(source_files, output_file, options):
    """
    Generate TLA+ specification from source code.

    Args:
        source_files: List of source file paths
        output_file: Output TLA+ file path
        options: Dictionary of generation options
    """
    print(f"[*] Generating TLA+ spec from {len(source_files)} file(s)...")

    # Analyze program
    analyzer = ProgramAnalyzer()

    for source_file in source_files:
        lang = detect_language(source_file)
        if lang == 'unknown':
            print(f"[!] Warning: Unknown language for {source_file}, skipping")
            continue

        print(f"[*] Analyzing {source_file} ({lang})...")
        analyzer.analyze_file(source_file, lang, options)

    # Extract specification data
    print("[*] Extracting specification structure...")
    spec_data = analyzer.extract_spec_data(options)

    # Generate TLA+ specification
    print("[*] Generating TLA+ specification...")
    generator = TLAPlusGenerator()
    tla_spec = generator.generate(spec_data, options)

    # Write output
    with open(output_file, 'w') as f:
        f.write(tla_spec)

    print(f"[+] TLA+ specification generated successfully: {output_file}")

    # Generate mapping explanation
    mapping_file = output_file.replace('.tla', '_mapping.txt')
    with open(mapping_file, 'w') as f:
        f.write(generator.generate_mapping_explanation(spec_data))

    print(f"[+] Mapping explanation written to: {mapping_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate TLA+ specifications from source code'
    )
    parser.add_argument('files', nargs='+', help='Source files to analyze')
    parser.add_argument('-o', '--output', required=True, help='Output TLA+ file')
    parser.add_argument('--abstraction', choices=['low', 'medium', 'high'],
                       default='medium', help='Abstraction level (default: medium)')
    parser.add_argument('--module-name', help='TLA+ module name (default: derived from output file)')
    parser.add_argument('--focus-functions', nargs='*',
                       help='Specific functions to focus on')
    parser.add_argument('--track-vars', nargs='*',
                       help='Specific variables to track in state')
    parser.add_argument('--processes', type=int,
                       help='Number of processes in distributed system')

    args = parser.parse_args()

    # Derive module name from output file if not specified
    module_name = args.module_name
    if not module_name:
        module_name = Path(args.output).stem

    options = {
        'abstraction': args.abstraction,
        'module_name': module_name,
        'focus_functions': args.focus_functions or [],
        'track_vars': args.track_vars or [],
        'num_processes': args.processes or 2
    }

    generate_spec(args.files, args.output, options)


if __name__ == '__main__':
    main()
