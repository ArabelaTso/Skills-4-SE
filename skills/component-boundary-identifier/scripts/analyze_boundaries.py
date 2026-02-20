#!/usr/bin/env python3
"""
Analyze Python project structure to identify component boundaries and violations.

This script analyzes import statements to:
- Identify module boundaries
- Detect circular dependencies
- Find layer violations
- Report coupling metrics

Usage:
    python analyze_boundaries.py <project_directory>
"""

import ast
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


class BoundaryAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.modules: Set[str] = set()
        self.boundaries: Dict[str, Set[str]] = defaultdict(set)

    def analyze(self):
        """Analyze the project structure."""
        print(f"Analyzing project: {self.project_root}\n")

        # Find all Python files
        python_files = list(self.project_root.rglob("*.py"))
        print(f"Found {len(python_files)} Python files\n")

        # Extract imports from each file
        for file_path in python_files:
            module_name = self._get_module_name(file_path)
            if module_name:
                self.modules.add(module_name)
                imports = self._extract_imports(file_path)
                self.imports[module_name] = imports

        # Identify boundaries
        self._identify_boundaries()

        # Report findings
        self._report_boundaries()
        self._report_violations()
        self._report_circular_dependencies()

    def _get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name."""
        try:
            rel_path = file_path.relative_to(self.project_root)
            parts = list(rel_path.parts[:-1]) + [rel_path.stem]
            if parts[-1] == "__init__":
                parts = parts[:-1]
            return ".".join(parts) if parts else ""
        except ValueError:
            return ""

    def _extract_imports(self, file_path: Path) -> Set[str]:
        """Extract import statements from a Python file."""
        imports = set()

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])

        except (SyntaxError, UnicodeDecodeError):
            pass

        return imports

    def _identify_boundaries(self):
        """Identify component boundaries based on top-level packages."""
        for module in self.modules:
            parts = module.split(".")
            if parts:
                boundary = parts[0]
                self.boundaries[boundary].add(module)

    def _report_boundaries(self):
        """Report identified boundaries."""
        print("=" * 80)
        print("IDENTIFIED BOUNDARIES")
        print("=" * 80)

        for boundary, modules in sorted(self.boundaries.items()):
            print(f"\n{boundary}/ ({len(modules)} modules)")
            for module in sorted(modules)[:5]:  # Show first 5
                print(f"  - {module}")
            if len(modules) > 5:
                print(f"  ... and {len(modules) - 5} more")

    def _report_violations(self):
        """Report boundary violations."""
        print("\n" + "=" * 80)
        print("BOUNDARY VIOLATIONS")
        print("=" * 80)

        violations = []

        # Check for common violation patterns
        for module, imports in self.imports.items():
            module_boundary = module.split(".")[0] if "." in module else module

            for imported in imports:
                # Check if it's a project module
                if imported not in self.boundaries:
                    continue

                # Check for violations
                violation = self._check_violation(module_boundary, imported, module)
                if violation:
                    violations.append(violation)

        if violations:
            for severity, msg in sorted(violations, key=lambda x: x[0]):
                print(f"\n[{severity}] {msg}")
        else:
            print("\nNo boundary violations detected!")

    def _check_violation(
        self, module_boundary: str, imported_boundary: str, module: str
    ) -> Tuple[str, str]:
        """Check if an import represents a boundary violation."""

        # Define architectural layers
        layers = {
            "api": 3,
            "application": 3,
            "web": 3,
            "domain": 2,
            "service": 2,
            "business": 2,
            "infrastructure": 1,
            "persistence": 1,
            "data": 1,
        }

        module_layer = layers.get(module_boundary, 0)
        imported_layer = layers.get(imported_boundary, 0)

        # Check for upward dependencies (lower layer depending on higher layer)
        if module_layer < imported_layer:
            return (
                "CRITICAL",
                f"{module} (layer {module_layer}) depends on {imported_boundary} (layer {imported_layer})",
            )

        # Check for domain depending on infrastructure
        if module_boundary in ["domain", "business"] and imported_boundary in [
            "infrastructure",
            "persistence",
        ]:
            return (
                "CRITICAL",
                f"{module} (domain) depends on {imported_boundary} (infrastructure)",
            )

        return None

    def _report_circular_dependencies(self):
        """Report circular dependencies."""
        print("\n" + "=" * 80)
        print("CIRCULAR DEPENDENCIES")
        print("=" * 80)

        visited = set()
        cycles = []

        for module in self.modules:
            if module not in visited:
                cycle = self._find_cycle(module, set(), [])
                if cycle:
                    cycles.append(cycle)
                    visited.update(cycle)

        if cycles:
            for i, cycle in enumerate(cycles, 1):
                print(f"\nCycle {i}:")
                for module in cycle:
                    print(f"  {module}")
                print(f"  └─> {cycle[0]} (circular)")
        else:
            print("\nNo circular dependencies detected!")

    def _find_cycle(
        self, module: str, visiting: Set[str], path: List[str]
    ) -> List[str]:
        """Find circular dependency starting from module."""
        if module in visiting:
            # Found a cycle
            cycle_start = path.index(module)
            return path[cycle_start:] + [module]

        visiting.add(module)
        path.append(module)

        for imported in self.imports.get(module, []):
            # Only check project modules
            if imported in self.modules:
                cycle = self._find_cycle(imported, visiting.copy(), path.copy())
                if cycle:
                    return cycle

        return []


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_boundaries.py <project_directory>")
        sys.exit(1)

    project_dir = sys.argv[1]

    if not os.path.isdir(project_dir):
        print(f"Error: '{project_dir}' is not a valid directory")
        sys.exit(1)

    analyzer = BoundaryAnalyzer(project_dir)
    analyzer.analyze()


if __name__ == "__main__":
    main()
