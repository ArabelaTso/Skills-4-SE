#!/usr/bin/env python3
"""
Analyze Python repository structure and generate quick start guide.

Usage:
    python analyze_repo.py <repo_path>
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class PythonRepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.files = self._scan_files()

    def _scan_files(self) -> Set[Path]:
        """Scan repository for relevant files."""
        files = set()
        for root, dirs, filenames in os.walk(self.repo_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'venv', '.venv', 'node_modules', '.tox'}]

            for filename in filenames:
                file_path = Path(root) / filename
                files.add(file_path.relative_to(self.repo_path))
        return files

    def identify_project_type(self) -> str:
        """Identify the type of Python project."""
        file_names = {f.name for f in self.files}

        if 'manage.py' in file_names:
            return "Django Web Application"
        elif any('flask' in str(f).lower() for f in self.files):
            return "Flask Web Application"
        elif any('fastapi' in str(f).lower() for f in self.files):
            return "FastAPI Web Application"
        elif any(f.suffix == '.ipynb' for f in self.files):
            return "Data Science / Jupyter Project"
        elif 'setup.py' in file_names or 'pyproject.toml' in file_names:
            if any(f.name in {'cli.py', '__main__.py'} for f in self.files):
                return "CLI Tool / Package"
            return "Python Package / Library"
        elif 'main.py' in file_names:
            return "Python Application"
        else:
            return "Python Project"

    def find_entry_points(self) -> List[str]:
        """Find potential entry points."""
        entry_points = []

        entry_files = ['main.py', 'app.py', 'run.py', 'manage.py', 'cli.py', '__main__.py']
        for entry in entry_files:
            if any(f.name == entry for f in self.files):
                entry_points.append(entry)

        return entry_points

    def find_dependencies(self) -> Dict[str, Path]:
        """Find dependency files."""
        dep_files = {}

        dep_patterns = {
            'requirements.txt': 'pip',
            'requirements-dev.txt': 'pip (dev)',
            'Pipfile': 'Pipenv',
            'poetry.lock': 'Poetry',
            'pyproject.toml': 'Poetry/Modern',
            'environment.yml': 'Conda',
            'setup.py': 'setuptools'
        }

        for pattern, manager in dep_patterns.items():
            matching = [f for f in self.files if f.name == pattern]
            if matching:
                dep_files[manager] = matching[0]

        return dep_files

    def find_config_files(self) -> List[Path]:
        """Find configuration files."""
        config_patterns = ['.env', '.env.example', 'config.py', 'settings.py',
                          'pytest.ini', 'tox.ini', 'setup.cfg']

        configs = []
        for pattern in config_patterns:
            matching = [f for f in self.files if f.name == pattern]
            configs.extend(matching)

        return configs

    def analyze(self) -> Dict:
        """Perform full analysis."""
        return {
            'project_type': self.identify_project_type(),
            'entry_points': self.find_entry_points(),
            'dependencies': self.find_dependencies(),
            'config_files': self.find_config_files(),
            'has_tests': any('test' in str(f) for f in self.files),
            'has_docs': any(f.name in {'README.md', 'README.rst'} for f in self.files)
        }

    def generate_report(self) -> str:
        """Generate analysis report."""
        analysis = self.analyze()

        report = []
        report.append("=" * 60)
        report.append("PYTHON REPOSITORY ANALYSIS")
        report.append("=" * 60)
        report.append(f"\nProject Type: {analysis['project_type']}")

        if analysis['entry_points']:
            report.append(f"\nEntry Points:")
            for entry in analysis['entry_points']:
                report.append(f"  - {entry}")

        if analysis['dependencies']:
            report.append(f"\nDependency Management:")
            for manager, file in analysis['dependencies'].items():
                report.append(f"  - {manager}: {file}")

        if analysis['config_files']:
            report.append(f"\nConfiguration Files:")
            for config in analysis['config_files']:
                report.append(f"  - {config}")

        report.append(f"\nHas Tests: {'Yes' if analysis['has_tests'] else 'No'}")
        report.append(f"Has Documentation: {'Yes' if analysis['has_docs'] else 'No'}")

        return "\n".join(report)


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a valid directory")
        sys.exit(1)

    analyzer = PythonRepoAnalyzer(repo_path)
    print(analyzer.generate_report())


if __name__ == '__main__':
    main()
