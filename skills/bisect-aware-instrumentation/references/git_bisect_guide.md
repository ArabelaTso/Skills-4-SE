# Git Bisect Guide

## Overview

Git bisect is a powerful binary search tool for finding the commit that introduced a bug or regression. It efficiently narrows down the problematic commit by testing commits in a logarithmic manner.

## How Git Bisect Works

### Binary Search Algorithm

Given a range of commits between a known "good" state and a known "bad" state, git bisect uses binary search to find the first bad commit:

```
Total commits: 100
Bisect steps: log₂(100) ≈ 7 tests
```

### Example Timeline

```
v1.0 (good) ─── commit A ─── commit B ─── commit C ─── HEAD (bad)
                    ↓           ↓           ↓
                  Test 1      Test 2      Test 3
                  (good)      (bad)    (not needed)
                              ↑
                        First bad commit!
```

## Basic Workflow

### Manual Bisect

```bash
# Start bisect session
git bisect start

# Mark current commit as bad
git bisect bad

# Mark a known good commit
git bisect good v1.0

# Git checks out a commit in the middle
# Test the commit manually
./run_tests.sh

# Mark the result
git bisect good   # if test passes
# OR
git bisect bad    # if test fails

# Repeat until git identifies the first bad commit

# End bisect session
git bisect reset
```

### Automated Bisect

```bash
# Start and mark good/bad commits
git bisect start HEAD v1.0

# Run automated bisect with test script
git bisect run ./bisect_test.sh

# Git will automatically test commits and find the culprit

# Review the results
git bisect log

# Reset to original state
git bisect reset
```

## Exit Codes for Automated Bisect

Git bisect interprets exit codes from test scripts:

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Good commit | Mark as good, continue bisecting |
| 1-124, 126-127 | Bad commit | Mark as bad, continue bisecting |
| 125 | Skip commit | Cannot test, skip this commit |
| 128+ | Fatal error | Abort bisect |

### Why Exit Code 125?

Exit code 125 is special - it tells git bisect to skip a commit that cannot be tested:

**Common skip scenarios**:
- Build fails
- Missing dependencies
- Incomplete feature (WIP commits)
- Test infrastructure not yet available
- Known broken commits

**Example**:
```bash
#!/bin/bash
# Skip commits that don't build
if ! make build; then
    exit 125  # Skip this commit
fi

# Run test
./run_test
```

## Advanced Techniques

### Bisect with Specific File Paths

Limit bisect to commits that touched specific files:

```bash
git bisect start -- path/to/file.py
git bisect bad HEAD
git bisect good v1.0
git bisect run ./test.sh
```

### Bisect with Date Range

```bash
# Find regression introduced after a specific date
git bisect start HEAD "$(git rev-list -1 --before='2024-01-01' HEAD)"
```

### Bisect with Commit Range

```bash
# Bisect between two specific commits
git bisect start <bad-commit> <good-commit>
```

### Skip Multiple Commits

```bash
# Skip a range of commits (e.g., known refactoring)
git bisect skip v1.1..v1.2

# Skip commits matching a pattern
git bisect skip $(git rev-list --grep="refactor" HEAD~50..HEAD)
```

### Bisect with Terms

Use custom terms instead of "good" and "bad":

```bash
# Use "old" and "new" for non-bug scenarios
git bisect start --term-old=old --term-new=new
git bisect new HEAD
git bisect old v1.0

# Or use "fast" and "slow" for performance
git bisect start --term-old=fast --term-new=slow
```

## Bisect Log and Replay

### Save Bisect Session

```bash
# Save bisect log
git bisect log > bisect_session.txt

# Reset bisect
git bisect reset

# Replay bisect session later
git bisect replay bisect_session.txt
```

### Bisect Log Format

```
# bad: [abc123] Commit message
# good: [def456] Commit message
git bisect start 'abc123' 'def456'
git bisect good xyz789
git bisect bad uvw012
```

## Visualizing Bisect Progress

### View Bisect State

```bash
# Show current bisect state
git bisect visualize

# Or with gitk
git bisect visualize --oneline --graph

# Show remaining commits to test
git bisect visualize --oneline | wc -l
```

### Bisect Log Analysis

```bash
# View full bisect log
git bisect log

# Count steps taken
git bisect log | grep -c "^git bisect"

# See which commits were tested
git bisect log | grep "^# "
```

## Common Patterns

### Pattern 1: Test Failure Bisect

