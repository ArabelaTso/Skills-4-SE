#!/usr/bin/env python3
"""
Replace deprecated API usage with modern alternatives.

Supports automatic replacement with validation.

Usage:
    python replace_deprecated_apis.py <file_or_directory> [--dry-run] [--language LANG]
"""

import re
import sys
import os
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Replacement:
    """Represents a replacement operation."""
    file_path: str
    line_number: int
    old_code: str
    new_code: str
    deprecated_api: str
    replacement_api: str


# Replacement patterns: (search_pattern, replacement_template, description)
REPLACEMENT_RULES = {
    'python': [
        # Python standard library
        (r'\bos\.popen\(([^)]+)\)', r'subprocess.run(\1, shell=True, capture_output=True, text=True)',
         'os.popen()', 'subprocess.run()'),
        (r'\btime\.clock\(\)', r'time.perf_counter()',
         'time.clock()', 'time.perf_counter()'),
        (r'\bfrom collections import (Mapping|MutableMapping|Iterable|Iterator)\b',
         r'from collections.abc import \1',
         'collections collections', 'collections.abc'),
        (r'\bcollections\.(Mapping|MutableMapping|Iterable|Iterator)\b',
         r'collections.abc.\1',
         'collections.*', 'collections.abc.*'),
        (r'\bimport imp\b', r'import importlib',
         'imp', 'importlib'),

        # Django
        (r'\bfrom django\.conf\.urls import url\b',
         r'from django.urls import path, re_path',
         'django.conf.urls.url', 'django.urls.path'),
        (r'\bdjango\.utils\.encoding\.force_text\(',
         r'django.utils.encoding.force_str(',
         'force_text()', 'force_str()'),
        (r'\bfrom django\.utils\.translation import ugettext as _\b',
         r'from django.utils.translation import gettext as _',
         'ugettext', 'gettext'),
        (r'\bfrom django\.utils\.translation import ugettext_lazy\b',
         r'from django.utils.translation import gettext_lazy',
         'ugettext_lazy', 'gettext_lazy'),

        # Flask
        (r'\bfrom flask\.json import jsonify\b',
         r'from flask import jsonify',
         'flask.json.jsonify', 'flask.jsonify'),
        (r'\.send_file\(([^,]+),\s*attachment_filename=([^)]+)\)',
         r'.send_file(\1, download_name=\2)',
         'attachment_filename', 'download_name'),
    ],
    'javascript': [
        # Node.js
        (r'\bconst url = require\([\'"]url[\'"]\);\s*url\.parse\(',
         r'new URL(',
         'url.parse()', 'new URL()'),
        (r'\brequire\([\'"]url[\'"]\)\.parse\(([^)]+)\)',
         r'new URL(\1)',
         'url.parse()', 'new URL()'),
        (r'\bnew Buffer\((\d+)\)',
         r'Buffer.alloc(\1)',
         'new Buffer()', 'Buffer.alloc()'),
        (r'\bnew Buffer\(([\'"][^\'"]+[\'"])\)',
         r'Buffer.from(\1)',
         'new Buffer()', 'Buffer.from()'),

        # React
        (r'\bReact\.createClass\(',
         r'class extends React.Component (',
         'React.createClass()', 'class component'),
        (r'\bReactDOM\.render\(',
         r'ReactDOM.createRoot(container).render(',
         'ReactDOM.render()', 'ReactDOM.createRoot()'),
        (r'\bimport PropTypes from [\'"]react[\'"]',
         r'import PropTypes from "prop-types"',
         'React.PropTypes', 'prop-types package'),
        (r'\bcomponentWillMount\s*\(\s*\)\s*\{',
         r'componentDidMount() {',
         'componentWillMount()', 'componentDidMount()'),
        (r'\bcomponentWillReceiveProps\s*\(\s*nextProps\s*\)\s*\{',
         r'static getDerivedStateFromProps(nextProps, prevState) {',
         'componentWillReceiveProps()', 'getDerivedStateFromProps()'),
    ],
    'java': [
        # Java core
        (r'\bnew Date\(([^)]+)\)',
         r'LocalDateTime.parse(\1)',
         'new Date()', 'LocalDateTime'),
        (r'\.stop\(\)',
         r'.interrupt()',
         'Thread.stop()', 'Thread.interrupt()'),

        # Spring
        (r'\bextends WebMvcConfigurerAdapter\b',
         r'implements WebMvcConfigurer',
         'WebMvcConfigurerAdapter', 'WebMvcConfigurer'),
        (r'\b@Autowired\s+@Nullable',
         r'@Autowired(required=false)',
         '@Autowired @Nullable', '@Autowired(required=false)'),
    ],
    'ruby': [
        (r'\bURI\.escape\(([^)]+)\)',
         r'CGI.escape(\1)',
         'URI.escape()', 'CGI.escape()'),
        (r'\bDir\.exists\?\(',
         r'Dir.exist?(',
         'Dir.exists?()', 'Dir.exist?()'),
        (r'\bFile\.exists\?\(',
         r'File.exist?(',
         'File.exists?()', 'File.exist?()'),
    ],
    'go': [
        (r'\bioutil\.ReadFile\(',
         r'os.ReadFile(',
         'ioutil.ReadFile()', 'os.ReadFile()'),
        (r'\bioutil\.WriteFile\(',
         r'os.WriteFile(',
         'ioutil.WriteFile()', 'os.WriteFile()'),
        (r'\bioutil\.TempDir\(',
         r'os.MkdirTemp(',
         'ioutil.TempDir()', 'os.MkdirTemp()'),
    ],
}


