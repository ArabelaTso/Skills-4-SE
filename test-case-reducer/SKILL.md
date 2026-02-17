---
name: test-case-reducer
description: Automatically reduces bug-triggering test cases to minimal form while preserving the failure. Use when debugging with large, complex test cases that need simplification, reproducing bugs with minimal examples, or creating regression tests from verbose failure scenarios. Takes a failing test and systematically removes unnecessary inputs, steps, assertions, and code using delta debugging and other reduction algorithms. Supports unit tests, integration tests, input files, and multiple programming languages (Python, JavaScript, Java, C/C++).
---

# Test Case Reducer

Automatically reduce bug-triggering test cases to minimal form while guaranteeing the reduced test still reproduces the same failure.

## Core Concept

Test case reduction works by:
1. **Identify**: Parse the test case and identify reducible elements
2. **Remove**: Systematically try removing elements (lines, statements, inputs)
3. **Validate**: Run the test after each removal to verify failure is preserved
4. **Iterate**: Continue until no further reduction is possible

## Workflow

### 1. Prepare the Test Case

Ensure you have:
- A test case that consistently reproduces the failure
- A way to run the test (command, script, test framework)
- A clear failure condition (oracle)

### 2. Define the Oracle

The oracle determines if the test still exhibits the expected failure:

**Exit code:**
- Test fails with specific exit code (e.g., non-zero)
- Example: `--oracle exit_code --expected 1`

**Exception type:**
- Test raises specific exception
- Example: `--oracle exception --expected ValueError`

**Output pattern:**
- Test output contains specific text
- Example: `--oracle output_pattern --expected "division by zero"`

**Assertion:**
- Test fails on specific assertion
- Example: `--oracle assertion --expected AssertionError`

### 3. Choose Reduction Strategy

**Aggressive** (fastest, smallest result):
- Binary search reduction first
- Delta debugging second
- Greedy line-by-line cleanup
- Use when: Test execution is fast, minimal size is critical

**Balanced** (recommended):
- Delta debugging only
- Good balance of speed and quality
- Use when: Standard reduction needs

**Conservative** (safest, most readable):
- Greedy line-by-line only
- Preserves more context
- Use when: Readability matters, test is already small

### 4. Run the Reduction

Using the provided script:

```bash
python scripts/reduce_test.py test_file.py \
  --command "python test_file.py" \
  --oracle exit_code \
  --expected 1 \
  --strategy balanced
```

Or manually apply reduction algorithms (see [references/algorithms.md](references/algorithms.md)).

### 5. Review the Result

Examine the reduced test case:
- Verify it still reproduces the failure
- Check that it's understandable
- Ensure no critical context was lost

## Quick Start Examples

### Example 1: Python Unit Test

**Original test (15 lines):**
```python
import unittest
from mymodule import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.test_data = [1, 2, 3, 4, 5]

    def test_divide(self):
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5)

        result = self.calc.divide(10, 0)  # This fails
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
```

**Reduction command:**
```bash
python scripts/reduce_test.py test_calc.py \
  --command "python test_calc.py" \
  --oracle exception \
  --expected "ZeroDivisionError"
```

**Reduced test (3 lines):**
```python
from mymodule import Calculator
Calculator().divide(10, 0)
```

### Example 2: JavaScript Integration Test

**Original test (20 lines):**
```javascript
const request = require('supertest');
const app = require('../app');

describe('API Tests', () => {
    beforeEach(() => {
        // Setup database
        db.reset();
        db.seed();
    });

    it('should handle invalid user ID', async () => {
        const response = await request(app)
            .get('/api/users/invalid')
            .set('Authorization', 'Bearer token')
            .expect(400);

        expect(response.body.error).toBe('Invalid user ID');
    });
});
```

**Reduced test (4 lines):**
```javascript
const request = require('supertest');
const app = require('../app');

request(app).get('/api/users/invalid').expect(400);
```

### Example 3: Input File Reduction

**Original input (100 lines of JSON):**
```json
{
  "users": [...100 user objects...],
  "settings": {...many settings...},
  "data": [...large data array...]
}
```

**Reduced input (5 lines):**
```json
{
  "users": [{"id": 42, "name": "Bob"}]
}
```

## Using the Reduction Script

### Basic Usage

```bash
python scripts/reduce_test.py <test_file> \
  --command "<command to run test>" \
  --oracle <oracle_type> \
  --expected <expected_value>
```

### Parameters

