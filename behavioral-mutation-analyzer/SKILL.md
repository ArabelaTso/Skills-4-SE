---
name: behavioral-mutation-analyzer
description: Analyzes surviving mutants from mutation testing to identify why tests failed to detect them. Takes repository code, test suite, and mutation testing results as input. Identifies root causes including insufficient coverage, equivalent mutants, weak assertions, and missed edge cases. Automatically generates actionable test improvements and new test cases. Use when analyzing mutation testing results, improving test suite effectiveness, investigating low mutation scores, generating tests to kill surviving mutants, or enhancing test quality based on mutation analysis.
---

# Behavioral Mutation Analyzer

## Overview

This skill systematically analyzes surviving mutants from mutation testing to understand test suite weaknesses and automatically generate improvements. It identifies why mutants survived, categorizes root causes, and produces actionable test enhancements to increase mutation detection rates.

## Analysis Workflow

### Step 1: Input Collection and Validation

Gather required inputs and verify completeness:

**Required Inputs:**
- Repository source code (path or files)
- Test suite (test files and framework)
- Mutation testing results (report file or data)

**Mutation Result Formats:**
- PIT (Java): XML or HTML reports
- Stryker (JavaScript/TypeScript): JSON reports
- mutmut (Python): result files
- Pitest, Infection (PHP), Cosmic Ray, etc.

**Validation checklist:**
- [ ] Source code accessible
- [ ] Test suite runnable
- [ ] Mutation results parseable
- [ ] Mutation tool and version identified

### Step 2: Surviving Mutant Extraction

Parse mutation results to identify all surviving mutants:

**Extract for each mutant:**
- Mutant ID
- Source file and line number
- Mutation operator (e.g., boundary change, negation)
- Original code
- Mutated code
- Status (survived/killed/timeout/error)

**Focus on survived mutants:**
Filter out killed mutants and focus analysis on survivors that indicate test weaknesses.

### Step 3: Root Cause Classification

Analyze each surviving mutant to determine why it survived:

#### Category 1: Insufficient Coverage

**Indicators:**
- Mutated line not executed by any test
- Mutated method/function never called
- Conditional branch not taken

**Analysis:**
- Check code coverage data
- Identify uncovered code paths
- Trace execution from test entry points

**Example:**
```java
// Original
public int calculate(int x) {
    if (x > 0) {
        return x * 2;  // Line 3: Covered
    }
    return 0;  // Line 5: NOT covered
}

// Mutant: Line 5 changed to "return 1;"
// Survives because no test calls calculate() with x <= 0
```

#### Category 2: Equivalent Mutants

**Indicators:**
- Mutation produces semantically identical behavior
- Mathematical or logical equivalence
- Dead code or unreachable state

**Analysis:**
- Compare control flow graphs
- Check for mathematical identities
- Identify redundant operations

**Example:**
```python
# Original
result = x * 1

# Mutant: changed to "result = x"
# Equivalent: multiplying by 1 has no effect
```

#### Category 3: Weak Assertions

**Indicators:**
- Test executes mutated code but doesn't verify output
- Assertions too broad or generic
- Only checking for exceptions, not correctness

**Analysis:**
- Review test assertions
- Check what properties are verified
- Identify missing postconditions

**Example:**
```javascript
// Test
test('calculate returns a number', () => {
    const result = calculate(5);
    expect(typeof result).toBe('number');  // Weak: doesn't check value
});

// Mutant: "return x * 2" → "return x * 3"
// Survives because test only checks type, not value
```

#### Category 4: Missed Edge Cases

**Indicators:**
- Mutation affects boundary conditions
- Special values not tested (null, zero, empty, max/min)
- Error handling paths not verified

**Analysis:**
- Identify boundary values in mutated code
- Check test inputs for edge case coverage
- Review exception handling tests

**Example:**
```java
// Original
public int divide(int a, int b) {
    return a / b;
}

// Mutant: added "if (b == 0) return 0;"
// Survives because no test checks division by zero
```

#### Category 5: Timing and Concurrency Issues

**Indicators:**
- Mutant affects timing, delays, or synchronization
- Race conditions or thread safety
- Asynchronous behavior changes

**Analysis:**
- Check for concurrent code
- Identify timing-dependent logic
- Review async/await patterns

#### Category 6: State-Dependent Behavior

**Indicators:**
- Mutant affects state transitions
- Order-dependent operations
- Side effects not verified

**Analysis:**
- Trace state changes
- Check for stateful objects
- Verify side effect assertions

### Step 4: Test Generation Strategy

For each surviving mutant, determine the appropriate test enhancement:

**Strategy 1: Add Missing Test Cases**
- When: Insufficient coverage
- Action: Generate new test that executes mutated code
- Focus: Cover the uncovered path

**Strategy 2: Strengthen Assertions**
- When: Weak assertions
- Action: Add specific value checks
- Focus: Verify exact expected behavior

