# Migration Strategy Guide

This document outlines strategies for safely migrating codebases while maintaining test-verified behavior.

## Core Migration Principles

### 1. Tests Define Correctness

The test suite is the contract that defines correct behavior. A successful migration means:
- All tests that passed before still pass after
- No new test failures introduced
- Same test coverage maintained
- Behavior observable by tests is unchanged

### 2. Incremental Changes

Make small, verifiable changes:
- Update one dependency at a time when possible
- Fix one category of errors before moving to the next
- Commit working states frequently
- Run tests after each logical change

### 3. Fail Fast, Fix Fast

- Run tests immediately after migration attempt
- Analyze failures systematically
- Fix highest-impact issues first
- Verify fixes don't break other tests

## Migration Workflow

### Phase 1: Pre-Migration Assessment

**Establish baseline**:
```bash
# Run full test suite
<test_command>

# Record results
# - Total tests: X
# - Passing: Y
# - Failing: Z (if any)
# - Test coverage: N%
```

**Analyze dependencies**:
- List all direct dependencies
- Identify transitive dependencies
- Check for known breaking changes
- Review migration guides

**Identify risks**:
- Deprecated API usage
- Version-specific features
- Custom integrations
- Performance-critical code

### Phase 2: Migration Execution

**Update dependencies**:

Option A - Incremental (safer):
```bash
# Update one dependency
npm install package@new-version
# or
pip install package==new-version

# Run tests
<test_command>

# Fix issues, commit, repeat
```

Option B - Batch update:
```bash
# Update all dependencies
npm update
# or
pip install -U -r requirements.txt

# Run tests and fix all issues
```

**Handle breaking changes**:
1. Read error messages carefully
2. Consult migration guide
3. Search for similar issues
4. Apply fixes systematically

### Phase 3: Test-Driven Fixing

**Analyze test failures**:
```bash
# Run tests with verbose output
pytest -v
# or
npm test -- --verbose

# Categorize failures:
# - Import/module errors
# - API signature changes
# - Behavior changes
# - Type errors
# - Configuration issues
```

**Fix by category**:

1. **Import errors** (fix first - blocks other tests):
   ```python
   # Old
   from collections import Mapping

   # New
   from collections.abc import Mapping
   ```

2. **API signature changes**:
   ```python
   # Old
   result = function(arg1, arg2)

   # New (parameter renamed)
   result = function(arg1, new_param_name=arg2)
   ```

3. **Removed APIs**:
   ```python
   # Old
   deprecated_function()

   # New (find replacement)
   new_function()
   ```

4. **Behavior changes**:
   ```python
   # Old behavior: returns None on error
   # New behavior: raises exception

   # Add error handling
   try:
       result = function()
   except NewException:
       result = None
   ```

**Iterative fixing**:
```bash
# Fix one category
# Run tests
<test_command>

# If more failures, repeat
# If all pass, commit
git add .
git commit -m "Fix: migration issue category X"
```

### Phase 4: Verification

**Run full test suite multiple times**:
```bash
# Run 3-5 times to catch flaky tests
for i in {1..5}; do
  echo "Run $i"
  <test_command>
done
```

**Verify coverage unchanged**:
```bash
# Generate coverage report
<coverage_command>

# Compare to baseline
# Coverage should be same or better
```

**Check for warnings**:
```bash
# Run with warnings enabled
python -W all -m pytest
# or
node --trace-warnings test
```

**Integration testing**:
- Run integration tests if available
- Test critical user flows manually
- Check performance benchmarks

### Phase 5: Cleanup

**Remove deprecated code**:
- Remove compatibility shims if no longer needed
- Clean up workarounds for old version bugs
- Update comments referencing old versions

**Update documentation**:
- Update dependency versions in README
- Document breaking changes
- Update installation instructions
- Note any behavior changes

**Update CI/CD**:
- Update CI configuration
- Update Docker images
- Update deployment scripts