def detect_language(file_path: str) -> Optional[str]:
    """Detect programming language from file extension."""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'javascript',
        '.tsx': 'javascript',
        '.java': 'java',
        '.rb': 'ruby',
        '.go': 'go',
    }

    ext = Path(file_path).suffix.lower()
    return extension_map.get(ext)


def replace_in_file(file_path: str, language: Optional[str] = None,
                   dry_run: bool = False) -> List[Replacement]:
    """Replace deprecated APIs in a single file."""
    if language is None:
        language = detect_language(file_path)

    if language is None:
        return []

    rules = REPLACEMENT_RULES.get(language, [])
    replacements = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
            content = original_content

        # Track line numbers for reporting
        lines = content.splitlines(keepends=True)

        # Apply each replacement rule
        for pattern, replacement_template, deprecated_api, replacement_api in rules:
            matches = list(re.finditer(pattern, content))

            for match in matches:
                old_code = match.group(0)
                new_code = re.sub(pattern, replacement_template, old_code)

                # Find line number
                line_number = content[:match.start()].count('\n') + 1

                replacements.append(Replacement(
                    file_path=file_path,
                    line_number=line_number,
                    old_code=old_code,
                    new_code=new_code,
                    deprecated_api=deprecated_api,
                    replacement_api=replacement_api
                ))

            # Apply replacement to content
            content = re.sub(pattern, replacement_template, content)

        # Write back if not dry run and changes were made
        if not dry_run and content != original_content:
            # Create backup
            backup_path = file_path + '.bak'
            shutil.copy2(file_path, backup_path)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    except (UnicodeDecodeError, PermissionError) as e:
        print(f"Warning: Could not process {file_path}: {e}")

    return replacements


def replace_in_directory(directory: str, language: Optional[str] = None,
                        dry_run: bool = False) -> List[Replacement]:
    """Recursively replace deprecated APIs in a directory."""
    all_replacements = []

    for root, dirs, files in os.walk(directory):
        # Skip common ignored directories
        dirs[:] = [d for d in dirs if d not in {'.git', '.svn', 'node_modules', '__pycache__', 'venv', '.venv'}]

        for file in files:
            file_path = os.path.join(root, file)
            replacements = replace_in_file(file_path, language, dry_run)
            all_replacements.extend(replacements)

    return all_replacements


def format_report(replacements: List[Replacement], dry_run: bool) -> str:
    """Format replacement report."""
    if not replacements:
        return "✅ No deprecated APIs found to replace!"

    mode = "DRY RUN - " if dry_run else ""
    output = [f"{mode}Replaced {len(replacements)} deprecated API usage(s):\n"]

    # Group by file
    by_file = {}
    for r in replacements:
        if r.file_path not in by_file:
            by_file[r.file_path] = []
        by_file[r.file_path].append(r)

    for file_path, file_replacements in by_file.items():
        output.append(f"📄 {file_path} ({len(file_replacements)} replacement(s))")

        for r in file_replacements:
            output.append(f"   Line {r.line_number}:")
            output.append(f"   - {r.old_code}")
            output.append(f"   + {r.new_code}")
            output.append(f"   ({r.deprecated_api} → {r.replacement_api})")
            output.append("")

    if not dry_run:
        output.append("\n💾 Backup files created with .bak extension")
        output.append("⚠️  Please test your code and run your test suite to verify the changes!")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python replace_deprecated_apis.py <file_or_directory> [--dry-run] [--language LANG]")
        sys.exit(1)

    path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    language = None

    # Parse language argument
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--language' and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]

    # Replace in file or directory
    if os.path.isfile(path):
        replacements = replace_in_file(path, language, dry_run)
    elif os.path.isdir(path):
        replacements = replace_in_directory(path, language, dry_run)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    # Output report
    print(format_report(replacements, dry_run))

    sys.exit(0)


if __name__ == '__main__':
    main()
