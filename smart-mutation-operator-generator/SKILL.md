---
name: smart-mutation-operator-generator
description: Analyzes a repository and its test suite to generate customized mutation operators tailored to the project. Use this skill when setting up mutation testing, improving test quality, or generating project-specific mutants. Considers language constructs, business logic patterns, API calls, data types, and code complexity to produce effective mutation operators that maximize test sensitivity while avoiding trivial or equivalent mutations. Generates prioritized operator sets (high/medium/low value) with impact summaries. Triggers when users ask to generate mutation operators, customize mutation testing, analyze code for mutation opportunities, or create project-specific mutants.
---

# Smart Mutation Operator Generator

Generate customized mutation operators tailored to a specific codebase to maximize mutation testing effectiveness.

## Workflow

### 1. Analyze Codebase

**Run analysis script**:
```bash
# Analyze entire repository
python scripts/generate_operators.py /path/to/repo

# Analyze single file
python scripts/generate_operators.py /path/to/file.py

# Save detailed report
python scripts/generate_operators.py /path/to/repo --output operators.json
```

**Script analyzes**:
- Arithmetic operations (AOR candidates)
- Comparison operations (ROR candidates)
- Logical operations (LCR candidates)
- Constants and literals (CRP candidates)
- Function calls (FCR candidates)
- API interactions
- Database operations
- Control flow structures
- Exception handling

### 2. Review Generated Operators

**Operator priorities**:
- 🔴 **High Priority**: Most effective at finding bugs
  - ROR (Relational Operator Replacement)
  - LCR (Logical Connector Replacement)
  - CRP (Constant Replacement)
  - COR (Conditional Operator Replacement)

- 🟡 **Medium Priority**: Useful but may generate equivalent mutants
  - AOR (Arithmetic Operator Replacement)
  - FCR (Function Call Replacement)
  - RVR (Return Value Replacement)
  - API/DB operation mutations

- 🔵 **Low Priority**: Often trivial or equivalent
  - UOI/UOD (Unary Operator Insertion/Deletion)
  - STR (String Replacement)
  - IHI/IHD (Hiding Variable Insertion/Deletion)

### 3. Customize for Project

**Consider project characteristics**:

**Financial/calculation-heavy code**:
- Prioritize AOR (arithmetic operators)
- Focus on CRP (numeric constants)
- Test boundary conditions

**API-heavy code**:
- Custom API call mutations
- Timeout/retry logic mutations
- Error response mutations

**Business logic code**:
- ROR (comparisons in business rules)
- LCR (logical conditions)
- COR (conditional branches)

**Data processing code**:
- Collection mutations
- Null/empty value mutations
- Type conversion mutations

### 4. Define Custom Operators

**Example custom operators**:

**API Timeout Mutation**:
```python
# Original
response = api.call(timeout=30)

# Mutant
response = api.call(timeout=1)  # Test timeout handling
```

**Retry Logic Mutation**:
```python
# Original
@retry(max_attempts=3)
def fetch_data():
    pass

# Mutant
@retry(max_attempts=1)  # Test with fewer retries
def fetch_data():
    pass
```

**Business Rule Mutation**:
```python
# Original
if age >= 18 and has_license:
    allow_driving()

# Mutants
if age > 18 and has_license:   # ROR
if age >= 18 or has_license:   # LCR
if age >= 21 and has_license:  # CRP (domain-specific)
```

### 5. Avoid Trivial Mutations

**Skip equivalent mutants**:
```python
# Equivalent (don't mutate)
x = a + 0  # → x = a - 0 (still equals a)
x = a * 1  # → x = a / 1 (still equals a)

# Non-equivalent (do mutate)
x = a + 1  # → x = a - 1 (different result)
x = a * 2  # → x = a / 2 (different result)
```

**Skip trivial mutations**:
```python
# Trivial (low value)
message = "Hello"  # → message = "" (obvious failure)

# Valuable (high value)
if count > 0:      # → if count >= 0 (subtle boundary)
```

### 6. Generate Mutation Test Plan

**Document operator selection**:
```
MUTATION TESTING PLAN
=====================

Project: MyApp
Language: Python
Files Analyzed: 45

SELECTED OPERATORS
------------------

High Priority (Apply to all code):
1. ROR - Relational Operator Replacement
   - Target: Comparison operations in business logic
   - Expected: 150 mutants
   - Rationale: Critical for boundary condition testing

2. LCR - Logical Connector Replacement
   - Target: Boolean expressions in validation
   - Expected: 80 mutants
   - Rationale: Tests logical condition coverage

3. CRP - Constant Replacement
   - Target: Numeric thresholds and limits
   - Expected: 120 mutants
   - Rationale: Tests boundary values

Medium Priority (Apply selectively):
4. AOR - Arithmetic Operator Replacement
   - Target: Calculation functions only
   - Expected: 60 mutants
   - Rationale: Financial calculations need thorough testing

Custom Operators:
5. RETRY - Retry Logic Mutation
   - Target: @retry decorators
   - Expected: 15 mutants
   - Rationale: Test resilience mechanisms

ESTIMATED RESULTS
-----------------
Total Mutants: ~425
Mutation Score Target: >80%
Execution Time: ~25 minutes
```

### 7. Implement with Mutation Tool

**Python (mutmut)**:
```bash
mutmut run --paths-to-mutate=src/
mutmut results
```

**JavaScript (Stryker)**:
```javascript
// stryker.conf.js
module.exports = {
  mutator: {
    excludedMutations: ['StringLiteral', 'UnaryOperator']
  }
};
```

## Quick Reference

### Standard Operators

See [standard_operators.md](references/standard_operators.md) for complete list.

**Most effective**:
- ROR: `>` → `>=`, `<`, `==`
- LCR: `and` → `or`
- CRP: `0` → `1`, `true` → `false`
- COR: `if x:` → `if not x:`

### Mutation Score

```
Mutation Score = (Killed Mutants / Total Mutants) × 100%
```

**Targets**:
- Excellent: >80%
- Good: 60-80%
- Needs improvement: <60%

## Best Practices

**Start small**:
- Begin with high-priority operators
- Test on small modules first
- Gradually expand coverage

**Focus on critical code**:
- Business logic
- Security-sensitive code
- Complex algorithms
- Error handling

**Avoid over-mutation**:
- Skip trivial mutations
- Exclude equivalent mutants
- Focus on meaningful changes

**Review results**:
- Killed: Tests are effective
- Survived: Add tests or improve existing ones
- Equivalent: Mark and exclude

## Helper Script

```bash
# Analyze repository
python scripts/generate_operators.py /path/to/repo

# Save detailed report
python scripts/generate_operators.py /path/to/repo --output report.json
```

**Output includes**:
- Detected code patterns
- Recommended operators by priority
- Estimated mutant count
- Customization suggestions
