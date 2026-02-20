---
name: multi-version-behavior-comparator
description: Compare behavior across multiple versions of programs or repositories. Use when you need to analyze how functionality changes between versions, identify regressions, compare outputs and exceptions, or validate upgrades. The skill compares execution behavior, test results, outputs, exceptions, and observable states across versions, generating detailed reports showing behavioral divergences, potential regressions, added/removed functionality, and areas requiring validation. Supports multiple programming languages and can work with test suites or execution traces.
---

# Multi-Version Behavior Comparator

## Overview

This skill compares behavior across multiple versions of programs, identifying functional changes, regressions, and behavioral divergences to guide safe upgrades and validation.

## Quick Start

```bash
# Compare two versions
python scripts/compare.py v1.0/ v2.0/

# Compare multiple versions with test suite
python scripts/compare.py v1.0/ v2.0/ v3.0/ --tests tests/

# Generate detailed report
python scripts/compare.py old/ new/ --output report.json
```

## What Gets Compared

1. **Functionality** - Added, removed, or modified features
2. **Outputs** - Return values, printed output, file changes
3. **Exceptions** - Error handling and exception types
4. **Test Results** - Pass/fail status across versions
5. **Observable States** - Side effects, state changes

## Comparison Report

Generates JSON report with:
- **Behavioral Divergences**: Where versions behave differently
- **Potential Regressions**: Functionality that may have broken
- **Added Features**: New functionality in newer versions
- **Removed Features**: Functionality no longer present
- **Validation Areas**: Code requiring manual review

## Usage

```bash
python scripts/compare.py <version1> <version2> [version3...] [--tests <test_dir>] [--output <report.json>]
```

## Tips

- Run before deploying new versions
- Use with existing test suites for comprehensive comparison
- Review regressions carefully before upgrading
- Validate high-risk areas identified in report
