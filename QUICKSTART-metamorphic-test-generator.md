# Quick Start Guide - Metamorphic Test Generator

## Installation

The skill has been packaged and saved to:
```
/Users/bella/Documents/Projects/LLM4SE-Skills/metamorphic-test-generator.skill
```

## What's Included

✅ **Main Script**: `scripts/generate.py` - Full-featured metamorphic test generator
✅ **Reference Guide**: `references/properties.md` - Detailed property documentation
✅ **Templates**:
   - `assets/test-cases-template.json` - Test case template
   - `assets/properties-template.json` - Properties configuration template
✅ **Example**: `assets/example-program.py` - Working example program

## Quick Test

Run the included example to see the skill in action:

```bash
cd metamorphic-test-generator
python3 scripts/generate.py assets/example-program.py \
  --tests assets/test-cases-template.json \
  --properties permutation,addition \
  --output report.json \
  --suite-output expanded-suite.json
```

## Supported Properties

1. **permutation** - Reordering inputs shouldn't affect output
2. **addition** - Adding elements should increase/maintain result
3. **multiplication** - Scaling inputs should scale outputs proportionally
4. **inverse** - Applying inverse operation should return original
5. **monotonicity** - Increasing input shouldn't decrease output
6. **equivalence** - Different representations should yield same result

## Usage Pattern

1. **Prepare your program** - Must read JSON from stdin and output JSON to stdout
2. **Create test cases** - JSON file or directory with test cases
3. **Select properties** - Choose appropriate metamorphic properties
4. **Run generator** - Execute the script
5. **Review results** - Check violations and anomalies

## Example Output

```
============================================================
METAMORPHIC TEST GENERATION SUMMARY
============================================================
Original tests:      3
Generated tests:     5
Properties applied:  permutation, addition
Violations found:    0
Anomalies found:     0
Property coverage:   100.0%
============================================================
```

## Next Steps

- Read `references/properties.md` for detailed property explanations
- Customize properties for your specific domain
- Integrate with your CI/CD pipeline
- Use violations to identify bugs

## Support

For detailed documentation, see the README.md in the skill directory.
