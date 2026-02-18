---
name: specification-to-temporal-logic-generator
description: Translate natural-language requirements or structured specification documents into formal temporal logic properties (LTL, CTL, safety/liveness properties). Use when users need to formalize requirements for model checking, formal verification, or property specification. Handles embedded/real-time systems, hardware verification, concurrent systems, and reactive systems. Resolves ambiguities, asks clarifying questions when needed, and outputs machine-checkable formulas with explanations. Supports multiple output formats (SPIN, NuSMV, Uppaal, TLA+, Maude).
---

# Specification-to-Temporal-Logic Generator

Translate natural-language requirements into formal temporal logic properties for model checking and formal verification.

## Workflow

### 1. Parse Input Requirements

Extract requirements from natural language text, structured documents, or semi-formal notations.

Identify key elements:
- **Events/Actions**: What happens (e.g., "request", "response", "button_press")
- **States/Conditions**: System states (e.g., "authenticated", "locked", "idle")
- **Temporal relationships**: When things happen (e.g., "always", "eventually", "before")
- **Quantification**: Scope (e.g., "every", "some", "at least once")

### 2. Identify Property Type

Classify requirements:

**Safety** (something bad never happens): Keywords "never", "always not", "must not" → `G(!bad_event)`

**Liveness** (something good eventually happens): Keywords "eventually", "will", "guaranteed" → `F(good_event)`

**Response** (if X then eventually Y): Keywords "whenever", "if...then", "leads to" → `G(X -> F Y)`

**Precedence** (X before Y): Keywords "before", "precedes", "only after" → `(!Y) U X`

**Fairness** (repeated opportunities): Keywords "infinitely often", "repeatedly" → `G F X`

### 3. Handle Ambiguities

When requirements are ambiguous:

**Check common ambiguities**: temporal scope, quantification, ordering, duration

**Ask clarifying questions**:
```
"The system responds to requests" could mean:
1. Every request eventually gets a response: G(request -> F response)
2. Some requests get responses: EF(request && response)
Which interpretation matches your intent?
```

**State assumptions explicitly**:
```
Formula: G(request -> F response)
Assumptions:
- "Every request" means all requests (universal quantification)
- "Responds" means eventually, with no time bound
```

See [ambiguity_resolution.md](references/ambiguity_resolution.md) for detailed patterns.

### 4. Select Appropriate Logic

**Use LTL** for single execution paths, "infinitely often" (G F), "eventually forever" (F G)

**Use CTL** for branching time, "on all paths" (A) vs "on some path" (E), reachability

### 5. Generate Formulas

**Match to pattern**: See [ltl_patterns.md](references/ltl_patterns.md) and [ctl_patterns.md](references/ctl_patterns.md)

**Instantiate pattern**:
```
Pattern: G(p -> F q)
Requirement: "Every request gets a response"
Formula: G(request -> F response)
```

**Validate syntax**:
```bash
python scripts/validate_formula.py "G(request -> F response)" LTL
```

**Add explanations**: Plain English, formal semantics, assumptions, counterexamples

### 6. Convert to Tool-Specific Syntax

Generate formulas for target tools using conversion script:
```bash
python scripts/convert_format.py "G(request -> F response)" LTL SPIN
```

See [tool_syntax.md](references/tool_syntax.md) for complete syntax reference.

## Output Format

For each requirement:

```
Requirement: [Original requirement]

Formula (LTL): [LTL formula]
Formula (CTL): [CTL formula, if applicable]

Property Type: [Safety/Liveness/Response/Precedence/Fairness]

Explanation:
- Plain English: [What it means]
- Formal Semantics: [Technical interpretation]
- Assumptions: [List of assumptions]
- Violation Example: [What would violate this]

Tool-Specific Syntax:
- SPIN: [Promela syntax]
- NuSMV: [NuSMV syntax]
- Uppaal: [Uppaal syntax]

Validation: [Result from validate_formula.py]
```

## Examples

### Safety Property

**Requirement**: "The system never enters a deadlock state"

**Output**:
```
Formula (LTL): G(!deadlock)
Formula (CTL): AG(!deadlock)
Property Type: Safety (Invariant)

Explanation:
- Plain English: The system never reaches a deadlock state
- Formal Semantics: At all time points, deadlock does not hold
- Assumptions: "deadlock" is a well-defined state predicate
- Violation: System reaches a state where no process can progress

Tool-Specific Syntax:
- SPIN: [] (!deadlock)
- NuSMV: SPEC AG(!deadlock)
- Uppaal: A[] not deadlock
```

### Response Property

**Requirement**: "Whenever a button is pressed, the light turns on within 3 time units"

**Output**:
```
Formula (TCTL): G(button_press -> F[<=3] light_on)
Property Type: Bounded Response (Liveness)

Explanation:
- Plain English: Every button press is followed by light turning on within 3 time units
- Assumptions: Time is discrete, light can turn on multiple times
- Violation: Button pressed but light doesn't turn on within 3 time units

Tool-Specific Syntax:
- Uppaal: A[] (button_press imply A<> light_on[<=3])
```

### Precedence Property

**Requirement**: "Users must authenticate before accessing the system"

**Output**:
```
Formula (LTL): (!access) U authenticated
Formula (CTL): A[(!access) U authenticated]
Property Type: Precedence (Safety)

Explanation:
- Plain English: No access occurs until authentication happens
- Assumptions: Authentication is one-time, access can occur multiple times after
- Violation: Access occurs before authentication

Tool-Specific Syntax:
- SPIN: ((!access) U authenticated)
- NuSMV: SPEC A[(!access) U authenticated]
```

## Resources

### scripts/
- `validate_formula.py` - Validate temporal logic syntax (LTL, CTL, SPIN)
- `convert_format.py` - Convert between tool formats (SPIN, NuSMV, Uppaal, TLA+, Maude)

### references/
- `ltl_patterns.md` - LTL property patterns and templates
- `ctl_patterns.md` - CTL property patterns
- `ambiguity_resolution.md` - Guidelines for handling ambiguous requirements
- `tool_syntax.md` - Syntax for different model checkers
