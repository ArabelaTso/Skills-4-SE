# CI/CD Platform Migrations

## Travis CI to GitHub Actions

### Basic Structure

**Travis CI (.travis.yml):**
```yaml
language: python
python:
  - "3.9"

install:
  - pip install -r requirements.txt

script:
  - pytest tests/

after_success:
  - codecov
```

**GitHub Actions (.github/workflows/ci.yml):**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests
      run: pytest tests/

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Matrix Builds

**Travis CI:**
```yaml
language: python
python:
  - "3.8"
  - "3.9"
  - "3.10"

os:
  - linux
  - osx
```

**GitHub Actions:**
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10']

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
```

### Environment Variables

**Travis CI:**
```yaml
env:
  global:
    - DATABASE_URL=postgres://localhost/test
    - secure: "encrypted_value"
```

**GitHub Actions:**
```yaml
env:
  DATABASE_URL: postgres://localhost/test

jobs:
  test:
    steps:
    - name: Use secret
      env:
        API_KEY: ${{ secrets.API_KEY }}
      run: echo "Using API key"
```

### Caching

**Travis CI:**
```yaml
cache:
  directories:
    - $HOME/.cache/pip
    - node_modules
```

**GitHub Actions:**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt') }}
```

## CircleCI to GitHub Actions

### Basic Structure

**CircleCI (.circleci/config.yml):**
```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/node:16.0

    steps:
      - checkout
      - run: npm install
      - run: npm test
```

**GitHub Actions:**
```yaml
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    container:
      image: cimg/node:16.0

    steps:
    - uses: actions/checkout@v3
    - run: npm install
    - run: npm test
```

### Workflows

**CircleCI:**
```yaml
workflows:
  version: 2
  build-and-deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main
```

**GitHub Actions:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building"

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying"
```

## Jenkins to GitLab CI

### Basic Pipeline

**Jenkins (Jenkinsfile):**
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

**GitLab CI (.gitlab-ci.yml):**
```yaml
stages:
  - build
  - test

build:
  stage: build
  script:
    - mvn clean package

test:
  stage: test
  script:
    - mvn test
```

### Parallel Execution

**Jenkins:**
```groovy
stage('Parallel Tests') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh 'npm run test:unit'
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'npm run test:integration'
            }
        }
    }
}
```

**GitLab CI:**
```yaml
test:unit:
  stage: test
  script:
    - npm run test:unit

test:integration:
  stage: test
  script:
    - npm run test:integration
```

## GitLab CI to GitHub Actions

### Basic Structure

**GitLab CI:**
```yaml
image: node:16

stages:
  - build
  - test

build:
  stage: build
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  script:
    - npm test
```

**GitHub Actions:**
```yaml
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    container: node:16

    steps:
    - uses: actions/checkout@v3

    - name: Build
      run: |
        npm install
        npm run build

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    container: node:16

    steps:
    - uses: actions/checkout@v3
    - run: npm test
```

### Services

**GitLab CI:**
```yaml
test:
  services:
    - postgres:13
    - redis:6
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: user
    POSTGRES_PASSWORD: password
  script:
    - npm test
```

**GitHub Actions:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: test
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s

      redis:
        image: redis:6

    steps:
    - run: npm test
```

## Common Patterns

### Conditional Execution

**Travis CI:**
```yaml
script:
  - if [ "$TRAVIS_BRANCH" == "main" ]; then npm run deploy; fi
```

**GitHub Actions:**
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: npm run deploy
```

**GitLab CI:**
```yaml
deploy:
  script:
    - npm run deploy
  only:
    - main
```

### Secrets Management

**Travis CI:**
```yaml
env:
  global:
    - secure: "encrypted_value"
```

**GitHub Actions:**
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

**GitLab CI:**
```yaml
variables:
  API_KEY: $CI_API_KEY
```

### Artifacts

**CircleCI:**
```yaml
- store_artifacts:
    path: test-results
```

**GitHub Actions:**
```yaml
- uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: test-results
```

**GitLab CI:**
```yaml
artifacts:
  paths:
    - test-results
```

## Migration Mapping Table

### Trigger Events

| Travis CI | GitHub Actions | GitLab CI |
|-----------|----------------|-----------|
| on: push | on: push | on: push |
| on: pull_request | on: pull_request | on: merge_request |
| on: schedule | on: schedule | schedules: |
| on: tag | on: push (tags) | on: tags |

### Runner/Agent Selection

| Travis CI | GitHub Actions | GitLab CI | Jenkins |
|-----------|----------------|-----------|---------|
| os: linux | runs-on: ubuntu-latest | tags: [linux] | agent any |
| os: osx | runs-on: macos-latest | tags: [macos] | agent { label 'mac' } |
| os: windows | runs-on: windows-latest | tags: [windows] | agent { label 'windows' } |

### Lifecycle Hooks

| Travis CI | GitHub Actions | GitLab CI |
|-----------|----------------|-----------|
| before_install | - (use step) | before_script |
| install | - (use step) | - (use script) |
| before_script | - (use step) | before_script |
| script | run: | script: |
| after_success | if: success() | after_script |
| after_failure | if: failure() | after_script |

## Migration Checklist

### Travis CI to GitHub Actions

- [ ] Convert .travis.yml to .github/workflows/*.yml
- [ ] Map language/runtime setup
- [ ] Convert matrix builds
- [ ] Migrate environment variables to secrets
- [ ] Update caching configuration
- [ ] Convert deployment steps
- [ ] Test all workflows
- [ ] Update badges in README

### CircleCI to GitHub Actions

- [ ] Convert .circleci/config.yml
- [ ] Map Docker images to containers
- [ ] Convert workflows to jobs with dependencies
- [ ] Migrate orbs to actions
- [ ] Update caching
- [ ] Test parallel execution
- [ ] Verify artifacts handling

### Jenkins to GitLab CI

- [ ] Convert Jenkinsfile to .gitlab-ci.yml
- [ ] Map stages
- [ ] Convert parallel execution
- [ ] Migrate credentials to CI/CD variables
- [ ] Update deployment scripts
- [ ] Test pipeline
- [ ] Configure runners

### GitLab CI to GitHub Actions

- [ ] Convert .gitlab-ci.yml to workflows
- [ ] Map services to GitHub Actions services
- [ ] Convert artifacts to actions/upload-artifact
- [ ] Migrate CI/CD variables to secrets
- [ ] Update conditional execution
- [ ] Test all jobs
- [ ] Configure branch protection
