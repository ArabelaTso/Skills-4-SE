# Test Automation Suite

Comprehensive test generation, optimization, and automation toolkit for all your testing needs.

## 📦 Included Skills (18)

### Test Generation
- **unit-test-generator** - Generate unit tests automatically
- **metamorphic-test-generator** - Generate metamorphic tests
- **mocking-test-generator** - Generate tests with mocks
- **bug-reproduction-test-generator** - Create tests that reproduce bugs
- **req-to-test** - Generate tests from requirements
- **test-driven-generation** - TDD-style code generation

### Regression Testing
- **java-regression-test-generator** - Generate Java regression tests
- **python-regression-test-generator** - Generate Python regression tests
- **java-test-updater** - Update Java tests after code changes
- **python-test-updater** - Update Python tests after code changes

### Test Optimization
- **mutation-test-suite-optimizer** - Optimize test suites using mutation testing
- **test-case-reducer** - Reduce test cases while maintaining coverage
- **test-deduplicator** - Remove duplicate tests
- **test-suite-prioritizer** - Prioritize test execution order
- **coverage-enhancer** - Improve test coverage

### Test Quality
- **test-oracle-generator** - Generate test oracles
- **test-case-documentation** - Document test cases
- **smart-mutation-operator-generator** - Generate effective mutation operators

## 🎯 Use Cases

### 1. Complete Test Suite Generation
```bash
# Generate unit tests
/unit-test-generator --source src/Calculator.java

# Add metamorphic tests
/metamorphic-test-generator --source src/Calculator.java

# Generate test oracles
/test-oracle-generator --tests test/CalculatorTest.java
```

### 2. Test Suite Optimization
```bash
# Remove duplicates
/test-deduplicator --test-dir tests/

# Optimize with mutation testing
/mutation-test-suite-optimizer --tests tests/ --source src/

# Prioritize execution
/test-suite-prioritizer --tests tests/ --strategy coverage
```

### 3. Regression Testing
```bash
# Generate regression tests
/python-regression-test-generator --old-version v1.0 --new-version v2.0

# Update existing tests
/python-test-updater --tests tests/ --changes changes.diff
```

### 4. Requirements-Based Testing
```bash
# Generate tests from requirements
/req-to-test --requirements requirements.md --output tests/

# Document test coverage
/test-case-documentation --tests tests/ --requirements requirements.md
```

## 🚀 Installation

```bash
cd skill-packs/test-automation-suite
./install.sh
```

## 📊 Testing Workflow

```
Requirements → Test Generation → Test Execution
     ↓              ↓                  ↓
Coverage Analysis ← Test Optimization → Bug Detection
```

## 🔗 Related Skill Packs

- **bug-fixing-suite** - Generate tests for bug reproduction
- **code-quality-toolkit** - Ensure testable code
- **formal-verification-toolkit** - Formal test properties

## 📖 Examples

### Example 1: TDD Workflow

```bash
# Start with requirements
/req-to-test --requirements feature.md

# Generate initial tests
/unit-test-generator --source src/Feature.java

# Implement code using TDD
/test-driven-generation --tests test/FeatureTest.java
```

### Example 2: Improve Test Suite

```bash
# Check current coverage
/coverage-enhancer --analyze --tests tests/

# Remove duplicates
/test-deduplicator --tests tests/

# Optimize with mutation testing
/mutation-test-suite-optimizer --tests tests/ --source src/

# Prioritize for CI
/test-suite-prioritizer --tests tests/ --strategy fast-fail
```

### Example 3: Regression Testing

```bash
# After code changes
/python-test-updater --tests tests/ --changes git-diff.patch

# Generate new regression tests
/python-regression-test-generator --baseline v1.0 --current HEAD

# Document changes
/test-case-documentation --tests tests/ --output test-docs.md
```

## 🛠️ Requirements

- Claude Code CLI
- Language-specific test frameworks (JUnit, pytest, etc.)
- Coverage tools (optional, for coverage-enhancer)

## 📝 License

MIT
