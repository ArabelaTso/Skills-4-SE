#!/usr/bin/env python3
"""
Migrate configuration files from source framework to target framework.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class ConfigMigrator:
    """Handles configuration migration between frameworks."""

    def __init__(self, repo_path: Path, source_framework: str, target_framework: str):
        self.repo_path = repo_path
        self.source_framework = source_framework
        self.target_framework = target_framework
        self.changes = []

    def migrate(self) -> bool:
        """Execute configuration migration."""
        success = True

        # Find config files
        config_files = ["config.py", "settings.py", ".env", "app.py", "main.py"]

        for config_name in config_files:
            config_file = self.repo_path / config_name
            if config_file.exists():
                if not self._migrate_config_file(config_file):
                    success = False

        # Create new config file if needed
        if self.target_framework == "fastapi":
            self._create_fastapi_config()

        return success

    def _migrate_config_file(self, file_path: Path) -> bool:
        """Migrate a configuration file."""
        try:
            content = file_path.read_text()
            original_content = content

            if self.source_framework == "flask" and self.target_framework == "fastapi":
                content = self._migrate_flask_config_to_fastapi(content)
            elif self.source_framework == "django" and self.target_framework == "fastapi":
                content = self._migrate_django_config_to_fastapi(content)

            if content != original_content:
                file_path.write_text(content)
                self.changes.append({
                    "type": "config",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": "Migrated configuration"
                })
                print(f"✓ Migrated config in {file_path.name}")

            return True

        except Exception as e:
            print(f"✗ Error migrating {file_path}: {e}")
            return False

    def _migrate_flask_config_to_fastapi(self, content: str) -> str:
        """Migrate Flask configuration to FastAPI."""
        # Replace Flask config patterns
        replacements = {
            r'app\.config\[([^\]]+)\]': r'settings.\1',
            r'FLASK_ENV': 'ENVIRONMENT',
            r'FLASK_DEBUG': 'DEBUG',
            r'SECRET_KEY': 'SECRET_KEY',
        }

        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)

        # Replace Flask app initialization
        content = re.sub(
            r'app = Flask\(__name__\)',
            'app = FastAPI(title="Migrated API", version="1.0.0")',
            content
        )

        # Add CORS if Flask-CORS was used
        if 'CORS' in content:
            content = re.sub(
                r'from flask_cors import CORS',
                'from fastapi.middleware.cors import CORSMiddleware',
                content
            )
            content = re.sub(
                r'CORS\(app\)',
                '''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)''',
                content
            )

        return content

    def _migrate_django_config_to_fastapi(self, content: str) -> str:
        """Migrate Django settings to FastAPI."""
        # Replace Django settings patterns
        replacements = {
            r'ALLOWED_HOSTS': 'ALLOWED_HOSTS',
            r'DEBUG': 'DEBUG',
            r'SECRET_KEY': 'SECRET_KEY',
            r'DATABASES': '# DATABASES - Use SQLAlchemy configuration',
        }

        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)

        return content

    def _create_fastapi_config(self):
        """Create a new FastAPI configuration file."""
        config_content = '''"""
FastAPI application configuration.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Migrated API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: Optional[str] = None

    # CORS
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
'''

        config_file = self.repo_path / "config.py"
        if not config_file.exists():
            config_file.write_text(config_content)
            self.changes.append({
                "type": "config",
                "file": "config.py",
                "description": "Created FastAPI configuration file"
            })
            print("✓ Created config.py for FastAPI")

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return list of changes made."""
        return self.changes
