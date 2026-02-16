# Static Bug Detection Patterns

This reference catalogs common bug patterns detectable through static analysis, with detection techniques and confidence assessment.

## Table of Contents

1. [Null Dereference Bugs](#null-dereference-bugs)
2. [Incorrect Condition Checks](#incorrect-condition-checks)
3. [Unreachable Code](#unreachable-code)
4. [Inconsistent State Updates](#inconsistent-state-updates)
5. [Logic Errors](#logic-errors)
6. [Resource Management Issues](#resource-management-issues)
7. [Type-Related Bugs](#type-related-bugs)
8. [Confidence Assessment](#confidence-assessment)

## Null Dereference Bugs

### Pattern 1: Dereferencing Without Null Check

**Detection:**
- Variable assigned from nullable source
- Used without null check
- No guarantee of non-null value

**Example (Java):**
```java
User user = userRepository.findById(id);  // May return null
String name = user.getName();  // BUG: Potential null dereference
```

**Report:**
```
Bug: Potential null dereference
Location: line 2
Severity: High
Confidence: High

Explanation: Variable 'user' may be null (returned from findById) but is
dereferenced without null check on line 2.

Recommendation: Add null check before dereferencing:
if (user != null) {
    String name = user.getName();
}
```

### Pattern 2: Null Return Without Documentation

**Detection:**
- Method returns null
- No @Nullable annotation or documentation
- Callers may not expect null

**Example (Python):**
```python
def find_user(user_id):
    if user_id in users:
        return users[user_id]
    return None  # BUG: Undocumented null return

# Caller doesn't check for None
user = find_user(123)
print(user.name)  # Potential AttributeError
```

**Report:**
```
Bug: Undocumented null/None return
Location: line 4
Severity: Medium
Confidence: Medium

Explanation: Method returns None but lacks documentation. Callers may not
expect None and could encounter AttributeError.

Recommendation: Document None return or use Optional type.
```

### Pattern 3: Null Check After Use

**Detection:**
- Variable used before null check
- Check comes too late

**Example (JavaScript):**
```javascript
function processUser(user) {
    console.log(user.name);  // BUG: Used before check
    if (user === null) {
        return;
    }
    // ...
}
```

**Report:**
```
Bug: Null check after dereference
Location: line 2
Severity: High
Confidence: High

Explanation: Variable 'user' is dereferenced on line 2 but null check
occurs on line 3. If user is null, TypeError occurs before check.

Recommendation: Move null check before first use.
```

## Incorrect Condition Checks

### Pattern 1: Always True/False Condition

**Detection:**
- Condition that's always true or false
- Dead branch or redundant check

**Example (Python):**
```python
x = 10
if x > 5:
    print("Greater")
if x < 5:  # BUG: Always false
    print("Less")
```

**Report:**
```
Bug: Always-false condition
Location: line 4
Severity: Low
Confidence: High

Explanation: Variable 'x' is assigned 10 on line 1. Condition 'x < 5'
on line 4 is always false, making the branch unreachable.

Recommendation: Remove dead code or fix condition logic.
```

### Pattern 2: Incorrect Comparison Operator

**Detection:**
- Suspicious comparison (e.g., = instead of ==)
- Likely typo or logic error

**Example (C):**
```c
if (status = SUCCESS) {  // BUG: Assignment instead of comparison
    printf("Success\n");
}
```

**Report:**
```
Bug: Assignment in condition
Location: line 1
Severity: High
Confidence: High

Explanation: Using '=' (assignment) instead of '==' (comparison).
This assigns SUCCESS to status and evaluates to true if non-zero.

Recommendation: Change to 'status == SUCCESS' for comparison.
```

### Pattern 3: Redundant Condition

**Detection:**
- Condition already checked
- Duplicate or subsumed check

**Example (Java):**
```java
if (x > 0 && x > 5) {  // BUG: x > 0 is redundant
    // ...
}
```

**Report:**
```
Bug: Redundant condition
Location: line 1
Severity: Low
Confidence: High

Explanation: Condition 'x > 0' is redundant because 'x > 5' implies 'x > 0'.

Recommendation: Simplify to 'if (x > 5)'.
```

### Pattern 4: Inverted Logic

**Detection:**
- Condition appears inverted
- Behavior opposite of expected

**Example (Python):**
```python
def is_valid(value):
    if value < 0:
        return True  # BUG: Suspicious - negative values valid?
    return False
```

**Report:**
```
Bug: Suspicious inverted logic
Location: line 3
Severity: Medium
Confidence: Medium

Explanation: Function 'is_valid' returns True for negative values, which
seems counterintuitive. May be inverted logic.

Recommendation: Verify intended behavior. Consider:
if value >= 0:
    return True
```

## Unreachable Code

### Pattern 1: Code After Return

**Detection:**
- Statements after unconditional return
- Never executed

**Example (JavaScript):**
```javascript
function calculate(x) {
    return x * 2;
    console.log("Done");  // BUG: Unreachable
}
```

**Report:**
```
Bug: Unreachable code
Location: line 3
Severity: Low
Confidence: High

Explanation: Statement on line 3 is unreachable because function returns
unconditionally on line 2.

Recommendation: Remove unreachable code or fix control flow.
```

### Pattern 2: Unreachable Branch

**Detection:**
- Branch that can never execute
- Condition always false

**Example (Python):**
```python
x = 10
if x > 20:  # BUG: Never true
    print("Large")
```

**Report:**
```
Bug: Unreachable branch
Location: line 2-3
Severity: Low
Confidence: High

Explanation: Variable 'x' is 10, condition 'x > 20' is always false,
making the branch unreachable.

Recommendation: Remove dead code or fix condition.
```

### Pattern 3: Code After Throw/Raise

**Detection:**
- Code after exception throw
- Never executed

**Example (Java):**
```java
if (value < 0) {
    throw new IllegalArgumentException();
    value = 0;  // BUG: Unreachable
}
```

**Report:**
```
Bug: Unreachable code after throw
Location: line 3
Severity: Low
Confidence: High

Explanation: Statement on line 3 is unreachable because exception is
thrown unconditionally on line 2.

Recommendation: Remove unreachable statement.
```

## Inconsistent State Updates

### Pattern 1: Partial State Update

**Detection:**
- Some fields updated, others not
- Inconsistent object state

**Example (Python):**
```python
class Account:
    def transfer(self, amount, to_account):
        self.balance -= amount  # Deduct from source
        # BUG: Missing to_account.balance += amount
```

**Report:**
```
Bug: Incomplete state update
Location: line 3
Severity: High
Confidence: Medium

Explanation: Method 'transfer' deducts from source balance but doesn't
add to destination balance, leaving system in inconsistent state.

Recommendation: Add corresponding update:
to_account.balance += amount
```

### Pattern 2: Update Without Validation

**Detection:**
- State modified without checking invariants
- May violate constraints

**Example (Java):**
```java
public void setAge(int age) {
    this.age = age;  // BUG: No validation
}
```

**Report:**
```
Bug: State update without validation
Location: line 2
Severity: Medium
Confidence: Medium

Explanation: Method sets 'age' without validating value. Negative or
unreasonable values could violate invariants.

Recommendation: Add validation:
if (age < 0 || age > 150) {
    throw new IllegalArgumentException();
}
```

### Pattern 3: Race Condition in Update

**Detection:**
- Non-atomic read-modify-write
- Potential race condition

**Example (Java):**
```java
public void increment() {
    int current = counter;  // BUG: Race condition
    counter = current + 1;
}
```

**Report:**
```
Bug: Non-atomic state update
Location: line 2-3
Severity: High
Confidence: Medium

Explanation: Read-modify-write operation is not atomic. Multiple threads
could read same value, causing lost updates.

Recommendation: Use atomic operation or synchronization:
counter++;  // or use AtomicInteger
```

## Logic Errors

### Pattern 1: Off-by-One Error

**Detection:**
- Loop boundary incorrect
- Array access off by one

**Example (C):**
```c
for (int i = 0; i <= n; i++) {  // BUG: Should be i < n
    array[i] = 0;  // Buffer overflow when i == n
}
```

**Report:**
```
Bug: Off-by-one error
Location: line 1
Severity: High
Confidence: High

Explanation: Loop condition 'i <= n' causes iteration when i == n,
accessing array[n] which is out of bounds for array of size n.

Recommendation: Change to 'i < n' for 0-indexed array.
```

### Pattern 2: Wrong Operator Precedence

**Detection:**
- Expression with unexpected precedence
- Likely needs parentheses

**Example (Python):**
```python
if x & 1 == 0:  # BUG: Parsed as x & (1 == 0)
    print("Even")
```

**Report:**
```
Bug: Operator precedence issue
Location: line 1
Severity: Medium
Confidence: High

Explanation: Expression parsed as 'x & (1 == 0)' due to precedence.
Likely intended '(x & 1) == 0' to check if x is even.

Recommendation: Add parentheses: if (x & 1) == 0:
```

### Pattern 3: Incorrect Loop Termination

**Detection:**
- Loop may not terminate
- Infinite loop potential

**Example (JavaScript):**
```javascript
let i = 0;
while (i < 10) {
    console.log(i);
    // BUG: Missing i++
}
```

**Report:**
```
Bug: Potential infinite loop
Location: line 2-4
Severity: High
Confidence: High

Explanation: Loop variable 'i' is never modified inside loop. Condition
'i < 10' remains true indefinitely, causing infinite loop.

Recommendation: Add loop variable update: i++;
```

### Pattern 4: Incorrect Boolean Logic

**Detection:**
- Boolean expression with error
- De Morgan's law violation

**Example (Java):**
```java
if (!(x > 0 && y > 0)) {  // Negation of AND
    // BUG: Likely meant !(x > 0 || y > 0)
}
```

**Report:**
```
Bug: Suspicious boolean logic
Location: line 1
Severity: Medium
Confidence: Medium

Explanation: Negation of 'x > 0 && y > 0' is 'x <= 0 || y <= 0'.
If intent was "neither positive", should use OR: !(x > 0 || y > 0).

Recommendation: Verify intended logic and apply De Morgan's law correctly.
```

## Resource Management Issues

### Pattern 1: Resource Leak

**Detection:**
- Resource opened but not closed
- Missing cleanup in error path

**Example (Python):**
```python
def read_file(path):
    f = open(path)  # BUG: Not closed
    data = f.read()
    return data
```

**Report:**
```
Bug: Resource leak
Location: line 2
Severity: Medium
Confidence: High

Explanation: File opened on line 2 but never closed. Resource leak if
exception occurs or in normal path.

Recommendation: Use context manager:
with open(path) as f:
    data = f.read()
    return data
```

### Pattern 2: Double Free/Close

**Detection:**
- Resource closed multiple times
- Potential error

**Example (Java):**
```java
stream.close();
// ... some code ...
stream.close();  // BUG: Double close
```

**Report:**
```
Bug: Double close
Location: line 3
Severity: Medium
Confidence: High

Explanation: Stream closed on line 1 and again on line 3. Second close
may throw exception or cause undefined behavior.

Recommendation: Remove duplicate close or use try-with-resources.
```

### Pattern 3: Use After Free/Close

**Detection:**
- Resource used after being closed
- Invalid operation

**Example (Python):**
```python
f = open(path)
f.close()
data = f.read()  # BUG: Use after close
```

**Report:**
```
Bug: Use after close
Location: line 3
Severity: High
Confidence: High

Explanation: File closed on line 2 but used on line 3. Reading from
closed file raises ValueError.

Recommendation: Reorder operations or reopen file.
```

## Type-Related Bugs

### Pattern 1: Type Mismatch

**Detection:**
- Value of wrong type passed
- Type error likely

**Example (Python):**
```python
def calculate(x: int, y: int) -> int:
    return x + y

result = calculate("5", "10")  # BUG: Strings instead of ints
```

**Report:**
```
Bug: Type mismatch
Location: line 4
Severity: Medium
Confidence: High

Explanation: Function expects int arguments but receives strings.
Will concatenate strings instead of adding numbers.

Recommendation: Convert to int: calculate(int("5"), int("10"))
```

### Pattern 2: Implicit Type Coercion

**Detection:**
- Unexpected type conversion
- May cause bugs

**Example (JavaScript):**
```javascript
if (value == 0) {  // BUG: Coerces "", false, null to 0
    // ...
}
```

**Report:**
```
Bug: Implicit type coercion
Location: line 1
Severity: Low
Confidence: Medium

Explanation: Using '==' allows type coercion. Empty string, false, and
null all coerce to 0, which may be unintended.

Recommendation: Use strict equality: if (value === 0)
```

## Confidence Assessment

### High Confidence (90-100%)

**Indicators:**
- Clear violation of language semantics
- Guaranteed to cause error
- No ambiguity in analysis

**Examples:**
- Null dereference without check
- Array index out of bounds
- Unreachable code after return
- Assignment in condition (= vs ==)

**Report Format:**
```
Confidence: High (95%)
This is almost certainly a bug that will cause runtime errors.
```

### Medium Confidence (60-89%)

**Indicators:**
- Likely bug but context-dependent
- May be intentional in rare cases
- Requires domain knowledge to confirm

**Examples:**
- Suspicious inverted logic
- Missing validation
- Potential race condition
- Incomplete state update

**Report Format:**
```
Confidence: Medium (75%)
This appears to be a bug but may be intentional. Review carefully.
```

### Low Confidence (30-59%)

**Indicators:**
- Suspicious pattern but uncertain
- Could be intentional design
- Needs more context

**Examples:**
- Redundant condition (may be for clarity)
- Unusual but valid logic
- Style issues that might hide bugs

**Report Format:**
```
Confidence: Low (45%)
This pattern is suspicious but may be intentional. Verify behavior.
```

### Factors Affecting Confidence

1. **Code Context:**
   - More context → Higher confidence
   - Isolated snippet → Lower confidence

2. **Language Semantics:**
   - Clear violation → High confidence
   - Ambiguous behavior → Lower confidence

3. **Common Patterns:**
   - Known bug pattern → Higher confidence
   - Unusual but valid → Lower confidence

4. **Documentation:**
   - Contradicts docs → Higher confidence
   - Matches docs → Lower confidence (may be intentional)

## Report Template

```markdown
## Bug: [Bug Type]

**Location:** [File]:[Line] or [Line Range]
**Severity:** [High/Medium/Low]
**Confidence:** [High/Medium/Low] ([Percentage]%)

### Description
[Clear explanation of what the bug is]

### Why This Is a Bug
[Explanation of why this is problematic]

### Potential Impact
[What could go wrong if not fixed]

### Recommendation
[Specific fix or mitigation]

### Code Context
```[language]
[Relevant code snippet with line numbers]
```

### Example Fix
```[language]
[Suggested corrected code]
```
```

## Detection Heuristics

### Null Dereference Detection

1. Track nullable sources:
   - Method returns (findById, get, etc.)
   - Nullable parameters
   - Conditional assignments

2. Track null checks:
   - if (x != null)
   - if (x == null) return
   - assert x != null

3. Flag dereferences without checks:
   - x.method()
   - x.field
   - x[index]

### Condition Analysis

1. Evaluate constant conditions:
   - Substitute known values
   - Check if always true/false

2. Check for common errors:
   - = vs ==
   - & vs &&
   - | vs ||

3. Analyze boolean logic:
   - Redundant conditions
   - Contradictory conditions
   - De Morgan's law violations

### Reachability Analysis

1. Track control flow:
   - Unconditional returns
   - Unconditional throws
   - Break/continue statements

2. Mark unreachable code:
   - After unconditional exit
   - In always-false branches

### State Consistency

1. Track state modifications:
   - Field assignments
   - Method calls that modify state

2. Check for completeness:
   - Paired operations (open/close)
   - Symmetric updates (add/remove)
   - Invariant maintenance

## Best Practices

### DO:
- ✅ Provide specific line numbers
- ✅ Explain why it's a bug
- ✅ Suggest concrete fixes
- ✅ Include confidence levels
- ✅ Show code context
- ✅ Prioritize by severity
- ✅ Group related bugs

### DON'T:
- ❌ Report style issues as bugs
- ❌ Flag intentional patterns without evidence
- ❌ Claim certainty without justification
- ❌ Ignore language-specific idioms
- ❌ Report false positives without caveats
- ❌ Overwhelm with low-confidence warnings
