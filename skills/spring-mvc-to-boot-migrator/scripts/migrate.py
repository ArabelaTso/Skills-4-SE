#!/usr/bin/env python3
"""
Main migration orchestrator for Spring MVC to Spring Boot migration.

Usage:
    python migrate.py <repo_path> [--build-tool <maven|gradle>]
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import xml.etree.ElementTree as ET


class SpringMigrationOrchestrator:
    """Orchestrates Spring MVC to Spring Boot migration."""

    def __init__(self, repo_path: str, build_tool: str = 'auto'):
        self.repo_path = Path(repo_path)
        self.build_tool = build_tool
        self.changes = []
        self.migration_plan = {}

    def validate_repository(self) -> bool:
        """Validate repository exists and is a git repo."""
        if not self.repo_path.exists():
            print(f"Error: Repository path does not exist: {self.repo_path}")
            return False

        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            print(f"Error: Not a git repository: {self.repo_path}")
            return False

        return True

    def detect_build_tool(self) -> str:
        """Detect build tool (Maven or Gradle)."""
        if (self.repo_path / "pom.xml").exists():
            return "maven"
        elif (self.repo_path / "build.gradle").exists() or (self.repo_path / "build.gradle.kts").exists():
            return "gradle"
        return "unknown"

    def detect_spring_version(self) -> str:
        """Detect current Spring Framework version."""
        if self.build_tool == "maven":
            pom_file = self.repo_path / "pom.xml"
            if pom_file.exists():
                try:
                    tree = ET.parse(pom_file)
                    root = tree.getroot()
                    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

                    # Check for Spring version property
                    for prop in root.findall('.//m:properties/*', ns):
                        if 'spring' in prop.tag.lower() and 'version' in prop.tag.lower():
                            return prop.text

                    # Check dependencies
                    for dep in root.findall('.//m:dependency', ns):
                        artifact = dep.find('m:artifactId', ns)
                        version = dep.find('m:version', ns)
                        if artifact is not None and 'spring' in artifact.text.lower():
                            if version is not None:
                                return version.text
                except Exception as e:
                    print(f"Warning: Could not parse pom.xml: {e}")

        return "unknown"

    def create_migration_branch(self) -> bool:
        """Create git branch for migration."""
        branch_name = "migrate-spring-mvc-to-boot"

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"Branch {branch_name} already exists. Using existing branch.")
            else:
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
        """Analyze codebase structure."""
        analysis = {
            "controllers": [],
            "services": [],
            "config_files": [],
            "test_files": [],
            "xml_configs": [],
            "properties_files": []
        }

        # Find Java files
        for java_file in self.repo_path.rglob("*.java"):
            if "target" in str(java_file) or "build" in str(java_file):
                continue

            relative_path = java_file.relative_to(self.repo_path)
            content = java_file.read_text(errors='ignore')

            # Categorize files
            if "test" in str(java_file).lower() or "Test.java" in str(java_file):
                analysis["test_files"].append(str(relative_path))
            elif "@Controller" in content or "@RestController" in content:
                analysis["controllers"].append(str(relative_path))
            elif "@Service" in content or "@Component" in content:
                analysis["services"].append(str(relative_path))
            elif "@Configuration" in content:
                analysis["config_files"].append(str(relative_path))

        # Find XML config files
        for xml_file in self.repo_path.rglob("*.xml"):
            if "target" not in str(xml_file) and "build" not in str(xml_file):
                if "spring" in xml_file.read_text(errors='ignore').lower():
                    analysis["xml_configs"].append(str(xml_file.relative_to(self.repo_path)))

        # Find properties files
        for prop_file in self.repo_path.rglob("*.properties"):
            if "target" not in str(prop_file) and "build" not in str(prop_file):
                analysis["properties_files"].append(str(prop_file.relative_to(self.repo_path)))

        return analysis

    def generate_migration_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate migration plan."""
        plan = {
            "source_framework": "Spring MVC",
            "target_framework": "Spring Boot",
            "build_tool": self.build_tool,
            "steps": [
                "Update build configuration (pom.xml/build.gradle)",
                "Add Spring Boot starter dependencies",
                "Create Spring Boot main application class",
                "Migrate XML configuration to Java configuration",
                "Update controller annotations",
                "Migrate web.xml to Spring Boot configuration",
                "Update application properties",
                "Migrate tests to Spring Boot test framework"
            ],
            "files_to_modify": [],
            "files_to_create": ["Application.java", "application.properties"]
        }

        plan["files_to_modify"] = (
            analysis["controllers"] +
            analysis["config_files"] +
            analysis["xml_configs"] +
            analysis["test_files"]
        )

        self.migration_plan = plan
        return plan

    def execute_migration(self) -> bool:
        """Execute migration plan."""
        print("\n=== Executing Migration ===\n")

        from migrate_build import BuildMigrator
        from migrate_annotations import AnnotationMigrator
        from migrate_config import ConfigMigrator
        from migrate_tests import TestMigrator

        success = True

        # Step 1: Migrate build configuration
        print("Step 1: Migrating build configuration...")
        build_migrator = BuildMigrator(self.repo_path, self.build_tool)
        if build_migrator.migrate():
            self.changes.extend(build_migrator.get_changes())
            self._commit_changes("Migrate build configuration to Spring Boot")
        else:
            success = False

        # Step 2: Migrate annotations
        print("\nStep 2: Migrating annotations...")
        annotation_migrator = AnnotationMigrator(self.repo_path)
        if annotation_migrator.migrate():
            self.changes.extend(annotation_migrator.get_changes())
            self._commit_changes("Update annotations for Spring Boot")
        else:
            success = False

        # Step 3: Migrate configuration
        print("\nStep 3: Migrating configuration...")
        config_migrator = ConfigMigrator(self.repo_path)
        if config_migrator.migrate():
            self.changes.extend(config_migrator.get_changes())
            self._commit_changes("Migrate configuration to Spring Boot")
        else:
            success = False

        # Step 4: Migrate tests
        print("\nStep 4: Migrating tests...")
        test_migrator = TestMigrator(self.repo_path)
        if test_migrator.migrate():
            self.changes.extend(test_migrator.get_changes())
            self._commit_changes("Migrate tests to Spring Boot")
        else:
            success = False

        return success

    def _commit_changes(self, message: str):
        """Commit changes to git."""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"{message}\n\nCo-Authored-By: Spring Migration Assistant <noreply@anthropic.com>"],
                cwd=self.repo_path,
                check=True
            )
            print(f"✓ Committed: {message}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not commit changes: {e}")

    def generate_summary(self) -> Dict[str, Any]:
        """Generate migration summary."""
        summary = {
            "source_framework": "Spring MVC",
            "target_framework": "Spring Boot",
            "build_tool": self.build_tool,
            "total_changes": len(self.changes),
            "changes_by_type": {},
            "files_modified": [],
            "migration_plan": self.migration_plan,
            "next_steps": [
                "Review the migration commits",
                "Run tests: mvn test or gradle test",
                "Start the application: mvn spring-boot:run or gradle bootRun",
                "Test endpoints manually",
                "Update documentation",
                "Merge the migration branch when ready"
            ]
        }

        # Categorize changes
        for change in self.changes:
            change_type = change.get("type", "other")
            if change_type not in summary["changes_by_type"]:
                summary["changes_by_type"][change_type] = 0
            summary["changes_by_type"][change_type] += 1

            if "file" in change:
                summary["files_modified"].append(change["file"])

        return summary

    def run(self) -> bool:
        """Run complete migration process."""
        print(f"=== Spring MVC to Spring Boot Migration Assistant ===")
        print(f"Repository: {self.repo_path}\n")

        # Step 1: Validate
        if not self.validate_repository():
            return False

        # Step 2: Detect build tool
        if self.build_tool == "auto":
            detected = self.detect_build_tool()
            if detected == "unknown":
                print("Error: Could not detect build tool (Maven or Gradle)")
                return False
            self.build_tool = detected
            print(f"Detected build tool: {self.build_tool}\n")

        # Step 3: Detect Spring version
        spring_version = self.detect_spring_version()
        print(f"Detected Spring version: {spring_version}\n")

        # Step 4: Create migration branch
        if not self.create_migration_branch():
            return False

        # Step 5: Analyze codebase
        print("\nAnalyzing codebase...")
        analysis = self.analyze_codebase()
        print(f"Found {len(analysis['controllers'])} controllers")
        print(f"Found {len(analysis['services'])} services")
        print(f"Found {len(analysis['config_files'])} config files")
        print(f"Found {len(analysis['test_files'])} test files")
        print(f"Found {len(analysis['xml_configs'])} XML configs\n")

        # Step 6: Generate migration plan
        print("Generating migration plan...")
        plan = self.generate_migration_plan(analysis)
        print(f"Migration plan created with {len(plan['steps'])} steps\n")

        # Step 7: Execute migration
        if not self.execute_migration():
            print("\n⚠ Migration completed with errors")
            return False

        # Step 8: Generate summary
        print("\n=== Migration Summary ===\n")
        summary = self.generate_summary()

        # Save summary
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
    parser = argparse.ArgumentParser(description="Spring MVC to Spring Boot Migration")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--build-tool", choices=["maven", "gradle", "auto"],
                       default="auto", help="Build tool (default: auto-detect)")

    args = parser.parse_args()

    orchestrator = SpringMigrationOrchestrator(args.repo_path, args.build_tool)
    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
