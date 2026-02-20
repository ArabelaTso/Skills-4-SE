---
name: metamorphic-test-generator
description: Generate test cases using metamorphic testing by applying transformations based on metamorphic properties. Use when you need to expand test suites, test programs without oracles, validate mathematical or algorithmic properties, or detect subtle bugs through input-output relationships. The skill takes a program, original test cases, and metamorphic properties as input, generates new test cases by applying transformations, executes tests, verifies outputs satisfy properties, reports violations and anomalies, and outputs an expanded test suite with property coverage summary. Supports multiple programming languages and property types.
---

# Metamorphic Test Generator

## Overview

This skill generates test cases using metamorphic testing, applying transformations based on metamorphic properties to expand test suites and detect bugs through input-output relationships.

## Quick Start

```bash
# Generate metamorphic tests
python scripts/generate.py program.py --tests tests/ --properties properties.json

# Use specific metamorphic properties
python scripts/generate.py program.py --tests tests/ --properties "permutation,addition"

# Generate report
python scripts/generate.py program.py --tests tests/ --properties props.json --output report.json
```

## What Gets Generated

1. **Follow-up Test Cases** - New inputs derived from original tests
2. **Property Verification** - Checks that outputs satisfy metamorphic relations
3. **Violation Reports** - Identifies property violations and anomalies
4. **Expanded Test Suite** - Original plus generated tests
5. **Coverage Summary** - Property coverage and effectiveness

## Common Metamorphic Properties

- **Permutation** - Reordering inputs should not affect output
- **Addition** - Adding elements should increase/maintain result
- **Multiplication** - Scaling inputs should scale outputs proportionally
- **Inverse** - Applying inverse operation should return original
- **Equivalence** - Different representations should yield same result
- **Monotonicity** - Increasing input should increase/maintain output

## Test Generation Report

Generates detailed report with:
- **Original Tests** - Initial test cases count
- **Generated Tests** - New test cases created
- **Properties Applied** - Metamorphic relations used
- **Violations Found** - Property violations detected
- **Property Coverage** - Percentage of properties satisfied
- **Anomalies** - Unexpected behaviors identified

Example report:
```json
{
  "original_tests": 20,
  "generated_tests": 60,
  "properties_applied": ["permutation", "addition", "inverse"],
  "violations": 3,
  "property_coverage": 95.0,
  "anomalies": ["inverse property failed for negative inputs"]
}
```

## Usage

```bash
python scripts/generate.py <program> --tests <test_dir> --properties <properties> [--output <report.json>]
```

## Tips

- Define properties based on program semantics
- Start with simple properties (permutation, addition)
- Use metamorphic testing when oracles are unavailable
- Violations often indicate real bugs
- Combine with traditional testing for best results
- Document properties for future test maintenance
