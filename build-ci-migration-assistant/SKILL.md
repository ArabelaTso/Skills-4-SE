---
name: build-ci-migration-assistant
description: Automatically migrates build systems and CI/CD configurations to target platforms. Use when modernizing build infrastructure, switching CI/CD providers, or standardizing across projects. Supports common migration paths including Maven↔Gradle, npm↔Yarn, Travis CI→GitHub Actions, CircleCI→GitHub Actions, Jenkins→GitLab CI, and GitLab CI→GitHub Actions. Analyzes existing configuration, generates equivalent target configuration, maps dependencies and commands, and provides validation and migration documentation.
---

# Build/CI Migration Assistant

Automatically migrate build systems and CI/CD configurations to target platforms while preserving functionality.

## Workflow

### 1. Analyze Source Configuration

Identify the current build system or CI/CD platform:

**Build Systems:**
- Maven (pom.xml)
- Gradle (build.gradle, build.gradle.kts)
- npm (package.json)
- Yarn (package.json + yarn.lock)
- Make (Makefile)
- CMake (CMakeLists.txt)

**CI/CD Platforms:**
- Travis CI (.travis.yml)
- CircleCI (.circleci/config.yml)
- Jenkins (Jenkinsfile)
- GitLab CI (.gitlab-ci.yml)
- GitHub Actions (.github/workflows/*.yml)

Read and parse the source configuration to understand:
- Dependencies and their versions
- Build commands and lifecycle
- Test configuration
- Environment variables and secrets
- Caching strategy
- Deployment steps

### 2. Map to Target Platform

Consult the appropriate reference guide:
- **Build systems**: See [references/build-systems.md](references/build-systems.md)
- **CI/CD platforms**: See [references/ci-platforms.md](references/ci-platforms.md)

Map source concepts to target equivalents:
- Dependencies → Target dependency format
- Build commands → Target command syntax
- Lifecycle phases → Target stages/jobs
- Environment variables → Target secrets/variables
- Caching → Target caching mechanism

### 3. Generate Target Configuration

Create the target configuration file(s):

**For build systems:**
- Generate new build file (build.gradle, pom.xml, etc.)
- Preserve dependency versions
- Map plugins and tasks
- Maintain build lifecycle

**For CI/CD platforms:**
- Generate workflow/pipeline file
- Convert jobs and stages
- Map triggers and conditions
- Configure runners/agents
- Set up caching and artifacts

### 4. Validate Migration

Test the generated configuration:

**Build system validation:**
```bash
# Maven
mvn clean install

# Gradle
./gradlew build

# npm
npm install && npm test
```

**CI/CD validation:**
- Create a test branch
- Push generated configuration
- Verify pipeline runs successfully
- Check all jobs complete
- Validate artifacts and deployments

### 5. Document Changes

Provide migration summary including:
- What was migrated
- What requires manual review
- Breaking changes or incompatibilities
- Manual steps needed
- Rollback instructions

## Common Migration Paths

### Maven to Gradle

**Use case:** Modernize Java build, improve build performance

**Steps:**
1. Read pom.xml
2. Map dependencies to Gradle format
3. Convert plugins to Gradle equivalents
4. Generate build.gradle
5. Test build: `./gradlew build`

**Example:**

Original Maven:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>2.7.0</version>
</dependency>
```

Generated Gradle:
```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:2.7.0'
}
```

See [references/build-systems.md](references/build-systems.md) for complete mapping.

### Travis CI to GitHub Actions

**Use case:** Migrate to GitHub-native CI/CD

**Steps:**
1. Read .travis.yml
2. Map language/runtime setup
3. Convert matrix builds
4. Migrate environment variables to secrets
5. Generate .github/workflows/ci.yml
6. Test workflow

**Example:**

Original Travis CI:
```yaml
language: python
python:
  - "3.9"
script:
  - pytest tests/
```

Generated GitHub Actions:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - run: pytest tests/
```

See [references/ci-platforms.md](references/ci-platforms.md) for complete mapping.

### CircleCI to GitHub Actions

**Use case:** Consolidate CI/CD on GitHub

**Steps:**
1. Read .circleci/config.yml
2. Map Docker images to containers
3. Convert workflows to jobs with dependencies
4. Migrate orbs to actions
5. Generate GitHub Actions workflow
6. Test all jobs

### GitLab CI to GitHub Actions

**Use case:** Migrate from GitLab to GitHub

**Steps:**
1. Read .gitlab-ci.yml
2. Map stages to jobs
3. Convert services to GitHub Actions services
4. Migrate CI/CD variables to secrets
5. Generate workflow files
6. Test pipeline

## Migration Checklist

### Before Migration

- [ ] Backup existing configuration
- [ ] Document current build/CI behavior
- [ ] Identify custom scripts and dependencies
- [ ] List environment variables and secrets
- [ ] Note any special requirements

### During Migration

- [ ] Generate target configuration
- [ ] Map all dependencies
- [ ] Convert all commands
- [ ] Migrate environment variables
- [ ] Set up caching
- [ ] Configure artifacts
- [ ] Update deployment steps

### After Migration

- [ ] Test build locally
- [ ] Test CI/CD pipeline
- [ ] Verify all jobs succeed
- [ ] Check artifacts are generated
- [ ] Validate deployments work
- [ ] Update documentation
- [ ] Train team on new system

## Validation Strategies

### Dry Run

Test migration without committing:
1. Generate configuration in separate branch
2. Run build/CI locally if possible
3. Review generated files
4. Identify issues before committing

### Parallel Running

Run both systems temporarily:
1. Keep old configuration
2. Add new configuration
3. Compare results
4. Fix discrepancies
5. Remove old configuration once validated

### Incremental Migration

Migrate in stages:
1. Start with basic build
2. Add tests
3. Add caching
4. Add deployment
5. Validate each stage

## Common Patterns

### Dependency Version Management

**Preserve exact versions:**
```
Maven: <version>2.7.0</version>
→ Gradle: implementation 'group:artifact:2.7.0'
```

**Convert version ranges:**
```
Maven: <version>[1.0,2.0)</version>
→ Gradle: implementation 'group:artifact:1.+'
```

### Environment Variables

**Travis CI:**
```yaml
env:
  global:
    - DATABASE_URL=postgres://localhost/test
```

**GitHub Actions:**
```yaml
env:
  DATABASE_URL: postgres://localhost/test
```

### Matrix Builds

**Travis CI:**
```yaml
python:
  - "3.8"
  - "3.9"
```

**GitHub Actions:**
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9']
```

### Caching

**CircleCI:**
```yaml
- save_cache:
    paths:
      - node_modules
    key: deps-{{ checksum "package.json" }}
```

**GitHub Actions:**
```yaml
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('package.json') }}
```

## Troubleshooting

### Build Fails After Migration

**Check:**
- Dependency versions match
- Build commands are correct
- Environment variables are set
- Required tools are installed

**Solution:**
- Compare old and new configurations
- Run build with verbose output
- Check for missing dependencies
- Verify tool versions

### CI Pipeline Fails

**Check:**
- Workflow syntax is correct
- Secrets are configured
- Runner has required tools
- Network access is available

**Solution:**
- Review pipeline logs
- Test locally if possible
- Check runner configuration
- Verify permissions

### Tests Fail

**Check:**
- Test commands are correct
- Test environment is set up
- Database/services are running
- Test data is available

**Solution:**
- Run tests locally
- Check service configuration
- Verify environment variables
- Review test logs

## Best Practices

### Preserve Functionality

- Keep exact dependency versions initially
- Maintain build lifecycle order
- Preserve all test configurations
- Keep deployment steps identical

### Incremental Changes

- Migrate one component at a time
- Test after each change
- Don't combine migration with upgrades
- Document each step

### Documentation

- Document what changed
- Note manual steps required
- Provide rollback instructions
- Update team documentation

### Testing

- Test locally before pushing
- Use test branches
- Run full test suite
- Validate deployments

## References

- **[build-systems.md](references/build-systems.md)**: Detailed mappings for Maven, Gradle, npm, Yarn, Make, CMake migrations
- **[ci-platforms.md](references/ci-platforms.md)**: Complete guides for Travis CI, CircleCI, Jenkins, GitLab CI, GitHub Actions migrations

## Tips

- **Start simple**: Migrate basic build first, add complexity later
- **Test thoroughly**: Validate every aspect of the migration
- **Keep backups**: Maintain old configuration until new one is proven
- **Document changes**: Clear documentation helps team adoption
- **Use references**: Consult reference files for detailed mappings
- **Validate incrementally**: Test each component as you migrate it
