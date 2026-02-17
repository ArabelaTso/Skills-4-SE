---
name: test-guided-migration-assistant
description: Automatically updates a codebase to a new language version, framework version, or library update while ensuring all tests still pass. Use this skill when migrating Python 2→3, upgrading framework versions (React, Django, Angular), updating dependencies, or performing any version migration where tests define correct behavior. The skill analyzes failing tests caused by migration, categorizes errors (import errors, API changes, type errors, behavior changes), proposes systematic fixes, and verifies that test-observable behavior remains unchanged. Triggers when users ask to migrate code versions, upgrade dependencies while keeping tests passing, update framework versions, or perform test-guided version migrations.
---

# Test-Guided Migration Assistant

Automatically update a codebase to a new language version, framework version, or library update while ensuring all tests continue to pass.

## Workflow

### 1. Establish Baseline

Before starting migration, establish the current state:

```bash
# Run full test suite
<test_command>

# Record baseline
# - Total tests: X
# - Passing: Y
# - Failing: Z (should be 0 or known failures)
# - Coverage: N%
```

**Document current state**:
- Current versions (language, framework, dependencies)
- Test results
- Any known issues

### 2. Understand Migration Context

**Gather information**:
- Target version (e.g., Python 3.12, React 18, Django 4.2)
- Migration scope (single library vs. full stack)
- Breaking changes expected

**Consult migration guides**:
- Official migration documentation
- Changelog/release notes
- Community migration guides
- See [migration_scenarios.md](references/migration_scenarios.md) for common patterns

**Identify risks**:
- Deprecated API usage
- Known breaking changes
- Custom integrations affected
- Performance implications

### 3. Perform Migration

**Update dependencies**:

Incremental approach (recommended):
```bash
# Update one dependency at a time
npm install package@new-version
# or
pip install package==new-version

# Run tests immediately
<test_command>
```

Batch approach (for experienced migrations):
```bash
# Update all dependencies
npm update
# or
pip install -U -r requirements.txt

# Run tests
<test_command>
```

**Update configuration**:
- Update build configuration
- Update CI/CD configuration
- Update environment files
- Update Docker images

### 4. Analyze Test Failures

Run tests and capture output:

```bash
# Pytest
pytest -v > test_output.txt 2>&1

# Jest
npm test > test_output.txt 2>&1

# Other frameworks
<test_command> > test_output.txt 2>&1
```

**Use analysis script**:
```bash
python scripts/analyze_test_failures.py test_output.txt
```

The script categorizes failures into:
- 🔴 **Import/Module Errors** (CRITICAL - fix first)
- 🟠 **API Signature Errors** (HIGH priority)
- 🟡 **Type Errors** (MEDIUM priority)
- 🟡 **Configuration Errors** (MEDIUM priority)
- 🟢 **Behavior Changes** (review carefully)
- 🔵 **Deprecation Warnings** (fix when possible)

### 5. Fix Issues Systematically

Follow priority order from analysis. See [migration_strategy.md](references/migration_strategy.md) for detailed strategies.

**Fix import errors first**:
```python
# Example: Module moved
# Old
from collections import Mapping

# New
from collections.abc import Mapping
```

**Fix API signature errors**:
```python
# Example: Parameter renamed
# Old
result = function(arg1, old_param=value)

# New
result = function(arg1, new_param=value)
```

**Fix type errors**:
```typescript
// Example: Stricter types
// Old
function process(value: string) { }

// New (handle undefined)
function process(value: string | undefined) {
  if (value === undefined) return;
  // ...
}
```

**Handle behavior changes**:
```python
# Example: Changed defaults
# Old behavior: returns None on error
# New behavior: raises exception

# Add error handling
try:
    result = function()
except NewException:
    result = None  # Preserve old behavior
```

**After each fix category**:
```bash
# Run tests
<test_command>

# Commit if tests pass
git add .
git commit -m "Fix: migration import errors"
```

### 6. Verify Behavior Preservation

**Run full test suite multiple times**:
```bash
# Catch flaky tests
for i in {1..3}; do
  echo "Run $i"
  <test_command>
done
```

**Verify coverage unchanged**:
```bash
# Generate coverage report
<coverage_command>

# Compare to baseline
# Should be same or better
```

**Check for warnings**:
```bash
# Python
python -W all -m pytest

# Node.js
node --trace-warnings test

# Look for deprecation warnings
```

**Success criteria**:
- [ ] All tests pass
- [ ] Same number of passing tests as baseline
- [ ] No new test failures
- [ ] Coverage maintained or improved
- [ ] Build succeeds
- [ ] No critical warnings

### 7. Document Migration

**Create migration summary**:
```
MIGRATION SUMMARY
=================

Migration: Python 3.8 → Python 3.12

Changes Made:
- Updated collections imports (Mapping → collections.abc.Mapping)
- Fixed asyncio.coroutine → async def
- Updated type hints for stricter checking
- Removed distutils usage

Test Results:
- Before: 156/156 passing
- After: 156/156 passing
- Coverage: 87% (unchanged)

Breaking Changes Addressed:
1. Collections ABC moved
2. asyncio.coroutine removed
3. Type checking stricter

Deprecation Warnings:
- None remaining
```

## Key Principles

**Tests Define Correctness**: If tests pass, behavior is preserved.

**Fix by Priority**: Import errors block everything - fix first. Then API errors, then types, then behavior.

**Incremental Changes**: Fix one category, test, commit. Don't accumulate many changes.

**Never Modify Tests**: Fix the code to make tests pass. Don't change tests to match new behavior (unless behavior change is intentional and documented).

**Fail Fast**: Run tests immediately after migration attempt. Don't wait.

## Common Migration Patterns

### Python 2 → 3
- `print` statement → `print()` function
- `xrange()` → `range()`
- `.iteritems()` → `.items()`
- `except Exception, e:` → `except Exception as e:`

### React 16 → 18
- `ReactDOM.render()` → `ReactDOM.createRoot().render()`
- Update for concurrent rendering
- Fix useEffect timing issues

### Django 2.2 → 4.2
- `django.conf.urls.url()` → `django.urls.re_path()`
- Update `ugettext` → `gettext`
- Remove `USE_L10N` setting

### Node.js 14 → 20
- Update deprecated APIs
- Fix OpenSSL changes
- Update crypto usage

## Helper Script

The `analyze_test_failures.py` script automates failure categorization:

```bash
# Analyze pytest output
python scripts/analyze_test_failures.py test_output.txt

# Analyze Jest output
python scripts/analyze_test_failures.py test_output.txt --format jest

# Auto-detect format
python scripts/analyze_test_failures.py test_output.txt --format auto
```

Output provides:
- Categorized failure list
- Priority order for fixes
- Example errors from each category
- Recommended fix strategies

## Rollback Strategy

If migration has too many failures (>20% of tests):

```bash
# Revert dependency changes
git checkout HEAD -- package.json package-lock.json
npm install

# Or revert commits
git revert <commit-hash>

# Verify tests pass
<test_command>
```

Then plan incremental migration or allocate more time.
