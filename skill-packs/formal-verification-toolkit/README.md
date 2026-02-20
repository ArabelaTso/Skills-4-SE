# Formal Verification Toolkit

## 📋 Overview

The Formal Verification Toolkit is a comprehensive collection of skills for formal verification of software systems. It enables you to generate formal specifications, verify properties, analyze counterexamples, and automatically repair code violations.

## 🎯 What's Included

This toolkit includes **17 skills** covering the complete formal verification workflow:

### Specification Generation
- **program-to-tlaplus-spec-generator** - Generate TLA+ specs from code
- **tlaplus-spec-generator** - Create TLA+ specs from requirements
- **requirement-to-tlaplus-property-generator** - Convert requirements to TLA+ properties
- **specification-to-temporal-logic-generator** - Generate temporal logic formulas (LTL/CTL)
- **formal-spec-generator** - Generate Isabelle/HOL or Coq specifications
- **smv-model-extractor** - Extract SMV models for symbolic model checking
- **verified-pseudocode-extractor** - Extract pseudocode from formally verified programs

### Code Translation to Verification Languages
- **c-cpp-to-lean4-translator** - Translate C/C++ to Lean4 for verification
- **cpp-to-dafny-translator** - Translate C++ to Dafny for verification
- **python-to-dafny-translator** - Translate Python to Dafny for verification
- **python-to-lean4-translator** - Translate Python to Lean4 for verification

### Property Inference
- **abstract-invariant-generator** - Infer loop invariants using abstract interpretation
- **invariant-inference** - Automatically infer program invariants

### Model Optimization
- **tlaplus-model-reduction** - Reduce TLA+ model complexity while preserving properties

### Code Repair
- **model-guided-code-repair** - Repair code violations using counterexamples
- **tlaplus-guided-code-repair** - Fix code based on TLA+ specification violations

### Testing
- **counterexample-to-test-generator** - Convert verification counterexamples to test cases

## 🚀 Quick Start

### Installation

```bash
# Install the entire toolkit
./install.sh

# Or install to custom location
./install.sh --path ~/.claude/skills
```

### Basic Usage

1. **Generate TLA+ specification from your code:**
   ```
   Use skill: program-to-tlaplus-spec-generator
   Input: Your source code
   Output: TLA+ specification
   ```

2. **Verify properties:**
   ```
   Use skill: requirement-to-tlaplus-property-generator
   Input: Natural language requirements
   Output: Formal TLA+ properties
   ```

3. **Repair violations:**
   ```
   Use skill: model-guided-code-repair
   Input: Code + counterexample
   Output: Fixed code + validation
   ```

## 📖 Complete Workflow

See [Verification Workflow](demo/verification-workflow.md) for a step-by-step guide.

```
┌─────────────┐
│ Source Code │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Generate TLA+ Spec      │ ← program-to-tlaplus-spec-generator
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ Generate Properties     │ ← requirement-to-tlaplus-property-generator
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ Model Check             │ (External: TLC/nuXmv)
└──────┬──────────────────┘
       │
       ├─── ✅ No violations → Done
       │
       └─── ❌ Counterexample found
              │
              ▼
       ┌─────────────────────────┐
       │ Analyze Counterexample  │
       └──────┬──────────────────┘
              │
              ▼
       ┌─────────────────────────┐
       │ Repair Code             │ ← model-guided-code-repair
       └──────┬──────────────────┘
              │
              ▼
       ┌─────────────────────────┐
       │ Generate Tests          │ ← counterexample-to-test-generator
       └─────────────────────────┘
```

## 💡 Use Cases

### 1. Concurrent System Verification
Verify correctness of multi-threaded programs, detect race conditions, and ensure mutual exclusion properties.

**Example:** [Concurrent Counter](examples/concurrent-counter)

### 2. Distributed Protocol Verification
Verify distributed consensus algorithms, message passing protocols, and ensure safety/liveness properties.

**Example:** [Distributed Consensus](examples/distributed-consensus)

### 3. Safety-Critical System Validation
Verify safety properties in embedded systems, real-time systems, and mission-critical applications.

**Example:** [Mutex Protocol](examples/mutex-protocol)

### 4. Code Translation for Verification
Translate production code to verification languages (Dafny, Lean4) for formal correctness proofs.

**Example:** Translate Python algorithm to Dafny with formal specifications

## 📚 Examples

Each example includes:
- Source code
- Specification
- Properties to verify
- Expected results
- Step-by-step instructions

Browse the [examples/](examples/) directory for complete working examples.

## 🔧 Requirements

- Claude Code or compatible LLM system
- (Optional) TLA+ Toolbox for model checking
- (Optional) NuSMV/nuXmv for symbolic model checking
- (Optional) Isabelle/HOL or Coq for proof checking
- (Optional) Dafny for verification
- (Optional) Lean4 for verification

## 📖 Documentation

- [Verification Workflow Guide](demo/verification-workflow.md)
- [TLA+ Basics](../../skills/program-to-tlaplus-spec-generator/references/tlaplus_syntax.md)
- [Temporal Logic Patterns](../../skills/model-guided-code-repair/references/temporal_logic_patterns.md)

## 🤝 Related Skill Packs

- **Code Translation Suite** - For general code translation
- **Security Scanner Suite** - For vulnerability detection
- **Test Automation Suite** - For comprehensive testing

## 📝 License

Same as the main Skills-4-SE repository.

## 🙋 Support

For issues or questions:
- Open an issue in the main repository
- Check the [FAQ](../../docs/FAQ.md)
- Join our community discussions
