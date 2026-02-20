#!/usr/bin/env python3
"""
Migrate configuration from Spring MVC to Spring Boot.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any


class ConfigMigrator:
    """Handles configuration migration."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.changes = []

    def migrate(self) -> bool:
        """Execute configuration migration."""
        success = True

        # Migrate XML configurations
        if not self._migrate_xml_configs():
            success = False

        # Migrate web.xml
        if not self._migrate_web_xml():
            success = False

        # Create application.properties
        if not self._create_application_properties():
            success = False

        return success

    def _migrate_xml_configs(self) -> bool:
        """Migrate Spring XML configuration files."""
        success = True

        for xml_file in self.repo_path.rglob("*-context.xml"):
            if "target" in str(xml_file) or "build" in str(xml_file):
                continue

            try:
                content = xml_file.read_text()
                if 'spring' not in content.lower():
                    continue

                print(f"⚠ Found XML config: {xml_file.name}")
                print(f"  Consider converting to Java @Configuration class")

                self.changes.append({
                    "type": "config",
                    "file": str(xml_file.relative_to(self.repo_path)),
                    "description": "XML config found - manual conversion recommended"
                })

            except Exception as e:
                print(f"✗ Error processing {xml_file}: {e}")
                success = False

        return success

    def _migrate_web_xml(self) -> bool:
        """Migrate web.xml to Spring Boot configuration."""
        web_xml = self.repo_path / "src" / "main" / "webapp" / "WEB-INF" / "web.xml"

        if not web_xml.exists():
            print("ℹ No web.xml found (already using Java config or not needed)")
            return True

        try:
            content = web_xml.read_text()

            # Extract servlet mappings
            servlet_mappings = re.findall(r'<url-pattern>(.*?)</url-pattern>', content)
            if servlet_mappings:
                print(f"ℹ Found servlet mappings in web.xml:")
                for mapping in servlet_mappings:
                    print(f"  - {mapping}")

            # Extract context parameters
            context_params = re.findall(
                r'<context-param>.*?<param-name>(.*?)</param-name>.*?<param-value>(.*?)</param-value>.*?</context-param>',
                content,
                re.DOTALL
            )

            if context_params:
                print(f"ℹ Found context parameters:")
                for name, value in context_params:
                    print(f"  - {name.strip()}: {value.strip()}")

            self.changes.append({
                "type": "config",
                "file": "web.xml",
                "description": "web.xml found - Spring Boot uses embedded servlet container"
            })

            print("✓ Analyzed web.xml (Spring Boot uses embedded container)")
            return True

        except Exception as e:
            print(f"✗ Error processing web.xml: {e}")
            return False

    def _create_application_properties(self) -> bool:
        """Create application.properties file."""
        resources_dir = self.repo_path / "src" / "main" / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)

        app_props = resources_dir / "application.properties"

        if app_props.exists():
            print("ℹ application.properties already exists")
            return True

        try:
            # Create basic application.properties
            properties_content = """# Spring Boot Application Configuration

# Server Configuration
server.port=8080
server.servlet.context-path=/

# Logging Configuration
logging.level.root=INFO
logging.level.org.springframework.web=DEBUG

# Spring MVC Configuration
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp

# Database Configuration (if needed)
# spring.datasource.url=jdbc:mysql://localhost:3306/mydb
# spring.datasource.username=root
# spring.datasource.password=
# spring.jpa.hibernate.ddl-auto=update

# Actuator Configuration (optional)
# management.endpoints.web.exposure.include=health,info
"""

            app_props.write_text(properties_content)
            print(f"✓ Created {app_props.relative_to(self.repo_path)}")

            self.changes.append({
                "type": "config",
                "file": str(app_props.relative_to(self.repo_path)),
                "description": "Created application.properties"
            })

            return True

        except Exception as e:
            print(f"✗ Error creating application.properties: {e}")
            return False

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
