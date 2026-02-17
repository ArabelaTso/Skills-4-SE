#!/usr/bin/env python3
"""
Migrate annotations from Spring MVC to Spring Boot.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class AnnotationMigrator:
    """Handles annotation migration."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.changes = []

    def migrate(self) -> bool:
        """Execute annotation migration."""
        success = True

        # Find all Java files
        for java_file in self.repo_path.rglob("*.java"):
            if "target" in str(java_file) or "build" in str(java_file):
                continue

            if not self._migrate_file(java_file):
                success = False

        # Create Spring Boot main application class
        self._create_main_application()

        return success

    def _migrate_file(self, file_path: Path) -> bool:
        """Migrate a single Java file."""
        try:
            content = file_path.read_text()
            original_content = content

            # Update imports
            content = self._update_imports(content)

            # Update controller annotations
            content = self._update_controller_annotations(content)

            # Update configuration annotations
            content = self._update_configuration_annotations(content)

            # Update request mapping annotations
            content = self._update_request_mappings(content)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "annotation",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Updated annotations"
                })
                print(f"✓ Updated annotations in {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def _update_imports(self, content: str) -> str:
        """Update import statements."""
        # Update Spring imports
        replacements = {
            'import org.springframework.stereotype.Controller;':
                'import org.springframework.stereotype.Controller;',
            'import org.springframework.web.bind.annotation.RequestMapping;':
                'import org.springframework.web.bind.annotation.RequestMapping;',
            'import javax.servlet.':
                'import jakarta.servlet.',
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        # Add Spring Boot imports if needed
        if '@SpringBootApplication' in content and 'import org.springframework.boot.SpringApplication;' not in content:
            content = 'import org.springframework.boot.SpringApplication;\n' + content

        if '@SpringBootApplication' in content and 'import org.springframework.boot.autoconfigure.SpringBootApplication;' not in content:
            content = 'import org.springframework.boot.autoconfigure.SpringBootApplication;\n' + content

        return content

    def _update_controller_annotations(self, content: str) -> str:
        """Update controller annotations."""
        # @Controller is compatible with Spring Boot, no changes needed
        # But we can add @RestController for REST APIs
        if '@Controller' in content and 'ResponseBody' in content:
            content = content.replace('@Controller', '@RestController')
            if 'import org.springframework.web.bind.annotation.RestController;' not in content:
                content = re.sub(
                    r'(import org\.springframework\.stereotype\.Controller;)',
                    r'import org.springframework.web.bind.annotation.RestController;',
                    content
                )

        return content

    def _update_configuration_annotations(self, content: str) -> str:
        """Update configuration annotations."""
        # @Configuration is compatible with Spring Boot
        # Add @EnableAutoConfiguration if needed
        if '@Configuration' in content and '@EnableAutoConfiguration' not in content:
            if 'public class' in content and 'Config' in content:
                # This is a configuration class, might benefit from auto-configuration
                pass

        return content

    def _update_request_mappings(self, content: str) -> str:
        """Update request mapping annotations."""
        # Update @RequestMapping to use more specific annotations
        # @RequestMapping(method = RequestMethod.GET) -> @GetMapping
        content = re.sub(
            r'@RequestMapping\(([^)]*?)method\s*=\s*RequestMethod\.GET([^)]*?)\)',
            r'@GetMapping(\1\2)',
            content
        )

        content = re.sub(
            r'@RequestMapping\(([^)]*?)method\s*=\s*RequestMethod\.POST([^)]*?)\)',
            r'@PostMapping(\1\2)',
            content
        )

        content = re.sub(
            r'@RequestMapping\(([^)]*?)method\s*=\s*RequestMethod\.PUT([^)]*?)\)',
            r'@PutMapping(\1\2)',
            content
        )

        content = re.sub(
            r'@RequestMapping\(([^)]*?)method\s*=\s*RequestMethod\.DELETE([^)]*?)\)',
            r'@DeleteMapping(\1\2)',
            content
        )

        # Add imports for new annotations
        if '@GetMapping' in content and 'import org.springframework.web.bind.annotation.GetMapping;' not in content:
            content = 'import org.springframework.web.bind.annotation.GetMapping;\n' + content

        if '@PostMapping' in content and 'import org.springframework.web.bind.annotation.PostMapping;' not in content:
            content = 'import org.springframework.web.bind.annotation.PostMapping;\n' + content

        if '@PutMapping' in content and 'import org.springframework.web.bind.annotation.PutMapping;' not in content:
            content = 'import org.springframework.web.bind.annotation.PutMapping;\n' + content

        if '@DeleteMapping' in content and 'import org.springframework.web.bind.annotation.DeleteMapping;' not in content:
            content = 'import org.springframework.web.bind.annotation.DeleteMapping;\n' + content

        return content

    def _create_main_application(self):
        """Create Spring Boot main application class."""
        # Find src/main/java directory
        src_main_java = self.repo_path / "src" / "main" / "java"
        if not src_main_java.exists():
            print("✗ src/main/java directory not found")
            return

        # Find base package
        base_package = None
        for java_file in src_main_java.rglob("*.java"):
            content = java_file.read_text()
            package_match = re.search(r'package\s+([\w.]+);', content)
            if package_match:
                base_package = package_match.group(1).split('.')[0:3]
                base_package = '.'.join(base_package)
                break

        if not base_package:
            base_package = "com.example.app"

        # Create package directory
        package_dir = src_main_java / base_package.replace('.', '/')
        package_dir.mkdir(parents=True, exist_ok=True)

        # Create Application.java
        app_file = package_dir / "Application.java"
        if not app_file.exists():
            app_content = f"""package {base_package};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {{

    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}
"""
            app_file.write_text(app_content)
            print(f"✓ Created {app_file.relative_to(self.repo_path)}")
            self.changes.append({
                "type": "annotation",
                "file": str(app_file.relative_to(self.repo_path)),
                "description": "Created Spring Boot main application class"
            })

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
