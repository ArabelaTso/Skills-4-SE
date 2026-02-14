#!/usr/bin/env python3
"""
Detect deprecated API usage in source code.

Supports multiple detection approaches:
1. AST parsing for precise detection (Python, JavaScript/TypeScript)
2. Pattern matching for faster detection across all languages

Usage:
    python detect_deprecated_apis.py <file_or_directory> [--language LANG] [--format json|text]
"""

import ast
import re
import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class DeprecationMatch:
    """Represents a detected deprecated API usage."""
    file_path: str
    line_number: int
    column: int
    deprecated_api: str
    suggested_replacement: Optional[str]
    context: str
    detection_method: str  # 'ast' or 'pattern'


# Common deprecation patterns across languages
DEPRECATION_PATTERNS = {
    'python': [
        # Python standard library
        (r'\bos\.popen\(', 'os.popen()', 'subprocess.run() or subprocess.Popen()'),
        (r'\bplatform\.dist\(', 'platform.dist()', 'distro.linux_distribution()'),
        (r'\btime\.clock\(', 'time.clock()', 'time.perf_counter() or time.process_time()'),
        (r'\bcollections\.Mapping\b', 'collections.Mapping', 'collections.abc.Mapping'),
        (r'\bcollections\.MutableMapping\b', 'collections.MutableMapping', 'collections.abc.MutableMapping'),
        (r'\bcollections\.Iterable\b', 'collections.Iterable', 'collections.abc.Iterable'),
        (r'\bimport imp\b', 'imp module', 'importlib'),

        # Django deprecations
        (r'\bdjango\.conf\.urls\.url\(', 'django.conf.urls.url()', 'django.urls.path() or re_path()'),
        (r'\bdjango\.utils\.encoding\.force_text\(', 'force_text()', 'force_str()'),
        (r'\bdjango\.utils\.translation\.ugettext', 'ugettext variants', 'gettext variants'),
        (r'\bon_delete\s*=\s*models\.CASCADE', 'implicit on_delete', 'explicit on_delete=models.CASCADE'),

        # Flask deprecations
        (r'\bflask\.json\.jsonify\(', 'flask.json.jsonify()', 'flask.jsonify()'),
        (r'\.send_file\([^,]+,\s*attachment_filename=', 'attachment_filename parameter', 'download_name parameter'),
    ],
    'javascript': [
        # Node.js deprecations
        (r'\brequire\([\'"]url[\'"]\)\.parse\(', 'url.parse()', 'new URL()'),
        (r'\brequire\([\'"]crypto[\'"]\)\.createCipher\(', 'crypto.createCipher()', 'crypto.createCipheriv()'),
        (r'\bbuffer\.Buffer\(\d+\)', 'Buffer() constructor', 'Buffer.alloc() or Buffer.from()'),
        (r'\bprocess\.binding\(', 'process.binding()', 'public APIs instead'),

        # React deprecations
        (r'\bReact\.createClass\(', 'React.createClass()', 'class or function components'),
        (r'\bReactDOM\.render\(', 'ReactDOM.render()', 'ReactDOM.createRoot()'),
        (r'\bReact\.PropTypes\b', 'React.PropTypes', 'prop-types package'),
        (r'\bcomponentWillMount\(', 'componentWillMount()', 'componentDidMount() or constructor()'),
        (r'\bcomponentWillReceiveProps\(', 'componentWillReceiveProps()', 'getDerivedStateFromProps()'),
        (r'\bFINDDOM_NODE', 'findDOMNode()', 'refs or callback refs'),
    ],
    'java': [
        # Java core deprecations
        (r'new Date\(', 'new Date()', 'java.time.LocalDate or java.time.Instant'),
        (r'new Thread\([^)]+\)\.stop\(', 'Thread.stop()', 'interrupt() or volatile flags'),
        (r'\.finalize\(\)', 'finalize()', 'try-with-resources or Cleaner'),
        (r'Integer\.parseInt\(\w+,\s*8\)', 'Integer.parseInt with octal', 'use explicit radix 8'),

        # Spring deprecations
        (r'@Autowired\s+@Nullable', '@Autowired with @Nullable', 'required=false'),
        (r'WebMvcConfigurerAdapter', 'WebMvcConfigurerAdapter', 'implements WebMvcConfigurer'),
        (r'\.getConnection\(\)', 'DriverManager.getConnection()', 'DataSource'),
    ],
    'ruby': [
        (r'\bURI\.escape\(', 'URI.escape()', 'CGI.escape() or ERB::Util.url_encode()'),
        (r'\bDir\.exists\?\(', 'Dir.exists?()', 'Dir.exist?()'),
        (r'\bFile\.exists\?\(', 'File.exists?()', 'File.exist?()'),
    ],
    'go': [
        (r'ioutil\.ReadFile\(', 'ioutil.ReadFile()', 'os.ReadFile()'),
        (r'ioutil\.WriteFile\(', 'ioutil.WriteFile()', 'os.WriteFile()'),
        (r'ioutil\.TempDir\(', 'ioutil.TempDir()', 'os.MkdirTemp()'),
    ],
}