**Strategy 3: Add Edge Case Tests**
- When: Missed edge cases
- Action: Generate boundary value tests
- Focus: Test special inputs (null, zero, empty, max, min)

**Strategy 4: Mark as Equivalent**
- When: Equivalent mutant
- Action: Document equivalence reasoning
- Focus: No test needed, update mutation config to ignore

**Strategy 5: Add Integration Tests**
- When: State or timing issues
- Action: Create tests verifying end-to-end behavior
- Focus: Observable effects and state transitions

### Step 5: Automated Test Generation

Generate concrete test code to kill surviving mutants:

**Test Generation Process:**
1. Identify test framework (JUnit, pytest, Jest, etc.)
2. Analyze existing test patterns and style
3. Generate test following project conventions
4. Include descriptive test names
5. Add comments explaining what mutant is targeted

**Example Generated Test:**
```python
def test_calculate_with_negative_input():
    """
    Test to kill mutant #42: calculate() with x <= 0
    Mutant changed 'return 0' to 'return 1' on line 5
    """
    result = calculate(-5)
    assert result == 0, "calculate() should return 0 for negative input"

    result = calculate(0)
    assert result == 0, "calculate() should return 0 for zero input"
```

### Step 6: Report Generation

Create comprehensive analysis report using template in `assets/mutation_analysis_report.md`:

**Report Sections:**
1. Executive summary (mutation score, survival rate)
2. Surviving mutants by category
3. Root cause analysis for each mutant
4. Generated test enhancements
5. Equivalent mutant documentation
6. Recommendations for test suite improvement

## Mutation Operators Reference

Common mutation operators and their implications:

**Arithmetic Operators:**
- `+` ↔ `-`, `*` ↔ `/`, `%` ↔ `*`
- Tests should verify exact numeric results

**Relational Operators:**
- `>` ↔ `>=`, `<` ↔ `<=`, `==` ↔ `!=`
- Tests should cover boundary conditions

**Logical Operators:**
- `&&` ↔ `||`, `!` insertion/removal
- Tests should verify boolean logic

**Conditional Boundaries:**
- `<` ↔ `<=`, `>` ↔ `>=`
- Tests should include boundary values

**Return Values:**
- Return value changes, void method calls removed
- Tests should assert return values

**Statement Deletion:**
- Remove method calls, assignments
- Tests should verify side effects

For detailed mutation operator catalog, see `references/mutation_operators.md`.

## Tool Integration

### PIT (Java)

Parse PIT XML reports:
```bash
# Run PIT
mvn org.pitest:pitest-maven:mutationCoverage

# Report location
target/pit-reports/YYYYMMDDHHMI/mutations.xml
```

### Stryker (JavaScript/TypeScript)

Parse Stryker JSON reports:
```bash
# Run Stryker
npx stryker run

# Report location
reports/mutation/mutation.json
```

### mutmut (Python)

Parse mutmut results:
```bash
# Run mutmut
mutmut run

# Show results
mutmut results
mutmut show [mutant-id]
```

For tool-specific parsing guidance, see `references/tool_integration.md`.

## Practical Examples

**Example 1: Insufficient Coverage**

Surviving mutant:
```java
// Line 15: return defaultValue; → return null;
```

Analysis: No test calls this method with conditions triggering line 15.

Generated test:
```java
@Test
public void testGetValueWithMissingKey() {
    // Kills mutant on line 15
    String result = config.getValue("nonexistent");
    assertEquals("default", result);
}
```

**Example 2: Weak Assertion**

Surviving mutant:
```python
# Line 8: return items[:5] → return items[:4]
```

Analysis: Test only checks `len(result) > 0`, not exact length.

Enhanced test:
```python
def test_get_top_items_returns_five():
    # Kills mutant on line 8
    items = create_test_items(10)
    result = get_top_items(items)
    assert len(result) == 5, "Should return exactly 5 items"
```

**Example 3: Equivalent Mutant**

Surviving mutant:
```javascript
// Original: if (x > 0 && x < 100)
// Mutant: if (0 < x && 100 > x)
```

Analysis: Logically equivalent, no behavioral difference.

Action: Mark as equivalent in mutation config, no test needed.

## Best Practices

**Prioritize mutants:**
1. High-impact code (critical business logic)
2. Frequently executed paths
3. Security-sensitive operations
4. Public API methods

**Test quality over quantity:**
- Focus on meaningful assertions
- Avoid brittle tests
- Test behavior, not implementation

**Iterative improvement:**
- Start with easiest mutants to kill
- Gradually tackle complex cases
- Re-run mutation testing after improvements

**Document equivalent mutants:**
- Maintain list of known equivalent mutants
- Configure mutation tool to skip them
- Explain equivalence reasoning

## References

For detailed information on specific topics:
- **Mutation operators**: See `references/mutation_operators.md`
- **Tool integration**: See `references/tool_integration.md`
- **Test patterns**: See `references/test_patterns.md`

