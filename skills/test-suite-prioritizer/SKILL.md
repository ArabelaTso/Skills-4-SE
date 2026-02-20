---
name: test-suite-prioritizer
description: Analyzes test suites and suggests optimal test execution order based on code change impact and project requirements. Use when optimizing CI/CD pipelines, deciding which tests to run before committing, or selecting critical tests under time constraints. Prioritizes tests by analyzing recently modified files, test dependencies, and coverage overlap. Outputs detailed rankings with priority scores and reasoning to help teams run the most impactful tests first.
---

# Test Suite Prioritizer

Intelligently prioritize test execution based on code changes and project impact.

## Core Capabilities

This skill helps optimize test execution by:

1. **Analyzing code changes** - Identifying which files were modified
2. **Mapping test coverage** - Determining which tests cover changed code
3. **Calculating priority scores** - Ranking tests by impact and relevance
4. **Generating execution order** - Creating an optimized test run sequence
5. **Providing reasoning** - Explaining why each test is prioritized

## Test Prioritization Workflow

### Step 1: Identify Code Changes

Determine what code has been modified to focus testing efforts.

**Sources of Change Information:**
- Git diff (most recent commit or uncommitted changes)
- Pull request file list
- Specific files mentioned by user
- Modified files in working directory

**Collect Changed Files:**

```bash
# Recent commit changes
git diff --name-only HEAD~1 HEAD

# Uncommitted changes
git diff --name-only

# Changes in current branch vs main
git diff --name-only main...HEAD

# Files in last N commits
git diff --name-only HEAD~N HEAD
```

**Example Output:**
```
src/auth/login.py
src/payment/processor.py
src/models/user.py
tests/test_auth.py
```

### Step 2: Analyze Test Coverage

Map which tests cover the changed code.

**Strategies:**

**1. Direct Test-to-Code Mapping**
- Tests in same directory as changed code
- Tests with similar names (e.g., `user.py` → `test_user.py`)
- Integration tests that import changed modules

**2. Static Analysis**
- Parse test files for imports
- Identify which modules each test uses
- Map dependencies transitively

**3. Coverage Data (if available)**
- Use pytest-cov, coverage.py, JaCoCo output
- Identify tests that execute changed lines
- Most accurate but requires prior test run

**Example Mapping:**

```
Changed: src/auth/login.py
Covered by:
  - tests/test_auth.py::test_login_success
  - tests/test_auth.py::test_login_failure
  - tests/integration/test_user_flow.py::test_complete_registration
  - tests/e2e/test_authentication_flow.py::test_full_auth_cycle

Changed: src/payment/processor.py
Covered by:
  - tests/test_payment.py::test_process_payment
  - tests/test_payment.py::test_refund
  - tests/integration/test_checkout.py::test_complete_purchase
```

### Step 3: Calculate Priority Scores

Assign priority scores based on change impact.

**Scoring Formula:**

```
Priority Score = Base Score × Change Impact Factor

Base Score factors:
- Direct coverage of changed file: +10 points
- Indirect coverage (imports changed file): +5 points
- Integration test covering changed area: +3 points
- Test in same module: +2 points

Change Impact Factor (multiply):
- Critical path code (auth, payments): ×1.5
- Recently failed test: ×1.3
- High historical failure rate: ×1.2
- Core business logic: ×1.2
- UI/cosmetic changes: ×0.8
```

**Example Scoring:**

```python
# Example: test_login_success
base_score = 10  # Directly tests login.py (changed)
impact_factor = 1.5  # Auth is critical path
priority_score = 10 × 1.5 = 15

# Example: test_user_flow
base_score = 5 + 3  # Imports login.py + integration test
impact_factor = 1.2  # Core business logic
priority_score = 8 × 1.2 = 9.6

# Example: test_ui_styling
base_score = 2  # Same module as changed file
impact_factor = 0.8  # UI/cosmetic
priority_score = 2 × 0.8 = 1.6
```

### Step 4: Generate Prioritized Test List

Create ordered execution sequence with scores and reasoning.

**Output Format:**

