---
name: java-api-consistency-validator
description: Validate API consistency between two versions of Java libraries. Use when you need to compare API behavior, signatures, and exceptions between Java library versions to identify breaking changes, incompatible modifications, and behavior differences. The skill performs static analysis of Java code, compares method signatures, class definitions, interface changes, parameter types, return types, exception declarations, and generates a detailed JSON report with breaking changes, warnings, and migration guidance. Supports Java libraries and packages.
---

# Java API Consistency Validator

## Overview

This skill validates API consistency between two versions of Java libraries by comparing signatures, behavior, and exceptions. It identifies breaking changes, incompatible modifications, and provides detailed reports to guide safe API migration or upgrade.

## Quick Start

```bash
# Compare two versions of a Java library
python scripts/validate.py /path/to/old_version /path/to/new_version

# Specify output file
python scripts/validate.py old_lib/ new_lib/ --output report.json
```

## What Gets Validated

1. **Method Signatures** - Parameters, return types, modifiers
2. **Class Definitions** - Methods, inheritance, interfaces
3. **Interface Changes** - Method additions, removals
4. **Parameter Changes** - Added, removed, or modified parameters
5. **Return Type Changes** - Modified return types
6. **Exception Declarations** - throws clauses
7. **Removed APIs** - Deleted classes, interfaces, or methods

## Validation Report

The tool generates a JSON report with:

- **Breaking Changes**: API removals, incompatible modifications
- **Warnings**: Type changes, signature modifications
- **Info**: New additions, non-breaking changes
- **Summary**: Total issues by severity

Example report:
```json
{
  "summary": {
    "breaking_changes": 3,
    "warnings": 5,
    "info": 2
  },
  "breaking_changes": [
    {
      "type": "method_removed",
      "class": "UserService",
      "method": "getUser",
      "severity": "breaking",
      "message": "Method 'UserService.getUser' was removed"
    }
  ]
}
```

## Usage

```bash
python scripts/validate.py <old_version_path> <new_version_path> [--output <report.json>]
```

The validator exits with code 1 if breaking changes are found, 0 otherwise.

## Tips

- Run validation before upgrading dependencies
- Review breaking changes carefully
- Check warnings for potential issues
- Use in CI/CD pipelines to catch API changes
- Compare against semantic versioning expectations
- Validate before releasing new library versions
