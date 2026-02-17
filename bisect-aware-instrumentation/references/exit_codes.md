# Exit Code Conventions for Git Bisect

## Overview

Exit codes are the primary communication mechanism between test scripts and git bisect. Understanding and using the correct exit codes is critical for successful automated bisection.

## Standard Exit Codes

### Exit Code 0: Good Commit

**Meaning**: The test passed; this commit does not contain the bug.

**When to use**:
- All tests pass
- Expected behavior is observed
- Performance meets requirements
- Build succeeds and tests pass

**Example**:
```bash
#!/bin/bash
if ./run_tests.sh; then
    echo "GOOD: Tests passed"
    exit 0
fi
```

### Exit Codes 1-124, 126-127: Bad Commit

**Meaning**: The test failed; this commit contains the bug or regression.

**When to use**:
- Tests fail
- Unexpected behavior occurs
- Performance regression detected
- Output doesn't match expected

**Common conventions**:
- `1`: General test failure
- `2`: Misuse of shell command
- `126`: Command cannot execute
- `127`: Command not found

**Example**:
```bash
#!/bin/bash
if ! ./run_tests.sh; then
    echo "BAD: Tests failed"
    exit 1
fi
```

### Exit Code 125: Skip Commit

**Meaning**: Cannot test this commit; skip it and try another.

**When to use**:
- Build fails
- Missing dependencies
- Test infrastructure not available
- Known broken commit (WIP)
- Test timeout
- Flaky test results

**Example**:
```bash
#!/bin/bash
# Skip if build fails
if ! make build 2>/dev/null; then
    echo "SKIP: Build failed"
    exit 125
fi

# Skip if dependencies missing
if ! command -v pytest &> /dev/null; then
    echo "SKIP: pytest not available"
    exit 125
fi

# Skip on timeout
timeout 30s ./run_tests.sh || {
    echo "SKIP: Test timeout"
    exit 125
}
```

### Exit Codes 128+: Fatal Error

**Meaning**: Fatal error occurred; abort bisect.

**When to use**:
- Unrecoverable error
- Invalid bisect state
- Critical system failure

**Note**: Git itself uses 128+ for fatal errors. Avoid using these in test scripts unless you want to abort the entire bisect session.

## Exit Code Decision Tree

```
Start Test
    ↓
Can build? ──No──→ exit 125 (skip)
    ↓ Yes
    ↓
Dependencies OK? ──No──→ exit 125 (skip)
    ↓ Yes
    ↓
Run test with timeout
    ↓
Timeout? ──Yes──→ exit 125 (skip)
    ↓ No
    ↓
Test passed? ──Yes──→ exit 0 (good)
    ↓ No
    ↓
Flaky? ──Yes──→ exit 125 (skip)
    ↓ No
    ↓
exit 1 (bad)
```

## Best Practices

### 1. Be Conservative with "Bad"

Only mark a commit as bad (exit 1) when you're certain the bug exists. When in doubt, skip (exit 125).

**Bad practice**:
```bash
# Don't mark as bad if build fails
make build || exit 1  # Wrong!
```

**Good practice**:
```bash
# Skip if build fails
make build || exit 125  # Correct!
```

### 2. Handle Timeouts Explicitly

Timeouts usually indicate an untestable commit, not a bad commit.

```bash
#!/bin/bash
timeout 30s ./run_tests.sh
RESULT=$?

if [ $RESULT -eq 124 ]; then
    echo "SKIP: Test timeout"
    exit 125
elif [ $RESULT -eq 0 ]; then
    echo "GOOD: Test passed"
    exit 0
else
    echo "BAD: Test failed"
    exit 1
fi
```

### 3. Distinguish Build Failures from Test Failures

Build failures should skip; test failures should mark as bad.

```bash
#!/bin/bash
# Build phase - skip on failure
if ! make build; then
    echo "SKIP: Build failed"
    exit 125
fi

# Test phase - mark as bad on failure
if ! make test; then
    echo "BAD: Test failed"
    exit 1
fi

echo "GOOD: All passed"
exit 0
```

### 4. Handle Flaky Tests

Flaky tests should be retried, and inconsistent results should skip.

```bash
#!/bin/bash
PASS_COUNT=0

for i in {1..3}; do
    if ./run_tests.sh; then
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

## Common Patterns

### Pattern 1: Simple Test

```bash
#!/bin/bash
./run_tests.sh
exit $?  # Pass through exit code
```

**Problem**: Doesn't handle build failures or timeouts.

**Better**:
```bash
#!/bin/bash
make build || exit 125
timeout 30s ./run_tests.sh || exit 1
exit 0
```

### Pattern 2: Multi-Stage Testing

```bash
#!/bin/bash
set -e  # Exit on error

# Stage 1: Build (skip on failure)
make build || exit 125

# Stage 2: Unit tests (bad on failure)
make test-unit || exit 1

# Stage 3: Integration tests (bad on failure)
make test-integration || exit 1

