---
name: test-deduplicator
description: Analyzes test suites to identify redundant and duplicate test cases using coverage analysis, semantic similarity, and execution results. Use this skill when you need to reduce test suite size, identify redundant tests, optimize test execution time, analyze test coverage overlap, find tests with identical behavior, or improve test suite maintainability. Triggers when users ask to deduplicate tests, find redundant test cases, reduce test suite size, identify duplicate tests, or optimize test coverage.
---

# Test Deduplicator

## Overview

This skill analyzes test suites to identify redundant or duplicate tests by examining code coverage, semantic similarity, and execution behavior. It groups equivalent tests, explains deduplication rationale, and recommends which tests can be safely removed while preserving overall test effectiveness.

## Workflow

### 1. Collect Test Coverage Data

First, gather coverage information for each test in the suite.

**For Python projects with pytest:**
```bash
# Run tests with coverage for each test individually
pytest --cov=src --cov-report=json tests/

# Or use the coverage analyzer script with pre-collected data
python scripts/coverage_analyzer.py coverage_data.json --output coverage_analysis.json
```

**Coverage data format:**
```json
{
  "test_module::test_function_1": {
    "coverage": {
      "src/module.py": [10, 11, 12, 15, 20],
      "src/utils.py": [5, 6, 7]
    }
  },
  "test_module::test_function_2": {
    "coverage": {
      "src/module.py": [10, 11, 12, 15, 20],
      "src/utils.py": [5, 6, 7]
    }
  }
}
```

### 2. Analyze Semantic Similarity

Parse test code to identify semantic similarities:

```bash
python scripts/semantic_analyzer.py tests/*.py --output semantic_analysis.json --threshold 0.7
```

This analyzes:
- Assertion patterns
- Function call sequences
- Code structure similarity
- Variable usage patterns

### 3. Generate Deduplication Recommendations

Combine coverage and semantic analysis to produce recommendations:

```bash
python scripts/deduplicator.py \
  --coverage coverage_analysis.json \
  --semantic semantic_analysis.json \
  --output recommendations.json \
  --threshold 0.8
```

### 4. Review Recommendations

Examine the generated recommendations:

```json
{
  "redundant_groups": [
    {
      "type": "identical_coverage",
      "tests": ["test_a", "test_b", "test_c"],
      "reason": "Tests have identical code coverage",
      "confidence": 1.0,
      "keep": "test_a",
      "remove": ["test_b", "test_c"],
      "rationale": "test_a has descriptive name, fast execution"
    }
  ],
  "removal_candidates": [...],
  "coverage_impact": {
    "coverage_preserved": true,
    "tests_removed": 15
  }
}
```

### 5. Apply Deduplication

After manual review, remove approved redundant tests and verify coverage is preserved.

## Analysis Types

### Coverage-Based Analysis

Identifies tests with overlapping or identical coverage patterns.

**Redundancy Types:**
- **Identical Coverage**: Tests covering exactly the same lines
- **Subsumption**: One test's coverage is a subset of another
- **High Overlap**: Tests with >80% coverage similarity

**Script:** `scripts/coverage_analyzer.py`

**Output:**
- Identical coverage groups
- Subsumed tests
- Coverage similarity matrix
- Unique coverage contributions

### Semantic Analysis

Identifies tests with similar code structure and assertions.

**Similarity Metrics:**
- Assertion similarity (40% weight)
- Function call similarity (30% weight)
- Source code similarity (30% weight)

**Script:** `scripts/semantic_analyzer.py`

**Output:**
- Tests with identical assertions
- Semantically similar test pairs
- Test pattern groups

### Integrated Analysis

Combines multiple signals for comprehensive recommendations.

**Redundancy Score:**
```
Redundancy = 0.5 × Coverage_Sim + 0.3 × Semantic_Sim + 0.2 × Execution_Sim
```

**Script:** `scripts/deduplicator.py`

**Output:**
- Prioritized removal recommendations
- Confidence scores
- Coverage impact analysis
- Rationale for each recommendation

## Configuration

Customize analysis using the configuration template:

```bash
cp assets/deduplication_config.json my_config.json
# Edit my_config.json
```

**Key Settings:**

**Thresholds:**
- `identical_coverage`: 1.0 (exact match)
- `highly_similar_coverage`: 0.9
- `semantic_similarity`: 0.7
- `overall_redundancy`: 0.8

**Prioritization Weights:**
- `unique_coverage_lines`: 10 (most important)
- `execution_speed_bonus`: 5
- `stability_bonus`: 3
- `name_clarity_bonus`: 2

