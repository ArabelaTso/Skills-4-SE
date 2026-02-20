# Requirements Engineering Suite

Complete toolkit for requirements analysis, enhancement, formalization, and traceability.

## 📦 Included Skills (12)

### Requirements Analysis
- **requirement-enhancer** - Enhance and formalize requirements
- **requirement-summarizer** - Create concise requirement summaries
- **requirement-summary** - Generate executive summaries
- **ambiguity-detector** - Detect ambiguous requirements

### Requirements Comparison
- **requirement-comparison-reporter** - Compare requirement versions
- **requirement-coverage-checker** - Check implementation coverage

### Formalization
- **nl-to-constraints** - Convert natural language to formal constraints
- **requirement-to-tlaplus-property-generator** - Generate TLA+ properties
- **specification-to-temporal-logic-generator** - Generate temporal logic specs

### Traceability
- **traceability-matrix-generator** - Generate traceability matrices
- **scenario-generator** - Generate test scenarios from requirements
- **req-to-test** - Generate tests from requirements

## 🎯 Use Cases

### 1. Requirements Quality Improvement
```bash
# Detect ambiguities
/ambiguity-detector --requirements requirements.md

# Enhance requirements
/requirement-enhancer --input requirements.md --output enhanced.md

# Summarize for stakeholders
/requirement-summarizer --requirements enhanced.md
```

### 2. Formal Specification
```bash
# Convert to formal constraints
/nl-to-constraints --requirements requirements.md

# Generate TLA+ properties
/requirement-to-tlaplus-property-generator --requirements requirements.md

# Generate temporal logic
/specification-to-temporal-logic-generator --spec requirements.md
```

### 3. Requirements Traceability
```bash
# Generate traceability matrix
/traceability-matrix-generator --requirements requirements.md --code src/

# Check coverage
/requirement-coverage-checker --requirements requirements.md --tests tests/

# Generate test scenarios
/scenario-generator --requirements requirements.md
```

### 4. Requirements Evolution
```bash
# Compare versions
/requirement-comparison-reporter --old v1-requirements.md --new v2-requirements.md

# Update traceability
/traceability-matrix-generator --requirements v2-requirements.md --code src/
```

## 🚀 Installation

```bash
cd skill-packs/requirements-engineering-suite
./install.sh
```

## 📊 Requirements Workflow

```
Natural Language → Ambiguity Detection → Enhancement
       ↓                                      ↓
Formalization ← Traceability Matrix → Test Generation
```

## 🔗 Related Skill Packs

- **formal-verification-toolkit** - Verify formal specifications
- **test-automation-suite** - Generate tests from requirements
- **code-quality-toolkit** - Ensure code meets requirements

## 📖 Examples

### Example 1: Formalize Requirements

```bash
# Input: "The system should respond quickly"
/ambiguity-detector --requirements vague.md
# Output: "Ambiguous term: 'quickly' - needs quantification"

# Enhance with formal constraints
/requirement-enhancer --input vague.md
# Output: "The system SHALL respond within 200ms for 95% of requests"

# Convert to formal property
/requirement-to-tlaplus-property-generator --requirements enhanced.md
# Output: TLA+ property: ResponseTime < 200
```

### Example 2: Requirements Traceability

```bash
# Generate traceability matrix
/traceability-matrix-generator --requirements requirements.md --code src/

# Output: requirements-traceability.md
# REQ-001 → UserService.java:42, UserTest.java:15
# REQ-002 → AuthController.java:28, AuthTest.java:33
```

### Example 3: Test Generation from Requirements

```bash
# Generate test scenarios
/scenario-generator --requirements requirements.md

# Generate actual tests
/req-to-test --requirements requirements.md --output tests/

# Verify coverage
/requirement-coverage-checker --requirements requirements.md --tests tests/
```

## 🛠️ Requirements

- Claude Code CLI
- Markdown support (for requirements documents)
- TLA+ tools (optional, for formal verification)

## 📝 Best Practices

1. **Start with ambiguity detection** - Clean requirements first
2. **Enhance incrementally** - Don't over-formalize too early
3. **Maintain traceability** - Update matrix with every change
4. **Generate tests early** - Catch misunderstandings quickly

## 📝 License

MIT
