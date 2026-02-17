---
name: framework-migration-assistant
description: Automatically migrate Python web applications between frameworks (Flask → FastAPI, Django → FastAPI). Use when you need to migrate an existing web application to a modern framework while preserving functionality. The skill analyzes the codebase, updates routes, handlers, configuration, dependency injection patterns, and tests. Creates git commits for each migration phase and generates a comprehensive summary of all changes. Supports automatic dependency updates, code transformations, and test adaptations.
---

# Framework Migration Assistant

## Overview

This skill automatically migrates Python web applications between frameworks, transforming code, configuration, and tests while preserving existing functionality. It handles route migration, request/response patterns, dependency injection, configuration updates, and test adaptations, committing changes incrementally with detailed summaries.

## Quick Start

### Basic Usage

```bash
# Navigate to your repository
cd /path/to/your/repo

# Run migration
python scripts/migrate.py . --from flask --to fastapi
```

The migration process will:
1. Create a migration branch
2. Analyze your codebase
3. Update dependencies
4. Migrate routes and handlers
5. Update configuration
6. Adapt tests
7. Generate a summary report

### Example: Flask to FastAPI

```bash
# Migrate Flask app to FastAPI
python scripts/migrate.py /path/to/flask-app --from flask --to fastapi

# Output:
# ✓ Created migration branch: migrate-flask-to-fastapi
# ✓ Analyzing codebase...
# ✓ Found 15 route files
# ✓ Found 23 test files
# ✓ Migrating dependencies...
# ✓ Migrating routes...
# ✓ Migrating configuration...
# ✓ Migrating tests...
# ✓ Migration completed successfully!
```

## Supported Migration Paths

### Flask → FastAPI

**What gets migrated:**
- Route decorators: `@app.route()` → `@app.get()`, `@app.post()`, etc.
- Request handling: `request.args` → query parameters, `request.json` → Pydantic models
- Response handling: `jsonify()` → direct return
- Configuration: Flask config → Pydantic Settings
- Tests: Flask test client → FastAPI TestClient
- Dependencies: Flask packages → FastAPI equivalents

**Example transformation:**

Before (Flask):
```python
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    return jsonify(user)
```

After (FastAPI):
```python
@app.get('/users/{user_id}')
async def get_user(user_id: int) -> UserSchema:
    user = await db.get_user(user_id)
    return user
```

### Django → FastAPI

**What gets migrated:**
- URL patterns → FastAPI routes
- Django views → FastAPI path operations
- Django ORM references → SQLAlchemy patterns
- Settings module → Pydantic Settings
- Django test cases → FastAPI tests

## Migration Process

### Phase 1: Preparation

The migration tool automatically:
- Validates the repository is a git repo
- Detects the source framework (if not specified)
- Creates a migration branch
- Analyzes the codebase structure

### Phase 2: Dependency Migration

Updates package dependencies:
- `requirements.txt`
- `pyproject.toml`
- Replaces framework-specific packages
- Adds required FastAPI dependencies

**Example changes:**
```
flask>=2.0.0          → fastapi>=0.104.0
werkzeug>=2.0.0       → uvicorn[standard]>=0.24.0
flask-cors>=3.0.0     → fastapi-cors>=0.0.6
```

### Phase 3: Route Migration

Transforms route definitions and handlers:
- Updates route decorators
- Converts HTTP method specifications
- Transforms path parameters
- Updates request/response handling
- Adds async/await where needed
- Adds type hints for validation

### Phase 4: Configuration Migration

Updates configuration files:
- Migrates Flask config to Pydantic Settings
- Updates environment variable handling
- Converts middleware setup
- Updates CORS configuration
- Creates new config files if needed

### Phase 5: Test Migration

Adapts test files:
- Updates test client initialization
- Converts test assertions
- Updates request methods
- Adapts fixtures and mocks
- Adds async test support

### Phase 6: Summary Generation

Creates a comprehensive report:
- Total changes made
- Files modified by category
- Migration plan executed
- Next steps for manual review
- Saved as `MIGRATION_SUMMARY.json`

## Using the Migration Scripts

### Main Migration Script

```bash
python scripts/migrate.py <repo_path> --from <source> --to <target>

# Options:
#   repo_path: Path to the repository
#   --from: Source framework (flask, django, or auto)
#   --to: Target framework (fastapi)
```

### Individual Migration Modules

You can also run individual migration steps:

```python
from migrate_dependencies import DependencyMigrator
from migrate_routes import RouteMigrator
from migrate_config import ConfigMigrator
from migrate_tests import TestMigrator

# Run specific migration
migrator = RouteMigrator(repo_path, 'flask', 'fastapi')
migrator.migrate()
```

## Post-Migration Steps

After migration completes:

1. **Review the changes**
   ```bash
   git log --oneline
   git diff main..migrate-flask-to-fastapi
   ```

2. **Install new dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Manual review needed for:**
   - Complex authentication logic
   - Custom middleware
   - Database connection strings
   - Third-party integrations
   - Advanced error handling

5. **Test the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Merge when ready**
   ```bash
   git checkout main
   git merge migrate-flask-to-fastapi
   ```

## Reference Documentation

- **`references/framework_comparison.md`** - Detailed comparison of Flask, Django, and FastAPI including architecture, routing, request handling, and performance
- **`references/migration_guide.md`** - Comprehensive migration guide with step-by-step instructions, common patterns, troubleshooting, and post-migration checklist
- **`references/migration_patterns.md`** - Common migration patterns for routes, requests, responses, authentication, database operations, and testing

## Example Applications

Example applications are provided in `assets/`:
- `example_flask_app.py` - Flask application before migration
- `example_fastapi_app.py` - Same application after migration to FastAPI

Compare these files to understand the transformations applied.

## Migration Summary

After migration, review `MIGRATION_SUMMARY.json`:

```json
{
  "source_framework": "flask",
  "target_framework": "fastapi",
  "total_changes": 47,
  "changes_by_type": {
    "dependency": 5,
    "route": 15,
    "config": 4,
    "test": 23
  },
  "files_modified": [...],
  "next_steps": [...]
}
```

## Tips

- Always commit or backup your code before migration
- Review each migration commit individually
- Test thoroughly after migration
- Update documentation to reflect framework changes
- Consider performance improvements with async/await
- Use the generated API documentation (FastAPI auto-generates OpenAPI docs)
- Consult reference documentation for complex patterns
- Run tests frequently during manual adjustments

## Troubleshooting

**Issue: Import errors after migration**
- Solution: Run `pip install -r requirements.txt`

**Issue: Tests fail with async errors**
- Solution: Add `@pytest.mark.asyncio` and install `pytest-asyncio`

**Issue: Database connections fail**
- Solution: Update connection strings for async SQLAlchemy

**Issue: CORS errors**
- Solution: Configure CORS middleware in FastAPI

See `references/migration_guide.md` for detailed troubleshooting.
