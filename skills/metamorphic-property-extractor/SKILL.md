---
name: metamorphic-property-extractor
description: Automatically identify metamorphic properties (symmetry, linearity, additivity, input invariances) from programs or functions. Use when generating metamorphic tests, discovering program properties, validating transformations, or creating test oracles without explicit specifications. Analyzes control flow, data flow, and sample executions to output structured properties for metamorphic test generation and verification.
---

# Metamorphic Property Extractor

## Overview

Automatically identify metamorphic properties from programs to enable metamorphic testing without explicit test oracles.

## Core Workflow

### 1. Extract Properties

```bash
python scripts/property_extractor.py --program function.py --output properties.json
```

### 2. Verify Properties

```bash
python scripts/verify_properties.py --program function.py --properties properties.json
```

## Metamorphic Properties

### Symmetry
`f(x, y) == f(y, x)`

### Linearity
`f(a*x) == a*f(x)`

### Additivity
`f(x + y) == f(x) + f(y)`

### Idempotence
`f(f(x)) == f(x)`

### Permutation Invariance
`f(permute(x)) == f(x)`

## Resources

- **[references/metamorphic_testing.md](references/metamorphic_testing.md)**: Metamorphic testing guide
- **scripts/property_extractor.py**: Property extraction tool
