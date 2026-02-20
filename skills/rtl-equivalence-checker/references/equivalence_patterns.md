# Verilog Equivalence Checking Patterns

Common patterns and scenarios in RTL equivalence checking.

## Pattern 1: Cosmetic Refactoring

### Signal Renaming

**Version A:**
```verilog
module counter(
    input clk,
    input rst,
    output reg [7:0] cnt
);
    always @(posedge clk or posedge rst) begin
        if (rst)
            cnt <= 8'b0;
        else
            cnt <= cnt + 1;
    end
endmodule
```

**Version B:**
```verilog
module counter(
    input clk,
    input rst,
    output reg [7:0] count_value
);
    always @(posedge clk or posedge rst) begin
        if (rst)
            count_value <= 8'b0;
        else
            count_value <= count_value + 1;
    end
endmodule
```

**Analysis:** EQUIVALENT - Only signal name changed (cnt → count_value)

### Code Formatting

**Version A:**
```verilog
assign result = (a & b) | (c & d);
```

**Version B:**
```verilog
assign result = (a & b) |
                (c & d);
```

**Analysis:** EQUIVALENT - Only formatting differs

### Expression Reordering (Commutative)

**Version A:**
```verilog
assign sum = a + b + c;
```

**Version B:**
```verilog
assign sum = c + a + b;
```

**Analysis:** EQUIVALENT - Addition is commutative

## Pattern 2: Structural Refactoring

### Combining Always Blocks

**Version A:**
```verilog
always @(posedge clk) begin
    if (rst)
        reg_a <= 0;
    else
        reg_a <= in_a;
end

always @(posedge clk) begin
    if (rst)
        reg_b <= 0;
    else
        reg_b <= in_b;
end
```

**Version B:**
```verilog
always @(posedge clk) begin
    if (rst) begin
        reg_a <= 0;
        reg_b <= 0;
    end else begin
        reg_a <= in_a;
        reg_b <= in_b;
    end
end
```

**Analysis:** EQUIVALENT - Blocks combined but logic unchanged

### Splitting Combinational Logic

**Version A:**
```verilog
assign result = (a & b) | (c & d);
```

**Version B:**
```verilog
wire term1, term2;
assign term1 = a & b;
assign term2 = c & d;
assign result = term1 | term2;
```

**Analysis:** EQUIVALENT - Logic split into intermediate signals

## Pattern 3: Semantic Differences

### Different Reset Logic

**Version A:**
```verilog
always @(posedge clk or posedge rst) begin
    if (rst)
        counter <= 0;
    else
        counter <= counter + 1;
end
```

**Version B:**
```verilog
always @(posedge clk) begin
    if (rst)
        counter <= 0;
    else
        counter <= counter + 1;
end
```

**Analysis:** NOT EQUIVALENT
- Version A: Asynchronous reset (immediate)
- Version B: Synchronous reset (waits for clock)

**Counterexample:** Assert reset between clock edges - A resets immediately, B waits for next clock

### Different Arithmetic

**Version A:**
```verilog
assign result = (a + b) * 2;
```

**Version B:**
```verilog
assign result = a * 2 + b * 2;
```

**Analysis:** EQUIVALENT (mathematically) but may differ in:
- Timing (different critical paths)
- Overflow behavior (if intermediate results overflow)

### Missing Edge Case

**Version A:**
```verilog
always @(*) begin
    case (state)
        2'b00: next_state = 2'b01;
        2'b01: next_state = 2'b10;
        2'b10: next_state = 2'b11;
        2'b11: next_state = 2'b00;
    endcase
end
```

**Version B:**
```verilog
always @(*) begin
    case (state)
        2'b00: next_state = 2'b01;
        2'b01: next_state = 2'b10;
        2'b10: next_state = 2'b11;
        default: next_state = 2'b00;
    endcase
end
```

