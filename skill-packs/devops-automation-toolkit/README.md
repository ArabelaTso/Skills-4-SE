# DevOps Automation Toolkit

Complete DevOps automation toolkit for CI/CD pipelines, containerization, configuration management, and deployment.

## 📦 Included Skills (10)

### CI/CD Pipeline
- **ci-pipeline-synthesizer** - Generate CI pipelines (GitHub Actions, GitLab CI, etc.)
- **cd-pipeline-generator** - Generate CD/deployment pipelines
- **build-ci-migration-assistant** - Migrate between CI/CD systems

### Containerization
- **containerization-assistant** - Generate Dockerfiles and container configs
- **configuration-generator** - Generate deployment configurations

### Configuration Management
- **config-consistency-checker** - Check configuration consistency
- **rollback-strategy-advisor** - Plan rollback strategies

### Release Management
- **release-notes-writer** - Generate release notes from commits
- **change-log-generator** - Generate changelogs automatically

### Security
- **time-aware-dependency-cve-scanner** - Scan dependencies for CVEs

## 🎯 Use Cases

### 1. CI/CD Pipeline Setup
```bash
# Generate GitHub Actions workflow
/ci-pipeline-synthesizer --platform github --language python

# Generate CD pipeline
/cd-pipeline-generator --target kubernetes --environment production
```

### 2. Containerization
```bash
# Generate Dockerfile
/containerization-assistant --project . --language java

# Generate deployment configs
/configuration-generator --target kubernetes --app myapp
```

### 3. Release Management
```bash
# Generate release notes
/release-notes-writer --from v1.0.0 --to v1.1.0

# Generate changelog
/change-log-generator --since 2024-01-01
```

### 4. Security & Compliance
```bash
# Scan for CVEs
/time-aware-dependency-cve-scanner --manifest package.json

# Check config consistency
/config-consistency-checker --configs config/
```

## 🚀 Installation

```bash
cd skill-packs/devops-automation-toolkit
./install.sh
```

## 📊 DevOps Workflow

```
Code → CI Pipeline → Build → Test → Container → CD Pipeline → Deploy
                      ↓                           ↓
                Security Scan ← Config Check → Monitoring
```

## 🔗 Related Skill Packs

- **test-automation-suite** - Integrate tests into CI/CD
- **security-scanner-suite** - Security scanning in pipelines
- **code-quality-toolkit** - Quality gates in CI

## 📖 Examples

### Example 1: Complete CI/CD Setup

```bash
# Generate CI pipeline
/ci-pipeline-synthesizer --platform github --language python --tests pytest

# Output: .github/workflows/ci.yml
# - Checkout code
# - Setup Python
# - Install dependencies
# - Run tests
# - Upload coverage

# Generate CD pipeline
/cd-pipeline-generator --target aws-ecs --environment production

# Output: .github/workflows/cd.yml
# - Build Docker image
# - Push to ECR
# - Deploy to ECS
```

### Example 2: Containerization

```bash
# Generate Dockerfile
/containerization-assistant --project . --language java --framework spring-boot

# Output: Dockerfile
# FROM openjdk:17-slim
# WORKDIR /app
# COPY target/*.jar app.jar
# EXPOSE 8080
# ENTRYPOINT ["java", "-jar", "app.jar"]

# Generate Kubernetes configs
/configuration-generator --target kubernetes --app myapp --replicas 3
```

### Example 3: Release Automation

```bash
# Generate release notes
/release-notes-writer --from v1.0.0 --to v1.1.0 --format markdown

# Output: RELEASE_NOTES.md
# ## New Features
# - Added user authentication (#123)
# - Improved performance (#145)
# ## Bug Fixes
# - Fixed memory leak (#134)

# Generate changelog
/change-log-generator --since 2024-01-01 --format keepachangelog
```

### Example 4: Migration

```bash
# Migrate from Jenkins to GitHub Actions
/build-ci-migration-assistant --from jenkins --to github-actions

# Check configuration consistency
/config-consistency-checker --configs config/ --environments dev,staging,prod
```

## 🛠️ Requirements

- Claude Code CLI
- Git (for release notes and changelogs)
- Docker (optional, for containerization)
- CI/CD platform access (GitHub, GitLab, etc.)

## 📝 Supported Platforms

### CI/CD Platforms
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI

### Container Platforms
- Docker
- Kubernetes
- AWS ECS
- Google Cloud Run

### Deployment Targets
- AWS (ECS, Lambda, EC2)
- Google Cloud Platform
- Azure
- Kubernetes clusters

## 📝 License

MIT
