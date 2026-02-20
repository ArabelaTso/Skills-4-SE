# Common Specification-RTL Violations

## Functional Violations

### Missing State Transitions

**Specification:**
"System transitions from IDLE to BUSY when start=1, and from BUSY to DONE when complete=1"

**Violation Example:**
```verilog
case (state)
    IDLE: if (start) next_state = BUSY;
    BUSY: next_state = BUSY;  // Missing transition to DONE!
    DONE: next_state = IDLE;
endcase
```

**Detection:**
- Check all specified transitions exist in RTL
- Verify transition conditions match specification

**Fix:**
```verilog
case (state)
    IDLE: if (start) next_state = BUSY;
    BUSY: if (complete) next_state = DONE;  // Added missing transition
    DONE: next_state = IDLE;
endcase
```

### Incorrect Transition Conditions

**Specification:**
"Transition to ERROR state if timeout occurs OR invalid input received"

**Violation Example:**
```verilog
if (timeout && invalid_input)  // Should be OR, not AND
    next_state = ERROR;
```

**Detection:**
- Compare boolean conditions in spec vs RTL
- Check for AND/OR mismatches

**Fix:**
```verilog
if (timeout || invalid_input)  // Corrected to OR
    next_state = ERROR;
```

### Missing Edge Cases

**Specification:**
"Counter increments on each clock cycle, saturates at MAX_VALUE"

**Violation Example:**
```verilog
always @(posedge clk) begin
    counter <= counter + 1;  // No saturation logic!
end
```

**Detection:**
- Check boundary conditions
- Verify overflow/underflow handling

**Fix:**
```verilog
always @(posedge clk) begin
    if (counter < MAX_VALUE)
        counter <= counter + 1;
    // Saturates at MAX_VALUE
end
```

### Wrong Default Values

**Specification:**
"Output defaults to 0 when not explicitly set"

**Violation Example:**
```verilog
always @(*) begin
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        // No default → latches previous value
    endcase
end
```

**Detection:**
- Check for default assignments
- Verify reset values match spec

**Fix:**
```verilog
always @(*) begin
    out = 0;  // Default value
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
    endcase
end
```

## Protocol Violations

### Handshake Protocol Errors

**Specification:**
"Data must remain stable while valid=1 until ready=1"

**Violation Example:**
```verilog
always @(posedge clk) begin
    if (has_new_data) begin
        valid <= 1;
        data <= new_data;  // Data changes even if previous not accepted!
    end
end
```

**Detection:**
- Trace data signal when valid=1 and ready=0
- Check if data changes

**Fix:**
```verilog
always @(posedge clk) begin
    if (!valid || ready) begin  // Only update when transfer completes
        if (has_new_data) begin
            valid <= 1;
            data <= new_data;
        end else begin
            valid <= 0;
        end
    end
    // Else hold data stable
end
```

### Missing Acknowledgment

**Specification:**
"Request must be acknowledged before next request"

**Violation Example:**
```verilog
always @(posedge clk) begin
    if (need_request) begin
        request <= 1;  // Can send multiple requests without ack!
    end
end
```

**Detection:**
- Check if request can be asserted multiple times
- Verify acknowledgment is checked

**Fix:**
```verilog
always @(posedge clk) begin
    if (need_request && !request) begin
        request <= 1;
    end else if (acknowledge) begin
        request <= 0;
    end
end
```

### Out-of-Order Operations

**Specification:**
"Write must complete before read can start"

**Violation Example:**
```verilog
// Write and read can happen simultaneously
assign write_en = wr_req;
assign read_en = rd_req;
```

**Detection:**
- Check operation ordering
- Verify dependencies are enforced

**Fix:**
```verilog
always @(posedge clk) begin
    case (state)
        IDLE: if (wr_req) state <= WRITING;
        WRITING: if (wr_done) state <= IDLE;
        // Read only allowed in IDLE after write completes
    endcase
end

assign write_en = (state == WRITING);
assign read_en = (state == IDLE) && rd_req && !wr_req;
```

## Timing Violations

### Incorrect Latency

**Specification:**
"Output valid 3 cycles after input valid"

**Violation Example:**
```verilog
always @(posedge clk) begin
    stage1 <= input_data;
    stage2 <= stage1;
    output_data <= stage2;  // Only 2 cycles!
end
```

**Detection:**
- Count pipeline stages
- Trace signal through registers

**Fix:**
```verilog
always @(posedge clk) begin
    stage1 <= input_data;
    stage2 <= stage1;
    stage3 <= stage2;
    output_data <= stage3;  // Now 3 cycles
end
```

### Missing Delay

**Specification:**
"Assert output 1 cycle after input condition met"

**Violation Example:**
```verilog
assign output_signal = input_condition;  // Combinational, no delay!
```

**Detection:**
- Check if signal is registered
- Verify timing of assertion

**Fix:**
```verilog
always @(posedge clk) begin
    output_signal <= input_condition;  // 1 cycle delay
end
```

### Throughput Mismatch

**Specification:**
"Process one transaction per cycle"

**Violation Example:**
```verilog
always @(posedge clk) begin
    if (valid && ready && !busy) begin
        busy <= 1;
        // Process takes multiple cycles
    end else if (busy && done) begin
        busy <= 0;
    end
end
```

**Detection:**
- Measure cycles between transactions
- Check if pipeline is full

**Fix:**
Add pipelining to achieve 1 transaction/cycle throughput.

## Reset Violations

### Missing Reset

**Specification:**
"All state must reset to known values"

