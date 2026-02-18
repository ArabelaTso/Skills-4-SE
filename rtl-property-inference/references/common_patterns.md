# Common RTL Patterns and Properties

## Valid-Ready Handshake Patterns

### Basic Valid-Ready Protocol
```systemverilog
// Pattern: valid-ready handshake
// Signals: valid, ready, data
```

**Properties:**
- **P1: Data stability**: When valid is asserted and ready is not, data must remain stable
  ```systemverilog
  property data_stable;
    @(posedge clk) (valid && !ready) |=> $stable(data);
  endproperty
  ```

- **P2: Valid persistence**: Valid must remain high until handshake completes
  ```systemverilog
  property valid_persist;
    @(posedge clk) (valid && !ready) |=> valid;
  endproperty
  ```

- **P3: No data loss**: Once valid is asserted, transaction must eventually complete
  ```systemverilog
  property no_data_loss;
    @(posedge clk) valid |-> strong(##[0:$] (valid && ready));
  endproperty
  ```

### Credit-Based Flow Control
```systemverilog
// Pattern: credit counter
// Signals: send, credit_count
```

**Properties:**
- **P1: Credit bounds**: Credit count never goes negative
  ```systemverilog
  property credit_nonnegative;
    @(posedge clk) credit_count >= 0;
  endproperty
  ```

## State Machine Patterns

### One-Hot Encoding
```systemverilog
// Pattern: one-hot state machine
// Signals: state[N-1:0]
```

**Properties:**
- **P1: One-hot invariant**: Exactly one bit is high
  ```systemverilog
  property onehot_check;
    @(posedge clk) $onehot(state);
  endproperty
  ```

- **P2: Valid states**: State is never all zeros
  ```systemverilog
  property state_not_zero;
    @(posedge clk) state != 0;
  endproperty
  ```

### Binary Encoding
```systemverilog
// Pattern: binary-encoded state machine
// Signals: state[N-1:0]
```

**Properties:**
- **P1: Valid state range**: State is within defined range
  ```systemverilog
  property valid_state_range;
    @(posedge clk) state inside {[0:MAX_STATE]};
  endproperty
  ```

## Mutual Exclusion Patterns

### Grant Signals
```systemverilog
// Pattern: arbiter with multiple grants
// Signals: grant[N-1:0]
```

**Properties:**
- **P1: Mutual exclusion**: At most one grant is active
  ```systemverilog
  property mutex_grants;
    @(posedge clk) $onehot0(grant);
  endproperty
  ```

- **P2: Request-grant relationship**: Grant implies corresponding request
  ```systemverilog
  property grant_needs_request;
    @(posedge clk) grant[i] |-> request[i];
  endproperty
  ```

### Enable Signals
```systemverilog
// Pattern: mutually exclusive enables
// Signals: enable_a, enable_b
```

**Properties:**
- **P1: Mutual exclusion**: Both enables never active simultaneously
  ```systemverilog
  property mutex_enables;
    @(posedge clk) !(enable_a && enable_b);
  endproperty
  ```

## Pipeline Patterns

### Simple Pipeline Stage
```systemverilog
// Pattern: pipeline with valid bits
// Signals: valid_stage[N-1:0], data_stage[N-1:0]
```

**Properties:**
- **P1: Valid propagation**: Valid propagates through stages
  ```systemverilog
  property valid_propagation;
    @(posedge clk) valid_stage[i] |=> valid_stage[i+1];
  endproperty
  ```

- **P2: Data stability**: Data stable when valid is high
  ```systemverilog
  property data_stable_when_valid;
    @(posedge clk) valid_stage[i] |=> $stable(data_stage[i]);
  endproperty
  ```

### Pipeline with Stall
```systemverilog
// Pattern: pipeline with stall signal
// Signals: stall, valid_stage[N-1:0]
```

**Properties:**
- **P1: Stall freezes pipeline**: When stalled, valid bits don't change
  ```systemverilog
  property stall_freezes;
    @(posedge clk) stall |=> $stable(valid_stage);
  endproperty
  ```

## FIFO Patterns

### FIFO with Full/Empty
```systemverilog
// Pattern: FIFO buffer
// Signals: full, empty, wr_en, rd_en, count
```

**Properties:**
- **P1: Full prevents write**: Cannot write when full
  ```systemverilog
  property no_write_when_full;
    @(posedge clk) full |-> !wr_en;
  endproperty
  ```

- **P2: Empty prevents read**: Cannot read when empty
  ```systemverilog
  property no_read_when_empty;
    @(posedge clk) empty |-> !rd_en;
  endproperty
  ```

- **P3: Count bounds**: Count is within valid range
  ```systemverilog
  property count_in_range;
    @(posedge clk) count inside {[0:DEPTH]};
  endproperty
  ```

- **P4: Full-empty mutual exclusion**: Cannot be both full and empty (unless depth=1)
  ```systemverilog
  property full_empty_mutex;
    @(posedge clk) !(full && empty) || (DEPTH == 1);
  endproperty
  ```

## Memory Access Patterns

### Read-Write Conflict
```systemverilog
// Pattern: memory with read/write ports
// Signals: rd_en, wr_en, rd_addr, wr_addr
```

**Properties:**
- **P1: No simultaneous read-write to same address**: Avoid undefined behavior
  ```systemverilog
  property no_rw_conflict;
    @(posedge clk) (rd_en && wr_en) |-> (rd_addr != wr_addr);
  endproperty
  ```

## Reset Patterns

### Synchronous Reset
```systemverilog
// Pattern: synchronous reset
// Signals: rst, state variables
```

**Properties:**
- **P1: Reset initialization**: Reset forces known state
  ```systemverilog
  property reset_init;
    @(posedge clk) rst |=> (state == IDLE);
  endproperty
  ```

### Asynchronous Reset
```systemverilog
// Pattern: asynchronous reset
// Signals: rst_n (active low)
```

**Properties:**
- **P1: Async reset effect**: Reset immediately forces state
  ```systemverilog
  property async_reset_effect;
    @(posedge clk or negedge rst_n) !rst_n |-> (state == IDLE);
  endproperty
  ```

## Counter Patterns

### Saturating Counter
```systemverilog
// Pattern: counter with saturation
// Signals: count, inc, dec, MAX_VAL
```

**Properties:**
- **P1: Upper bound**: Counter never exceeds maximum
  ```systemverilog
  property count_upper_bound;
    @(posedge clk) count <= MAX_VAL;
  endproperty
  ```

- **P2: Lower bound**: Counter never goes negative
  ```systemverilog
  property count_lower_bound;
    @(posedge clk) count >= 0;
  endproperty
  ```

### Wraparound Counter
```systemverilog
// Pattern: counter with wraparound
// Signals: count, inc, MAX_VAL
```

**Properties:**
- **P1: Wraparound behavior**: Counter wraps at maximum
  ```systemverilog
  property count_wraparound;
    @(posedge clk) (count == MAX_VAL && inc) |=> (count == 0);
  endproperty
  ```
