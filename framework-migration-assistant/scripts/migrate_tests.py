#!/usr/bin/env python3
"""
Migrate tests from source framework to target framework.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class TestMigrator:
    """Handles test migration between frameworks."""

    def __init__(self, repo_path: Path, source_framework: str, target_framework: str):
        self.repo_path = repo_path
        self.source_framework = source_framework
        self.target_framework = target_framework
        self.changes = []

    def migrate(self) -> bool:
        """Execute test migration."""
        success = True

        # Find all test files
        for test_file in self.repo_path.rglob("test_*.py"):
            if "venv" not in str(test_file) and "env" not in str(test_file):
                if not self._migrate_test_file(test_file):
                    success = False

        for test_file in self.repo_path.rglob("*_test.py"):
            if "venv" not in str(test_file) and "env" not in str(test_file):
                if not self._migrate_test_file(test_file):
                    success = False

        return success

    def _migrate_test_file(self, file_path: Path) -> bool:
        """Migrate a single test file."""
        try:
            content = file_path.read_text()
            original_content = content

            if self.source_framework == "flask" and self.target_framework == "fastapi":
                content = self._migrate_flask_tests_to_fastapi(content)
            elif self.source_framework == "django" and self.target_framework == "fastapi":
                content = self._migrate_django_tests_to_fastapi(content)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "test",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Migrated tests"
                })
                print(f"✓ Migrated tests in {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def _migrate_flask_tests_to_fastapi(self, content: str) -> str:
        """Migrate Flask tests to FastAPI."""
        # Replace imports
        content = re.sub(
            r'from flask import ([^\\n]+)',
            'from fastapi.testclient import TestClient',
            content,
            count=1
        )

        # Replace test client initialization
        content = re.sub(
            r'client = app\.test_client\(\)',
            'client = TestClient(app)',
            content
        )

        # Replace test client calls
        # Flask: response = client.get('/path')
        # FastAPI: response = client.get('/path')
        # (mostly compatible, but response format differs)

        # Replace response assertions
        content = re.sub(
            r'response\.get_json\(\)',
            'response.json()',
            content
        )

        content = re.sub(
            r'response\.status_code',
            'response.status_code',
            content
        )

        # Replace Flask test context
        content = re.sub(
            r'with app\.app_context\(\):',
            '# FastAPI does not require app context',
            content
        )

        # Add pytest-asyncio if async tests are needed
        if 'async def test_' in content:
            if 'import pytest' not in content:
                content = 'import pytest\n' + content
            content = re.sub(
                r'async def (test_\w+)',
                r'@pytest.mark.asyncio\nasync def \1',
                content
            )

        return content

    def _migrate_django_tests_to_fastapi(self, content: str) -> str:
        """Migrate Django tests to FastAPI."""
        # Replace imports
        content = re.sub(
            r'from django\.test import ([^\\n]+)',
            'from fastapi.testclient import TestClient\nimport pytest',
            content
        )

        # Replace TestCase classes
        content = re.sub(
            r'class (\w+)\(TestCase\):',
            r'class \1:',
            content
        )

        # Replace Django test client
        content = re.sub(
            r'self\.client\.get\(',
            'client.get(',
            content
        )

        content = re.sub(
            r'self\.client\.post\(',
            'client.post(',
            content
        )

        # Replace assertions
        content = re.sub(
            r'self\.assertEqual\(([^,]+),\s*([^)]+)\)',
            r'assert \1 == \2',
            content
        )

        content = re.sub(
            r'self\.assertTrue\(([^)]+)\)',
            r'assert \1',
            content
        )

        content = re.sub(
            r'self\.assertFalse\(([^)]+)\)',
            r'assert not \1',
            content
        )

        return content

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
