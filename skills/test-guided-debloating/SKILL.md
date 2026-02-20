---
name: test-guided-debloating
description: Removes unnecessary code from a repository while preserving exactly the behavior exercised by a given test suite. Use this skill when you need to debloat, slim down, or remove unused code from a codebase based on test coverage. The skill analyzes which code elements (files, classes, functions, methods, branches, imports) are exercised by tests, identifies unreachable or unused code, and safely removes it while ensuring all tests continue to pass. Triggers when users ask to remove unused code, debloat based on tests, eliminate dead code guided by test coverage, or slim down a repository to only test-required functionality.
---

# Test-Guided Debloating

Remove unnecessary code from a repository while preserving exactly the behavior exercised by a given test suite.

## Workflow

### 1. Understand Requirements

**Inputs needed**:
- Target repository path
- Test command to run the test suite
- Programming language/framework

**Clarify scope**:
- Which tests define required behavior (all tests, specific test files, integration tests only)?
- Should test files themselves be preserved (yes, never modify tests)?
- Are there any files that must be kept regardless of coverage (configuration, documentation)?

### 2. Run Coverage Analysis

Generate test coverage data to identify exercised code. See [coverage_tools.md](references/coverage_tools.md) for language-specific commands.

**Python example**:
```bash
pytest --cov=. --cov-report=json --cov-report=html
```

**JavaScript example**:
```bash
npm test -- --coverage --coverageReporters=json --coverageReporters=html
```

**Java example**:
```bash
mvn clean test jacoco:report
```

**Verify**:
- Coverage report generated successfully
- All tests pass
- Coverage data includes all source files

### 3. Analyze Coverage Data

Use `scripts/analyze_coverage.py` to identify removal candidates:

```bash
python scripts/analyze_coverage.py coverage.json --output analysis.json
```

The script identifies:
- **Uncovered files** (0% coverage) - safest to remove
- **Partially covered files** - require manual review
- **Uncovered lines** - potential dead code within files

**Manual review checklist**:
- Are uncovered files truly unused (check imports)?
- Do uncovered functions have side effects?
- Are there dynamic imports or reflection?
- Is this a library with public API requirements?

### 4. Incremental Removal

Remove code incrementally, validating after each step. See [debloating_strategy.md](references/debloating_strategy.md) for detailed strategy.

**Removal order** (safest to riskiest):

1. **Unused imports**
   ```python
   # Remove unused import statements
   # Run tests after removal
   ```

2. **Uncovered files** (0% coverage, not imported)
   ```bash
   # Remove file
   rm path/to/unused_file.py
   # Run tests
   pytest
   ```

3. **Uncovered functions/methods**
   ```python
   # Remove function definition
   # Run tests
   ```

4. **Dead branches**
   ```python
   # Before: if condition that's always true
   if always_true_condition:
       do_something()
   else:
       never_executed()  # Remove this branch

   # After:
   do_something()
   ```

5. **Unused classes**
   ```python
   # Remove class definition if never instantiated
   # Run tests
   ```

**After each removal**:
```bash
# Run full test suite
<test_command>

# Verify all tests pass
# Check for import errors
# Verify build succeeds
```

### 5. Validate Preservation of Behavior

**Final validation**:
- [ ] All tests pass
- [ ] Build succeeds without errors
- [ ] No import/module errors
- [ ] No runtime errors during test execution
- [ ] Test coverage of remaining code unchanged
- [ ] No modifications to test files

**Run tests multiple times** to catch flaky tests or timing issues.

### 6. Document Changes

Generate removal report:

```
DEBLOATING SUMMARY
==================

Removed Elements:
- 15 unused files
- 42 unused functions
- 8 unused classes
- 156 unused imports
- 23 dead branches

Total lines removed: 3,847
Tests passing: 156/156

Preservation Justification:
All test-defined behavior is preserved because:
1. All test-covered code remains intact
2. All transitive dependencies of test-covered code remain
3. No side effects required by tests were removed
4. Build succeeds and all 156 tests pass
```

## Key Principles

**Test-Defined Behavior**: The test suite is the single source of truth for required functionality.

**Conservative Removal**: When in doubt, keep the code. Only remove code you're confident is unused.

**Incremental Validation**: Remove code in small batches and run tests after each change.

**Never Modify Tests**: Test files define the required behavior and must not be changed.

**Preserve Side Effects**: Be cautious with code that has side effects (logging, initialization, registration).

## Common Pitfalls

**Avoid removing**:
- Code with side effects (module-level initialization, decorators, metaclasses)
- Code used via reflection or dynamic imports
- Public API methods (if building a library)
- Configuration files
- Error handling needed in production (even if untested)

**Watch for**:
- Dynamic behavior (eval, exec, importlib, reflection)
- Transitive dependencies (code called by covered code)
- Module-level code execution
- Static initializers
- Decorator/annotation side effects

## Helper Script

The `analyze_coverage.py` script automates coverage analysis:

```bash
# Analyze Python coverage
python scripts/analyze_coverage.py coverage.json

# Analyze JavaScript coverage
python scripts/analyze_coverage.py coverage-final.json --format javascript

# Save detailed analysis
python scripts/analyze_coverage.py coverage.json --output analysis.json
```

Output includes:
- List of uncovered files (safe to remove)
- Partially covered files (review needed)
- Uncovered line ranges
- Safety ratings for removal candidates
