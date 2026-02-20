---
name: rtl-specification-consistency-checker
description: Check behavioral consistency between high-level hardware specifications and RTL implementations. Use when asked to check RTL consistency, verify RTL against spec, check hardware specification compliance, validate RTL implementation, find spec violations in RTL, check behavioral consistency, or when working with hardware designs that need verification against protocol specifications, timing requirements, or functional specifications in Verilog, VHDL, or SystemVerilog.
---

# RTL-Specification Consistency Checker

## Overview

This skill enables systematic checking of behavioral consistency between high-level hardware specifications and RTL implementations. It extracts requirements from specifications, maps them to RTL logic, and classifies each requirement as satisfied, violated, underspecified, or uncheckable.

## Consistency Checking Workflow

Follow this sequential process to check RTL-specification consistency:

### 1. Parse and Understand Inputs

Read and analyze both the specification and RTL code:

**Specification Analysis:**
- Identify the format (natural language, tables, timing diagrams, protocol rules)
- Extract all behavioral requirements
- Note any assumptions or constraints
- Identify ambiguous or incomplete sections

**RTL Analysis:**
- Identify the HDL language (Verilog, VHDL, SystemVerilog)
- Locate key modules and their interfaces
- Identify state machines, registers, and control logic
- Note clock domains and reset strategies

### 2. Extract Behavioral Requirements

Formalize each requirement from the specification:

**Requirement Types:**

**Functional Requirements:**
- Input-output relationships
- State transitions
- Data transformations
- Protocol sequences

**Timing Requirements:**
- Setup/hold times
- Latency constraints
- Throughput requirements
- Clock cycle counts

**Safety Properties:**
- Invariants that must always hold
- Forbidden states or transitions
- Mutual exclusion constraints
- Data integrity conditions

**Liveness Properties:**
- Progress guarantees
- Eventual responses
- Fairness conditions

**For each requirement, document:**
- Requirement ID
- Description in natural language
- Formalized property (if possible)
- Source location in specification
- Priority/criticality

### 3. Map Requirements to RTL

Identify RTL constructs corresponding to each requirement:

**Signal Mapping:**
- Map specification signals to RTL signals
- Identify relevant registers and wires
- Note signal widths and types

**Logic Mapping:**
- Identify modules implementing each requirement
- Locate state machines and control logic
- Find combinational and sequential logic blocks
- Note line numbers and code locations

**State Mapping:**
- Map specification states to RTL state encodings
- Identify state registers and transition logic
- Document state machine structure

### 4. Check Consistency

For each requirement, verify RTL behavior:

**Verification Methods:**

**Static Analysis:**
- Check signal connectivity
- Verify state machine completeness
- Analyze control flow paths
- Check for missing cases or conditions

**Trace Analysis:**
- Construct example execution traces
- Check if traces satisfy requirements
- Look for counterexamples
- Verify timing constraints

**Pattern Matching:**
- Compare RTL patterns against specification patterns
- Check for common implementation errors
- Verify protocol compliance

### 5. Classify Requirements

Assign each requirement to one of four categories:

**✅ Satisfied:**
- RTL correctly implements the requirement
- All test cases pass
- No violations found

**❌ Violated:**
- RTL behavior contradicts the requirement
- Counterexample exists
- Clear mismatch identified

**⚠️ Underspecified:**
- Specification is ambiguous or incomplete
- Multiple valid interpretations exist
- Missing details prevent verification

**❓ Uncheckable:**
- Missing environmental assumptions
- Depends on external components
- Requires information not provided

### 6. Document Violations

For each violated requirement, provide detailed analysis:

**Violation Report Structure:**

```
Requirement ID: REQ-XXX
Status: ❌ VIOLATED

Description:
[What the requirement specifies]

RTL Location:
Module: [module_name]
File: [file_path]
Lines: [line_numbers]

Mismatch Explanation:
[Clear explanation of how RTL differs from spec]

Example Trace:
Cycle | Signal1 | Signal2 | State | Expected | Actual
------|---------|---------|-------|----------|-------
  0   |    0    |    1    | IDLE  |   IDLE   |  IDLE
  1   |    1    |    1    | IDLE  |   BUSY   |  IDLE  <- Violation
  2   |    1    |    0    | IDLE  |   DONE   |  IDLE

Root Cause:
[Analysis of why the violation occurs]

Suggested Fix:
[Proposed correction to RTL]
```

