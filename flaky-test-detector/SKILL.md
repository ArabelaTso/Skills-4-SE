---
name: flaky-test-detector
description: Identifies non-deterministic or unreliable tests through static code analysis and test result analysis. Use when Claude needs to find flaky tests, analyze test reliability, or investigate intermittent test failures. Supports Python (pytest, unittest) and Java (JUnit, TestNG) test frameworks. Trigger when users mention "flaky tests", "intermittent failures", "non-deterministic tests", "unreliable tests", or ask to "find flaky tests", "analyze test stability", or "why tests fail randomly".
---

# Flaky Test Detector

Identify and fix non-deterministic tests that intermittently fail without code changes.

## Quick Start

When a user reports flaky tests or asks for test reliability analysis:

1. **Identify the approach**: Determine if analyzing code patterns or test execution results
2. **Analyze for flakiness**: Look for common flaky patterns in test code or execution history
3. **Report findings**: List identified flaky tests with specific issues
4. **Suggest fixes**: Provide concrete remediation strategies

## What Makes Tests Flaky

Flaky tests fail intermittently without code changes due to:

- **Timing issues**: Race conditions, fixed sleeps, async/await problems
- **State management**: Shared state between tests, improper cleanup
- **External dependencies**: Network calls, database connections, file system
- **Randomness**: Unseeded random data, UUID generation
- **Time dependencies**: Current time/date, timezone assumptions
- **Resource issues**: Leaks, insufficient cleanup
- **Test order**: Dependencies between tests
- **Environment**: Hardcoded paths, missing env vars

## Detection Methods

### Static Code Analysis

Analyze test code for common flaky patterns.

**When to use:**
- Reviewing test code for potential issues
- Proactive flakiness prevention
- Code review of new tests
- Refactoring existing tests

**Process:**
1. Read test files
2. Search for flaky patterns (see [flaky-patterns.md](references/flaky-patterns.md))
3. Identify specific issues with line numbers
4. Suggest fixes (see [remediation-strategies.md](references/remediation-strategies.md))

**Common patterns to detect:**

**Timing issues:**
- `time.sleep()`, `Thread.sleep()` - Fixed waits
- Missing `await` in async functions
- Race conditions with threading

**State issues:**
- Class or global variables in test classes
- Missing setUp/tearDown or fixtures
- Database operations without cleanup

**External dependencies:**
- `requests.get()`, `http.client` - Real network calls
- Database connections to production/external DBs
- File operations without temp directories

**Randomness:**
- `random.` without seed
- `UUID.randomUUID()` without mocking
- Non-deterministic data generation

**Time dependencies:**
- `datetime.now()`, `System.currentTimeMillis()`
- Timezone-dependent assertions
- Date comparisons without mocking

### Test Result Analysis

Analyze test execution history to find inconsistent results.

**When to use:**
- Tests are failing intermittently in CI/CD
- Investigating specific test reliability
- Analyzing test suite health
- Tracking flakiness over time

**Process:**
1. Collect test results from multiple runs
2. Use `scripts/analyze_test_results.py` to analyze patterns
3. Review flakiness scores and patterns
4. Investigate high-scoring tests

**Script usage:**
```bash
python scripts/analyze_test_results.py test_results.json
```

**Input format (JSON):**
```json
[
  {
    "test_name": "test_user_login",
    "status": "passed",
    "timestamp": "2024-01-01T10:00:00",
    "duration": 1.23
  },
  {
    "test_name": "test_user_login",
    "status": "failed",
    "timestamp": "2024-01-01T11:00:00",
    "duration": 1.45
  }
]
```

**Metrics:**
- **Flakiness score**: 0-1, higher = more flaky (based on pass rate variance)
- **Pass rate**: Percentage of successful runs
- **Pattern**: Recent pass/fail sequence (P = pass, F = fail)
- **Alternating**: Whether test alternates between pass/fail
- **Duration variance**: Inconsistent execution time indicates issues

