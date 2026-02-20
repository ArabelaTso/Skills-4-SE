#!/usr/bin/env python3
"""
Main migration orchestrator that coordinates the entire framework migration process.

Usage:
    python migrate.py <repo_path> --from <source_framework> --to <target_framework>
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import subprocess


class MigrationOrchestrator:
    """Orchestrates the entire framework migration process."""

    def __init__(self, repo_path: str, source_framework: str, target_framework: str):
        self.repo_path = Path(repo_path)
        self.source_framework = source_framework
        self.target_framework = target_framework
        self.changes = []
        self.migration_plan = {}

    def validate_repository(self) -> bool:
        """Validate that the repository exists and is a git repo."""
        if not self.repo_path.exists():
            print(f"Error: Repository path does not exist: {self.repo_path}")
            return False

        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            print(f"Error: Not a git repository: {self.repo_path}")
            return False

        return True

    def detect_framework(self) -> str:
        """Detect the current framework used in the repository."""
        # Check for Python frameworks
        requirements_file = self.repo_path / "requirements.txt"
        pyproject_file = self.repo_path / "pyproject.toml"

        if requirements_file.exists():
            content = requirements_file.read_text()
            if "flask" in content.lower():
                return "flask"
            elif "django" in content.lower():
                return "django"
            elif "fastapi" in content.lower():
                return "fastapi"

        if pyproject_file.exists():
            content = pyproject_file.read_text()
            if "flask" in content.lower():
                return "flask"
            elif "django" in content.lower():
                return "django"
            elif "fastapi" in content.lower():
                return "fastapi"

        return "unknown"

    def create_migration_branch(self) -> bool:
        """Create a new git branch for the migration."""
        branch_name = f"migrate-{self.source_framework}-to-{self.target_framework}"

        try:
            # Check if branch already exists
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"Branch {branch_name} already exists. Using existing branch.")
            else:
                # Create new branch
                subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=self.repo_path,
                    check=True
                )
                print(f"Created migration branch: {branch_name}")

            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch: {e}")
            return False

    def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the codebase to understand its structure."""
        analysis = {
            "routes": [],
            "models": [],
            "config_files": [],
            "test_files": [],
            "dependencies": []
        }

        # Find Python files
        for py_file in self.repo_path.rglob("*.py"):
            if "venv" in str(py_file) or "env" in str(py_file):
                continue

            relative_path = py_file.relative_to(self.repo_path)

            # Categorize files
            if "test" in str(py_file).lower():
                analysis["test_files"].append(str(relative_path))
            elif "model" in str(py_file).lower():
                analysis["models"].append(str(relative_path))
            else:
                # Check if it contains routes
                content = py_file.read_text(errors='ignore')
                if "@app.route" in content or "@router" in content:
                    analysis["routes"].append(str(relative_path))

        # Find config files
        for config_file in ["config.py", "settings.py", "requirements.txt", "pyproject.toml"]:
            config_path = self.repo_path / config_file
            if config_path.exists():
                analysis["config_files"].append(config_file)

        return analysis

    def generate_migration_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed migration plan."""
        plan = {
            "source_framework": self.source_framework,
            "target_framework": self.target_framework,
            "steps": [],
            "files_to_modify": [],
            "files_to_create": [],
            "dependencies_to_update": []
        }

        # Add migration steps based on frameworks
        if self.source_framework == "flask" and self.target_framework == "fastapi":
            plan["steps"] = [
                "Update dependencies (Flask → FastAPI)",
                "Migrate route decorators (@app.route → @app.get/post)",
                "Update request/response handling",
                "Migrate configuration",
                "Update dependency injection patterns",
                "Adapt tests for FastAPI TestClient"
            ]

            plan["files_to_modify"] = analysis["routes"] + analysis["config_files"]
            plan["dependencies_to_update"] = ["flask", "werkzeug"]

        elif self.source_framework == "django" and self.target_framework == "fastapi":
            plan["steps"] = [
                "Update dependencies (Django → FastAPI)",
                "Migrate URL patterns to FastAPI routes",
                "Convert Django views to FastAPI path operations",
                "Migrate models (Django ORM → SQLAlchemy/Pydantic)",
                "Update configuration and settings",
                "Adapt tests for FastAPI"
            ]

            plan["files_to_modify"] = analysis["routes"] + analysis["models"] + analysis["config_files"]

        self.migration_plan = plan
        return plan

    def execute_migration(self) -> bool:
        """Execute the migration plan."""
        print("\n=== Executing Migration ===\n")

        # Import migration modules
        from migrate_dependencies import DependencyMigrator
        from migrate_routes import RouteMigrator
        from migrate_config import ConfigMigrator
        from migrate_tests import TestMigrator

        success = True

        # Step 1: Migrate dependencies
        print("Step 1: Migrating dependencies...")
        dep_migrator = DependencyMigrator(self.repo_path, self.source_framework, self.target_framework)
        if dep_migrator.migrate():
            self.changes.extend(dep_migrator.get_changes())
            self._commit_changes("Migrate dependencies")
        else:
            success = False

        # Step 2: Migrate routes
        print("\nStep 2: Migrating routes...")
        route_migrator = RouteMigrator(self.repo_path, self.source_framework, self.target_framework)
        if route_migrator.migrate():
            self.changes.extend(route_migrator.get_changes())
            self._commit_changes("Migrate routes and handlers")
        else:
            success = False

        # Step 3: Migrate configuration
        print("\nStep 3: Migrating configuration...")
        config_migrator = ConfigMigrator(self.repo_path, self.source_framework, self.target_framework)
        if config_migrator.migrate():
            self.changes.extend(config_migrator.get_changes())
            self._commit_changes("Migrate configuration")
        else:
            success = False

        # Step 4: Migrate tests
        print("\nStep 4: Migrating tests...")
        test_migrator = TestMigrator(self.repo_path, self.source_framework, self.target_framework)
        if test_migrator.migrate():
            self.changes.extend(test_migrator.get_changes())
            self._commit_changes("Migrate tests")
        else:
            success = False

        return success

    def _commit_changes(self, message: str):
        """Commit changes to git."""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"{message}\n\nCo-Authored-By: Framework Migration Assistant <noreply@anthropic.com>"],
                cwd=self.repo_path,
                check=True
            )
            print(f"✓ Committed: {message}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not commit changes: {e}")

    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of all changes made."""
        summary = {
            "source_framework": self.source_framework,
            "target_framework": self.target_framework,
            "total_changes": len(self.changes),
            "changes_by_type": {},
            "files_modified": [],
            "migration_plan": self.migration_plan,
            "next_steps": []
        }

        # Categorize changes
        for change in self.changes:
            change_type = change.get("type", "other")
            if change_type not in summary["changes_by_type"]:
                summary["changes_by_type"][change_type] = 0
            summary["changes_by_type"][change_type] += 1

            if "file" in change:
                summary["files_modified"].append(change["file"])

        # Add next steps
        summary["next_steps"] = [
            "Review the migration commits",
            "Run tests to verify functionality",
            "Update documentation if needed",
            "Test the application manually",
            "Merge the migration branch when ready"
        ]

        return summary

    def run(self) -> bool:
        """Run the complete migration process."""
        print(f"=== Framework Migration Assistant ===")
        print(f"Repository: {self.repo_path}")
        print(f"Migration: {self.source_framework} → {self.target_framework}\n")

        # Step 1: Validate
        if not self.validate_repository():
            return False

        # Step 2: Detect framework if not specified
        if self.source_framework == "auto":
            detected = self.detect_framework()
            if detected == "unknown":
                print("Error: Could not detect source framework")
                return False
            self.source_framework = detected
            print(f"Detected source framework: {self.source_framework}\n")

        # Step 3: Create migration branch
        if not self.create_migration_branch():
            return False

        # Step 4: Analyze codebase
        print("\nAnalyzing codebase...")
        analysis = self.analyze_codebase()
        print(f"Found {len(analysis['routes'])} route files")
        print(f"Found {len(analysis['test_files'])} test files")
        print(f"Found {len(analysis['config_files'])} config files\n")

        # Step 5: Generate migration plan
        print("Generating migration plan...")
        plan = self.generate_migration_plan(analysis)
        print(f"Migration plan created with {len(plan['steps'])} steps\n")

        # Step 6: Execute migration
        if not self.execute_migration():
            print("\n⚠ Migration completed with errors")
            return False

        # Step 7: Generate summary
        print("\n=== Migration Summary ===\n")
        summary = self.generate_summary()

        # Save summary to file
        summary_file = self.repo_path / "MIGRATION_SUMMARY.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"Total changes: {summary['total_changes']}")
        print(f"Files modified: {len(summary['files_modified'])}")
        print(f"\nSummary saved to: {summary_file}")

        print("\n✓ Migration completed successfully!")
        print("\nNext steps:")
        for step in summary["next_steps"]:
            print(f"  - {step}")

        return True


def main():
    parser = argparse.ArgumentParser(description="Framework Migration Assistant")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--from", dest="source_framework", required=True,
                       help="Source framework (flask, django, or auto)")
    parser.add_argument("--to", dest="target_framework", required=True,
                       help="Target framework (fastapi, etc.)")

    args = parser.parse_args()

    orchestrator = MigrationOrchestrator(
        args.repo_path,
        args.source_framework,
        args.target_framework
    )

    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