**Required:**
- `test_file`: Path to the test file to reduce
- `--command`: Command to execute the test (e.g., `python test.py`, `npm test`)
- `--oracle`: Type of failure oracle (exit_code, exception, output_pattern, assertion)
- `--expected`: Expected value for the oracle

**Optional:**
- `--strategy`: Reduction strategy (aggressive, balanced, conservative)
- `--timeout`: Timeout in seconds for test execution

### Examples

**Python test with exception:**
```bash
python scripts/reduce_test.py test.py \
  --command "python test.py" \
  --oracle exception \
  --expected "ValueError"
```

**JavaScript test with exit code:**
```bash
python scripts/reduce_test.py test.js \
  --command "node test.js" \
  --oracle exit_code \
  --expected 1 \
  --strategy aggressive
```

**Java test with timeout:**
```bash
python scripts/reduce_test.py Test.java \
  --command "javac Test.java && java Test" \
  --oracle output_pattern \
  --expected "NullPointerException" \
  --timeout 10
```

## Manual Reduction Workflow

When not using the script, follow this process:

### 1. Verify Original Failure

```bash
# Run original test
python test.py
# Verify it fails as expected
```

### 2. Try Removing Large Chunks

Remove half the test:
```python
# Original
line1
line2
line3
line4

# Try first half
line1
line2

# Or second half
line3
line4
```

### 3. Apply Delta Debugging

See [references/algorithms.md](references/algorithms.md) for detailed algorithm.

### 4. Clean Up Line by Line

Remove one line at a time, testing after each removal.

### 5. Verify Final Result

Ensure reduced test still fails with same error.

## Language-Specific Guidance

For detailed language-specific reduction techniques, see [references/language-specific.md](references/language-specific.md).

**Python:**
- Remove unused imports
- Simplify test setup
- Reduce assertions to minimum

**JavaScript:**
- Remove describe blocks if possible
- Simplify mock setup
- Reduce to single assertion

**Java:**
- Remove @Before/@After if not needed
- Simplify test class structure
- Reduce verbose assertions

**C/C++:**
- Remove unnecessary includes
- Simplify test fixtures
- Reduce to single EXPECT/ASSERT

## Common Scenarios

### Scenario 1: Large Integration Test

**Problem:** Integration test with 200 lines fails intermittently

**Solution:**
1. Run test multiple times to ensure consistent failure
2. Use aggressive strategy for fast reduction
3. Reduce to minimal API calls that trigger failure

### Scenario 2: Complex Input File

**Problem:** 10MB JSON file causes parser to crash

**Solution:**
1. Use binary search to find problematic section
2. Apply delta debugging to reduce section
3. Result: Small JSON snippet that triggers crash

### Scenario 3: Verbose Unit Test

**Problem:** Unit test with extensive setup fails on one assertion

**Solution:**
1. Use conservative strategy to preserve readability
2. Remove setup code not needed for failure
3. Keep minimal context for understanding

## Best Practices

### Before Reduction

- **Verify determinism:** Ensure test fails consistently
- **Backup original:** Keep copy of original test
- **Document failure:** Note exact error message and conditions

### During Reduction

- **Start aggressive:** Use aggressive strategy first, then refine
- **Validate frequently:** Check each reduction preserves failure
- **Watch for side effects:** Be careful with tests that modify state
- **Set timeouts:** Prevent hanging on infinite loops

### After Reduction

- **Verify manually:** Run reduced test several times
- **Check readability:** Ensure reduced test is understandable
- **Add comments:** Document what the test is checking
- **Create regression test:** Use reduced test as regression test

## Troubleshooting

**Reduction removes too much:**
- Use conservative strategy
- Preserve specific elements manually
- Check oracle is correct

**Test becomes non-deterministic:**
- Original test may have race condition
- Run multiple times to verify
- Consider recording non-deterministic inputs

**Reduction is too slow:**
- Use aggressive strategy
- Increase timeout
- Simplify test command

**Syntax errors after reduction:**
- Use language-aware reduction
- Preserve structural elements
- Validate syntax after each step

## References

- **[algorithms.md](references/algorithms.md)**: Detailed explanation of delta debugging, binary search, and other reduction algorithms
- **[language-specific.md](references/language-specific.md)**: Language-specific reduction techniques for Python, JavaScript, Java, C/C++

## Tips

- **Start with script:** Use provided script for automatic reduction
- **Iterate strategies:** Try different strategies if first doesn't work well
- **Preserve context:** Don't over-reduce; keep enough context to understand
- **Test determinism:** Ensure failure is reproducible before reducing
- **Use version control:** Commit before reduction to easily revert
- **Document oracle:** Clearly specify what constitutes failure
