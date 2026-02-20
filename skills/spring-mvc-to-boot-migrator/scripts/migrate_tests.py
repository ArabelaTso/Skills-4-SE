#!/usr/bin/env python3
"""
Migrate tests from Spring MVC to Spring Boot.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class TestMigrator:
    """Handles test migration."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.changes = []

    def migrate(self) -> bool:
        """Execute test migration."""
        success = True

        # Find all test files
        test_dirs = [
            self.repo_path / "src" / "test" / "java",
            self.repo_path / "src" / "test" / "kotlin"
        ]

        for test_dir in test_dirs:
            if not test_dir.exists():
                continue

            for test_file in test_dir.rglob("*Test.java"):
                if not self._migrate_test_file(test_file):
                    success = False

        return success

    def _migrate_test_file(self, file_path: Path) -> bool:
        """Migrate a single test file."""
        try:
            content = file_path.read_text()
            original_content = content

            # Update imports
            content = self._update_test_imports(content)

            # Update test annotations
            content = self._update_test_annotations(content)

            # Update test context configuration
            content = self._update_test_context(content)

            # Update MockMvc setup
            content = self._update_mockmvc_setup(content)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "test",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Updated test configuration"
                })
                print(f"✓ Updated test: {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating test {file_path}: {e}")
            return False

    def _update_test_imports(self, content: str) -> str:
        """Update test imports."""
        # Update JUnit imports
        content = content.replace(
            'import org.junit.Test;',
            'import org.junit.jupiter.api.Test;'
        )
        content = content.replace(
            'import org.junit.Before;',
            'import org.junit.jupiter.api.BeforeEach;'
        )
        content = content.replace(
            'import org.junit.After;',
            'import org.junit.jupiter.api.AfterEach;'
        )
        content = content.replace(
            'import org.junit.Assert;',
            'import org.junit.jupiter.api.Assertions;'
        )

        # Update Spring test imports
        content = content.replace(
            'import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;',
            'import org.springframework.boot.test.context.SpringBootTest;'
        )
        content = content.replace(
            'import org.springframework.test.context.junit4.SpringRunner;',
            'import org.springframework.boot.test.context.SpringBootTest;'
        )

        # Add Spring Boot test imports if needed
        if '@SpringBootTest' in content and 'import org.springframework.boot.test.context.SpringBootTest;' not in content:
            content = 'import org.springframework.boot.test.context.SpringBootTest;\n' + content

        if '@AutoConfigureMockMvc' in content and 'import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;' not in content:
            content = 'import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;\n' + content

        return content

    def _update_test_annotations(self, content: str) -> str:
        """Update test annotations."""
        # Replace @RunWith(SpringRunner.class) with @SpringBootTest
        content = re.sub(
            r'@RunWith\(SpringRunner\.class\)\s*\n\s*@ContextConfiguration',
            '@SpringBootTest',
            content
        )

        content = re.sub(
            r'@RunWith\(SpringJUnit4ClassRunner\.class\)\s*\n\s*@ContextConfiguration',
            '@SpringBootTest',
            content
        )

        # Update @Before to @BeforeEach
        content = content.replace('@Before', '@BeforeEach')

        # Update @After to @AfterEach
        content = content.replace('@After', '@AfterEach')

        # Update Assert to Assertions
        content = re.sub(r'\bAssert\.', 'Assertions.', content)

        return content

    def _update_test_context(self, content: str) -> str:
        """Update test context configuration."""
        # Replace @ContextConfiguration with @SpringBootTest
        if '@ContextConfiguration' in content and '@SpringBootTest' not in content:
            content = re.sub(
                r'@ContextConfiguration\([^)]*\)',
                '@SpringBootTest',
                content
            )

        # Add @AutoConfigureMockMvc for web tests
        if 'MockMvc' in content and '@AutoConfigureMockMvc' not in content:
            # Find the class declaration and add annotation before it
            content = re.sub(
                r'(@SpringBootTest.*?\n)(public class)',
                r'\1@AutoConfigureMockMvc\n\2',
                content,
                flags=re.DOTALL
            )

        return content

    def _update_mockmvc_setup(self, content: str) -> str:
        """Update MockMvc setup."""
        # If MockMvc is manually set up, suggest using @AutoConfigureMockMvc
        if 'MockMvcBuilders' in content and '@AutoConfigureMockMvc' not in content:
            print("  ℹ Consider using @AutoConfigureMockMvc instead of manual MockMvc setup")

        # Update MockMvc setup to use @Autowired
        if 'private MockMvc mockMvc;' in content and '@Autowired' not in content:
            content = re.sub(
                r'(private MockMvc mockMvc;)',
                r'@Autowired\n    \1',
                content
            )

        return content

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