**Analysis:** EQUIVALENT - Default case handles same value (2'b11)

### Different State Encoding

**Version A:**
```verilog
parameter IDLE = 2'b00;
parameter ACTIVE = 2'b01;
parameter DONE = 2'b10;
```

**Version B:**
```verilog
parameter IDLE = 2'b00;
parameter ACTIVE = 2'b10;
parameter DONE = 2'b01;
```

**Analysis:** NOT EQUIVALENT (unless state encoding is abstracted)
- Different bit patterns for same states
- May affect downstream logic

## Pattern 4: Timing Differences

### Pipeline Depth

**Version A (1 cycle):**
```verilog
always @(posedge clk) begin
    result <= a + b;
end
```

**Version B (2 cycles):**
```verilog
always @(posedge clk) begin
    temp <= a + b;
    result <= temp;
end
```

**Analysis:** NOT EQUIVALENT
- Different latency (1 vs 2 cycles)
- Different throughput characteristics

**Counterexample:** Apply input at cycle 0, check output at cycle 1 - A has result, B doesn't

### Clock Domain Crossing

**Version A:**
```verilog
always @(posedge clk_a) begin
    data_out <= data_in;
end
```

**Version B:**
```verilog
reg sync_reg;
always @(posedge clk_b) begin
    sync_reg <= data_in;
    data_out <= sync_reg;
end
```

**Analysis:** NOT EQUIVALENT
- Different clock domains
- Version B has synchronizer (2-cycle delay)

## Pattern 5: Optimization Differences

### Constant Propagation

**Version A:**
```verilog
wire enable = 1'b1;
assign result = enable ? data : 8'b0;
```

**Version B:**
```verilog
assign result = data;
```

**Analysis:** EQUIVALENT - Constant propagation optimization

### Dead Code Elimination

**Version A:**
```verilog
always @(*) begin
    temp = a & b;
    unused = c | d;
    result = temp;
end
```

**Version B:**
```verilog
always @(*) begin
    result = a & b;
end
```

**Analysis:** EQUIVALENT (if unused is truly unused)
- Dead code removed

### Logic Minimization

**Version A:**
```verilog
assign result = (a & b) | (a & c) | (b & c);
```

**Version B:**
```verilog
assign result = (a & b) | (a & c) | (b & c);
// Could be minimized to: (a & (b | c)) | (b & c)
```

**Analysis:** EQUIVALENT - Same logic, different form

## Checking Guidelines

### When Designs Are Equivalent

1. **Signal renaming only**
2. **Code reformatting**
3. **Commutative operation reordering**
4. **Structural refactoring without logic change**
5. **Constant propagation**
6. **Dead code elimination**
7. **Logically equivalent expressions**

### When Designs Are NOT Equivalent

1. **Different reset behavior (async vs sync)**
2. **Different arithmetic operations**
3. **Missing or extra logic**
4. **Different state encodings (without abstraction)**
5. **Different pipeline depths**
6. **Different clock domains**
7. **Different edge sensitivity**
8. **Different bit widths**

### Ambiguous Cases (Require Assumptions)

1. **State encoding differences** - May be equivalent if abstracted
2. **Timing differences** - May be equivalent if latency is abstracted
3. **Optimization differences** - May be equivalent if unused signals ignored
4. **X-propagation** - May differ in simulation but equivalent in synthesis

## Counterexample Patterns

### Reset Sequence
```
Cycle 0: rst=1, clk=0
Cycle 1: rst=1, clk=1  (A resets here if async)
Cycle 2: rst=0, clk=0
Cycle 3: rst=0, clk=1  (B resets here if sync)
```

### Edge Case Input
```
Cycle 0: input = 0x00
Cycle 1: input = 0xFF  (all 1s)
Cycle 2: input = 0xAA  (alternating)
Cycle 3: input = 0x55  (alternating opposite)
```

### State Transition
```
Cycle 0: state = IDLE
Cycle 1: trigger = 1
Cycle 2: state = ACTIVE (check if both designs transition)
Cycle 3: done = 1
Cycle 4: state = DONE (check if both designs complete)
```
