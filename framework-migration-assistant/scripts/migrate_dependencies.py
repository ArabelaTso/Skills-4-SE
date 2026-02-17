#!/usr/bin/env python3
"""
Migrate dependencies from source framework to target framework.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class DependencyMigrator:
    """Handles dependency migration between frameworks."""

    def __init__(self, repo_path: Path, source_framework: str, target_framework: str):
        self.repo_path = repo_path
        self.source_framework = source_framework
        self.target_framework = target_framework
        self.changes = []

    def migrate(self) -> bool:
        """Execute dependency migration."""
        success = True

        # Migrate requirements.txt
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            if not self._migrate_requirements(requirements_file):
                success = False

        # Migrate pyproject.toml
        pyproject_file = self.repo_path / "pyproject.toml"
        if pyproject_file.exists():
            if not self._migrate_pyproject(pyproject_file):
                success = False

        return success

    def _migrate_requirements(self, file_path: Path) -> bool:
        """Migrate requirements.txt file."""
        try:
            content = file_path.read_text()
            original_content = content

            # Define dependency mappings
            if self.source_framework == "flask" and self.target_framework == "fastapi":
                replacements = {
                    r'flask[>=<\d.]*': 'fastapi>=0.104.0',
                    r'werkzeug[>=<\d.]*': 'uvicorn[standard]>=0.24.0',
                    r'flask-cors[>=<\d.]*': 'fastapi-cors>=0.0.6',
                    r'flask-sqlalchemy[>=<\d.]*': 'sqlalchemy>=2.0.0',
                }

                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

                # Add FastAPI-specific dependencies if not present
                if 'pydantic' not in content.lower():
                    content += '\npydantic>=2.0.0'
                if 'uvicorn' not in content.lower():
                    content += '\nuvicorn[standard]>=0.24.0'

            elif self.source_framework == "django" and self.target_framework == "fastapi":
                replacements = {
                    r'django[>=<\d.]*': 'fastapi>=0.104.0',
                    r'djangorestframework[>=<\d.]*': 'pydantic>=2.0.0',
                }

                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

                # Add FastAPI dependencies
                if 'uvicorn' not in content.lower():
                    content += '\nuvicorn[standard]>=0.24.0'
                if 'sqlalchemy' not in content.lower():
                    content += '\nsqlalchemy>=2.0.0'

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "dependency",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Updated dependencies for target framework"
                })
                print(f"✓ Updated {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def _migrate_pyproject(self, file_path: Path) -> bool:
        """Migrate pyproject.toml file."""
        try:
            content = file_path.read_text()
            original_content = content

            # Similar replacements for pyproject.toml
            if self.source_framework == "flask" and self.target_framework == "fastapi":
                replacements = {
                    r'"flask[^"]*"': '"fastapi>=0.104.0"',
                    r'"werkzeug[^"]*"': '"uvicorn[standard]>=0.24.0"',
                }

                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "dependency",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Updated dependencies in pyproject.toml"
                })
                print(f"✓ Updated {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
