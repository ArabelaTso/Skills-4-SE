---
name: spring-mvc-to-boot-migrator
description: Automatically migrate Spring MVC applications to Spring Boot. Use when you need to modernize a Spring MVC project to Spring Boot while preserving functionality. The skill analyzes the codebase, updates build configuration (Maven/Gradle), migrates annotations, converts XML configuration to Java/properties, updates controllers and tests, and creates the Spring Boot main application class. Creates git commits for each migration phase and generates a comprehensive summary. Supports both Maven and Gradle projects.
---

# Spring MVC to Spring Boot Migrator

## Overview

This skill automatically migrates Spring MVC applications to Spring Boot, transforming build configuration, annotations, XML configuration, controllers, and tests while preserving existing functionality. It handles Maven and Gradle projects, creates incremental git commits, and generates detailed migration summaries.

## Quick Start

### Basic Usage

```bash
# Navigate to your Spring MVC project
cd /path/to/spring-mvc-project

# Run migration (auto-detects Maven or Gradle)
python scripts/migrate.py .

# Or specify build tool explicitly
python scripts/migrate.py . --build-tool maven
```

The migration process will:
1. Create a migration branch
2. Analyze your codebase
3. Update build configuration
4. Migrate annotations
5. Convert configuration files
6. Update tests
7. Generate a summary report

### Example Migration

```bash
# Migrate Spring MVC project
python scripts/migrate.py /path/to/project

# Output:
# ✓ Detected build tool: maven
# ✓ Detected Spring version: 5.3.20
# ✓ Created migration branch: migrate-spring-mvc-to-boot
# ✓ Analyzing codebase...
# ✓ Found 8 controllers
# ✓ Found 12 services
# ✓ Found 15 test files
# ✓ Migrating build configuration...
# ✓ Migrating annotations...
# ✓ Migrating configuration...
# ✓ Migrating tests...
# ✓ Migration completed successfully!
```

## Supported Migration Paths

### Spring MVC → Spring Boot

**What gets migrated:**

1. **Build Configuration**
   - Maven: Add Spring Boot parent, update dependencies, add Spring Boot plugin
   - Gradle: Add Spring Boot plugin, update dependencies

2. **Annotations**
   - `@Controller` + `@ResponseBody` → `@RestController`
   - `@RequestMapping(method = RequestMethod.GET)` → `@GetMapping`
   - Similar for `@PostMapping`, `@PutMapping`, `@DeleteMapping`
   - Update imports from `javax.*` to `jakarta.*`

3. **Configuration**
   - XML configuration → Java configuration + application.properties
   - web.xml → Spring Boot auto-configuration
   - Create Spring Boot main application class

4. **Tests**
   - JUnit 4 → JUnit 5
   - `@RunWith(SpringRunner.class)` → `@SpringBootTest`
   - Manual MockMvc setup → `@AutoConfigureMockMvc`

**Example transformation:**

Before (Spring MVC):
```java
@Controller
@RequestMapping("/users")
public class UserController {

    @RequestMapping(method = RequestMethod.GET)
    @ResponseBody
    public List<User> getUsers() {
        return userService.findAll();
    }
}
```

After (Spring Boot):
```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }
}
```

## Migration Process

### Phase 1: Preparation

The migration tool automatically:
- Validates the repository is a git repo
- Detects build tool (Maven or Gradle)
- Detects current Spring version
- Creates a migration branch
- Analyzes codebase structure

### Phase 2: Build Configuration Migration

**Maven projects:**
- Adds Spring Boot parent POM
- Replaces individual Spring dependencies with Spring Boot starters
- Adds Spring Boot Maven plugin
- Updates dependency versions

**Gradle projects:**
- Adds Spring Boot plugin
- Adds dependency management plugin
- Replaces dependencies with Spring Boot starters
- Updates build configuration

### Phase 3: Annotation Migration

Updates Java annotations:
- Controller annotations (`@RestController`)
- Request mapping annotations (`@GetMapping`, `@PostMapping`, etc.)
- Import statements (`javax.*` → `jakarta.*`)
- Creates Spring Boot main application class with `@SpringBootApplication`

### Phase 4: Configuration Migration

Converts configuration:
- XML configuration → Java configuration classes
- web.xml → Spring Boot auto-configuration
- Creates `application.properties` with common settings
- Identifies manual conversion needs for complex XML configs

