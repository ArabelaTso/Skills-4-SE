#!/usr/bin/env python3
"""
Main script for extracting SMV models from source code.
Supports C/C++, Java, and Python programs.
"""

import sys
import os
import argparse
from pathlib import Path
from cfg_analyzer import CFGAnalyzer
from smv_generator import SMVGenerator
from language_parser import LanguageParser


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
        '.java': 'java',
        '.py': 'python'
    }
    return lang_map.get(ext, 'unknown')


def extract_model(source_files, output_file, options):
    """
    Extract SMV model from source code.

    Args:
        source_files: List of source file paths
        output_file: Output SMV file path
        options: Dictionary of extraction options
    """
    print(f"[*] Extracting model from {len(source_files)} file(s)...")

    # Parse source files
    parser = LanguageParser()
    ast_data = []

    for source_file in source_files:
        lang = detect_language(source_file)
        if lang == 'unknown':
            print(f"[!] Warning: Unknown language for {source_file}, skipping")
            continue

        print(f"[*] Parsing {source_file} ({lang})...")
        ast = parser.parse_file(source_file, lang)
        ast_data.append((source_file, lang, ast))

    # Analyze control flow
    print("[*] Analyzing control flow...")
    cfg_analyzer = CFGAnalyzer()
    cfg_data = cfg_analyzer.analyze(ast_data, options)

    # Generate SMV model
    print("[*] Generating SMV model...")
    smv_gen = SMVGenerator()
    smv_model = smv_gen.generate(cfg_data, options)

    # Write output
    with open(output_file, 'w') as f:
        f.write(smv_model)

    print(f"[+] Model extracted successfully to {output_file}")

    # Generate mapping explanation
    mapping_file = output_file.replace('.smv', '_mapping.txt')
    with open(mapping_file, 'w') as f:
        f.write(smv_gen.generate_mapping_explanation(cfg_data))

    print(f"[+] Mapping explanation written to {mapping_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract SMV models from source code for model checking'
    )
    parser.add_argument('files', nargs='+', help='Source files to analyze')
    parser.add_argument('-o', '--output', required=True, help='Output SMV file')
    parser.add_argument('--abstraction', choices=['low', 'medium', 'high'],
                       default='medium', help='Abstraction level (default: medium)')
    parser.add_argument('--focus-functions', nargs='*',
                       help='Specific functions to focus on')
    parser.add_argument('--track-vars', nargs='*',
                       help='Specific variables to track in state')

    args = parser.parse_args()

    options = {
        'abstraction': args.abstraction,
        'focus_functions': args.focus_functions or [],
        'track_vars': args.track_vars or []
    }

    extract_model(args.files, args.output, options)


if __name__ == '__main__':
    main()