```bash
#!/bin/bash
# Find commit that broke a specific test

pytest tests/test_feature.py::test_specific_case
exit $?
```

### Pattern 2: Performance Regression Bisect

```bash
#!/bin/bash
# Find commit that caused performance regression

THRESHOLD=1000  # milliseconds
DURATION=$(./benchmark | grep "Duration:" | awk '{print $2}')

if [ $DURATION -lt $THRESHOLD ]; then
    exit 0  # Good performance
else
    exit 1  # Performance regression
fi
```

### Pattern 3: Output Change Bisect

```bash
#!/bin/bash
# Find commit that changed program output

EXPECTED="Expected output"
ACTUAL=$(./program 2>&1)

if [ "$ACTUAL" = "$EXPECTED" ]; then
    exit 0  # Good
else
    exit 1  # Bad
fi
```

### Pattern 4: Build Failure Bisect

```bash
#!/bin/bash
# Find commit that broke the build

if make clean && make all; then
    exit 0  # Build succeeds
else
    exit 1  # Build fails
fi
```

## Troubleshooting

### Problem: Bisect Identifies Wrong Commit

**Causes**:
- Flaky tests (non-deterministic behavior)
- Incorrect exit codes in test script
- External dependencies changed
- Test environment not isolated

**Solutions**:
```bash
# Add retry logic
for i in {1..3}; do
    if ./test.sh; then
        ((PASS++))
    fi
done
[ $PASS -eq 3 ] && exit 0 || exit 1

# Fix random seeds
export RANDOM_SEED=42
export TZ=UTC

# Clean state
rm -rf /tmp/cache
```

### Problem: Too Many Commits Skipped

**Causes**:
- Build system changed during history
- Dependencies not available in older commits
- Test infrastructure added later

**Solutions**:
```bash
# Be more lenient with skipping
if ! make build 2>/dev/null; then
    exit 125  # Skip instead of failing
fi

# Install missing dependencies
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt || exit 125
fi
```

### Problem: Bisect Takes Too Long

**Causes**:
- Slow test execution
- Large commit range
- Many commits to test

**Solutions**:
```bash
# Add timeout
timeout 10s ./test.sh || exit 125

# Optimize test
# - Run only relevant tests
# - Use parallel execution
# - Cache build artifacts

# Narrow the range
git bisect start HEAD v1.5  # Instead of v1.0
```

### Problem: Cannot Reproduce Issue

**Causes**:
- Environment differences
- Missing configuration
- External dependencies

**Solutions**:
```bash
# Document environment
echo "Testing environment:" > bisect_env.txt
env >> bisect_env.txt
git --version >> bisect_env.txt

# Use containers for consistency
docker run --rm -v $(pwd):/code test-image ./bisect_test.sh
```

## Best Practices

1. **Test the test script first**: Verify it works on known good and bad commits
   ```bash
   git checkout <good-commit>
   ./bisect_test.sh  # Should exit 0

   git checkout <bad-commit>
   ./bisect_test.sh  # Should exit 1
   ```

2. **Make tests deterministic**: Fix random seeds, timestamps, and external state

3. **Keep tests fast**: Bisect runs O(log n) tests, but slow tests still add up

4. **Use exit code 125 liberally**: Skip untestable commits rather than marking them bad

5. **Log everything**: Save detailed logs for each tested commit

6. **Clean state between tests**: Remove caches, temporary files, and build artifacts

7. **Handle timeouts**: Prevent hanging tests from blocking bisect

8. **Document the process**: Save bisect logs and test scripts for future reference

## Performance Optimization

### Parallel Bisect

For independent test suites, run multiple bisects in parallel:

```bash
# Terminal 1: Bisect unit tests
git bisect start HEAD v1.0
git bisect run pytest tests/unit/

# Terminal 2: Bisect integration tests
git bisect start HEAD v1.0
git bisect run pytest tests/integration/
```

### Incremental Builds

Cache build artifacts to speed up compilation:

```bash
#!/bin/bash
# Use ccache for C/C++ builds
export CCACHE_DIR=/tmp/bisect_ccache
make CC="ccache gcc"
```

### Shallow Bisect

For very large repositories, use shallow clones:

```bash
git clone --depth 100 <repo-url>
git bisect start HEAD HEAD~50
```

## References

- Git bisect documentation: https://git-scm.com/docs/git-bisect
- Pro Git book chapter: https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git
- Git bisect examples: https://github.com/git/git/tree/master/contrib/examples
