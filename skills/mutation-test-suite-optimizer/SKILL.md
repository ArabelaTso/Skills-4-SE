---
name: mutation-test-suite-optimizer
description: Optimize test suites using mutation testing to maximize mutation kill rate with minimal tests. Use when you need to reduce test suite size while maintaining quality, identify redundant tests, improve mutation coverage, or validate test effectiveness. The skill analyzes test coverage, execution intervals, and redundancy using mutation operators, selects or generates a minimal subset of tests that maximizes mutation kill rate, and outputs an optimized test suite with detailed reports showing killed and surviving mutants. Supports multiple programming languages and mutation testing frameworks.
---

# Mutation Test Suite Optimizer

## Overview

This skill optimizes test suites using mutation testing, selecting a minimal subset of tests that maximizes mutation kill rate while reducing execution time and redundancy.

## Quick Start

```bash
# Optimize test suite with mutation testing
python scripts/optimize.py /path/to/repo --tests tests/

# Use specific mutation operators
python scripts/optimize.py repo/ --tests tests/ --operators AOR,ROR,COR

# Generate optimization report
python scripts/optimize.py repo/ --tests tests/ --output report.json
```

## What Gets Optimized

1. **Test Selection** - Identify minimal test subset for maximum coverage
2. **Redundancy Removal** - Eliminate tests that kill same mutants
3. **Mutation Coverage** - Maximize mutants killed
4. **Execution Time** - Reduce overall test execution time
5. **Test Quality** - Identify weak or ineffective tests

## Mutation Operators

Supports common mutation operators:
- **AOR** - Arithmetic Operator Replacement
- **ROR** - Relational Operator Replacement
- **COR** - Conditional Operator Replacement
- **SOR** - Shift Operator Replacement
- **LOR** - Logical Operator Replacement
- **ASR** - Assignment Operator Replacement

## Optimization Report

Generates detailed report with:
- **Optimized Test Suite** - Minimal test subset
- **Mutation Kill Rate** - Percentage of mutants killed
- **Killed Mutants** - List of detected mutants
- **Surviving Mutants** - Mutants that escaped detection
- **Redundant Tests** - Tests that can be removed
- **Execution Time Savings** - Time reduction achieved

Example report:
```json
{
  "original_tests": 150,
  "optimized_tests": 45,
  "mutation_kill_rate": 92.5,
  "killed_mutants": 185,
  "surviving_mutants": 15,
  "time_savings": "67%"
}
```

## Usage

```bash
python scripts/optimize.py <repo_path> --tests <test_dir> [--operators <ops>] [--output <report.json>]
```

## Tips

- Run regularly to maintain test suite quality
- Focus on high-value tests that kill unique mutants
- Remove redundant tests to speed up CI/CD
- Use surviving mutants to guide new test creation
- Balance mutation score with execution time
- Integrate into continuous testing pipeline
