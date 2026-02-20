---
name: code-repair-generation-combo
description: Automatically repair buggy code and generate comprehensive tests for Python, Java, and C++ programs. Use when users need to fix logic errors or runtime errors in functions, modules, or repositories. Accepts specifications via natural language descriptions, existing test cases, or input/output examples. Generates corrected code, creates or updates tests to verify correctness and prevent regressions, and produces a detailed report explaining the bug, fix, and testing strategy. Triggers on requests like "fix this bug", "repair this code", "debug this function", or "this code is broken".
---

# Code Repair + Generation Combo

Automatically diagnose and repair buggy code while generating comprehensive tests to verify correctness and prevent regressions.

## Workflow

Follow this systematic approach for bug fixing and test generation:

### 1. Understand the Bug

**Read the buggy code** - Use Read tool to examine the problematic code thoroughly.

**Analyze the specification** - Understand expected behavior from:
- Natural language description from user
- Existing failing test cases
- Input/output examples provided
- Error messages or stack traces

**Identify the scope** - Determine if the bug affects:
- A single function
- Multiple related functions
- An entire module
- Cross-module interactions

### 2. Diagnose the Root Cause

**Trace the logic** - Walk through the code execution mentally or with examples.

**Identify the bug type**:
- **Logic error**: Code runs but produces wrong results (off-by-one, wrong operator, incorrect condition)
- **Runtime error**: Code crashes or throws exceptions (null pointer, array out of bounds, type mismatch)

**Pinpoint the exact location** - Identify the specific lines causing the issue.

**Understand side effects** - Check if the bug affects other parts of the codebase.

### 3. Fix the Code

**Apply minimal changes** - Fix only what's broken, preserve existing functionality.

**Use Edit tool** - Make precise changes to the buggy code.

**Verify the fix logic** - Ensure the fix addresses the root cause, not just symptoms.

**Preserve code style** - Match existing formatting, naming conventions, and patterns.

### 4. Generate Comprehensive Tests

**Load testing patterns** - Read the appropriate reference file:
- Python: `references/python-testing.md`
- Java: `references/java-testing.md`
- C++: `references/cpp-testing.md`

**Create test cases covering**:
- **Normal cases**: Typical valid inputs
- **Edge cases**: Boundary values, empty inputs, single elements
- **Error cases**: Invalid inputs, null values, exceptions
- **Regression cases**: Specific inputs that triggered the original bug

**Update existing tests** if they exist, or create new test files following language conventions.

**Use parametrized tests** when testing multiple similar cases.

### 5. Verify and Run Tests

**Execute the tests** - Use Bash tool to run the test suite:
- Python: `pytest test_file.py -v`
- Java: `mvn test` or `gradle test`
- C++: `./test_executable` or `ctest`

**Ensure all tests pass** - If tests fail, revisit the fix.

**Check coverage** - Verify that the fix and related code paths are tested.

### 6. Generate Bug Fix Report

**Use the report template** - Read `assets/bug-fix-report-template.md` and populate it with:
- Summary of the bug and fix
- Root cause analysis
- Changes made with file paths and line numbers
- Test coverage details
- Verification of regression safety

**Be specific and clear** - Include code snippets, test results, and reasoning.

## Example Usage

**Example 1: Python logic error**
```
User: "This factorial function returns 24 instead of 120 for input 5. Fix it."

1. Read the buggy code
2. Identify: off-by-one error in loop range
3. Fix: Change `range(1, n)` to `range(1, n+1)`
4. Generate tests covering 0, 1, 5, negative numbers
5. Run pytest and verify all pass
6. Generate report
```

**Example 2: Java runtime error**
```
User: "My sorting method throws NullPointerException with null elements."

1. Read the code and identify null comparison issue
2. Fix: Add null checks before comparisons
3. Generate JUnit tests for arrays with nulls, empty arrays, normal cases
4. Run tests and verify
5. Generate report
```

**Example 3: C++ logic error with examples**
```
User: "Binary search returns -1 for existing elements. For [1,3,5,7,9] and target 5, should return 2."

1. Read code and trace with provided example
2. Identify: incorrect mid calculation or boundary condition
3. Fix the bug
4. Generate Google Test cases with provided example and additional edge cases
5. Compile and run tests
6. Generate report
```

## Language-Specific Notes

**Python**:
- Use pytest framework
- Follow PEP 8 style
- Use type hints if present in original code

**Java**:
- Use JUnit 5 framework
- Follow Java naming conventions
- Handle null safety explicitly

**C++**:
- Use Google Test or Catch2
- Check for memory leaks with valgrind if applicable
- Handle pointer safety and bounds checking

## Resources

**references/** - Testing patterns and best practices for each language
**assets/** - Bug fix report template for consistent documentation
