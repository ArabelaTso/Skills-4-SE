#!/usr/bin/env python3
"""
Equivalence Analyzer - Analyzes two RTL designs for equivalence.
"""

from difflib import SequenceMatcher


class EquivalenceAnalyzer:
    """Analyzes equivalence between two RTL designs."""

    def __init__(self, design_a, design_b, options):
        self.design_a = design_a
        self.design_b = design_b
        self.options = options

    def align_designs(self):
        """
        Align interfaces and state variables between two designs.

        Returns:
            Dictionary containing alignment information
        """
        # Align ports
        port_alignment = self._align_ports()

        # Align state elements
        state_alignment = self._align_state_elements()

        # Check if alignment is successful
        success = (
            len(port_alignment['unmatched_a']) == 0 and
            len(port_alignment['unmatched_b']) == 0
        )

        return {
            'success': success,
            'matched_ports': port_alignment['matched'],
            'unmatched_a': port_alignment['unmatched_a'],
            'unmatched_b': port_alignment['unmatched_b'],
            'matched_state': state_alignment['matched'],
            'unmatched_state_a': state_alignment['unmatched_a'],
            'unmatched_state_b': state_alignment['unmatched_b']
        }

    def _align_ports(self):
        """Align ports between two designs."""
        ports_a = {p['name']: p for p in self.design_a['ports']}
        ports_b = {p['name']: p for p in self.design_b['ports']}

        matched = []
        unmatched_a = []
        unmatched_b = []

        # Find matches by name
        for name_a, port_a in ports_a.items():
            if name_a in ports_b:
                port_b = ports_b[name_a]

                # Check if ports are compatible
                if self._ports_compatible(port_a, port_b):
                    matched.append({
                        'name': name_a,
                        'port_a': port_a,
                        'port_b': port_b
                    })
                else:
                    unmatched_a.append(name_a)
                    unmatched_b.append(name_a)
            else:
                # Try fuzzy matching if ignore_names is set
                if self.options.get('ignore_names'):
                    match = self._find_similar_port(port_a, ports_b)
                    if match:
                        matched.append({
                            'name': f"{name_a} <-> {match['name']}",
                            'port_a': port_a,
                            'port_b': match
                        })
                        continue

                unmatched_a.append(name_a)

        # Find unmatched ports in B
        matched_names_b = {m['port_b']['name'] for m in matched}
        for name_b in ports_b:
            if name_b not in ports_a and name_b not in matched_names_b:
                unmatched_b.append(name_b)

        return {
            'matched': matched,
            'unmatched_a': unmatched_a,
            'unmatched_b': unmatched_b
        }

    def _ports_compatible(self, port_a, port_b):
        """Check if two ports are compatible."""
        return (
            port_a['direction'] == port_b['direction'] and
            port_a['width'] == port_b['width']
        )

    def _find_similar_port(self, port, port_dict):
        """Find similar port using fuzzy matching."""
        best_match = None
        best_ratio = 0.6  # Minimum similarity threshold

        for name, candidate in port_dict.items():
            if self._ports_compatible(port, candidate):
                ratio = SequenceMatcher(None, port['name'], name).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = candidate

        return best_match

    def _align_state_elements(self):
        """Align state elements between two designs."""
        state_a = {s['name']: s for s in self.design_a['state_elements']}
        state_b = {s['name']: s for s in self.design_b['state_elements']}

        matched = []
        unmatched_a = []
        unmatched_b = []

        # Find matches by name
        for name_a, elem_a in state_a.items():
            if name_a in state_b:
                matched.append({
                    'name': name_a,
                    'elem_a': elem_a,
                    'elem_b': state_b[name_a]
                })
            else:
                unmatched_a.append(name_a)

        # Find unmatched state elements in B
        for name_b in state_b:
            if name_b not in state_a:
                unmatched_b.append(name_b)

        return {
            'matched': matched,
            'unmatched_a': unmatched_a,
            'unmatched_b': unmatched_b
        }

    def find_differences(self):
        """
        Find differences between two designs.

        Returns:
            Dictionary containing cosmetic and semantic differences
        """
        cosmetic = []
        semantic = []

        # Check module names
        if self.design_a['module_name'] != self.design_b['module_name']:
            cosmetic.append({
                'type': 'module_name',
                'description': f"Module names differ: '{self.design_a['module_name']}' vs '{self.design_b['module_name']}'"
            })

        # Compare always blocks
        always_diff = self._compare_always_blocks()
        cosmetic.extend(always_diff['cosmetic'])
        semantic.extend(always_diff['semantic'])

        # Compare assign statements
        assign_diff = self._compare_assigns()
        cosmetic.extend(assign_diff['cosmetic'])
        semantic.extend(assign_diff['semantic'])

        return {
            'cosmetic': cosmetic,
            'semantic': semantic
        }

    def _compare_always_blocks(self):
        """Compare always blocks between designs."""
        cosmetic = []
        semantic = []

        blocks_a = self.design_a['always_blocks']
        blocks_b = self.design_b['always_blocks']

        if len(blocks_a) != len(blocks_b):
            semantic.append({
                'type': 'always_block_count',
                'description': f"Different number of always blocks: {len(blocks_a)} vs {len(blocks_b)}",
                'location': 'always blocks'
            })

        # Compare block types
        seq_a = sum(1 for b in blocks_a if b['type'] == 'sequential')
        seq_b = sum(1 for b in blocks_b if b['type'] == 'sequential')

        if seq_a != seq_b:
            semantic.append({
                'type': 'sequential_block_count',
                'description': f"Different number of sequential blocks: {seq_a} vs {seq_b}",
                'location': 'always blocks'
            })

        # Compare sensitivity lists
        for i, (block_a, block_b) in enumerate(zip(blocks_a, blocks_b)):
            if block_a['sensitivity'] != block_b['sensitivity']:
                # Check if semantically equivalent (e.g., different order)
                if self._sensitivity_equivalent(block_a['sensitivity'], block_b['sensitivity']):
                    cosmetic.append({
                        'type': 'sensitivity_order',
                        'description': f"Block {i}: Sensitivity list order differs"
                    })
                else:
                    semantic.append({
                        'type': 'sensitivity_list',
                        'description': f"Block {i}: Different sensitivity: '{block_a['sensitivity']}' vs '{block_b['sensitivity']}'",
                        'location': f'always block {i}'
                    })

            # Compare block bodies (simplified)
            if block_a['body'] != block_b['body']:
                # This is a simplified check - real implementation would do deeper analysis
                semantic.append({
                    'type': 'logic_difference',
                    'description': f"Block {i}: Logic differs",
                    'location': f'always block {i}'
                })

        return {'cosmetic': cosmetic, 'semantic': semantic}

    def _sensitivity_equivalent(self, sens_a, sens_b):
        """Check if two sensitivity lists are semantically equivalent."""
        # Normalize and compare
        tokens_a = set(sens_a.replace(',', ' ').split())
        tokens_b = set(sens_b.replace(',', ' ').split())
        return tokens_a == tokens_b

    def _compare_assigns(self):
        """Compare continuous assignments."""
        cosmetic = []
        semantic = []

        assigns_a = {a['lhs']: a['rhs'] for a in self.design_a['assigns']}
        assigns_b = {a['lhs']: a['rhs'] for a in self.design_b['assigns']}

        # Check for differences
        all_signals = set(assigns_a.keys()) | set(assigns_b.keys())

        for signal in all_signals:
            if signal in assigns_a and signal in assigns_b:
                if assigns_a[signal] != assigns_b[signal]:
                    # Check if expressions are equivalent
                    if self._expressions_equivalent(assigns_a[signal], assigns_b[signal]):
                        cosmetic.append({
                            'type': 'expression_format',
                            'description': f"Signal '{signal}': Equivalent expressions with different formatting"
                        })
                    else:
                        semantic.append({
                            'type': 'assignment_difference',
                            'description': f"Signal '{signal}': Different assignments: '{assigns_a[signal]}' vs '{assigns_b[signal]}'",
                            'location': f'assign {signal}'
                        })
            elif signal in assigns_a:
                semantic.append({
                    'type': 'missing_assignment',
                    'description': f"Signal '{signal}' assigned in A but not in B",
                    'location': f'assign {signal}'
                })
            else:
                semantic.append({
                    'type': 'extra_assignment',
                    'description': f"Signal '{signal}' assigned in B but not in A",
                    'location': f'assign {signal}'
                })

        return {'cosmetic': cosmetic, 'semantic': semantic}

    def _expressions_equivalent(self, expr_a, expr_b):
        """Check if two expressions are semantically equivalent."""
        # Normalize expressions (remove whitespace)
        norm_a = ''.join(expr_a.split())
        norm_b = ''.join(expr_b.split())
        return norm_a == norm_b

    def explain_differences(self, semantic_differences):
        """Generate plain language explanation of differences."""
        if not semantic_differences:
            return "No semantic differences found."

        explanations = []

        for diff in semantic_differences:
            if diff['type'] == 'always_block_count':
                explanations.append(
                    f"The designs have different numbers of always blocks, "
                    f"indicating structural differences in the logic implementation."
                )
            elif diff['type'] == 'logic_difference':
                explanations.append(
                    f"The logic in {diff['location']} differs between the two designs, "
                    f"which will result in different behavior."
                )
            elif diff['type'] == 'assignment_difference':
                explanations.append(
                    f"The assignment for {diff['location']} is different, "
                    f"causing the signal to have different values in the two designs."
                )
            elif diff['type'] == 'sensitivity_list':
                explanations.append(
                    f"The sensitivity list for {diff['location']} differs, "
                    f"which may cause the block to trigger at different times."
                )
            else:
                explanations.append(diff['description'])

        return " ".join(explanations)
