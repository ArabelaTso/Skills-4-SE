# Formal Verification Tools Reference

Guide to using formal equivalence checking tools with generated scripts.

## Tool-Agnostic Approach

This skill generates tool-agnostic analysis that can be used with any formal verification tool. The analysis identifies:

1. Interface alignment
2. Structural differences
3. Semantic differences
4. Counterexample scenarios

## Synopsys Formality

### Basic Workflow

```tcl
# Set up design
read_verilog -r design_a.v
set_top r:/WORK/module_a

read_verilog -i design_b.v
set_top i:/WORK/module_b

# Match designs
match

# Verify equivalence
verify

# Report results
report_failing_points
report_aborted_points
```

### With Assumptions

```tcl
# Clock and reset assumptions
set_constant r:/WORK/module_a/rst 0
set_constant i:/WORK/module_b/rst 0

# Ignore specific signals
set_dont_verify_point r:/WORK/module_a/debug_signal

# Match and verify
match
verify
```

### Analyzing Counterexamples

```tcl
# Generate counterexample
set verification_failing_point_limit 1
verify

# Analyze failing point
analyze_points -failing

# Generate waveform
report_verification -format vcd -file counterexample.vcd
```

## Cadence Conformal

### Basic Workflow

```tcl
# Read designs
read design -golden design_a.v -verilog
read design -revised design_b.v -verilog

# Set root modules
set root module golden_module -golden
set root module revised_module -revised

# Map key points
add mapped points -all

# Run LEC
compare

# Report
report verification
report compare data
```

### With Constraints

```tcl
# Add constraints
add pin constraints 0 rst -both

# Ignore specific logic
set ignore outputs debug_* -both

# Compare
compare
```

### Debug Non-Equivalence

```tcl
# Analyze failing points
analyze datapath -failing

# Generate counterexample
diagnose -failing

# Create waveform
create testbench -failing -file counterexample.v
```

## Yosys (Open Source)

### Basic Equivalence Check

```tcl
# Read designs
read_verilog design_a.v
prep -top module_a
design -stash gold

read_verilog design_b.v
prep -top module_b
design -stash gate

# Equivalence check
design -copy-from gold -as gold module_a
design -copy-from gate -as gate module_b

equiv_make gold gate equiv
equiv_simple
equiv_status
```

### With SAT-based Verification

```tcl
# Use SAT solver for equivalence
equiv_make gold gate equiv
equiv_simple
equiv_induct
equiv_status -assert
```

## Interpreting Results

### Equivalent Designs

**Formality:**
```
Verification SUCCEEDED
  Matched points: 100%
  Verified points: 100%
```

**Conformal:**
```
Compare Results:
  Equivalent: 100%
  Non-equivalent: 0%
```

### Non-Equivalent Designs

**Formality:**
```
Verification FAILED
  Failing points: 5
  Aborted points: 0

Failing Points:
  output_signal: NOT EQUIVALENT
```

**Conformal:**
```
Compare Results:
  Equivalent: 95%
  Non-equivalent: 5%

Non-equivalent Points:
  output_signal: DIFFERENT
```

### Aborted/Unknown

**Formality:**
```
Verification ABORTED
  Aborted points: 3
  Reason: Complexity timeout
```

**Conformal:**
```
Compare Results:
  Equivalent: 90%
  Abort: 10%

Aborted Points:
  complex_signal: ABORT (timeout)
```

## Common Assumptions

### Clock Assumptions

```tcl
# Formality
set_constant r:/WORK/top/clk 0 -type clock

# Conformal
add clock clk -both
```

### Reset Assumptions

```tcl
# Formality - assume reset inactive
set_constant r:/WORK/top/rst 0
set_constant i:/WORK/top/rst 0

# Conformal - constrain reset
add pin constraints 0 rst -both
```

### State Encoding

```tcl
# Formality - abstract state encoding
set_encoding_style r:/WORK/top/state_reg -auto
set_encoding_style i:/WORK/top/state_reg -auto

# Conformal - map states
add state mapping state_reg -golden state_reg -revised
```

### Ignoring Signals

```tcl
# Formality
set_dont_verify_point r:/WORK/top/debug_*

# Conformal
set ignore outputs debug_* -both
```

## Debugging Strategies

### 1. Start Simple

- Verify small modules first
- Build up to full design
- Isolate problematic blocks

### 2. Use Constraints

- Add clock/reset assumptions
- Constrain unused inputs
- Abstract state encodings

### 3. Analyze Counterexamples

- Generate waveforms
- Trace signal values
- Identify root cause

### 4. Incremental Verification

- Verify submodules independently
- Use hierarchical approach
- Leverage proven equivalences

## Integration with This Skill

The RTL Equivalence Checker skill provides:

1. **Pre-analysis** - Identifies differences before running formal tools
2. **Guidance** - Suggests which assumptions to use
3. **Counterexample hints** - Provides test scenarios to try
4. **Plain language explanation** - Interprets formal tool results

### Workflow

1. Run this skill's checker:
   ```bash
   python3 scripts/check_equivalence.py design_a.v design_b.v
   ```

2. Review analysis:
   - Check alignment results
   - Identify semantic differences
   - Note suggested assumptions

3. Run formal tool with appropriate constraints:
   ```tcl
   # Use assumptions from skill analysis
   set_constant rst 0
   match
   verify
   ```

4. Compare results:
   - Skill analysis vs. formal tool results
   - Validate counterexamples
   - Refine assumptions if needed

## Tips

- **Use both approaches** - Skill analysis + formal tools
- **Start with skill analysis** - Faster, identifies obvious issues
- **Use formal tools for proof** - Rigorous verification
- **Iterate assumptions** - Refine based on results
- **Document assumptions** - Critical for understanding equivalence
