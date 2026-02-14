# Framework-Specific Test Analysis Guides

Commands and techniques for analyzing tests in different testing frameworks.

## Table of Contents

1. [Python - pytest](#python-pytest)
2. [Python - unittest](#python-unittest)
3. [JavaScript/TypeScript - Jest](#javascripttypescript-jest)
4. [JavaScript/TypeScript - Mocha](#javascripttypescript-mocha)
5. [Java - JUnit](#java-junit)
6. [Java - TestNG](#java-testng)
7. [Go - testing](#go-testing)

---

## Python - pytest

### Discover Tests

```bash
# List all tests
pytest --collect-only

# List in quiet mode (just test names)
pytest --collect-only -q

# List with full paths
pytest --collect-only --verbose

# Count total tests
pytest --collect-only -q | wc -l
```

### Analyze Test Duration

```bash
# Run with duration report
pytest --durations=0

# Show slowest 10 tests
pytest --durations=10

# Only show tests slower than 1 second
pytest --durations=0 --durations-min=1.0

# Export to JSON for analysis
pytest --json-report --json-report-file=report.json
```

### Get Coverage Data

```bash
# Run with coverage
pytest --cov=src --cov-report=term

# Export coverage to JSON
pytest --cov=src --cov-report=json

# Coverage with line numbers
pytest --cov=src --cov-report=term-missing

# Coverage for specific files
pytest --cov=src/auth --cov-report=term
```

### Find Tests for Specific Files

```bash
# Tests that import a specific module
grep -r "from src.auth import\|import src.auth" tests/

# Tests in same directory as source
# For src/auth/login.py, check tests/auth/test_login.py
test_file=$(echo "src/auth/login.py" | sed 's|src/|tests/test_|' | sed 's|\.py|\.py|')
```

### Run Specific Test Subsets

```bash
# Run tests matching pattern
pytest -k "auth"

# Run tests with specific marker
pytest -m "critical"

# Run tests in specific file
pytest tests/test_auth.py

# Run specific test function
pytest tests/test_auth.py::test_login_success

# Run tests that failed last time
pytest --lf  # last failed
pytest --ff  # failed first, then others
```

### Custom Test Collection

```python
# conftest.py - Custom test prioritization
def pytest_collection_modifyitems(config, items):
    # Get changed files from environment or git
    import subprocess
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', 'HEAD~1']
    ).decode().splitlines()

    # Prioritize tests based on changes
    priority_tests = []
    other_tests = []

    for item in items:
        test_file = str(item.fspath)
        # Check if test relates to changed files
        is_priority = any(
            changed_file in test_file or
            changed_file.replace('src/', 'test_') in test_file
            for changed_file in changed
        )

        if is_priority:
            priority_tests.append(item)
        else:
            other_tests.append(item)

    # Reorder: priority tests first
    items[:] = priority_tests + other_tests
```

---

## Python - unittest

### Discover Tests

```bash
# Discover all tests
python -m unittest discover

# Discover in specific directory
python -m unittest discover -s tests

# Discover with pattern
python -m unittest discover -p "*_test.py"

# Verbose discovery
python -m unittest discover -v
```

### Run Specific Tests

```bash
# Run specific test module
python -m unittest tests.test_auth

# Run specific test class
python -m unittest tests.test_auth.TestLogin

# Run specific test method
python -m unittest tests.test_auth.TestLogin.test_success
```

### Analyze Test Output

```bash
# Run with verbose output
python -m unittest discover -v

# Capture timing information
python -m unittest discover -v 2>&1 | grep -E "^test_|OK|FAIL"
```

---

## JavaScript/TypeScript - Jest

### Discover Tests

```bash
# List all tests
jest --listTests

# Show test structure
jest --verbose

# Dry run (don't execute)
jest --listTests --json
```

### Analyze Test Duration

```bash
# Show test timing
jest --verbose

# Only run slow tests
jest --testTimeout=5000  # Fail tests over 5 seconds

# Export results to JSON
jest --json --outputFile=results.json
```

### Get Coverage Data

```bash
# Run with coverage
jest --coverage

# Coverage for specific files
jest --coverage --collectCoverageFrom='src/auth/**'

# Export coverage to JSON
jest --coverage --coverageReporters=json

# Show uncovered lines
jest --coverage --coverageReporters=text-summary
```

### Find Tests for Specific Files

```bash
# Find test files
find . -name "*.test.js" -o -name "*.spec.js" -o -name "*.test.ts"

# Find tests that import a module
grep -r "from.*auth" tests/ --include="*.test.js"

# Jest's built-in related tests (requires Git)
jest --findRelatedTests src/auth/login.js
```

### Run Specific Test Subsets

```bash
# Run tests matching pattern
jest auth

# Run specific test file
jest tests/auth.test.js

# Run specific test by name
jest -t "login success"

# Run only changed tests (requires Git)
jest --onlyChanged

# Run failed tests from last run
jest --onlyFailures

# Watch mode with selective running
jest --watch
```

### Custom Test Selection

```javascript
// jest.config.js
module.exports = {
  // Run setup file to mark critical tests
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
};

// jest.setup.js
// Mark critical tests
global.critical = (name, fn) => {
  test.only(name, fn);  // Run only critical tests
};

// In tests
critical('login should work', () => {
  // This test will run when using --onlyChanged
});
```

---

## JavaScript/TypeScript - Mocha

### Discover Tests

```bash
# List all tests
mocha --reporter json

# Dry run
mocha --dry-run

# Show test structure
mocha --reporter spec
```

### Analyze Test Duration

```bash
# Show slow tests (threshold: 75ms default)
mocha --reporter spec

# Set slow threshold
mocha --slow 200

# Export to JSON
mocha --reporter json > results.json
```

### Run Specific Test Subsets

```bash
# Run tests matching grep pattern
mocha --grep "auth"

# Run specific file
mocha tests/auth.test.js

# Invert grep (run tests NOT matching)
mocha --grep "slow" --invert

# Bail after first failure
mocha --bail
```

---

## Java - JUnit

### Discover Tests (JUnit 5)

```bash
# Using Maven
mvn test -Dtest=TestClass

# List all tests
mvn test -DfailIfNoTests=false

# Using Gradle
./gradlew test --tests TestClass
```

### Analyze Test Duration

```bash
# Maven: Test reports in target/surefire-reports/
cat target/surefire-reports/*.xml

# Extract timing information
grep -r "time=" target/surefire-reports/*.xml

# Parse XML for slow tests
xmlstarlet sel -t -m "//testcase[@time>1.0]" \
  -v "concat(@name, ': ', @time)" -n \
  target/surefire-reports/*.xml
```

### Get Coverage Data

```bash
# Using JaCoCo with Maven
mvn clean test jacoco:report

# Coverage report in target/site/jacoco/
open target/site/jacoco/index.html

# Using Gradle
./gradlew test jacocoTestReport

# Coverage report in build/reports/jacoco/test/html/
```

### Find Tests for Specific Classes

```bash
# Find test classes
find . -name "*Test.java"

# Find tests that reference a class
grep -r "import.*LoginService" src/test/

# Maven: Run tests for specific package
mvn test -Dtest=com.example.auth.**
```

### Run Specific Test Subsets

```bash
# Maven: Run specific test class
mvn test -Dtest=LoginTest

# Run specific test method
mvn test -Dtest=LoginTest#testLoginSuccess

# Run multiple test classes
mvn test -Dtest=LoginTest,PaymentTest

# Run tests matching pattern
mvn test -Dtest=*Auth*

# Gradle: Run specific tests
./gradlew test --tests com.example.LoginTest
./gradlew test --tests "*Auth*"
```

### JUnit 5 Selective Execution

```java
// Tag tests for selective execution
import org.junit.jupiter.api.Tag;

@Tag("critical")
@Test
public void testLogin() {
    // Critical test
}

// Run only critical tests
mvn test -Dgroups="critical"

// Exclude slow tests
mvn test -DexcludedGroups="slow"
```

---

## Java - TestNG

### Discover Tests

```bash
# Using Maven
mvn test

# Using Gradle
./gradlew test
```

### Run Specific Test Subsets

```xml
<!-- testng.xml - Define test suites -->
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="CriticalTests">
    <test name="AuthTests">
        <classes>
            <class name="com.example.LoginTest"/>
            <class name="com.example.AuthTest"/>
        </classes>
    </test>
</suite>
```

```bash
# Run specific suite
mvn test -DsuiteXmlFile=testng-critical.xml
```

### TestNG Groups (Similar to JUnit Tags)

```java
import org.testng.annotations.Test;

@Test(groups = {"critical", "auth"})
public void testLogin() {
    // Critical auth test
}

// Run specific groups
mvn test -Dgroups="critical"

// Exclude groups
mvn test -DexcludedGroups="slow"
```

---

## Go - testing

### Discover Tests

```bash
# List all tests
go test -list .

# List in specific package
go test -list ./auth

# Count tests
go test -list . | wc -l
```

### Analyze Test Duration

```bash
# Run with verbose timing
go test -v

# Show only slow tests
go test -v -timeout 30s

# Benchmark tests
go test -bench . -benchmem
```

### Run Specific Test Subsets

```bash
# Run specific test
go test -run TestLogin

# Run tests matching pattern
go test -run "Auth"

# Run in specific package
go test ./auth

# Run with coverage
go test -cover ./...

# Coverage profile
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Parallel Execution

```go
// Mark test for parallel execution
func TestLogin(t *testing.T) {
    t.Parallel()  // Run in parallel with other parallel tests
    // Test code
}

// Run with specific parallelism
go test -parallel 4
```

---

## General Techniques

### Git Integration for Change Detection

```bash
# Find changed files in last commit
git diff --name-only HEAD~1 HEAD

# Find changed files vs main branch
git diff --name-only main...HEAD

# Find uncommitted changes
git diff --name-only

# Find changed files in last N commits
git diff --name-only HEAD~N HEAD

# Get changed files and map to tests
git diff --name-only HEAD~1 | while read file; do
    # Convert src/auth/login.py to tests/test_auth.py
    test_file=$(echo "$file" | sed 's|^src/|tests/test_|' | sed 's|\.py$|.py|')
    if [ -f "$test_file" ]; then
        echo "$test_file"
    fi
done
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Prioritized Tests
on: [push, pull_request]

jobs:
  quick-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 2  # Need history for git diff

      - name: Get changed files
        id: changed
        run: |
          echo "::set-output name=files::$(git diff --name-only HEAD~1)"

      - name: Run prioritized tests
        run: |
          # Run tests for changed files
          pytest tests/test_auth.py tests/test_payment.py
```

#### GitLab CI

```yaml
stages:
  - quick-test
  - full-test

quick-tests:
  stage: quick-test
  script:
    - git diff --name-only $CI_COMMIT_BEFORE_SHA | grep "src/auth\|src/payment"
    - pytest tests/test_auth.py tests/test_payment.py

full-tests:
  stage: full-test
  script:
    - pytest
```

### Coverage Analysis Automation

```python
# Script to analyze coverage and prioritize tests
import json
import subprocess

def get_coverage_data():
    """Run tests with coverage and return data."""
    subprocess.run(['pytest', '--cov=src', '--cov-report=json'])

    with open('coverage.json') as f:
        return json.load(f)

def find_tests_for_file(source_file):
    """Find tests that cover a specific source file."""
    coverage = get_coverage_data()

    if source_file in coverage['files']:
        # This is simplified - actual implementation needs
        # per-test coverage data
        return coverage['files'][source_file]['executed_lines']

    return []
```