## Framework-Specific Guidance

### Python (pytest, unittest)

**Common issues:**
- Missing fixtures or improper fixture scope
- Shared class variables
- Not using `tmp_path` for file operations
- Missing `@pytest.mark.django_db` for database tests
- Unseeded `random` module usage

**Best practices:**
- Use fixtures for test data and cleanup
- Use `tmp_path` fixture for file operations
- Mock external calls with `pytest-mock` or `unittest.mock`
- Use `freezegun` for time mocking
- Seed random with `random.seed()`

### Java (JUnit, TestNG)

**Common issues:**
- Static variables in test classes
- Missing `@Before`/`@After` cleanup
- Not using `@Transactional` for database tests
- Fixed `Thread.sleep()` calls
- Hardcoded file paths

**Best practices:**
- Use `@Before`/`@After` for setup/cleanup
- Use `@Transactional` for automatic rollback
- Mock with Mockito
- Use `Clock` for time mocking
- Use try-with-resources for resource management

## Workflow

### 1. Understand the Context

Ask clarifying questions:
- What tests are flaky?
- How often do they fail?
- What's the failure pattern?
- Any recent changes?
- CI/CD or local environment?

### 2. Choose Detection Method

**Static analysis** if:
- Reviewing code proactively
- No test execution history available
- Want to prevent flakiness

**Result analysis** if:
- Have test execution history
- Tests failing intermittently
- Need to quantify flakiness

### 3. Analyze for Flakiness

**For static analysis:**
- Read test files
- Search for patterns from [flaky-patterns.md](references/flaky-patterns.md)
- Note specific issues with line numbers
- Categorize by issue type

**For result analysis:**
- Run `analyze_test_results.py` script
- Review flakiness scores
- Identify high-risk tests
- Examine failure patterns

### 4. Report Findings

Structure the report:
- **Summary**: Number of flaky tests found
- **High priority**: Tests with highest flakiness scores
- **By category**: Group by issue type
- **Specific issues**: File paths and line numbers

Example format:
```
Found 5 potentially flaky tests:

HIGH PRIORITY:
- test_user_login (flakiness: 0.85)
  - Line 45: time.sleep(2) - fixed wait
  - Line 52: Shared class variable 'user_data'

MEDIUM PRIORITY:
- test_api_call (flakiness: 0.62)
  - Line 23: requests.get() - unmocked network call
```

### 5. Suggest Remediation

For each issue, provide:
- **What's wrong**: Explain the flaky pattern
- **Why it's flaky**: Describe the non-determinism
- **How to fix**: Concrete code example

Reference [remediation-strategies.md](references/remediation-strategies.md) for detailed fixes.

## Example Usage Patterns

**User:** "Our test_checkout test keeps failing randomly"
→ Analyze test code for flaky patterns, report findings with fixes

**User:** "Find all flaky tests in the test suite"
→ Scan all test files for common flaky patterns

**User:** "This test has a 60% pass rate, why?"
→ Analyze test code and suggest specific fixes

**User:** "Analyze these test results for flakiness"
→ Use analyze_test_results.py script on provided data

**User:** "How do I fix this race condition in my test?"
→ Provide remediation strategy with code examples

**User:** "Review this test for potential flakiness"
→ Static analysis of specific test with recommendations

## Best Practices

### Detection
- Look for multiple flaky patterns, not just one
- Consider the test framework's idioms
- Check both test code and test fixtures/setup
- Review recent changes that might introduce flakiness

### Reporting
- Prioritize by severity and frequency
- Provide specific line numbers
- Group related issues together
- Include confidence level in assessment

### Remediation
- Suggest framework-appropriate fixes
- Provide complete code examples
- Explain why the fix works
- Consider test maintainability

### Prevention
- Recommend test design patterns
- Suggest CI/CD improvements (retry policies, test isolation)
- Encourage test independence
- Promote proper mocking and fixtures
