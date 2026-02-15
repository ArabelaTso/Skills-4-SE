#!/usr/bin/env python3
"""
Analyze Python repository structure to understand codebase organization.

Usage:
    python analyze_repo_structure.py <repo_path>
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.python_files = self._find_python_files()

    def _find_python_files(self) -> List[Path]:
        """Find all Python files in repository."""
        files = []
        for path in self.repo_path.rglob("*.py"):
            # Skip common ignore directories
            if any(part in path.parts for part in ['.git', '__pycache__', 'venv', '.venv', 'env']):
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
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'methods': methods
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    else:
                        module = node.module or ''
                        imports.append(module)

            return {
                'file': str(file_path.relative_to(self.repo_path)),
                'functions': functions,
                'classes': classes,
                'imports': list(set(imports)),
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.repo_path)),
                'error': str(e)
            }

    def find_test_files(self) -> List[Path]:
        """Find test files in repository."""
        test_files = []
        for file in self.python_files:
            if 'test' in file.name or 'tests' in file.parts:
                test_files.append(file)
        return test_files

    def find_main_modules(self) -> List[Path]:
        """Find main application modules (non-test files)."""
        test_files = set(self.find_test_files())
        return [f for f in self.python_files if f not in test_files]

    def analyze_structure(self) -> Dict:
        """Analyze overall repository structure."""
        test_files = self.find_test_files()
        main_files = self.find_main_modules()

        # Analyze all files
        file_analyses = []
        for file in main_files:
            analysis = self.analyze_file(file)
            if 'error' not in analysis:
                file_analyses.append(analysis)

        # Collect statistics
        total_functions = sum(len(a['functions']) for a in file_analyses)
        total_classes = sum(len(a['classes']) for a in file_analyses)
        total_lines = sum(a['lines'] for a in file_analyses)

        # Find common imports
        all_imports = []
        for analysis in file_analyses:
            all_imports.extend(analysis['imports'])

        import_counts = {}
        for imp in all_imports:
            import_counts[imp] = import_counts.get(imp, 0) + 1

        common_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'total_files': len(main_files),
            'test_files': len(test_files),
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_lines': total_lines,
            'common_imports': common_imports,
            'file_details': file_analyses
        }

    def generate_report(self) -> str:
        """Generate analysis report."""
        structure = self.analyze_structure()

        report = []
        report.append("=" * 60)
        report.append("PYTHON REPOSITORY STRUCTURE ANALYSIS")
        report.append("=" * 60)
        report.append(f"\nRepository: {self.repo_path}")

        report.append(f"\n📊 Statistics:")
        report.append(f"  Total Python files: {structure['total_files']}")
        report.append(f"  Test files: {structure['test_files']}")
        report.append(f"  Total functions: {structure['total_functions']}")
        report.append(f"  Total classes: {structure['total_classes']}")
        report.append(f"  Total lines of code: {structure['total_lines']}")

        if structure['common_imports']:
            report.append(f"\n📦 Most Common Imports:")
            for imp, count in structure['common_imports']:
                report.append(f"  {imp}: {count} files")

        report.append(f"\n📁 File Details:")
        for file_info in structure['file_details'][:10]:  # Show first 10 files
            report.append(f"\n  {file_info['file']}")
            report.append(f"    Lines: {file_info['lines']}")
            report.append(f"    Functions: {len(file_info['functions'])}")
            report.append(f"    Classes: {len(file_info['classes'])}")

            if file_info['classes']:
                report.append(f"    Class names: {', '.join(c['name'] for c in file_info['classes'])}")

        if len(structure['file_details']) > 10:
            report.append(f"\n  ... and {len(structure['file_details']) - 10} more files")

        return "\n".join(report)


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo_structure.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not Path(repo_path).exists():
        print(f"Error: Path '{repo_path}' not found")
        sys.exit(1)

    analyzer = RepoAnalyzer(repo_path)
    print(analyzer.generate_report())


if __name__ == '__main__':
    main()
