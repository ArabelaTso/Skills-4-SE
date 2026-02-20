#!/usr/bin/env python3
"""
Analyze differences between old and new Python code versions.

Usage:
    python analyze_code_diff.py <old_file> <new_file>
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from difflib import unified_diff


class CodeDiffAnalyzer:
    def __init__(self, old_file: str, new_file: str):
        self.old_file = Path(old_file)
        self.new_file = Path(new_file)
        self.old_content = self.old_file.read_text(encoding='utf-8')
        self.new_content = self.new_file.read_text(encoding='utf-8')

    def get_text_diff(self) -> str:
        """Get unified diff of the two files."""
        old_lines = self.old_content.splitlines(keepends=True)
        new_lines = self.new_content.splitlines(keepends=True)

        diff = unified_diff(
            old_lines,
            new_lines,
            fromfile=str(self.old_file),
            tofile=str(self.new_file),
            lineterm=''
        )

        return ''.join(diff)

    def analyze_functions(self, content: str) -> Dict[str, Dict]:
        """Analyze functions in code."""
        try:
            tree = ast.parse(content)
            functions = {}

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get function signature
                    args = [arg.arg for arg in node.args.args]
                    defaults = [ast.unparse(d) for d in node.args.defaults] if node.args.defaults else []

                    functions[node.name] = {
                        'line': node.lineno,
                        'args': args,
                        'defaults': defaults,
                        'returns': ast.unparse(node.returns) if node.returns else None,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    }

            return functions
        except Exception as e:
            return {}

    def analyze_classes(self, content: str) -> Dict[str, Dict]:
        """Analyze classes in code."""
        try:
            tree = ast.parse(content)
            classes = {}

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            args = [arg.arg for arg in item.args.args]
                            methods.append({
                                'name': item.name,
                                'args': args,
                                'line': item.lineno
                            })

                    classes[node.name] = {
                        'line': node.lineno,
                        'methods': methods,
                        'bases': [ast.unparse(base) for base in node.bases]
                    }

            return classes
        except Exception as e:
            return {}

    def compare_functions(self) -> Dict:
        """Compare functions between old and new versions."""
        old_functions = self.analyze_functions(self.old_content)
        new_functions = self.analyze_functions(self.new_content)

        added = set(new_functions.keys()) - set(old_functions.keys())
        removed = set(old_functions.keys()) - set(new_functions.keys())
        common = set(old_functions.keys()) & set(new_functions.keys())

        modified = []
        for name in common:
            old_func = old_functions[name]
            new_func = new_functions[name]

            changes = []
            if old_func['args'] != new_func['args']:
                changes.append('signature')
            if old_func['returns'] != new_func['returns']:
                changes.append('return_type')
            if old_func['is_async'] != new_func['is_async']:
                changes.append('async')

            if changes:
                modified.append({
                    'name': name,
                    'changes': changes,
                    'old': old_func,
                    'new': new_func
                })

        return {
            'added': list(added),
            'removed': list(removed),
            'modified': modified
        }

    def compare_classes(self) -> Dict:
        """Compare classes between old and new versions."""
        old_classes = self.analyze_classes(self.old_content)
        new_classes = self.analyze_classes(self.new_content)

        added = set(new_classes.keys()) - set(old_classes.keys())
        removed = set(old_classes.keys()) - set(new_classes.keys())
        common = set(old_classes.keys()) & set(new_classes.keys())

        modified = []
        for name in common:
            old_class = old_classes[name]
            new_class = new_classes[name]

            changes = []

            # Check for method changes
            old_methods = {m['name'] for m in old_class['methods']}
            new_methods = {m['name'] for m in new_class['methods']}

            if old_methods != new_methods:
                changes.append('methods')

            # Check for base class changes
            if old_class['bases'] != new_class['bases']:
                changes.append('inheritance')

            if changes:
                modified.append({
                    'name': name,
                    'changes': changes,
                    'old': old_class,
                    'new': new_class
                })

        return {
            'added': list(added),
            'removed': list(removed),
            'modified': modified
        }

    def generate_report(self) -> str:
        """Generate analysis report."""
        report = []
        report.append("=" * 60)
        report.append("CODE DIFFERENCE ANALYSIS")
        report.append("=" * 60)
        report.append(f"\nOld: {self.old_file}")
        report.append(f"New: {self.new_file}")

        # Function changes
        func_changes = self.compare_functions()
        report.append(f"\n📝 Function Changes:")

        if func_changes['added']:
            report.append(f"\n  Added Functions:")
            for name in func_changes['added']:
                report.append(f"    + {name}()")

        if func_changes['removed']:
            report.append(f"\n  Removed Functions:")
            for name in func_changes['removed']:
                report.append(f"    - {name}()")

        if func_changes['modified']:
            report.append(f"\n  Modified Functions:")
            for func in func_changes['modified']:
                report.append(f"    ~ {func['name']}()")
                report.append(f"      Changes: {', '.join(func['changes'])}")
                if 'signature' in func['changes']:
                    report.append(f"      Old args: {func['old']['args']}")
                    report.append(f"      New args: {func['new']['args']}")

        # Class changes
        class_changes = self.compare_classes()
        report.append(f"\n🏛️  Class Changes:")

        if class_changes['added']:
            report.append(f"\n  Added Classes:")
            for name in class_changes['added']:
                report.append(f"    + {name}")

        if class_changes['removed']:
            report.append(f"\n  Removed Classes:")
            for name in class_changes['removed']:
                report.append(f"    - {name}")

        if class_changes['modified']:
            report.append(f"\n  Modified Classes:")
            for cls in class_changes['modified']:
                report.append(f"    ~ {cls['name']}")
                report.append(f"      Changes: {', '.join(cls['changes'])}")

        # Text diff
        report.append(f"\n📄 Text Diff:")
        report.append(self.get_text_diff())

        return "\n".join(report)


def main():
    if len(sys.argv) != 3:
        print("Usage: python analyze_code_diff.py <old_file> <new_file>")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]

    if not Path(old_file).exists():
        print(f"Error: File '{old_file}' not found")
        sys.exit(1)

    if not Path(new_file).exists():
        print(f"Error: File '{new_file}' not found")
        sys.exit(1)

    analyzer = CodeDiffAnalyzer(old_file, new_file)
    print(analyzer.generate_report())


if __name__ == '__main__':
    main()
