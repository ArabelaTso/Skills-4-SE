# SZZ Algorithm Reference

## Overview

The SZZ algorithm (named after Śliwerski, Zimmermann, and Zeller) is a widely-used approach for identifying bug-introducing commits in software repositories. It works by tracing bug-fixing commits backward through version history to find the commits that introduced the bugs.

## Traditional SZZ Algorithm

### Basic Workflow

1. **Identify Bug-Fix Commits**: Find commits that fix bugs (e.g., commits with "fix" in message, linked to bug reports)

2. **Extract Changed Lines**: Determine which lines were modified in the bug-fix commit

3. **Blame Analysis**: Use `git blame` to find which commits last modified those lines before the fix

4. **Result**: The commits identified by blame are considered bug-introducing commits

### Example

```
Commit A: Introduces buggy code
  line 10: if (x > 0)  // Should be x >= 0

Commit B: Other changes
  line 15: unrelated change

Commit C: Bug fix
  line 10: if (x >= 0)  // Fixed!
```

Running SZZ on Commit C:
- Changed line: 10
- `git blame` on line 10 before Commit C → Commit A
- Result: Commit A is bug-introducing

## Limitations of Traditional SZZ

### 1. False Positives from Refactoring

**Problem**: Code movements, renaming, and refactoring are incorrectly identified as bug-introducing.

**Example**:
```python
# Commit A: Original code
def calculate(x):
    return x * 2

# Commit B: Refactoring (extract method)
def multiply_by_two(x):
    return x * 2

def calculate(x):
    return multiply_by_two(x)

# Commit C: Bug fix
def multiply_by_two(x):
    return x * 3  # Fixed multiplier
```

Traditional SZZ blames Commit B (refactoring), but the bug was actually in Commit A.

### 2. False Positives from Formatting

**Problem**: Whitespace changes, comment modifications, and formatting are flagged as bug-introducing.

**Example**:
```python
# Commit A: Original
def foo(x):
  return x+1

# Commit B: Formatting
def foo(x):
    return x + 1  # Added spaces

# Commit C: Bug fix
def foo(x):
    return x + 2  # Fixed logic
```

Traditional SZZ blames Commit B (formatting), not Commit A.

### 3. False Positives from Code Movement

**Problem**: Moving code between files or functions is incorrectly identified.

**Example**:
```python
# Commit A: Code in file1.py
def buggy_function():
    return wrong_value

# Commit B: Move to file2.py
# (same buggy code, just moved)

# Commit C: Fix in file2.py
def buggy_function():
    return correct_value
```

Traditional SZZ blames Commit B (movement), not Commit A.

## SZZ Variants

### MA-SZZ (Meta-Annotated SZZ)

Filters out commits that only change:
- Comments
- Whitespace
- Blank lines

**Limitation**: Still produces false positives from refactoring and code movement.

### RA-SZZ (Refactoring-Aware SZZ)

Uses refactoring detection tools to filter out refactoring commits.

**Limitation**: Refactoring detection is imperfect; some refactorings are missed or misclassified.

### AG-SZZ (Annotation Graph SZZ)

Builds a graph of code annotations and dependencies to improve accuracy.

**Limitation**: Complex to implement; requires extensive code analysis infrastructure.

## Why Semantic SZZ?

Semantic SZZ addresses these limitations by:

1. **AST-Based Comparison**: Compares abstract syntax trees instead of text, ignoring formatting
2. **Control-Flow Analysis**: Detects when control flow is preserved (refactoring) vs. changed (semantic)
3. **Data-Flow Analysis**: Tracks variable usage patterns to identify semantic changes
4. **Semantic Equivalence**: Determines if code changes are semantically equivalent despite textual differences

## Key Metrics

### Precision

```
Precision = True Positives / (True Positives + False Positives)
```

Traditional SZZ: ~40-60% precision
Semantic SZZ: ~70-85% precision

### Recall

```
Recall = True Positives / (True Positives + False Negatives)
```

Both approaches: ~80-90% recall

### F1-Score

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

Semantic SZZ shows significant improvement in F1-score due to reduced false positives.

## References

- Śliwerski, J., Zimmermann, T., & Zeller, A. (2005). "When do changes induce fixes?"
- Kim, S., et al. (2006). "Automatic identification of bug-introducing changes"
- Da Costa, D. A., et al. (2017). "A framework for evaluating the results of the SZZ approach"
- Rodríguez-Pérez, G., et al. (2018). "Reproducibility and credibility in empirical software engineering"
