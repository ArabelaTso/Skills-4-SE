# HDL-Specific Verification Patterns

## Verilog/SystemVerilog Patterns

### State Machine Patterns

#### Two-Process State Machine

**Specification:**
"Implement a state machine with states IDLE, BUSY, DONE"

**Correct RTL Pattern:**
```verilog
// State register (sequential)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= IDLE;
    else
        state <= next_state;
end

// Next state logic (combinational)
always @(*) begin
    next_state = state; // Default: stay in current state
    case (state)
        IDLE: if (start) next_state = BUSY;
        BUSY: if (done_flag) next_state = DONE;
        DONE: if (ack) next_state = IDLE;
        default: next_state = IDLE;
    endcase
end

// Output logic (combinational or registered)
always @(*) begin
    busy = (state == BUSY);
    ready = (state == IDLE);
end
```

**Common Violations:**
- Missing default case → latches inferred
- Missing default assignment → incomplete sensitivity
- Using blocking assignments in sequential block
- Incomplete state coverage

#### One-Process State Machine

```verilog
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= IDLE;
        output_reg <= 0;
    end else begin
        case (state)
            IDLE: begin
                if (start) begin
                    state <= BUSY;
                    output_reg <= 1;
                end
            end
            BUSY: begin
                if (done_flag) begin
                    state <= DONE;
                    output_reg <= 0;
                end
            end
            // ... other states
        endcase
    end
end
```

### Handshake Protocols

#### Valid-Ready Handshake

**Specification:**
"Data transfer occurs when both valid and ready are high"

**Correct Pattern:**
```verilog
// Producer side
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        valid <= 0;
        data <= 0;
    end else begin
        if (!valid || ready) begin
            // Can send new data
            if (has_data) begin
                valid <= 1;
                data <= new_data;
            end else begin
                valid <= 0;
            end
        end
        // If valid && !ready, hold data stable
    end
end

// Consumer side
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ready <= 0;
    end else begin
        ready <= can_accept_data;
    end
end

// Transfer occurs when:
wire transfer = valid && ready;
```

**Common Violations:**
- Data changes while valid=1 and ready=0
- Valid deasserted before ready asserted
- Missing backpressure handling

### FIFO Patterns

**Specification:**
"Implement a synchronous FIFO with full/empty flags"

**Correct Pattern:**
```verilog
module sync_fifo #(
    parameter DEPTH = 16,
    parameter WIDTH = 8
) (
    input wire clk,
    input wire rst_n,
    input wire wr_en,
    input wire [WIDTH-1:0] wr_data,
    input wire rd_en,
    output reg [WIDTH-1:0] rd_data,
    output wire full,
    output wire empty
);

    reg [WIDTH-1:0] mem [0:DEPTH-1];
    reg [$clog2(DEPTH):0] wr_ptr, rd_ptr;

    assign full = (wr_ptr[$clog2(DEPTH)] != rd_ptr[$clog2(DEPTH)]) &&
                  (wr_ptr[$clog2(DEPTH)-1:0] == rd_ptr[$clog2(DEPTH)-1:0]);
    assign empty = (wr_ptr == rd_ptr);

    // Write
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= 0;
        end else if (wr_en && !full) begin
            mem[wr_ptr[$clog2(DEPTH)-1:0]] <= wr_data;
            wr_ptr <= wr_ptr + 1;
        end
    end

    // Read
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_ptr <= 0;
            rd_data <= 0;
        end else if (rd_en && !empty) begin
            rd_data <= mem[rd_ptr[$clog2(DEPTH)-1:0]];
            rd_ptr <= rd_ptr + 1;
        end
    end

endmodule
```

**Common Violations:**
- Writing when full
- Reading when empty
- Incorrect full/empty flag logic
- Pointer overflow issues

### Clock Domain Crossing

**Specification:**
"Safely transfer signal from clock domain A to clock domain B"

**Correct Pattern (Two-FF Synchronizer):**
```verilog
// For single-bit signals
reg [1:0] sync_ff;

always @(posedge clk_b or negedge rst_n) begin
    if (!rst_n)
        sync_ff <= 2'b0;
    else
        sync_ff <= {sync_ff[0], signal_from_clk_a};
end

assign signal_in_clk_b = sync_ff[1];
```

**Correct Pattern (Handshake for Multi-bit):**
```verilog
// Clock domain A
always @(posedge clk_a) begin
    if (data_ready && !req) begin
        req <= 1;
        data_reg <= data;
    end else if (ack_sync) begin
        req <= 0;
    end
end

// Synchronize req to clock domain B
// ... two-FF synchronizer ...

// Clock domain B
always @(posedge clk_b) begin
    if (req_sync && !ack) begin
        ack <= 1;
        captured_data <= data_reg;
    end else if (!req_sync) begin
        ack <= 0;
    end
end
```