## Error Analysis Patterns

### Import/Module Errors

**Pattern**: `ModuleNotFoundError`, `ImportError`, `Cannot find module`

**Causes**:
- Package renamed
- Module moved to different location
- Package split into multiple packages
- Submodule removed

**Resolution**:
1. Check migration guide for new import path
2. Search package documentation
3. Use IDE auto-import suggestions
4. Check package changelog

**Example**:
```python
# Error: ImportError: cannot import name 'soft_unicode' from 'markupsafe'
# Fix: soft_unicode was removed, use soft_str instead
from markupsafe import soft_str
```

### API Signature Errors

**Pattern**: `TypeError: function() got unexpected keyword argument`, `TypeError: function() missing required argument`

**Causes**:
- Parameter renamed
- Parameter removed
- New required parameter added
- Parameter order changed

**Resolution**:
1. Read function documentation
2. Check migration guide
3. Update all call sites
4. Use IDE refactoring tools

**Example**:
```javascript
// Error: TypeError: render() got unexpected keyword argument 'container'
// Old: ReactDOM.render(<App />, container)
// New: ReactDOM.createRoot(container).render(<App />)
```

### Type Errors

**Pattern**: `TypeError: expected X, got Y`, type checker errors

**Causes**:
- Return type changed
- Parameter type changed
- Stricter type checking
- Generic type changes

**Resolution**:
1. Update type annotations
2. Add type conversions
3. Update interfaces
4. Fix type mismatches

**Example**:
```typescript
// Error: Type 'string | undefined' is not assignable to type 'string'
// Old: function process(value: string)
// New: function process(value: string | undefined)
```

### Behavior Changes

**Pattern**: Tests fail with unexpected values, assertions fail

**Causes**:
- Default values changed
- Algorithm changed
- Error handling changed
- Side effects changed

**Resolution**:
1. Read migration guide carefully
2. Understand new behavior
3. Update code to match new semantics
4. Update tests if behavior change is intentional

**Example**:
```python
# Old: dict.keys() returns list
# New: dict.keys() returns dict_keys view
# Fix: Convert to list if needed
keys = list(my_dict.keys())
```

### Configuration Errors

**Pattern**: `ConfigurationError`, warnings about deprecated config

**Causes**:
- Configuration format changed
- Settings renamed
- Default values changed
- New required settings

**Resolution**:
1. Update configuration files
2. Migrate settings to new format
3. Set explicit values for changed defaults
4. Remove deprecated settings

## Rollback Strategy

**When to rollback**:
- Too many test failures (>20% of tests)
- Critical functionality broken
- Performance severely degraded
- Deadline pressure

**How to rollback**:
```bash
# Revert dependency changes
git checkout HEAD -- package.json package-lock.json
npm install

# Or revert commits
git revert <commit-hash>

# Verify tests pass
<test_command>
```

**After rollback**:
- Document issues encountered
- Plan incremental migration
- Allocate more time
- Consider compatibility layers

## Success Criteria

Migration is complete when:
- [ ] All tests pass
- [ ] No new test failures
- [ ] Test coverage maintained or improved
- [ ] No critical warnings
- [ ] Build succeeds
- [ ] Integration tests pass
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Team reviewed changes

## Common Pitfalls

### Ignoring Warnings

Deprecation warnings indicate future breaking changes. Address them during migration.

### Batch Fixing Without Testing

Fix one issue, test, commit. Don't accumulate many fixes without verification.

### Assuming Backward Compatibility

Always check migration guides. Minor version updates can have breaking changes.

### Skipping Integration Tests

Unit tests may pass but integration may fail. Test the full system.

### Not Reading Error Messages

Error messages often contain the solution. Read them carefully.

### Changing Test Behavior

Never modify tests to make them pass. Fix the code, not the tests.

### Ignoring Performance

Migration may introduce performance regressions. Monitor and optimize.
