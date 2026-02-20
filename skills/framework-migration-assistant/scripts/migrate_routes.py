#!/usr/bin/env python3
"""
Migrate routes and handlers from source framework to target framework.
"""

import re
import ast
from pathlib import Path
from typing import List, Dict, Any


class RouteMigrator:
    """Handles route and handler migration between frameworks."""

    def __init__(self, repo_path: Path, source_framework: str, target_framework: str):
        self.repo_path = repo_path
        self.source_framework = source_framework
        self.target_framework = target_framework
        self.changes = []

    def migrate(self) -> bool:
        """Execute route migration."""
        success = True

        # Find all Python files with routes
        for py_file in self.repo_path.rglob("*.py"):
            if "venv" in str(py_file) or "env" in str(py_file) or "test" in str(py_file):
                continue

            try:
                content = py_file.read_text()

                # Check if file contains routes
                if self._has_routes(content):
                    if not self._migrate_file(py_file):
                        success = False
            except Exception as e:
                print(f"Warning: Could not process {py_file}: {e}")

        return success

    def _has_routes(self, content: str) -> bool:
        """Check if file contains route definitions."""
        if self.source_framework == "flask":
            return "@app.route" in content or "@bp.route" in content
        elif self.source_framework == "django":
            return "path(" in content or "url(" in content
        return False

    def _migrate_file(self, file_path: Path) -> bool:
        """Migrate a single file."""
        try:
            content = file_path.read_text()
            original_content = content

            if self.source_framework == "flask" and self.target_framework == "fastapi":
                content = self._migrate_flask_to_fastapi(content)
            elif self.source_framework == "django" and self.target_framework == "fastapi":
                content = self._migrate_django_to_fastapi(content)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "route",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Migrated routes and handlers"
                })
                print(f"✓ Migrated routes in {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def _migrate_flask_to_fastapi(self, content: str) -> str:
        """Migrate Flask routes to FastAPI."""
        # Replace imports
        content = re.sub(
            r'from flask import ([^\\n]+)',
            r'from fastapi import FastAPI, Request, Response\nfrom pydantic import BaseModel',
            content,
            count=1
        )

        # Replace app initialization
        content = re.sub(
            r'app = Flask\(__name__\)',
            'app = FastAPI()',
            content
        )

        # Migrate route decorators
        # @app.route('/path', methods=['GET']) -> @app.get('/path')
        def replace_route(match):
            path = match.group(1)
            methods = match.group(2) if match.group(2) else "['GET']"

            if 'POST' in methods:
                return f'@app.post({path})'
            elif 'PUT' in methods:
                return f'@app.put({path})'
            elif 'DELETE' in methods:
                return f'@app.delete({path})'
            elif 'PATCH' in methods:
                return f'@app.patch({path})'
            else:
                return f'@app.get({path})'

        content = re.sub(
            r'@app\.route\(([^,)]+)(?:,\s*methods=(\[[^\]]+\]))?\)',
            replace_route,
            content
        )

        # Replace request handling
        content = re.sub(r'from flask import request', 'from fastapi import Request', content)
        content = re.sub(r'request\.args\.get\(', 'request.query_params.get(', content)
        content = re.sub(r'request\.form\.get\(', 'request.form().get(', content)
        content = re.sub(r'request\.json', 'await request.json()', content)

        # Replace response handling
        content = re.sub(r'jsonify\(([^)]+)\)', r'\1', content)
        content = re.sub(r'return ([^,\n]+), (\d+)', r'return Response(content=\1, status_code=\2)', content)

        # Add async to route handlers
        content = re.sub(
            r'(@app\.(get|post|put|delete|patch)\([^)]+\))\ndef ',
            r'\1\nasync def ',
            content
        )

        return content

    def _migrate_django_to_fastapi(self, content: str) -> str:
        """Migrate Django views to FastAPI."""
        # Replace imports
        content = re.sub(
            r'from django\.http import ([^\\n]+)',
            'from fastapi import FastAPI, Request, Response',
            content
        )

        # Migrate class-based views to FastAPI path operations
        # This is a simplified version - real migration would be more complex
        content = re.sub(
            r'class (\w+)\(View\):',
            r'# Migrated from Django View: \1\n# TODO: Convert to FastAPI path operations',
            content
        )

        # Migrate function-based views
        content = re.sub(
            r'def (\w+)\(request\):',
            r'@app.get("/\1")\nasync def \1(request: Request):',
            content
        )

        # Replace HttpResponse
        content = re.sub(r'HttpResponse\(([^)]+)\)', r'Response(content=\1)', content)
        content = re.sub(r'JsonResponse\(([^)]+)\)', r'\1', content)

        return content

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