class PythonASTAnalyzer(ast.NodeVisitor):
    """AST-based analyzer for Python deprecated APIs."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.deprecations: List[DeprecationMatch] = []

    def visit_Import(self, node: ast.Import):
        """Check for deprecated module imports."""
        for alias in node.names:
            if alias.name == 'imp':
                self._add_deprecation(
                    node, 'imp module', 'importlib',
                    f"import {alias.name}"
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Check for deprecated imports from modules."""
        if node.module and node.module.startswith('collections'):
            for alias in node.names:
                if alias.name in ['Mapping', 'MutableMapping', 'Iterable', 'Iterator']:
                    self._add_deprecation(
                        node, f'collections.{alias.name}',
                        f'collections.abc.{alias.name}',
                        f"from {node.module} import {alias.name}"
                    )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Check for deprecated function/method calls."""
        # Check for os.popen()
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and
                node.func.value.id == 'os' and
                node.func.attr == 'popen'):
                self._add_deprecation(
                    node, 'os.popen()', 'subprocess.run() or subprocess.Popen()',
                    self._get_source_segment(node)
                )

            # Check for time.clock()
            elif (isinstance(node.func.value, ast.Name) and
                  node.func.value.id == 'time' and
                  node.func.attr == 'clock'):
                self._add_deprecation(
                    node, 'time.clock()', 'time.perf_counter() or time.process_time()',
                    self._get_source_segment(node)
                )

        self.generic_visit(node)

    def _add_deprecation(self, node: ast.AST, deprecated_api: str,
                        replacement: str, context: str):
        """Add a deprecation match."""
        self.deprecations.append(DeprecationMatch(
            file_path=self.file_path,
            line_number=node.lineno,
            column=node.col_offset,
            deprecated_api=deprecated_api,
            suggested_replacement=replacement,
            context=context,
            detection_method='ast'
        ))

    def _get_source_segment(self, node: ast.AST) -> str:
        """Extract source code segment for a node."""
        if hasattr(node, 'lineno') and node.lineno <= len(self.source_lines):
            return self.source_lines[node.lineno - 1].strip()
        return ""


def detect_with_ast(file_path: str, language: str) -> List[DeprecationMatch]:
    """Detect deprecated APIs using AST parsing."""
    matches = []

    if language == 'python':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=file_path)
            analyzer = PythonASTAnalyzer(file_path, source_code)
            analyzer.visit(tree)
            matches.extend(analyzer.deprecations)
        except (SyntaxError, UnicodeDecodeError) as e:
            # Fall back to pattern matching if AST parsing fails
            pass

    return matches


def detect_with_patterns(file_path: str, language: str) -> List[DeprecationMatch]:
    """Detect deprecated APIs using regex patterns."""
    matches = []
    patterns = DEPRECATION_PATTERNS.get(language, [])

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            for pattern, deprecated_api, replacement in patterns:
                if re.search(pattern, line):
                    match = re.search(pattern, line)
                    matches.append(DeprecationMatch(
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start() if match else 0,
                        deprecated_api=deprecated_api,
                        suggested_replacement=replacement,
                        context=line.strip(),
                        detection_method='pattern'
                    ))
    except (UnicodeDecodeError, PermissionError):
        pass

    return matches


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
        '.php': 'php',
    }

    ext = Path(file_path).suffix.lower()
    return extension_map.get(ext)


def scan_file(file_path: str, language: Optional[str] = None) -> List[DeprecationMatch]:
    """Scan a single file for deprecated APIs."""
    if language is None:
        language = detect_language(file_path)

    if language is None:
        return []

    matches = []

    # Try AST parsing first for supported languages
    if language in ['python']:
        ast_matches = detect_with_ast(file_path, language)
        matches.extend(ast_matches)

    # Use pattern matching as well
    pattern_matches = detect_with_patterns(file_path, language)
    matches.extend(pattern_matches)

    # Remove duplicates (same line and API)
    seen = set()
    unique_matches = []
    for match in matches:
        key = (match.file_path, match.line_number, match.deprecated_api)
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)

    return unique_matches


def scan_directory(directory: str, language: Optional[str] = None) -> List[DeprecationMatch]:
    """Recursively scan a directory for deprecated APIs."""
    all_matches = []

    for root, dirs, files in os.walk(directory):
        # Skip common ignored directories
        dirs[:] = [d for d in dirs if d not in {'.git', '.svn', 'node_modules', '__pycache__', 'venv', '.venv'}]

        for file in files:
            file_path = os.path.join(root, file)
            matches = scan_file(file_path, language)
            all_matches.extend(matches)

    return all_matches


def format_output(matches: List[DeprecationMatch], format_type: str = 'text') -> str:
    """Format detection results."""
    if format_type == 'json':
        return json.dumps([asdict(m) for m in matches], indent=2)

    # Text format
    if not matches:
        return "✅ No deprecated APIs found!"

    output = [f"Found {len(matches)} deprecated API usage(s):\n"]

    for match in matches:
        output.append(f"📍 {match.file_path}:{match.line_number}:{match.column}")
        output.append(f"   Deprecated: {match.deprecated_api}")
        if match.suggested_replacement:
            output.append(f"   Replacement: {match.suggested_replacement}")
        output.append(f"   Context: {match.context}")
        output.append(f"   Detection: {match.detection_method}")
        output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python detect_deprecated_apis.py <file_or_directory> [--language LANG] [--format json|text]")
        sys.exit(1)

    path = sys.argv[1]
    language = None
    format_type = 'text'

    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--language' and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]
        elif arg == '--format' and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1]

    # Scan file or directory
    if os.path.isfile(path):
        matches = scan_file(path, language)
    elif os.path.isdir(path):
        matches = scan_directory(path, language)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    # Output results
    print(format_output(matches, format_type))

    # Exit with error code if deprecations found
    sys.exit(1 if matches else 0)


if __name__ == '__main__':
    main()