**Violation Example:**
```verilog
always @(posedge clk) begin
    if (!rst_n) begin
        state <= IDLE;
        // counter not reset!
    end else begin
        counter <= counter + 1;
    end
end
```

**Detection:**
- Check all registers in reset block
- Verify all state is initialized

**Fix:**
```verilog
always @(posedge clk) begin
    if (!rst_n) begin
        state <= IDLE;
        counter <= 0;  // Added reset
    end else begin
        counter <= counter + 1;
    end
end
```

### Wrong Reset Value

**Specification:**
"Counter resets to 10"

**Violation Example:**
```verilog
if (!rst_n)
    counter <= 0;  // Should be 10!
```

**Detection:**
- Compare reset values in spec vs RTL

**Fix:**
```verilog
if (!rst_n)
    counter <= 10;  // Correct reset value
```

### Incomplete Reset

**Specification:**
"Synchronous reset for all logic"

**Violation Example:**
```verilog
always @(posedge clk or negedge rst_n) begin  // Async reset!
    if (!rst_n)
        state <= IDLE;
    elsif rising_edge(clk)
        // ...
end
```

**Detection:**
- Check reset style (sync vs async)
- Verify consistency across design

**Fix:**
```verilog
always @(posedge clk) begin  // Synchronous reset
    if (!rst_n)
        state <= IDLE;
    else
        // ...
end
```

## Data Path Violations

### Wrong Data Width

**Specification:**
"Data bus is 32 bits wide"

**Violation Example:**
```verilog
reg [15:0] data_bus;  // Only 16 bits!
```

**Detection:**
- Compare signal widths
- Check for truncation

**Fix:**
```verilog
reg [31:0] data_bus;  // Correct width
```

### Missing Data Validation

**Specification:**
"Input data must be validated before use"

**Violation Example:**
```verilog
always @(posedge clk) begin
    result <= input_data + offset;  // No validation!
end
```

**Detection:**
- Check for validation logic
- Verify error handling

**Fix:**
```verilog
always @(posedge clk) begin
    if (input_valid && input_data < MAX_VALUE) begin
        result <= input_data + offset;
        error <= 0;
    end else begin
        error <= 1;
    end
end
```

### Incorrect Arithmetic

**Specification:**
"Calculate average of two inputs: (A + B) / 2"

**Violation Example:**
```verilog
assign average = (A + B) >> 1;  // Overflow if A+B > max!
```

**Detection:**
- Check arithmetic operations
- Verify overflow handling

**Fix:**
```verilog
wire [WIDTH:0] sum = {1'b0, A} + {1'b0, B};  // Extra bit for overflow
assign average = sum[WIDTH:1];  // Divide by 2
```

## Control Flow Violations

### Missing Priority

**Specification:**
"Error condition has highest priority"

**Violation Example:**
```verilog
if (normal_req) next_state = PROCESS;
else if (error) next_state = ERROR;  // Error checked last!
```

**Detection:**
- Check condition ordering
- Verify priority matches spec

**Fix:**
```verilog
if (error) next_state = ERROR;  // Error checked first
else if (normal_req) next_state = PROCESS;
```

### Unreachable States

**Specification:**
"System has states: IDLE, BUSY, DONE"

**Violation Example:**
```verilog
case (state)
    IDLE: next_state = BUSY;
    BUSY: next_state = BUSY;  // Can never reach DONE!
    DONE: next_state = IDLE;
endcase
```

**Detection:**
- Analyze state reachability
- Check for dead states

**Fix:**
Add proper transition to DONE state.

### Deadlock Conditions

**Specification:**
"System must always make progress"

**Violation Example:**
```verilog
case (state)
    WAIT_A: if (signal_b) next_state = WAIT_B;
    WAIT_B: if (signal_a) next_state = WAIT_A;
    // Deadlock if both signals false!
endcase
```

**Detection:**
- Check for circular wait conditions
- Verify progress guarantees

**Fix:**
Add timeout or alternative exit path.

## Underspecified Scenarios

### Ambiguous Behavior

**Specification:**
"Output updates when input changes"

**Issue:**
- Does it update immediately (combinational)?
- Does it update on next clock (registered)?
- What if input changes multiple times in one cycle?

**Resolution Needed:**
Clarify timing and update mechanism in specification.

### Missing Corner Cases

**Specification:**
"Increment counter on enable"

**Issue:**
- What happens at maximum value?
- Wrap around or saturate?
- Generate overflow flag?

**Resolution Needed:**
Specify boundary behavior explicitly.

### Undefined Initial State

**Specification:**
"State machine with states A, B, C"

**Issue:**
- What is the initial state?
- How does system enter initial state?

**Resolution Needed:**
Specify reset behavior and initial state.

## Uncheckable Scenarios

### Missing Environmental Assumptions

**Specification:**
"Process input when valid signal asserted"

**Issue:**
- How long does valid stay asserted?
- Can valid be asserted back-to-back?
- What is maximum valid duration?

**Needed:**
Environmental constraints or assumptions about input behavior.

### External Dependencies

**Specification:**
"Interface with external memory controller"

**Issue:**
- Memory controller behavior not specified
- Timing of memory responses unknown
- Error conditions not defined

**Needed:**
External component specifications or interface protocol definition.

### Incomplete Timing Information

**Specification:**
"Fast response required"

**Issue:**
- How fast is "fast"?
- Measured in cycles or time?
- Under what conditions?

**Needed:**
Quantitative timing requirements with units and conditions.
