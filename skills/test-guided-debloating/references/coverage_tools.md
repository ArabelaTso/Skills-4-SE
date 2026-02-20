# Coverage Analysis Tools

This document provides commands and configurations for running coverage analysis across different languages and frameworks.

## Python

### pytest with coverage

**Installation**:
```bash
pip install pytest pytest-cov
```

**Basic usage**:
```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=json

# Specify source directory
pytest --cov=src --cov-report=html --cov-report=json

# Show missing lines
pytest --cov=. --cov-report=term-missing

# Generate XML report (for CI)
pytest --cov=. --cov-report=xml
```

**Output files**:
- `htmlcov/index.html` - Interactive HTML report
- `coverage.json` - Machine-readable JSON report
- `.coverage` - Coverage database

**Reading JSON report**:
```python
import json

with open('coverage.json') as f:
    data = json.load(f)

# Get files and their coverage
for filename, info in data['files'].items():
    executed_lines = info['executed_lines']
    missing_lines = info['missing_lines']
    print(f"{filename}: {len(executed_lines)} executed, {len(missing_lines)} missing")
```

### unittest with coverage

```bash
coverage run -m unittest discover
coverage report
coverage html
coverage json
```

## JavaScript/TypeScript

### Jest with coverage

**Configuration** (jest.config.js):
```javascript
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['html', 'json', 'text', 'lcov'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.test.{js,jsx,ts,tsx}',
    '!src/**/*.spec.{js,jsx,ts,tsx}'
  ]
};
```

**Usage**:
```bash
# Run tests with coverage
npm test -- --coverage

# Or with Jest directly
jest --coverage

# Watch mode with coverage
jest --coverage --watch
```

**Output files**:
- `coverage/index.html` - HTML report
- `coverage/coverage-final.json` - JSON report
- `coverage/lcov.info` - LCOV format

### nyc (Istanbul) for Node.js

**Installation**:
```bash
npm install --save-dev nyc
```

**Usage**:
```bash
# With npm test
nyc npm test

# With specific test command
nyc mocha test/**/*.js

# Generate reports
nyc --reporter=html --reporter=json --reporter=text npm test
```

**Configuration** (.nycrc.json):
```json
{
  "all": true,
  "include": ["src/**/*.js"],
  "exclude": ["**/*.test.js", "**/*.spec.js"],
  "reporter": ["html", "json", "text"],
  "report-dir": "./coverage"
}
```

## Java

### JaCoCo with Maven

**Configuration** (pom.xml):
```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.11</version>
      <executions>
        <execution>
          <goals>
            <goal>prepare-agent</goal>
          </goals>
        </execution>
        <execution>
          <id>report</id>
          <phase>test</phase>
          <goals>
            <goal>report</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

**Usage**:
```bash
# Run tests with coverage
mvn clean test

# Generate report
mvn jacoco:report

# View report
open target/site/jacoco/index.html
```

**Output files**:
- `target/site/jacoco/index.html` - HTML report
- `target/jacoco.exec` - Binary coverage data

### JaCoCo with Gradle

**Configuration** (build.gradle):
```groovy
plugins {
    id 'jacoco'
}

jacoco {
    toolVersion = "0.8.11"
}

test {
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
        csv.required = false
    }
}
```

**Usage**:
```bash
# Run tests with coverage
./gradlew test jacocoTestReport

# View report
open build/reports/jacoco/test/html/index.html
```

## Go

### Built-in coverage

**Usage**:
```bash
# Run tests with coverage
go test -coverprofile=coverage.out ./...

# View coverage report
go tool cover -html=coverage.out

# Get coverage percentage
go test -cover ./...

# Detailed coverage by function
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

**Output files**:
- `coverage.out` - Coverage profile

**Generate HTML report**:
```bash
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

## Ruby

### SimpleCov

**Installation**:
```ruby
# Gemfile
gem 'simplecov', require: false, group: :test
```

**Configuration** (test/test_helper.rb or spec/spec_helper.rb):
```ruby
require 'simplecov'
SimpleCov.start do
  add_filter '/test/'
  add_filter '/spec/'
end
```

**Usage**:
```bash
# Run tests (SimpleCov runs automatically)
rake test
# or
rspec

# View report
open coverage/index.html
```

**Output files**:
- `coverage/index.html` - HTML report
- `coverage/.resultset.json` - JSON data

## C/C++

### gcov/lcov

**Usage**:
```bash
# Compile with coverage flags
gcc -fprofile-arcs -ftest-coverage -o program program.c

# Run program/tests
./program

# Generate coverage data
gcov program.c

# Generate HTML report with lcov
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html

# View report
open coverage_html/index.html
```

**CMake configuration**:
```cmake
if(CMAKE_BUILD_TYPE STREQUAL "Coverage")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-arcs -ftest-coverage")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -lgcov")
endif()
```

## Rust

### cargo-tarpaulin

**Installation**:
```bash
cargo install cargo-tarpaulin
```

**Usage**:
```bash
# Run tests with coverage
cargo tarpaulin --out Html --out Json

# View report
open tarpaulin-report.html
```

### llvm-cov (nightly)

```bash
# Install llvm-tools
rustup component add llvm-tools-preview

# Run tests with coverage
cargo +nightly test --all-features --no-fail-fast
cargo +nightly llvm-cov --html

# View report
open target/llvm-cov/html/index.html
```

## PHP

### PHPUnit with coverage

**Usage**:
```bash
# Run tests with coverage (requires Xdebug or PCOV)
phpunit --coverage-html coverage

# View report
open coverage/index.html

# Generate other formats
phpunit --coverage-clover coverage.xml
phpunit --coverage-text
```

**Configuration** (phpunit.xml):
```xml
<coverage>
    <include>
        <directory suffix=".php">src</directory>
    </include>
    <exclude>
        <directory>tests</directory>
    </exclude>
</coverage>
```

## Interpreting Coverage Reports

### Key Metrics

- **Line Coverage**: Percentage of lines executed
- **Branch Coverage**: Percentage of conditional branches taken
- **Function Coverage**: Percentage of functions called
- **Statement Coverage**: Percentage of statements executed

### Identifying Uncovered Code

1. **Zero coverage files**: Files with 0% coverage - safe to remove if not imported
2. **Uncovered functions**: Functions never called - candidates for removal
3. **Uncovered branches**: Dead code paths - can be simplified
4. **Uncovered lines**: Unreachable code - can be removed

### Coverage Report Analysis

Look for:
- Files with 0% coverage
- Functions/methods with 0% coverage
- Large blocks of consecutive uncovered lines
- Branches that are never taken (always true/false conditions)
- Exception handlers never triggered
