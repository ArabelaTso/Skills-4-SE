# SystemVerilog Assertions (SVA) Quick Reference

## Basic Assertion Structure

```systemverilog
property property_name;
  @(posedge clk) disable iff (rst)
    antecedent |-> consequent;
endproperty

assert_name: assert property (property_name)
  else $error("Assertion failed: description");
```

## Temporal Operators

### Implication Operators

- **`|->` (Overlapping implication)**: Consequent checked in same cycle
  ```systemverilog
  @(posedge clk) req |-> gnt;  // If req, then gnt in same cycle
  ```

- **`|=>` (Non-overlapping implication)**: Consequent checked next cycle
  ```systemverilog
  @(posedge clk) req |=> gnt;  // If req, then gnt in next cycle
  ```

### Delay Operators

- **`##n` (Fixed delay)**: Exactly n cycles later
  ```systemverilog
  @(posedge clk) req |-> ##3 ack;  // ack exactly 3 cycles after req
  ```

- **`##[m:n]` (Range delay)**: Between m and n cycles later
  ```systemverilog
  @(posedge clk) req |-> ##[1:5] ack;  // ack within 1-5 cycles
  ```

- **`##[0:$]` (Eventual)**: Eventually (unbounded)
  ```systemverilog
  @(posedge clk) req |-> ##[0:$] ack;  // ack eventually
  ```

### Repetition Operators

- **`[*n]` (Consecutive repetition)**: Signal true for n consecutive cycles
  ```systemverilog
  @(posedge clk) busy[*3] |=> done;  // busy for 3 cycles, then done
  ```

- **`[*m:n]` (Range repetition)**: Signal true for m to n consecutive cycles
  ```systemverilog
  @(posedge clk) busy[*1:5] |=> done;  // busy for 1-5 cycles
  ```

- **`[->n]` (Goto repetition)**: Signal true n times (not necessarily consecutive)
  ```systemverilog
  @(posedge clk) req[->3] |=> done;  // req occurs 3 times total
  ```

- **`[=n]` (Non-consecutive repetition)**: Signal true n times, match at last occurrence
  ```systemverilog
  @(posedge clk) req[=3] |=> done;  // after 3rd req occurrence
  ```

### Sequence Operators

- **`and` (Sequence conjunction)**: Both sequences must match
  ```systemverilog
  (seq1 and seq2)
  ```

- **`or` (Sequence disjunction)**: Either sequence must match
  ```systemverilog
  (seq1 or seq2)
  ```

- **`intersect` (Sequence intersection)**: Both sequences match with same length
  ```systemverilog
  (seq1 intersect seq2)
  ```

- **`throughout` (Condition throughout sequence)**: Signal must be true during entire sequence
  ```systemverilog
  enable throughout (req ##1 ack)
  ```

- **`within` (Sequence within another)**: One sequence occurs within another
  ```systemverilog
  seq1 within seq2
  ```

## System Functions

### Sampled Value Functions

- **`$past(signal, n)`**: Value of signal n cycles ago
  ```systemverilog
  @(posedge clk) valid |-> (data == $past(data, 1));
  ```

- **`$stable(signal)`**: Signal unchanged from previous cycle
  ```systemverilog
  @(posedge clk) hold |-> $stable(data);
  ```

- **`$rose(signal)`**: Signal transitioned from 0 to 1
  ```systemverilog
  @(posedge clk) $rose(req) |-> ##[1:3] ack;
  ```

- **`$fell(signal)`**: Signal transitioned from 1 to 0
  ```systemverilog
  @(posedge clk) $fell(busy) |-> done;
  ```

### Bit Vector Functions

- **`$onehot(vector)`**: Exactly one bit is high
  ```systemverilog
  @(posedge clk) $onehot(grant);
  ```

- **`$onehot0(vector)`**: At most one bit is high
  ```systemverilog
  @(posedge clk) $onehot0(grant);
  ```

- **`$isunknown(signal)`**: Signal contains X or Z
  ```systemverilog
  @(posedge clk) !$isunknown(data);
  ```

- **`$countones(vector)`**: Number of high bits
  ```systemverilog
  @(posedge clk) $countones(grant) <= 1;
  ```

## Property Types

### Safety Properties
Properties that assert "bad things never happen"

```systemverilog
// Example: Mutual exclusion
property mutex;
  @(posedge clk) !(req_a && req_b);
endproperty
```

### Liveness Properties
Properties that assert "good things eventually happen"

```systemverilog
// Example: Request eventually granted
property eventual_grant;
  @(posedge clk) req |-> strong(##[0:$] gnt);
endproperty
```

Note: Use `strong()` for liveness to ensure property holds even at end of simulation.

### Fairness Properties
Properties that assert repeated opportunities

```systemverilog
// Example: Fair arbitration
property fair_arb;
  @(posedge clk) req[*3] |-> ##[0:10] gnt;
endproperty
```

## Assertion Directives

### Assert
Check property holds (design verification)
```systemverilog
assert_name: assert property (@(posedge clk) property_expr)
  else $error("Assertion failed");
```

### Assume
Assume property holds (environment constraint)
```systemverilog
assume_name: assume property (@(posedge clk) property_expr);
```

### Cover
Check if property can be satisfied (reachability)
```systemverilog
cover_name: cover property (@(posedge clk) property_expr);
```

## Common Patterns

### Stability Check
```systemverilog
property data_stable;
  @(posedge clk) (valid && !ready) |=> $stable(data);
endproperty
```

### Bounded Response
```systemverilog
property bounded_response;
  @(posedge clk) req |-> ##[1:MAX_DELAY] ack;
endproperty
```

### Mutual Exclusion
```systemverilog
property mutex;
  @(posedge clk) !(sig_a && sig_b);
endproperty
```

### One-Hot Check
```systemverilog
property onehot_state;
  @(posedge clk) $onehot(state);
endproperty
```

### Handshake Protocol
```systemverilog
property handshake;
  @(posedge clk) (valid && !ready) |=> valid;
endproperty
```

### Reset Behavior
```systemverilog
property reset_state;
  @(posedge clk) rst |=> (state == IDLE);
endproperty
```

## Disable Conditions

Use `disable iff` for reset or other global conditions:

```systemverilog
property prop_with_reset;
  @(posedge clk) disable iff (rst)
    req |-> ##[1:5] ack;
endproperty
```

## Vacuous Success

Be careful of vacuous success (antecedent never true):

```systemverilog
// Bad: May never trigger
property may_be_vacuous;
  @(posedge clk) rare_condition |-> result;
endproperty

// Better: Add cover to check antecedent
cover_antecedent: cover property (@(posedge clk) rare_condition);
```