### 7. Generate Consistency Report

Produce a structured report with all findings:

## Report Structure

### Executive Summary

```
Total Requirements: X
✅ Satisfied: Y (Z%)
❌ Violated: A (B%)
⚠️ Underspecified: C (D%)
❓ Uncheckable: E (F%)

Critical Violations: G
```

### Detailed Findings

**For each requirement, include:**

#### REQ-001: [Requirement Name]
**Status:** [✅/❌/⚠️/❓]
**Priority:** [High/Medium/Low]
**Category:** [Functional/Timing/Safety/Liveness]

**Specification:**
[Requirement description from spec]

**RTL Mapping:**
- Module: [module_name]
- Signals: [signal_list]
- Lines: [line_numbers]

**Analysis:**
[Detailed consistency check results]

**[If violated] Violation Details:**
[Explanation, trace, root cause, suggested fix]

**[If underspecified] Clarification Needed:**
[What information is missing or ambiguous]

**[If uncheckable] Missing Assumptions:**
[What additional information is required]

---

### Recommendations

**Specification Improvements:**
- [List of specification clarifications needed]

**RTL Fixes:**
- [List of required RTL corrections]

**Verification Suggestions:**
- [Additional checks or formal verification recommendations]

## Common Verification Patterns

### Protocol Compliance

**Specification Pattern:**
"When valid is asserted, data must remain stable until ready is asserted"

**RTL Check:**
```verilog
// Look for:
always @(posedge clk) begin
    if (valid && !ready) begin
        // data should not change
        assert(data == $past(data));
    end
end
```

**Violation Example:**
Data changes while valid=1 and ready=0

### State Machine Verification

**Specification Pattern:**
"System must transition from IDLE to BUSY when start signal is asserted"

**RTL Check:**
```verilog
// Look for:
case (state)
    IDLE: if (start) next_state = BUSY;
    // Check if this transition exists
endcase
```

**Violation Example:**
Missing transition or wrong next state

### Timing Constraints

**Specification Pattern:**
"Output must be valid within 3 clock cycles of input"

**RTL Check:**
- Trace signal propagation through pipeline
- Count register stages
- Verify latency matches specification

**Violation Example:**
Output appears after 4 cycles instead of 3

### Reset Behavior

**Specification Pattern:**
"All registers must reset to known values"

**RTL Check:**
```verilog
// Look for:
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Check all registers have reset values
    end
end
```

**Violation Example:**
Register missing from reset logic

## HDL-Specific Considerations

### Verilog/SystemVerilog

**Key Checks:**
- Blocking vs non-blocking assignments
- Sensitivity list completeness
- Latch inference (unintended)
- Race conditions in always blocks
- X-propagation issues

**Common Patterns:**
```verilog
// State machine
always @(posedge clk) begin
    state <= next_state;
end

// Combinational logic
always @(*) begin
    case (state)
        // Check all states covered
    endcase
end
```

### VHDL

**Key Checks:**
- Process sensitivity lists
- Signal vs variable usage
- Incomplete case statements
- Uninitialized signals
- Clock edge detection

**Common Patterns:**
```vhdl
-- Sequential process
process(clk, rst)
begin
    if rst = '1' then
        -- Reset logic
    elsif rising_edge(clk) then
        -- State updates
    end if;
end process;
```

## Tips for Effective Checking

- **Start with critical requirements**: Focus on safety-critical and high-priority items first
- **Use concrete examples**: Create specific test scenarios for each requirement
- **Check edge cases**: Verify boundary conditions and corner cases
- **Trace signal flow**: Follow signals through the design hierarchy
- **Verify completeness**: Ensure all specification requirements are addressed
- **Check for unintended behavior**: Look for RTL functionality not in spec
- **Document assumptions**: Make all implicit assumptions explicit
- **Suggest improvements**: Recommend specification or RTL enhancements

## Reference Materials

For detailed HDL syntax and common patterns:
- See [references/hdl_patterns.md](references/hdl_patterns.md) for HDL-specific verification patterns
- See [references/common_violations.md](references/common_violations.md) for typical spec-RTL mismatches
