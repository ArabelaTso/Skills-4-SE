# Test-Guided Debloating Strategy

This document outlines the strategy and methodology for safely removing unnecessary code while preserving test-defined behavior.

## Core Principles

1. **Test-Defined Behavior**: The provided test suite is the single source of truth for required functionality
2. **Conservative Removal**: When in doubt, keep the code
3. **Incremental Validation**: Remove code incrementally and verify tests pass after each change
4. **No Test Modification**: Never modify the test code itself

## Analysis Phases

### Phase 1: Test Coverage Analysis

**Objective**: Identify all code elements exercised by the test suite

**Steps**:
1. Run tests with coverage instrumentation (pytest-cov, Istanbul/nyc, JaCoCo, etc.)
2. Generate detailed coverage reports showing:
   - Files covered
   - Functions/methods executed
   - Lines executed
   - Branches taken
3. Identify uncovered code elements:
   - Unused files
   - Unused classes
   - Unused functions/methods
   - Unused branches
   - Unused imports

**Tools by Language**:
- **Python**: `pytest --cov=. --cov-report=html --cov-report=json`
- **JavaScript/TypeScript**: `nyc --reporter=html --reporter=json npm test`
- **Java**: JaCoCo Maven/Gradle plugin
- **Go**: `go test -coverprofile=coverage.out`
- **Ruby**: SimpleCov
- **C/C++**: gcov/lcov

### Phase 2: Dependency Analysis

**Objective**: Understand dependencies between code elements

**Steps**:
1. Build call graph showing function/method invocations
2. Build import/dependency graph
3. Identify transitive dependencies from test-covered code
4. Mark code as "required" if:
   - Directly executed by tests
   - Called by test-executed code
   - Imported by required code
   - Contains side effects needed by tests

**Consider**:
- Static method calls
- Dynamic dispatch (polymorphism)
- Reflection/metaprogramming
- Configuration files
- Data files
- Environment variables

### Phase 3: Safe Removal Identification

**Objective**: Categorize code for removal

**Categories**:

1. **Safe to Remove**:
   - Unused files not imported anywhere
   - Unused functions never called
   - Unused classes never instantiated
   - Dead branches never taken
   - Unused imports
   - Commented-out code
   - Unreachable code after return/break

2. **Potentially Safe to Remove** (requires careful analysis):
   - Code with side effects (logging, metrics)
   - Code in __init__ files
   - Module-level code
   - Static initializers
   - Decorators/annotations
   - Abstract base classes

3. **Keep** (even if uncovered):
   - Code with external side effects tests don't verify
   - Public API methods (if library)
   - Error handling for untested error paths (if required for production)
   - Configuration/setup code

## Removal Strategy

### Incremental Removal Process

1. **Start with safest removals**:
   - Unused imports
   - Commented code
   - Unreachable code

2. **Remove unused files**:
   - Files with zero coverage
   - Not imported anywhere
   - Run tests after each file removal

3. **Remove unused functions/methods**:
   - Functions never called
   - Private methods with zero coverage
   - Run tests after each removal or batch

4. **Remove unused classes**:
   - Classes never instantiated
   - No subclasses
   - Run tests after removal

5. **Simplify control flow**:
   - Remove dead branches
   - Simplify always-true/false conditions
   - Remove unreachable exception handlers

6. **Clean up dependencies**:
   - Remove unused imports
   - Remove unused dependencies from package files

### Validation After Each Step

```bash
# Run full test suite
<test_command>

# Verify all tests pass
# Verify build succeeds
# Check for import errors
```

## Language-Specific Considerations

### Python

- Check for `__init__.py` side effects
- Consider dynamic imports (`importlib`)
- Check for metaclasses and decorators
- Look for `__getattr__` and `__getattribute__`
- Consider module-level code execution

### JavaScript/TypeScript

- Check for side effects in module imports
- Consider dynamic requires
- Look for prototype modifications
- Check for global variable assignments
- Consider webpack/bundler tree-shaking

### Java

- Check for static initializers
- Consider reflection usage
- Look for annotation processors
- Check for service loaders
- Consider Spring/dependency injection

### Go

- Check for init() functions
- Consider build tags
- Look for interface implementations
- Check for blank imports (side effects)

## Output Format

### Removal Report

For each removed element, document:

```
Type: [File|Class|Function|Method|Branch|Import]
Location: path/to/file.py:line_number
Name: element_name
Reason: Not covered by tests, no transitive dependencies
Impact: None - never executed
```

### Preservation Justification

Explain why test behavior is preserved:

```
All test-defined behavior is preserved because:
1. All test-covered code remains intact
2. All transitive dependencies of test-covered code remain
3. No side effects required by tests were removed
4. Build succeeds and all N tests pass
```

## Safety Checks

Before finalizing debloating:

- [ ] All tests pass
- [ ] Build succeeds without errors
- [ ] No import/module errors
- [ ] No runtime errors during test execution
- [ ] Coverage report shows same covered lines still covered
- [ ] No changes to test files
- [ ] Documentation updated if needed

## Common Pitfalls

1. **Removing code with side effects**: Logging, metrics, initialization
2. **Ignoring dynamic behavior**: Reflection, eval, dynamic imports
3. **Missing transitive dependencies**: Code called by covered code
4. **Removing error handling**: May be needed in production
5. **Breaking public APIs**: If code is a library
6. **Removing configuration**: Environment setup, constants
