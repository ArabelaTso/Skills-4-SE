#!/usr/bin/env python3
"""
Control Flow Graph (CFG) analyzer for extracting state-transition models.
"""

import re
from collections import defaultdict, deque


class CFGAnalyzer:
    """Analyzes control flow and extracts state-transition information."""

    def __init__(self):
        self.states = []
        self.transitions = []
        self.variables = set()
        self.state_counter = 0

    def analyze(self, ast_data, options):
        """
        Analyze AST data to extract control flow graph.

        Args:
            ast_data: List of (file_path, language, ast) tuples
            options: Extraction options

        Returns:
            Dictionary containing CFG data
        """
        cfg_data = {
            'states': [],
            'transitions': [],
            'variables': set(),
            'initial_state': None,
            'functions': []
        }

        for file_path, lang, ast in ast_data:
            self._analyze_ast(ast, lang, cfg_data, options)

        # Apply abstraction
        if options['abstraction'] == 'high':
            cfg_data = self._apply_high_abstraction(cfg_data)
        elif options['abstraction'] == 'medium':
            cfg_data = self._apply_medium_abstraction(cfg_data)

        return cfg_data

    def _analyze_ast(self, ast, lang, cfg_data, options):
        """Analyze AST for a single file."""
        if not ast:
            return

        # Extract functions
        functions = self._extract_functions(ast, lang)

        # Filter functions if specified
        if options['focus_functions']:
            functions = [f for f in functions if f['name'] in options['focus_functions']]

        cfg_data['functions'].extend(functions)

        # Extract control flow for each function
        for func in functions:
            self._extract_function_cfg(func, cfg_data, options)

    def _extract_functions(self, ast, lang):
        """Extract function definitions from AST."""
        functions = []

        # Simplified extraction - in real implementation, use proper AST traversal
        if lang in ['c', 'cpp']:
            functions = self._extract_c_functions(ast)
        elif lang == 'java':
            functions = self._extract_java_functions(ast)
        elif lang == 'python':
            functions = self._extract_python_functions(ast)

        return functions

    def _extract_c_functions(self, ast):
        """Extract C/C++ functions."""
        # Placeholder - real implementation would parse AST
        return [{'name': 'main', 'body': ast, 'params': [], 'type': 'c'}]

    def _extract_java_functions(self, ast):
        """Extract Java methods."""
        return [{'name': 'method', 'body': ast, 'params': [], 'type': 'java'}]

    def _extract_python_functions(self, ast):
        """Extract Python functions."""
        return [{'name': 'function', 'body': ast, 'params': [], 'type': 'python'}]

    def _extract_function_cfg(self, func, cfg_data, options):
        """Extract CFG for a single function."""
        # Create initial state
        state_id = f"s{self.state_counter}"
        self.state_counter += 1

        if cfg_data['initial_state'] is None:
            cfg_data['initial_state'] = state_id

        cfg_data['states'].append({
            'id': state_id,
            'label': f"{func['name']}_entry",
            'type': 'entry'
        })

        # Analyze function body for control structures
        self._analyze_control_structures(func['body'], state_id, cfg_data, options)

    def _analyze_control_structures(self, body, current_state, cfg_data, options):
        """Analyze control structures (if, while, for, switch) in function body."""
        # Simplified analysis - real implementation would traverse AST properly

        # Extract variables
        vars_to_track = options.get('track_vars', [])
        if vars_to_track:
            cfg_data['variables'].update(vars_to_track)
        else:
            # Auto-detect important variables
            cfg_data['variables'].update(self._detect_state_variables(body))

        # Create basic control flow states
        # This is a simplified version - real implementation would handle:
        # - Conditional branches (if/else)
        # - Loops (while/for)
        # - Switch statements
        # - Function calls
        # - Return statements

    def _detect_state_variables(self, body):
        """Automatically detect variables that should be part of state."""
        # Heuristics for important variables:
        # - Variables used in conditions
        # - Variables modified in loops
        # - Global/static variables
        # - Variables passed between functions
        return set()

    def _apply_medium_abstraction(self, cfg_data):
        """Apply medium-level abstraction to CFG."""
        # Medium abstraction:
        # - Merge sequential states without branches
        # - Abstract data values to finite domains
        # - Keep control flow structure
        # - Preserve loop and branch conditions

        abstracted = cfg_data.copy()
        # Implementation would merge linear sequences of states
        return abstracted

    def _apply_high_abstraction(self, cfg_data):
        """Apply high-level abstraction to CFG."""
        # High abstraction:
        # - Collapse to protocol phases
        # - Abstract away internal details
        # - Focus on external interactions

        abstracted = cfg_data.copy()
        # Implementation would create high-level protocol states
        return abstracted
