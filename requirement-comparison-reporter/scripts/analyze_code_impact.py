#!/usr/bin/env python3
"""
Analyze code structure and dependencies for requirement impact analysis.

Usage:
    python analyze_code_impact.py <repo_path>
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class CodeImpactAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.python_files = self._find_python_files()
        self.dependency_graph = defaultdict(set)
        self.reverse_dependency_graph = defaultdict(set)

    def _find_python_files(self) -> List[Path]:
        """Find all Python files in repository."""
        files = []
        for path in self.repo_path.rglob("*.py"):
            if any(part in path.parts for part in ['.git', '__pycache__', 'venv', '.venv']):
                continue
            files.append(path)
        return files

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single Python file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)

            functions = []
            classes = []
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'is_private': node.name.startswith('_'),
                        'docstring': ast.get_docstring(node)
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append({
                                'name': item.name,
                                'line': item.lineno,
                                'is_private': item.name.startswith('_')
                            })
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'methods': methods,
                        'docstring': ast.get_docstring(node)
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append({
                                'module': alias.name,
                                'name': alias.asname or alias.name,
                                'type': 'import'
                            })
                    else:
                        module = node.module or ''
                        for alias in node.names:
                            imports.append({
                                'module': module,
                                'name': alias.name,
                                'type': 'from'
                            })

            return {
                'file': str(file_path.relative_to(self.repo_path)),
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.repo_path)),
                'error': str(e)
            }

    def build_dependency_graph(self):
        """Build dependency graph for all files."""
        file_map = {}

        # Create file map
        for file in self.python_files:
            rel_path = str(file.relative_to(self.repo_path))
            file_map[rel_path] = file

        # Analyze dependencies
        for file in self.python_files:
            analysis = self.analyze_file(file)
            if 'error' in analysis:
                continue

            file_name = analysis['file']

            # Track imports as dependencies
            for imp in analysis['imports']:
                module = imp['module']
                # Try to map import to actual file
                possible_paths = [
                    f"{module.replace('.', '/')}.py",
                    f"{module.replace('.', '/')}/__init__.py"
                ]

                for possible_path in possible_paths:
                    if possible_path in file_map:
                        self.dependency_graph[file_name].add(possible_path)
                        self.reverse_dependency_graph[possible_path].add(file_name)
                        break

    def find_components_by_keyword(self, keyword: str) -> List[Dict]:
        """Find components (classes, functions) matching keyword."""
        results = []
        keyword_lower = keyword.lower()

        for file in self.python_files:
            analysis = self.analyze_file(file)
            if 'error' in analysis:
                continue

            # Check functions
            for func in analysis['functions']:
                if keyword_lower in func['name'].lower():
                    results.append({
                        'type': 'function',
                        'file': analysis['file'],
                        'name': func['name'],
                        'line': func['line'],
                        'docstring': func['docstring']
                    })

            # Check classes and methods
            for cls in analysis['classes']:
                if keyword_lower in cls['name'].lower():
                    results.append({
                        'type': 'class',
                        'file': analysis['file'],
                        'name': cls['name'],
                        'line': cls['line'],
                        'docstring': cls['docstring']
                    })

                for method in cls['methods']:
                    if keyword_lower in method['name'].lower():
                        results.append({
                            'type': 'method',
                            'file': analysis['file'],
                            'class': cls['name'],
                            'name': method['name'],
                            'line': method['line']
                        })

        return results

    def get_dependencies(self, file_path: str) -> Set[str]:
        """Get direct dependencies of a file."""
        return self.dependency_graph.get(file_path, set())

    def get_dependents(self, file_path: str) -> Set[str]:
        """Get files that depend on this file."""
        return self.reverse_dependency_graph.get(file_path, set())

    def analyze_impact(self, affected_files: List[str]) -> Dict:
        """Analyze impact of changes to given files."""
        self.build_dependency_graph()

        direct_impact = set(affected_files)
        indirect_impact = set()

        # Find all files that depend on affected files
        for file in affected_files:
            dependents = self.get_dependents(file)
            indirect_impact.update(dependents)

        # Remove direct impact from indirect
        indirect_impact -= direct_impact

        return {
            'direct_impact': list(direct_impact),
            'indirect_impact': list(indirect_impact),
            'total_affected': len(direct_impact) + len(indirect_impact)
        }

    def generate_report(self) -> str:
        """Generate code structure report."""
        self.build_dependency_graph()

        report = []
        report.append("=" * 60)
        report.append("CODE STRUCTURE ANALYSIS")
        report.append("=" * 60)
        report.append(f"\nRepository: {self.repo_path}")

        # Statistics
        total_files = len(self.python_files)
        total_functions = 0
        total_classes = 0
        total_lines = 0

        for file in self.python_files:
            analysis = self.analyze_file(file)
            if 'error' not in analysis:
                total_functions += len(analysis['functions'])
                total_classes += len(analysis['classes'])
                total_lines += analysis['lines']

        report.append(f"\n📊 Statistics:")
        report.append(f"  Total files: {total_files}")
        report.append(f"  Total functions: {total_functions}")
        report.append(f"  Total classes: {total_classes}")
        report.append(f"  Total lines: {total_lines}")

        # Dependency information
        report.append(f"\n🔗 Dependencies:")
        report.append(f"  Files with dependencies: {len(self.dependency_graph)}")

        # Most depended-upon files
        dep_counts = [(f, len(deps)) for f, deps in self.reverse_dependency_graph.items()]
        dep_counts.sort(key=lambda x: x[1], reverse=True)

        if dep_counts:
            report.append(f"\n  Most depended-upon files:")
            for file, count in dep_counts[:5]:
                report.append(f"    {file}: {count} dependents")

        return "\n".join(report)


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_code_impact.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not Path(repo_path).exists():
        print(f"Error: Path '{repo_path}' not found")
        sys.exit(1)

    analyzer = CodeImpactAnalyzer(repo_path)
    print(analyzer.generate_report())


if __name__ == '__main__':
    main()