# All passed
exit 0
```

### Pattern 3: Performance Testing

```bash
#!/bin/bash
THRESHOLD=1000

# Build
make build || exit 125

# Run benchmark
DURATION=$(./benchmark | grep "Duration:" | awk '{print $2}')

# Check if benchmark ran
if [ -z "$DURATION" ]; then
    echo "SKIP: Benchmark failed to run"
    exit 125
fi

# Check performance
if [ $DURATION -lt $THRESHOLD ]; then
    echo "GOOD: Performance ${DURATION}ms < ${THRESHOLD}ms"
    exit 0
else
    echo "BAD: Performance ${DURATION}ms >= ${THRESHOLD}ms"
    exit 1
fi
```

### Pattern 4: Conditional Skip

```bash
#!/bin/bash

# Skip known broken commits
if git log -1 --format=%s | grep -qE "WIP|BROKEN"; then
    echo "SKIP: Known broken commit"
    exit 125
fi

# Skip if feature not yet implemented
if ! grep -q "feature_flag" src/config.py; then
    echo "SKIP: Feature not yet implemented"
    exit 125
fi

# Run test
./run_tests.sh
exit $?
```

## Exit Code Testing

### Test Your Test Script

Before running bisect, verify exit codes on known commits:

```bash
#!/bin/bash
# test_bisect_script.sh - Verify bisect script exit codes

SCRIPT="./bisect_test.sh"
GOOD_COMMIT="v1.0"
BAD_COMMIT="HEAD"

echo "Testing bisect script..."

# Test on good commit
git checkout $GOOD_COMMIT
$SCRIPT
GOOD_EXIT=$?

if [ $GOOD_EXIT -ne 0 ]; then
    echo "ERROR: Good commit returned exit code $GOOD_EXIT (expected 0)"
    exit 1
fi

# Test on bad commit
git checkout $BAD_COMMIT
$SCRIPT
BAD_EXIT=$?

if [ $BAD_EXIT -eq 0 ]; then
    echo "ERROR: Bad commit returned exit code 0 (expected 1)"
    exit 1
fi

if [ $BAD_EXIT -eq 125 ]; then
    echo "WARNING: Bad commit returned exit code 125 (skip)"
fi

echo "✓ Bisect script exit codes are correct"
```

### Debug Exit Codes

Add verbose logging to understand exit codes:

```bash
#!/bin/bash
set -x  # Enable debug output

# Your test logic here
./run_tests.sh
EXIT_CODE=$?

echo "Test exited with code: $EXIT_CODE"

# Interpret exit code
case $EXIT_CODE in
    0)
        echo "Interpretation: GOOD"
        ;;
    125)
        echo "Interpretation: SKIP"
        ;;
    *)
        echo "Interpretation: BAD"
        ;;
esac

exit $EXIT_CODE
```

## Language-Specific Exit Codes

### Python

```python
#!/usr/bin/env python3
import sys
import subprocess

# Good
sys.exit(0)

# Bad
sys.exit(1)

# Skip
sys.exit(125)

# Run subprocess and propagate exit code
result = subprocess.run(['pytest', 'tests/'])
sys.exit(result.returncode)
```

### Node.js

```javascript
#!/usr/bin/env node

// Good
process.exit(0);

// Bad
process.exit(1);

// Skip
process.exit(125);

// Run command and propagate exit code
const { spawnSync } = require('child_process');
const result = spawnSync('npm', ['test']);
process.exit(result.status);
```

### Ruby

```ruby
#!/usr/bin/env ruby

# Good
exit 0

# Bad
exit 1

# Skip
exit 125

# Run command and propagate exit code
system('rake test')
exit $?.exitstatus
```

## Troubleshooting

### Problem: Bisect Marks Wrong Commit

**Cause**: Incorrect exit codes in test script.

**Solution**: Add logging to verify exit codes:
```bash
#!/bin/bash
./run_tests.sh
EXIT_CODE=$?
echo "Exit code: $EXIT_CODE" >> bisect_debug.log
exit $EXIT_CODE
```

### Problem: All Commits Skipped

**Cause**: Test script always returns 125.

**Solution**: Review skip conditions:
```bash
# Too aggressive skipping
if ! make build; then
    exit 125  # This might skip everything
fi

# Better: only skip on specific build errors
if ! make build 2>&1 | grep -v "warning"; then
    exit 125
fi
```

### Problem: Bisect Never Finds Bad Commit

**Cause**: Test script always returns 0 (good).

**Solution**: Verify test actually detects the bug:
```bash
# Test the test on known bad commit
git checkout <bad-commit>
./bisect_test.sh
echo "Exit code: $?"  # Should be 1, not 0
```

## Summary

| Exit Code | Meaning | Use Case |
|-----------|---------|----------|
| 0 | Good | Test passed, no bug |
| 1 | Bad | Test failed, bug present |
| 125 | Skip | Cannot test this commit |
| 128+ | Fatal | Abort bisect (rare) |

**Golden Rule**: When in doubt, skip (exit 125) rather than marking as bad (exit 1).