**Safety Checks:**
- `preserve_coverage`: true (must maintain coverage)
- `require_manual_review`: true (human approval needed)
- `min_confidence_for_auto_removal`: 0.95

## Common Use Cases

### Use Case 1: Reduce Test Suite Size
```
User: "Our test suite has grown to 500 tests and takes too long to run. Find redundant tests."
→ Run coverage analysis on all tests
→ Run semantic analysis on test files
→ Generate deduplication recommendations
→ Review and remove redundant tests
→ Verify coverage is preserved
```

### Use Case 2: Identify Duplicate Tests After Merge
```
User: "We merged two branches and suspect there are duplicate tests now."
→ Analyze tests from both branches
→ Find tests with identical coverage and assertions
→ Recommend which duplicates to remove
→ Prioritize keeping tests with better names/documentation
```

### Use Case 3: Optimize CI/CD Pipeline
```
User: "Tests take 30 minutes in CI. Which tests can we safely remove?"
→ Analyze coverage overlap
→ Find subsumed tests (tests fully covered by others)
→ Calculate time savings from removal
→ Generate removal plan with coverage guarantee
```

### Use Case 4: Test Suite Refactoring
```
User: "Clean up our test suite and remove low-value tests."
→ Identify tests with zero unique coverage contribution
→ Find tests with identical assertions
→ Group semantically similar tests
→ Recommend merging or removing redundant tests
```

## Understanding Results

### Redundancy Types in Reports

**Identical Coverage (Confidence: 1.0)**
- Tests execute exactly the same code paths
- Safe to remove all but one
- Keep the test with the best name/documentation

**Subsumed Tests (Confidence: 0.95)**
- One test's coverage is completely contained in another
- The subsumed test adds no unique value
- Safe to remove

**Highly Similar (Confidence: 0.85)**
- Tests have >80% redundancy score
- Review manually before removal
- Consider merging instead of removing

**Semantically Identical (Confidence: 0.90)**
- Tests have identical assertions and logic
- Different only in variable names or formatting
- Safe to remove duplicates

### Prioritization Rationale

Tests are prioritized to keep based on:

1. **Unique Coverage**: Tests covering lines no other test covers
2. **Execution Speed**: Faster tests preferred
3. **Stability**: Tests that consistently pass
4. **Descriptiveness**: Clear, well-named tests
5. **Recency**: Recently updated tests

## Best Practices

1. **Start Conservative**: Use high thresholds (≥0.9) initially

2. **Preserve Coverage**: Always verify total coverage remains unchanged

3. **Manual Review**: Review recommendations before removing tests

4. **Incremental Removal**: Remove tests in small batches, verify after each

5. **Consider Test Intent**: Don't remove tests that document important edge cases

6. **Monitor Impact**: Track test suite effectiveness after deduplication

## Limitations

1. **Parameterized Tests**: May appear similar but test different values

2. **Test Intent**: Cannot detect if tests serve different documentation purposes

3. **Flaky Tests**: Inconsistent coverage may affect analysis

4. **Integration Tests**: May intentionally duplicate unit test coverage

5. **Language Support**: Currently optimized for Python (extensible to other languages)

## Resources

### scripts/coverage_analyzer.py
Analyzes test coverage to identify redundant tests:
- Loads coverage data for each test
- Calculates coverage similarity (Jaccard index)
- Finds identical coverage groups
- Identifies subsumed tests
- Calculates unique coverage contributions

### scripts/semantic_analyzer.py
Analyzes test code for semantic similarity:
- Parses test files using AST
- Extracts assertions and function calls
- Calculates assertion similarity
- Compares code structure
- Identifies semantically identical tests

### scripts/deduplicator.py
Integrated deduplication engine:
- Combines coverage and semantic analysis
- Calculates composite redundancy scores
- Prioritizes tests to keep
- Generates actionable recommendations
- Validates coverage preservation

### references/deduplication_methodology.md
Comprehensive methodology guide covering:
- Redundancy types and detection methods
- Similarity metrics and formulas
- Deduplication strategies
- Prioritization algorithms
- Best practices and pitfalls
- Coverage impact analysis
- False positive mitigation

Read this reference when you need deeper understanding of the methodology, want to customize similarity metrics, or need to explain the approach to stakeholders.

### assets/deduplication_config.json
Configuration template for customizing:
- Analysis thresholds
- Prioritization weights
- Filtering rules
- Safety checks
- Output formats

Copy and modify this template to create custom configurations for specific projects or test suite characteristics.