```markdown
# Test Execution Priority List

## Summary
- Total tests analyzed: 45
- High priority (score ≥ 10): 8 tests
- Medium priority (score 5-9): 15 tests
- Low priority (score < 5): 22 tests
- Estimated time for high priority tests: ~2 minutes

## Recommended Execution Order

### Priority 1: Critical Tests (Run First)

1. **tests/test_auth.py::test_login_success** (Score: 15.0)
   - Directly tests modified file: src/auth/login.py
   - Critical path: Authentication
   - Reason: Core security functionality changed

2. **tests/test_auth.py::test_login_failure** (Score: 15.0)
   - Directly tests modified file: src/auth/login.py
   - Critical path: Authentication
   - Reason: Error handling for authentication changed

3. **tests/test_payment.py::test_process_payment** (Score: 15.0)
   - Directly tests modified file: src/payment/processor.py
   - Critical path: Payment processing
   - Reason: Payment logic modified, high business impact

### Priority 2: High Impact Tests

4. **tests/integration/test_user_flow.py::test_complete_registration** (Score: 9.6)
   - Indirect coverage: Imports src/auth/login.py
   - Integration test: End-to-end user flow
   - Reason: Validates auth changes in realistic scenario

5. **tests/integration/test_checkout.py::test_complete_purchase** (Score: 9.6)
   - Indirect coverage: Imports src/payment/processor.py
   - Integration test: Full checkout flow
   - Reason: Validates payment changes with real workflow

6. **tests/test_models.py::test_user_model** (Score: 7.0)
   - Related file: src/models/user.py modified
   - Dependency: Auth and payment depend on user model
   - Reason: Foundation for changed functionality

### Priority 3: Supporting Tests

7. **tests/test_validators.py::test_email_validation** (Score: 4.0)
   - Indirect dependency: Used by auth module
   - Reason: Input validation for authentication

8. **tests/e2e/test_authentication_flow.py::test_full_auth_cycle** (Score: 3.9)
   - E2E coverage: Complete authentication flow
   - Reason: Comprehensive validation but slow to execute

[... remaining tests with lower scores ...]

## Quick Commands

Run high priority tests only (8 tests, ~2 min):
```bash
pytest tests/test_auth.py::test_login_success \
       tests/test_auth.py::test_login_failure \
       tests/test_payment.py::test_process_payment \
       tests/integration/test_user_flow.py::test_complete_registration \
       tests/integration/test_checkout.py::test_complete_purchase \
       tests/test_models.py::test_user_model \
       tests/test_validators.py::test_email_validation \
       tests/e2e/test_authentication_flow.py::test_full_auth_cycle
```

Run critical tests only (3 tests, ~30 sec):
```bash
pytest tests/test_auth.py tests/test_payment.py::test_process_payment
```

## Time Estimates

- Critical tests (3): ~30 seconds
- High priority tests (8): ~2 minutes
- All prioritized tests (23): ~5 minutes
- Full test suite (45): ~15 minutes

## Recommendations

1. **Pre-commit**: Run critical tests (score ≥ 15) before committing
2. **CI fast lane**: Run high priority tests (score ≥ 9) in first stage
3. **Full validation**: Run all tests in parallel after merge
```

### Step 5: Handle Special Cases

Adjust prioritization for specific scenarios.

**Time-Constrained Testing:**

```markdown
## 1-Minute Quick Check (Top 3 Critical Tests)

pytest tests/test_auth.py::test_login_success \
       tests/test_auth.py::test_login_failure \
       tests/test_payment.py::test_process_payment

These cover the most critical changed functionality.
```

**Post-Refactoring:**

```markdown
## Post-Refactor Validation

Changed file: src/utils/helpers.py (used by 25 modules)

Priority:
1. All tests directly importing helpers.py (18 tests)
2. Integration tests using helper functions (8 tests)
3. Tests in dependent modules (25 tests)

Reason: Wide-reaching refactor requires comprehensive validation.
```

**Flaky Test Handling:**

```markdown
## Note: Flaky Tests Detected

The following tests have high failure rates but low priority scores:
- tests/test_cache.py::test_concurrent_access (30% failure rate)
- tests/test_api.py::test_rate_limiting (25% failure rate)

Recommendation:
- Fix flaky tests before relying on prioritization
- Consider quarantining or mocking timing-dependent code
```

### Step 6: Provide Execution Guidance

Offer practical commands and strategies.

**For CI/CD Pipelines:**

```yaml
# .github/workflows/ci.yml example
jobs:
  quick-tests:
    name: Critical Tests (Fast Feedback)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run critical tests
        run: |
          # Run tests with score ≥ 15 first
          pytest -v tests/test_auth.py tests/test_payment.py

  full-tests:
    name: Complete Test Suite
    runs-on: ubuntu-latest
    needs: quick-tests  # Only run if critical tests pass
    steps:
      - uses: actions/checkout@v2
      - name: Run all tests
        run: pytest
```

**For Local Development:**

```bash
# Pre-commit hook (.git/hooks/pre-commit)
#!/bin/bash

# Get changed files
changed_files=$(git diff --cached --name-only)

# Run prioritized tests for changed files
if echo "$changed_files" | grep -q "src/auth/"; then
    pytest tests/test_auth.py || exit 1
fi

if echo "$changed_files" | grep -q "src/payment/"; then
    pytest tests/test_payment.py || exit 1
fi
```

**For Selective Test Execution:**

```python
# pytest conftest.py - custom marker
import pytest

def pytest_collection_modifyitems(config, items):
    # Mark tests based on priority
    for item in items:
        if "test_auth" in item.nodeid or "test_payment" in item.nodeid:
            item.add_marker(pytest.mark.critical)

# Run only critical tests
# pytest -m critical
```

## Prioritization Strategies

### Strategy 1: Code Change Impact (Primary)

Focus on tests covering modified code:

1. **Direct coverage** - Tests that explicitly test changed files
2. **Indirect coverage** - Tests that import/use changed modules
3. **Dependency coverage** - Tests for code that depends on changes

