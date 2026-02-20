#!/usr/bin/env python3
"""
RTL Parser - Parses Verilog RTL designs and extracts structure.
"""

import re
from collections import defaultdict


class RTLParser:
    """Parses Verilog RTL designs."""

    def parse(self, file_path):
        """
        Parse a Verilog file and extract design structure.

        Args:
            file_path: Path to Verilog file

        Returns:
            Dictionary containing design structure
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

        # Remove comments
        content = self._remove_comments(content)

        # Extract module information
        module_info = self._extract_module(content)

        if not module_info:
            print(f"No module found in {file_path}")
            return None

        # Extract ports
        ports = self._extract_ports(content, module_info)

        # Extract signals (wires, regs)
        signals = self._extract_signals(content)

        # Extract always blocks
        always_blocks = self._extract_always_blocks(content)

        # Extract assign statements
        assigns = self._extract_assigns(content)

        # Extract state elements (registers)
        state_elements = self._extract_state_elements(always_blocks)

        return {
            'file_path': file_path,
            'module_name': module_info['name'],
            'ports': ports,
            'signals': signals,
            'always_blocks': always_blocks,
            'assigns': assigns,
            'state_elements': state_elements
        }

    def _remove_comments(self, content):
        """Remove single-line and multi-line comments."""
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content

    def _extract_module(self, content):
        """Extract module name and definition."""
        pattern = r'module\s+(\w+)\s*(?:#\s*\([^)]*\))?\s*\('
        match = re.search(pattern, content)

        if match:
            return {
                'name': match.group(1),
                'start': match.start(),
                'end': self._find_module_end(content, match.end())
            }
        return None

    def _find_module_end(self, content, start):
        """Find the end of module definition."""
        pattern = r'endmodule'
        match = re.search(pattern, content[start:])
        if match:
            return start + match.end()
        return len(content)

    def _extract_ports(self, content, module_info):
        """Extract port declarations."""
        ports = []

        # Extract from module declaration
        module_decl_pattern = r'module\s+\w+\s*(?:#\s*\([^)]*\))?\s*\((.*?)\);'
        match = re.search(module_decl_pattern, content, re.DOTALL)

        if match:
            port_list = match.group(1)

            # Parse individual ports
            port_pattern = r'(input|output|inout)\s+(?:(wire|reg)\s+)?(?:\[([^\]]+)\]\s+)?(\w+)'
            for port_match in re.finditer(port_pattern, port_list):
                direction = port_match.group(1)
                port_type = port_match.group(2) or 'wire'
                width = port_match.group(3)
                name = port_match.group(4)

                ports.append({
                    'name': name,
                    'direction': direction,
                    'type': port_type,
                    'width': width
                })

        return ports

    def _extract_signals(self, content):
        """Extract wire and reg declarations."""
        signals = []

        # Extract wire declarations
        wire_pattern = r'wire\s+(?:\[([^\]]+)\]\s+)?(\w+)'
        for match in re.finditer(wire_pattern, content):
            width = match.group(1)
            name = match.group(2)
            signals.append({
                'name': name,
                'type': 'wire',
                'width': width
            })

        # Extract reg declarations
        reg_pattern = r'reg\s+(?:\[([^\]]+)\]\s+)?(\w+)'
        for match in re.finditer(reg_pattern, content):
            width = match.group(1)
            name = match.group(2)
            signals.append({
                'name': name,
                'type': 'reg',
                'width': width
            })

        return signals

    def _extract_always_blocks(self, content):
        """Extract always blocks."""
        always_blocks = []

        pattern = r'always\s*@\s*\(([^)]+)\)\s*(begin)?(.*?)(end)?(?=\s*(?:always|assign|endmodule|$))'
        for match in re.finditer(pattern, content, re.DOTALL):
            sensitivity = match.group(1).strip()
            body = match.group(3).strip()

            # Determine if sequential or combinational
            is_sequential = 'posedge' in sensitivity or 'negedge' in sensitivity

            always_blocks.append({
                'sensitivity': sensitivity,
                'body': body,
                'type': 'sequential' if is_sequential else 'combinational'
            })

        return always_blocks

    def _extract_assigns(self, content):
        """Extract continuous assignments."""
        assigns = []

        pattern = r'assign\s+(\w+)\s*=\s*([^;]+);'
        for match in re.finditer(pattern, content):
            lhs = match.group(1)
            rhs = match.group(2).strip()

            assigns.append({
                'lhs': lhs,
                'rhs': rhs
            })

        return assigns

    def _extract_state_elements(self, always_blocks):
        """Extract state elements (registers) from always blocks."""
        state_elements = []

        for block in always_blocks:
            if block['type'] == 'sequential':
                # Extract register assignments
                pattern = r'(\w+)\s*<=\s*([^;]+);'
                for match in re.finditer(pattern, block['body']):
                    reg_name = match.group(1)
                    if reg_name not in [s['name'] for s in state_elements]:
                        state_elements.append({
                            'name': reg_name,
                            'type': 'register'
                        })

        return state_elements
