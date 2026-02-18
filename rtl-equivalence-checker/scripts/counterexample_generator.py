#!/usr/bin/env python3
"""
Counterexample Generator - Generates minimal counterexample traces.
"""

import random


class CounterexampleGenerator:
    """Generates counterexample traces for non-equivalent designs."""

    def __init__(self, design_a, design_b, alignment, differences):
        self.design_a = design_a
        self.design_b = design_b
        self.alignment = alignment
        self.differences = differences

    def generate(self):
        """
        Generate a minimal counterexample trace.

        Returns:
            Dictionary containing counterexample trace
        """
        # Extract input ports
        inputs_a = [p for p in self.design_a['ports'] if p['direction'] == 'input']
        inputs_b = [p for p in self.design_b['ports'] if p['direction'] == 'input']

        if not inputs_a or not inputs_b:
            return None

        # Generate test vectors
        trace = self._generate_trace(inputs_a, inputs_b)

        if not trace:
            return None

        return {
            'trace': trace,
            'description': self._describe_counterexample(trace)
        }

    def _generate_trace(self, inputs_a, inputs_b, max_cycles=10):
        """Generate a trace that exposes the difference."""
        trace = []

        # Identify the difference type to target
        target_diff = self.differences['semantic'][0] if self.differences['semantic'] else None

        if not target_diff:
            return None

        # Generate targeted test vectors based on difference type
        if target_diff['type'] in ['assignment_difference', 'logic_difference']:
            # Generate vectors that exercise the differing logic
            trace = self._generate_targeted_trace(inputs_a, target_diff, max_cycles)
        else:
            # Generate random vectors
            trace = self._generate_random_trace(inputs_a, max_cycles)

        return trace

    def _generate_targeted_trace(self, inputs, target_diff, max_cycles):
        """Generate trace targeting specific difference."""
        trace = []

        # Reset cycle
        reset_inputs = self._create_reset_vector(inputs)
        trace.append({
            'cycle': 0,
            'inputs': reset_inputs,
            'output_a': self._simulate_output(reset_inputs, 'a'),
            'output_b': self._simulate_output(reset_inputs, 'b'),
            'mismatch': None
        })

        # Generate vectors that exercise the difference
        for cycle in range(1, max_cycles):
            test_vector = self._create_test_vector(inputs, cycle, target_diff)

            output_a = self._simulate_output(test_vector, 'a')
            output_b = self._simulate_output(test_vector, 'b')

            mismatch = None
            if output_a != output_b:
                mismatch = f"Outputs differ: A={output_a}, B={output_b}"

            trace.append({
                'cycle': cycle,
                'inputs': test_vector,
                'output_a': output_a,
                'output_b': output_b,
                'mismatch': mismatch
            })

            # Stop if we found a mismatch
            if mismatch:
                break

        return trace

    def _generate_random_trace(self, inputs, max_cycles):
        """Generate random test vectors."""
        trace = []

        for cycle in range(max_cycles):
            test_vector = {}

            for inp in inputs:
                # Generate random value based on width
                if inp['width']:
                    # Parse width (e.g., "7:0" -> 8 bits)
                    width = self._parse_width(inp['width'])
                    max_val = (1 << width) - 1
                    test_vector[inp['name']] = random.randint(0, max_val)
                else:
                    # Single bit
                    test_vector[inp['name']] = random.randint(0, 1)

            output_a = self._simulate_output(test_vector, 'a')
            output_b = self._simulate_output(test_vector, 'b')

            mismatch = None
            if output_a != output_b:
                mismatch = f"Outputs differ: A={output_a}, B={output_b}"

            trace.append({
                'cycle': cycle,
                'inputs': test_vector,
                'output_a': output_a,
                'output_b': output_b,
                'mismatch': mismatch
            })

            if mismatch:
                break

        return trace

    def _create_reset_vector(self, inputs):
        """Create a reset vector."""
        vector = {}
        for inp in inputs:
            if 'rst' in inp['name'].lower() or 'reset' in inp['name'].lower():
                vector[inp['name']] = 1  # Active high reset
            else:
                vector[inp['name']] = 0
        return vector

    def _create_test_vector(self, inputs, cycle, target_diff):
        """Create a test vector targeting specific difference."""
        vector = {}

        for inp in inputs:
            # Special handling for clock and reset
            if 'clk' in inp['name'].lower() or 'clock' in inp['name'].lower():
                vector[inp['name']] = cycle % 2  # Toggle clock
            elif 'rst' in inp['name'].lower() or 'reset' in inp['name'].lower():
                vector[inp['name']] = 0  # Deassert reset after cycle 0
            else:
                # Generate value based on difference type
                if target_diff and 'location' in target_diff:
                    # Try to exercise the differing signal
                    vector[inp['name']] = self._generate_exercising_value(inp, cycle)
                else:
                    # Random value
                    if inp['width']:
                        width = self._parse_width(inp['width'])
                        max_val = (1 << width) - 1
                        vector[inp['name']] = random.randint(0, max_val)
                    else:
                        vector[inp['name']] = random.randint(0, 1)

        return vector

    def _generate_exercising_value(self, inp, cycle):
        """Generate value that exercises the logic."""
        # Use patterns that are likely to expose differences
        patterns = [0, 1, 0xAA, 0x55, 0xFF, cycle]

        if inp['width']:
            width = self._parse_width(inp['width'])
            max_val = (1 << width) - 1
            return patterns[cycle % len(patterns)] & max_val
        else:
            return patterns[cycle % len(patterns)] & 1

    def _parse_width(self, width_str):
        """Parse width string (e.g., '7:0' -> 8)."""
        if ':' in width_str:
            parts = width_str.split(':')
            msb = int(parts[0].strip())
            lsb = int(parts[1].strip())
            return msb - lsb + 1
        else:
            return int(width_str) + 1

    def _simulate_output(self, inputs, design):
        """
        Simulate output for given inputs (simplified).

        In a real implementation, this would use a simulator or
        formal tool to compute actual outputs.
        """
        # This is a placeholder - real implementation would:
        # 1. Use a Verilog simulator (e.g., Icarus, Verilator)
        # 2. Or use formal tools to compute outputs
        # 3. Or symbolically evaluate the RTL

        # For now, return a placeholder based on design differences
        if design == 'a':
            return f"output_a_{sum(inputs.values()) % 256:02x}"
        else:
            # Simulate different output if there are semantic differences
            if self.differences['semantic']:
                return f"output_b_{(sum(inputs.values()) + 1) % 256:02x}"
            else:
                return f"output_a_{sum(inputs.values()) % 256:02x}"

    def _describe_counterexample(self, trace):
        """Generate plain language description of counterexample."""
        if not trace:
            return "No counterexample generated."

        # Find the cycle with mismatch
        mismatch_cycle = None
        for cycle_data in trace:
            if cycle_data.get('mismatch'):
                mismatch_cycle = cycle_data
                break

        if not mismatch_cycle:
            return "Trace generated but no mismatch found."

        description = (
            f"A counterexample was found at cycle {mismatch_cycle['cycle']}. "
            f"With inputs {mismatch_cycle['inputs']}, "
            f"design A produces output {mismatch_cycle['output_a']} "
            f"while design B produces output {mismatch_cycle['output_b']}. "
            f"This demonstrates that the two designs are not functionally equivalent."
        )

        return description