**When to use:**
- After code modifications
- Pre-commit validation
- Pull request testing

### Strategy 2: Risk-Based Prioritization

Prioritize based on business and technical risk:

**High Risk Areas:**
- Authentication and authorization
- Payment processing
- Data integrity (database operations)
- Security-critical functions
- APIs and public interfaces

**Medium Risk Areas:**
- Business logic
- User workflows
- Data validation
- Email/notification systems

**Low Risk Areas:**
- UI cosmetics
- Logging
- Internal utilities
- Development tools

### Strategy 3: Failure History

Prioritize tests that fail often:

```python
# Example: Analyze test failure history from CI
# tests with >10% historical failure rate get boosted priority

Historical Failures:
- test_concurrent_access: 12 failures / 100 runs = 12% → Priority boost ×1.2
- test_database_connection: 5 failures / 100 runs = 5% → No boost
```

### Strategy 4: Execution Time Optimization

Balance coverage with speed:

**Fast-First Strategy:**
- Run quick unit tests first (< 1 second each)
- Get rapid feedback on basic functionality
- Then run slower integration/E2E tests

**Critical-First Strategy:**
- Run most important tests first regardless of speed
- Better for catching major issues early
- May take longer for initial feedback

**Hybrid Approach (Recommended):**
- Run quick critical tests first (best of both worlds)
- Then slow critical tests
- Then fast non-critical tests
- Finally slow non-critical tests

## Analyzing Different Project Types

### Python (pytest)

**Analyze test structure:**

```bash
# Find all test files
find . -name "test_*.py" -o -name "*_test.py"

# Get test functions
pytest --collect-only -q

# Analyze imports in tests
grep -r "^import\|^from" tests/
```

### JavaScript/TypeScript (Jest)

**Analyze test structure:**

```bash
# Find test files
find . -name "*.test.js" -o -name "*.spec.js"

# Get test list
npm test -- --listTests

# Analyze coverage
npm test -- --coverage --coverageReporters=json
```

### Java (JUnit)

**Analyze test structure:**

```bash
# Find test classes
find . -name "*Test.java"

# Run with verbose output
mvn test -X

# Get test reports
cat target/surefire-reports/*.xml
```

## Best Practices

1. **Update prioritization regularly** - Re-analyze when code structure changes significantly
2. **Combine with coverage tools** - Use actual coverage data when available
3. **Consider test stability** - Deprioritize flaky tests or fix them first
4. **Balance speed and coverage** - Don't sacrifice important slow tests
5. **Communicate reasoning** - Explain why tests are prioritized to team
6. **Adjust for context** - Pre-commit vs. CI vs. nightly runs need different priorities
7. **Monitor effectiveness** - Track if prioritized tests catch bugs earlier
8. **Keep it simple** - Start with basic change-impact prioritization
9. **Document critical paths** - Maintain list of high-priority areas
10. **Automate where possible** - Integrate into CI/CD workflows

## Example Scenarios

### Scenario 1: Pre-Commit Validation

**Context:** Developer modified `src/auth/login.py`

**Prioritization:**
```
Top 3 tests to run (30 seconds):
1. tests/test_auth.py::test_login_success
2. tests/test_auth.py::test_login_failure
3. tests/test_auth.py::test_session_creation

Reasoning: Direct tests of changed functionality, fast execution.
```

### Scenario 2: CI/CD Fast Lane

**Context:** Pull request with 15 files changed across 3 modules

**Prioritization:**
```
Stage 1 - Critical Tests (2 min):
- All auth tests (5 tests)
- All payment tests (4 tests)
- Core user model tests (3 tests)

Stage 2 - Integration Tests (5 min):
- User flow integration (8 tests)
- API integration (6 tests)

Stage 3 - Full Suite (parallel, 10 min):
- Remaining tests (120 tests)

Reasoning: Fast feedback on critical paths, comprehensive validation in parallel.
```

### Scenario 3: Time-Constrained Testing

**Context:** 5 minutes before deadline, need to validate changes

**Prioritization:**
```
Must-run tests (2 min):
1. Tests directly covering changed files (8 tests)
2. Integration tests for critical paths (4 tests)

Nice-to-run tests (3 min):
3. Related unit tests (15 tests)

Skip for now:
- E2E tests (too slow)
- Unrelated tests (no impact)

Reasoning: Maximum validation coverage in minimum time.
```

## Resources

- **`references/prioritization_algorithms.md`** - Detailed algorithms and formulas for calculating priority scores
- **`references/framework_guides.md`** - Framework-specific commands for test analysis (pytest, jest, junit, etc.)

## Quick Reference

| Scenario | Priority Strategy | Recommended Tests |
|----------|------------------|-------------------|
| Pre-commit | Code change impact | Direct tests of modified files |
| CI fast lane | Critical path + changes | High-priority + change-impacted |
| Time-limited | Highest scores only | Top 10-20 by priority score |
| Post-refactor | Wide coverage | All tests touching refactored code |
| Nightly build | Full comprehensive | All tests (no prioritization) |
