---
name: bisect-aware-instrumentation
description: Instrument code to support efficient git bisect by producing deterministic pass/fail signals and concise runtime summaries for each tested commit. Use when debugging regressions with git bisect, automating bisect workflows, creating bisect test scripts, handling flaky tests during bisection, or needing clear exit codes and logging for automated bisect runs. Helps identify the exact commit that introduced a bug through automated testing.
---

# Bisect-Aware Instrumentation

## Overview

Instrument code to support efficient git bisect operations by producing deterministic pass/fail signals and concise runtime summaries. This skill helps create robust test scripts that work reliably with `git bisect run`, handling edge cases like flaky tests, build failures, and non-deterministic behavior.

## Core Workflow

### 1. Understand the Regression

Before instrumenting, clarify:
- What behavior changed? (bug introduced, performance regression, test failure)
- What is the "good" commit? (known working state)
- What is the "bad" commit? (known broken state)
- How to reproduce the issue? (test command, manual steps)

### 2. Create Bisect Test Script

Generate a test script that returns proper exit codes for git bisect:

**Exit Code Convention**:
- `0`: Good commit (test passes)
- `1-124, 126-127`: Bad commit (test fails)
- `125`: Skip commit (cannot test - build failure, missing dependencies)

**Template**:
```bash
#!/bin/bash
# bisect_test.sh - Test script for git bisect run

set -e  # Exit on error

# Build/setup phase
if ! make build 2>/dev/null; then
    echo "SKIP: Build failed"
    exit 125
fi

# Run test with timeout
timeout 30s ./run_test || TEST_RESULT=$?

# Interpret results
if [ $TEST_RESULT -eq 0 ]; then
    echo "GOOD: Test passed"
    exit 0
elif [ $TEST_RESULT -eq 124 ]; then
    echo "SKIP: Test timeout"
    exit 125
else
    echo "BAD: Test failed with code $TEST_RESULT"
    exit 1
fi
```

### 3. Add Determinism Safeguards

Handle non-deterministic behavior:

**Retry Logic for Flaky Tests**:
```bash
# Run test multiple times to confirm
PASS_COUNT=0
for i in {1..3}; do
    if ./run_test; then
        ((PASS_COUNT++))
    fi
done

if [ $PASS_COUNT -eq 3 ]; then
    echo "GOOD: All 3 runs passed"
    exit 0
elif [ $PASS_COUNT -eq 0 ]; then
    echo "BAD: All 3 runs failed"
    exit 1
else
    echo "SKIP: Flaky test ($PASS_COUNT/3 passed)"
    exit 125
fi
```

**Environment Isolation**:
```bash
# Clean state before each test
rm -rf /tmp/test_cache
export RANDOM_SEED=42
export TZ=UTC
```

### 4. Add Logging and Summaries

Generate concise output for each commit:

```bash
#!/bin/bash
COMMIT=$(git rev-parse --short HEAD)
LOG_FILE="bisect_log_${COMMIT}.txt"

echo "Testing commit: $COMMIT" | tee $LOG_FILE
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a $LOG_FILE

# Run test and capture output
if ./run_test > test_output.txt 2>&1; then
    echo "RESULT: GOOD" | tee -a $LOG_FILE
    exit 0
else
    echo "RESULT: BAD" | tee -a $LOG_FILE
    echo "Error output:" | tee -a $LOG_FILE
    tail -20 test_output.txt | tee -a $LOG_FILE
    exit 1
fi
```

### 5. Run Git Bisect

Execute the bisect workflow:

```bash
# Start bisect
git bisect start

# Mark known good and bad commits
git bisect bad HEAD
git bisect good v1.2.0

# Run automated bisect
chmod +x bisect_test.sh
git bisect run ./bisect_test.sh

# Review results
git bisect log
```

## Instrumentation Patterns

### Pattern 1: Performance Regression Detection

```bash
#!/bin/bash
# Detect when performance drops below threshold

THRESHOLD=1000  # milliseconds

# Run benchmark
DURATION=$(./benchmark | grep "Duration:" | awk '{print $2}')

if [ -z "$DURATION" ]; then
    echo "SKIP: Benchmark failed to run"
    exit 125
fi

if [ $DURATION -lt $THRESHOLD ]; then
    echo "GOOD: Performance $DURATION ms (< $THRESHOLD ms)"
    exit 0
else
    echo "BAD: Performance $DURATION ms (>= $THRESHOLD ms)"
    exit 1
fi
```

### Pattern 2: Test Suite Bisection

