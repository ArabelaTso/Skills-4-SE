#!/usr/bin/env python3
"""
Parse TLC counterexample traces and extract violation information.

This script parses TLC model checker output to extract:
- Violated property/invariant
- State trace leading to violation
- Variable values at each state
"""

import re
import sys
import json
from typing import List, Dict, Any, Optional


def parse_tlc_trace(trace_content: str) -> Dict[str, Any]:
    """
    Parse TLC trace output and extract structured violation information.

    Args:
        trace_content: Raw TLC trace output as string

    Returns:
        Dictionary containing:
        - violation_type: Type of violation (invariant, temporal, deadlock, etc.)
        - property: The violated property/invariant
        - states: List of states in the counterexample trace
        - error_message: Original error message
    """
    result = {
        "violation_type": None,
        "property": None,
        "states": [],
        "error_message": None
    }

    # Extract error message
    error_match = re.search(r'Error: (.+?)(?:\n|$)', trace_content)
    if error_match:
        result["error_message"] = error_match.group(1).strip()

    # Detect violation type
    if "Invariant" in trace_content and "is violated" in trace_content:
        result["violation_type"] = "invariant"
        inv_match = re.search(r'Invariant\s+(\w+)\s+is violated', trace_content)
        if inv_match:
            result["property"] = inv_match.group(1)
    elif "Deadlock reached" in trace_content:
        result["violation_type"] = "deadlock"
        result["property"] = "Deadlock"
    elif "Temporal properties" in trace_content:
        result["violation_type"] = "temporal"
        temp_match = re.search(r'Temporal property\s+(\w+)', trace_content)
        if temp_match:
            result["property"] = temp_match.group(1)

    # Parse state trace
    state_pattern = re.compile(r'State\s+(\d+):\s*<([^>]+)>(.*?)(?=State\s+\d+:|$)', re.DOTALL)
    states = state_pattern.findall(trace_content)

    for state_num, state_type, state_content in states:
        state_vars = {}

        # Parse variable assignments in the state
        var_pattern = re.compile(r'/\\\\s*(\w+)\s*=\s*(.+?)(?=\n/\\\\|\n\n|$)', re.DOTALL)
        for var_name, var_value in var_pattern.findall(state_content):
            state_vars[var_name.strip()] = var_value.strip()

        result["states"].append({
            "number": int(state_num),
            "type": state_type.strip(),
            "variables": state_vars
        })

    return result


def format_trace_summary(parsed_trace: Dict[str, Any]) -> str:
    """Format parsed trace into human-readable summary."""
    lines = []
    lines.append(f"Violation Type: {parsed_trace['violation_type']}")
    lines.append(f"Violated Property: {parsed_trace['property']}")
    lines.append(f"Error: {parsed_trace['error_message']}")
    lines.append(f"\nTrace Length: {len(parsed_trace['states'])} states")
    lines.append("\nState Trace:")

    for state in parsed_trace['states']:
        lines.append(f"\n  State {state['number']} ({state['type']}):")
        for var, val in state['variables'].items():
            lines.append(f"    {var} = {val}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_tlc_trace.py <trace_file>")
        print("   or: parse_tlc_trace.py --json <trace_file>")
        sys.exit(1)

    output_json = False
    trace_file = sys.argv[1]

    if sys.argv[1] == "--json":
        output_json = True
        trace_file = sys.argv[2] if len(sys.argv) > 2 else None
        if not trace_file:
            print("Error: trace file required")
            sys.exit(1)

    try:
        with open(trace_file, 'r') as f:
            trace_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{trace_file}' not found")
        sys.exit(1)

    parsed = parse_tlc_trace(trace_content)

    if output_json:
        print(json.dumps(parsed, indent=2))
    else:
        print(format_trace_summary(parsed))


if __name__ == "__main__":
    main()