### Phase 5: Test Migration

Updates test files:
- JUnit 4 → JUnit 5 annotations
- Test runner annotations
- MockMvc setup
- Test context configuration
- Assertion methods

### Phase 6: Summary Generation

Creates comprehensive report:
- Total changes made
- Files modified by category
- Migration plan executed
- Next steps for manual review
- Saved as `MIGRATION_SUMMARY.json`

## Using the Migration Scripts

### Main Migration Script

```bash
python scripts/migrate.py <repo_path> [--build-tool <maven|gradle|auto>]

# Options:
#   repo_path: Path to the Spring MVC repository
#   --build-tool: Build tool (default: auto-detect)
```

### Individual Migration Modules

You can also run individual migration steps:

```python
from migrate_build import BuildMigrator
from migrate_annotations import AnnotationMigrator
from migrate_config import ConfigMigrator
from migrate_tests import TestMigrator

# Run specific migration
migrator = AnnotationMigrator(repo_path)
migrator.migrate()
```

## Post-Migration Steps

After migration completes:

1. **Review the changes**
   ```bash
   git log --oneline
   git diff main..migrate-spring-mvc-to-boot
   ```

2. **Build the project**
   ```bash
   # Maven
   mvn clean package

   # Gradle
   gradle clean build
   ```

3. **Run the application**
   ```bash
   # Maven
   mvn spring-boot:run

   # Gradle
   gradle bootRun

   # Or run JAR directly
   java -jar target/myapp.jar
   ```

4. **Run tests**
   ```bash
   # Maven
   mvn test

   # Gradle
   gradle test
   ```

5. **Manual review needed for:**
   - Complex XML configuration (convert to Java config)
   - Custom servlet filters
   - Advanced security configuration
   - Third-party integrations
   - Custom view resolvers

6. **Test endpoints**
   ```bash
   curl http://localhost:8080/users
   ```

7. **Merge when ready**
   ```bash
   git checkout main
   git merge migrate-spring-mvc-to-boot
   ```

## Reference Documentation

- **`references/migration_guide.md`** - Comprehensive step-by-step migration guide covering all aspects from build configuration to testing, with detailed examples and troubleshooting
- **`references/framework_comparison.md`** - Detailed comparison of Spring MVC and Spring Boot including architecture, configuration, controllers, testing, and deployment

## Example Code

Example controller files are provided in `assets/`:
- `UserController_Before.java` - Spring MVC controller before migration
- `UserController_After.java` - Spring Boot controller after migration

Compare these files to understand the transformations applied.

## Migration Summary

After migration, review `MIGRATION_SUMMARY.json`:

```json
{
  "source_framework": "Spring MVC",
  "target_framework": "Spring Boot",
  "build_tool": "maven",
  "total_changes": 35,
  "changes_by_type": {
    "build": 5,
    "annotation": 12,
    "config": 6,
    "test": 12
  },
  "files_modified": [...],
  "next_steps": [...]
}
```

## Tips

- Always backup your code before migration
- Review each migration commit individually
- Test thoroughly after migration
- Convert complex XML configs to Java configuration manually
- Update documentation to reflect Spring Boot conventions
- Enable Spring Boot Actuator for production monitoring
- Use Spring Boot DevTools for development
- Consult reference documentation for complex patterns
- Run tests frequently during manual adjustments

## Troubleshooting

**Issue: Application won't start**
- Solution: Check for `@SpringBootApplication` annotation and correct package structure

**Issue: Controllers not found**
- Solution: Ensure controllers are in same package or sub-package as Application class

**Issue: Build fails**
- Solution: Run `mvn clean install` or `gradle clean build` to refresh dependencies

**Issue: Tests fail**
- Solution: Update JUnit 4 to JUnit 5, check test annotations

**Issue: Database connection fails**
- Solution: Update connection properties in application.properties

See `references/migration_guide.md` for detailed troubleshooting.

## Benefits of Migration

1. **Reduced Configuration**: 80% less configuration code
2. **Faster Development**: Quick setup and development cycles
3. **Production Ready**: Built-in monitoring and health checks
4. **Modern Standards**: Latest Spring features and best practices
5. **Easier Deployment**: Self-contained executable JARs
6. **Better Testing**: Simplified test configuration
7. **Microservices Ready**: Perfect for microservices architecture