```bash
#!/bin/bash
# Find commit that broke specific test

TEST_NAME="test_user_authentication"

# Run specific test
if pytest tests/${TEST_NAME}.py -v; then
    echo "GOOD: $TEST_NAME passed"
    exit 0
else
    echo "BAD: $TEST_NAME failed"
    exit 1
fi
```

### Pattern 3: Build Failure Detection

```bash
#!/bin/bash
# Find commit that broke the build

if make clean && make all; then
    echo "GOOD: Build succeeded"
    exit 0
else
    echo "BAD: Build failed"
    exit 1
fi
```

### Pattern 4: Output Validation

```bash
#!/bin/bash
# Find commit that changed program output

EXPECTED_OUTPUT="Success: 42"

ACTUAL_OUTPUT=$(./program 2>&1)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "GOOD: Output matches expected"
    exit 0
else
    echo "BAD: Output mismatch"
    echo "  Expected: $EXPECTED_OUTPUT"
    echo "  Actual: $ACTUAL_OUTPUT"
    exit 1
fi
```

## Advanced Techniques

### Handling Complex Build Systems

```bash
#!/bin/bash
# Handle projects with complex dependencies

# Check if dependencies are available
if ! command -v node &> /dev/null; then
    echo "SKIP: Node.js not available in this commit"
    exit 125
fi

# Install dependencies (with caching)
if [ -f package.json ]; then
    npm ci --silent || {
        echo "SKIP: Dependency installation failed"
        exit 125
    }
fi

# Run test
npm test
```

### Parallel Test Execution

```bash
#!/bin/bash
# Run multiple tests in parallel for faster bisection

# Run tests in parallel
parallel --halt soon,fail=1 ::: \
    "pytest tests/unit/" \
    "pytest tests/integration/" \
    "npm run lint"

if [ $? -eq 0 ]; then
    echo "GOOD: All tests passed"
    exit 0
else
    echo "BAD: At least one test failed"
    exit 1
fi
```

### State Preservation

```bash
#!/bin/bash
# Preserve state between bisect steps

STATE_DIR=".bisect_state"
mkdir -p $STATE_DIR

# Save current commit info
git rev-parse HEAD > $STATE_DIR/current_commit

# Run test
./run_test
RESULT=$?

# Log result
echo "$(git rev-parse --short HEAD): $RESULT" >> $STATE_DIR/results.log

exit $RESULT
```

## Troubleshooting

### Issue: Bisect Marks Wrong Commit

**Cause**: Test script has incorrect exit codes or flaky behavior

**Solution**: Add verbose logging and retry logic
```bash
set -x  # Enable debug output
# Add retry logic as shown in section 3
```

### Issue: Too Many Commits Skipped

**Cause**: Build failures or missing dependencies across history

**Solution**: Use broader skip conditions
```bash
# Skip commits with known issues
if git log -1 --format=%s | grep -q "WIP\|broken"; then
    echo "SKIP: Known broken commit"
    exit 125
fi
```

### Issue: Bisect Takes Too Long

**Cause**: Slow test execution

**Solution**: Optimize test or use binary search hints
```bash
# Use timeout to fail fast
timeout 10s ./run_test || exit 125

# Or provide bisect hints
git bisect skip $(git rev-list --grep="refactor" HEAD~50..HEAD)
```

## Best Practices

1. **Make tests deterministic**: Fix random seeds, timestamps, and external dependencies
2. **Use timeouts**: Prevent hanging tests from blocking bisect
3. **Log everything**: Save detailed logs for each tested commit
4. **Handle build failures gracefully**: Use exit code 125 to skip untestable commits
5. **Test the test script**: Verify it works on known good and bad commits before bisecting
6. **Keep it fast**: Optimize tests to run quickly (bisect tests O(log n) commits)

## Quick Reference

**Start bisect**:
```bash
git bisect start
git bisect bad <bad-commit>
git bisect good <good-commit>
```

**Run automated bisect**:
```bash
git bisect run ./bisect_test.sh
```

**Manual bisect**:
```bash
git bisect good  # Current commit is good
git bisect bad   # Current commit is bad
git bisect skip  # Cannot test current commit
```

**End bisect**:
```bash
git bisect reset
```

## Resources

- **[references/git_bisect_guide.md](references/git_bisect_guide.md)**: Comprehensive git bisect documentation
- **[references/exit_codes.md](references/exit_codes.md)**: Exit code conventions and best practices
- **scripts/bisect_template.sh**: Template bisect test script
- **scripts/bisect_wrapper.py**: Python wrapper for complex bisect logic