**Common Violations:**
- No synchronization (metastability risk)
- Single FF synchronizer (insufficient)
- Multi-bit bus without handshake
- Missing constraints in timing analysis

### Reset Patterns

**Specification:**
"All registers must have defined reset values"

**Asynchronous Reset:**
```verilog
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // All registers reset here
        state <= IDLE;
        counter <= 0;
        valid <= 0;
    end else begin
        // Normal operation
    end
end
```

**Synchronous Reset:**
```verilog
always @(posedge clk) begin
    if (!rst_n) begin
        // All registers reset here
        state <= IDLE;
        counter <= 0;
        valid <= 0;
    end else begin
        // Normal operation
    end
end
```

**Common Violations:**
- Registers missing from reset
- Inconsistent reset polarity
- Reset not reaching all flops
- Combinational logic in reset path

## VHDL Patterns

### State Machine Pattern

```vhdl
type state_type is (IDLE, BUSY, DONE);
signal state, next_state : state_type;

-- State register
process(clk, rst)
begin
    if rst = '1' then
        state <= IDLE;
    elsif rising_edge(clk) then
        state <= next_state;
    end if;
end process;

-- Next state logic
process(state, start, done_flag)
begin
    next_state <= state; -- Default
    case state is
        when IDLE =>
            if start = '1' then
                next_state <= BUSY;
            end if;
        when BUSY =>
            if done_flag = '1' then
                next_state <= DONE;
            end if;
        when DONE =>
            next_state <= IDLE;
        when others =>
            next_state <= IDLE;
    end case;
end process;
```

### FIFO Pattern

```vhdl
entity sync_fifo is
    generic (
        DEPTH : integer := 16;
        WIDTH : integer := 8
    );
    port (
        clk     : in  std_logic;
        rst     : in  std_logic;
        wr_en   : in  std_logic;
        wr_data : in  std_logic_vector(WIDTH-1 downto 0);
        rd_en   : in  std_logic;
        rd_data : out std_logic_vector(WIDTH-1 downto 0);
        full    : out std_logic;
        empty   : out std_logic
    );
end sync_fifo;

architecture rtl of sync_fifo is
    type mem_type is array (0 to DEPTH-1) of std_logic_vector(WIDTH-1 downto 0);
    signal mem : mem_type;
    signal wr_ptr, rd_ptr : integer range 0 to DEPTH-1;
    signal count : integer range 0 to DEPTH;
begin
    full <= '1' when count = DEPTH else '0';
    empty <= '1' when count = 0 else '0';

    process(clk, rst)
    begin
        if rst = '1' then
            wr_ptr <= 0;
            rd_ptr <= 0;
            count <= 0;
        elsif rising_edge(clk) then
            if wr_en = '1' and count < DEPTH then
                mem(wr_ptr) <= wr_data;
                wr_ptr <= (wr_ptr + 1) mod DEPTH;
                count <= count + 1;
            end if;

            if rd_en = '1' and count > 0 then
                rd_data <= mem(rd_ptr);
                rd_ptr <= (rd_ptr + 1) mod DEPTH;
                count <= count - 1;
            end if;
        end if;
    end process;
end rtl;
```

## Common Anti-Patterns

### Combinational Loops

**Violation:**
```verilog
assign a = b & c;
assign b = a | d;  // Creates combinational loop
```

**Fix:**
Break the loop with a register.

### Incomplete Sensitivity Lists

**Violation:**
```verilog
always @(a) begin  // Missing b in sensitivity
    out = a & b;
end
```

**Fix:**
```verilog
always @(*) begin  // Use @(*) for combinational
    out = a & b;
end
```

### Unintended Latches

**Violation:**
```verilog
always @(*) begin
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        // Missing cases → latch inferred
    endcase
end
```

**Fix:**
```verilog
always @(*) begin
    out = 0; // Default assignment
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        2'b10: out = c;
        2'b11: out = d;
    endcase
end
```

### Multiple Drivers

**Violation:**
```verilog
always @(posedge clk) begin
    if (cond1) signal <= val1;
end

always @(posedge clk) begin
    if (cond2) signal <= val2;  // Multiple drivers!
end
```

**Fix:**
Combine into single always block or use proper arbitration.

## Timing-Related Patterns

### Pipeline Stages

**Specification:**
"3-cycle latency from input to output"

**Verification:**
```verilog
// Count register stages
always @(posedge clk) begin
    stage1 <= input_data;
    stage2 <= stage1;
    stage3 <= stage2;
    output_data <= stage3;  // 3 cycles total
end
```

### Registered Outputs

**Specification:**
"All outputs must be registered"

**Check:**
- Verify all output assignments are in clocked always blocks
- No combinational paths to outputs

### Setup/Hold Requirements

**Specification:**
"Input must be stable for 2ns before clock edge"

**Verification:**
- Check timing constraints in SDC/XDC
- Verify input synchronization if from async source
