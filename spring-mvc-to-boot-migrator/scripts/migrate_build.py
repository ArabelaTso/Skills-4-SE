#!/usr/bin/env python3
"""
Migrate build configuration from Spring MVC to Spring Boot.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any


class BuildMigrator:
    """Handles build configuration migration."""

    def __init__(self, repo_path: Path, build_tool: str):
        self.repo_path = repo_path
        self.build_tool = build_tool
        self.changes = []

    def migrate(self) -> bool:
        """Execute build configuration migration."""
        if self.build_tool == "maven":
            return self._migrate_maven()
        elif self.build_tool == "gradle":
            return self._migrate_gradle()
        return False

    def _migrate_maven(self) -> bool:
        """Migrate Maven pom.xml to Spring Boot."""
        pom_file = self.repo_path / "pom.xml"
        if not pom_file.exists():
            print("✗ pom.xml not found")
            return False

        try:
            tree = ET.parse(pom_file)
            root = tree.getroot()
            ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

            # Register namespace
            ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

            # Add Spring Boot parent
            parent = root.find('m:parent', ns)
            if parent is None:
                parent = ET.SubElement(root, 'parent')
                groupId = ET.SubElement(parent, 'groupId')
                groupId.text = 'org.springframework.boot'
                artifactId = ET.SubElement(parent, 'artifactId')
                artifactId.text = 'spring-boot-starter-parent'
                version = ET.SubElement(parent, 'version')
                version.text = '3.2.0'
                relativePath = ET.SubElement(parent, 'relativePath')
                print("✓ Added Spring Boot parent")
                self.changes.append({
                    "type": "build",
                    "file": "pom.xml",
                    "description": "Added Spring Boot parent"
                })

            # Update dependencies
            dependencies = root.find('m:dependencies', ns)
            if dependencies is not None:
                # Add Spring Boot starters
                self._add_maven_dependency(dependencies, 'org.springframework.boot',
                                          'spring-boot-starter-web', ns)
                self._add_maven_dependency(dependencies, 'org.springframework.boot',
                                          'spring-boot-starter-test', ns, scope='test')

                # Remove old Spring dependencies
                for dep in dependencies.findall('m:dependency', ns):
                    artifact = dep.find('m:artifactId', ns)
                    if artifact is not None and artifact.text:
                        if 'spring-webmvc' in artifact.text or 'spring-web' in artifact.text:
                            dependencies.remove(dep)
                            print(f"✓ Removed old dependency: {artifact.text}")

            # Add Spring Boot Maven plugin
            build = root.find('m:build', ns)
            if build is None:
                build = ET.SubElement(root, 'build')

            plugins = build.find('m:plugins', ns)
            if plugins is None:
                plugins = ET.SubElement(build, 'plugins')

            # Check if plugin already exists
            plugin_exists = False
            for plugin in plugins.findall('m:plugin', ns):
                artifact = plugin.find('m:artifactId', ns)
                if artifact is not None and 'spring-boot-maven-plugin' in artifact.text:
                    plugin_exists = True
                    break

            if not plugin_exists:
                plugin = ET.SubElement(plugins, 'plugin')
                groupId = ET.SubElement(plugin, 'groupId')
                groupId.text = 'org.springframework.boot'
                artifactId = ET.SubElement(plugin, 'artifactId')
                artifactId.text = 'spring-boot-maven-plugin'
                print("✓ Added Spring Boot Maven plugin")
                self.changes.append({
                    "type": "build",
                    "file": "pom.xml",
                    "description": "Added Spring Boot Maven plugin"
                })

            # Write back
            tree.write(pom_file, encoding='utf-8', xml_declaration=True)
            print("✓ Updated pom.xml")

            return True

        except Exception as e:
            print(f"✗ Error migrating pom.xml: {e}")
            return False

    def _add_maven_dependency(self, dependencies, group_id: str, artifact_id: str,
                             ns: dict, scope: str = None):
        """Add Maven dependency if not exists."""
        # Check if dependency already exists
        for dep in dependencies.findall('m:dependency', ns):
            existing_artifact = dep.find('m:artifactId', ns)
            if existing_artifact is not None and existing_artifact.text == artifact_id:
                return

        # Add new dependency
        dependency = ET.SubElement(dependencies, 'dependency')
        groupId_elem = ET.SubElement(dependency, 'groupId')
        groupId_elem.text = group_id
        artifactId_elem = ET.SubElement(dependency, 'artifactId')
        artifactId_elem.text = artifact_id

        if scope:
            scope_elem = ET.SubElement(dependency, 'scope')
            scope_elem.text = scope

        print(f"✓ Added dependency: {artifact_id}")
        self.changes.append({
            "type": "build",
            "file": "pom.xml",
            "description": f"Added {artifact_id}"
        })

    def _migrate_gradle(self) -> bool:
        """Migrate Gradle build.gradle to Spring Boot."""
        gradle_file = self.repo_path / "build.gradle"
        gradle_kts_file = self.repo_path / "build.gradle.kts"

        target_file = gradle_file if gradle_file.exists() else gradle_kts_file
        if not target_file.exists():
            print("✗ build.gradle not found")
            return False

        try:
            content = target_file.read_text()
            original_content = content

            # Add Spring Boot plugin
            if 'org.springframework.boot' not in content:
                plugins_section = """plugins {
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
    id 'java'
}
"""
                if 'plugins {' in content:
                    # Add to existing plugins block
                    content = re.sub(
                        r'plugins\s*\{',
                        "plugins {\n    id 'org.springframework.boot' version '3.2.0'\n    id 'io.spring.dependency-management' version '1.1.4'",
                        content,
                        count=1
                    )
                else:
                    # Add new plugins block at the beginning
                    content = plugins_section + '\n' + content

                print("✓ Added Spring Boot plugin")
                self.changes.append({
                    "type": "build",
                    "file": target_file.name,
                    "description": "Added Spring Boot plugin"
                })

            # Update dependencies
            if 'dependencies {' in content:
                # Add Spring Boot starters
                if 'spring-boot-starter-web' not in content:
                    content = re.sub(
                        r'dependencies\s*\{',
                        "dependencies {\n    implementation 'org.springframework.boot:spring-boot-starter-web'",
                        content,
                        count=1
                    )
                    print("✓ Added spring-boot-starter-web")

                if 'spring-boot-starter-test' not in content:
                    content = re.sub(
                        r'dependencies\s*\{',
                        "dependencies {\n    testImplementation 'org.springframework.boot:spring-boot-starter-test'",
                        content,
                        count=1
                    )
                    print("✓ Added spring-boot-starter-test")

                # Remove old Spring dependencies
                content = re.sub(
                    r".*['\"]org\.springframework:spring-webmvc['\"].*\n",
                    "",
                    content
                )
                content = re.sub(
                    r".*['\"]org\.springframework:spring-web['\"].*\n",
                    "",
                    content
                )

            if content != original_content:
                target_file.write_text(content)
                print(f"✓ Updated {target_file.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {target_file.name}: {e}")
            return False

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
