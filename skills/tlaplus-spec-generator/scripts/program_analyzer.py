#!/usr/bin/env python3
"""
Program analyzer for extracting specification data from source code.
Analyzes control flow, data flow, and state transitions.
"""

import ast
import re
from collections import defaultdict


class ProgramAnalyzer:
    """Analyzes programs to extract specification-relevant information."""

    def __init__(self):
        self.functions = []
        self.state_variables = set()
        self.actions = []
        self.processes = []
        self.message_types = set()
        self.invariants = []

    def analyze_file(self, file_path, language, options):
        """Analyze a source file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        if language == 'python':
            self._analyze_python(source_code, options)
        elif language in ['c', 'cpp']:
            self._analyze_c_cpp(source_code, options)

    def _analyze_python(self, source_code, options):
        """Analyze Python source code."""
        try:
            tree = ast.parse(source_code)
            self._extract_python_structure(tree, options)
        except SyntaxError as e:
            print(f"[!] Python syntax error: {e}")

    def _extract_python_structure(self, tree, options):
        """Extract structure from Python AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'body': node.body,
                    'is_action': self._is_action_function(node),
                    'modifies': self._extract_modified_vars(node)
                }
                self.functions.append(func_info)

                # Identify actions (functions that modify state)
                if func_info['is_action']:
                    self.actions.append({
                        'name': node.name,
                        'params': func_info['args'],
                        'modifies': func_info['modifies']
                    })

            elif isinstance(node, ast.ClassDef):
                # Classes might represent processes or state
                if self._is_process_class(node):
                    self.processes.append({
                        'name': node.name,
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    })

        # Extract state variables (global vars, class attributes)
        self._extract_state_variables(tree)

    def _is_action_function(self, func_node):
        """Determine if a function represents an action (modifies state)."""
        # Check for assignments, attribute modifications
        for node in ast.walk(func_node):
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                return True
        return False

    def _extract_modified_vars(self, func_node):
        """Extract variables modified by a function."""
        modified = set()
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        modified.add(target.id)
                    elif isinstance(target, ast.Attribute):
                        modified.add(ast.unparse(target))
        return modified

    def _is_process_class(self, class_node):
        """Check if a class represents a process."""
        # Heuristic: classes with run/execute methods or threading
        method_names = [m.name for m in class_node.body if isinstance(m, ast.FunctionDef)]
        return any(name in ['run', 'execute', 'start', 'main'] for name in method_names)

    def _extract_state_variables(self, tree):
        """Extract global state variables."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                # Global assignments
                var_name = node.targets[0].id
                if not var_name.startswith('_'):  # Skip private vars
                    self.state_variables.add(var_name)

    def _analyze_c_cpp(self, source_code, options):
        """Analyze C/C++ source code (simplified)."""
        # Extract global variables
        global_var_pattern = r'(?:int|bool|char|float|double|struct\s+\w+)\s+(\w+)\s*(?:=|;)'
        for match in re.finditer(global_var_pattern, source_code):
            var_name = match.group(1)
            self.state_variables.add(var_name)

        # Extract functions
        func_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
        for match in re.finditer(func_pattern, source_code):
            return_type = match.group(1)
            func_name = match.group(2)

            # Skip main function
            if func_name == 'main':
                continue

            self.functions.append({
                'name': func_name,
                'return_type': return_type,
                'is_action': True  # Assume all functions are potential actions
            })

            self.actions.append({
                'name': func_name,
                'params': [],
                'modifies': set()
            })

        # Detect message passing patterns
        if 'send' in source_code.lower() or 'recv' in source_code.lower():
            self.message_types.add('Message')

    def extract_spec_data(self, options):
        """Extract and organize data for TLA+ specification generation."""
        # Filter based on options
        focus_functions = options.get('focus_functions', [])
        if focus_functions:
            self.actions = [a for a in self.actions if a['name'] in focus_functions]

        track_vars = options.get('track_vars', [])
        if track_vars:
            self.state_variables = set(track_vars)

        # Organize specification data
        spec_data = {
            'state_variables': self._abstract_variables(options),
            'actions': self.actions,
            'processes': self.processes,
            'message_types': self.message_types,
            'invariants': self._infer_invariants(),
            'constants': self._extract_constants(options)
        }

        return spec_data

    def _abstract_variables(self, options):
        """Apply abstraction to state variables."""
        abstraction = options.get('abstraction', 'medium')
        abstracted = {}

        for var in self.state_variables:
            if abstraction == 'high':
                # High abstraction: minimal state
                if var in ['state', 'status', 'phase']:
                    abstracted[var] = {'type': 'enum', 'values': ['Init', 'Active', 'Done']}
            elif abstraction == 'medium':
                # Medium abstraction: key variables with bounded domains
                abstracted[var] = self._infer_variable_type(var)
            else:
                # Low abstraction: preserve more detail
                abstracted[var] = self._infer_variable_type(var)

        return abstracted

    def _infer_variable_type(self, var_name):
        """Infer TLA+ type for a variable."""
        # Heuristics based on variable name
        if 'count' in var_name.lower() or 'num' in var_name.lower():
            return {'type': 'int', 'range': '0..N'}
        elif 'flag' in var_name.lower() or 'is_' in var_name.lower():
            return {'type': 'boolean'}
        elif 'state' in var_name.lower() or 'status' in var_name.lower():
            return {'type': 'enum', 'values': ['Init', 'Working', 'Done']}
        elif 'queue' in var_name.lower() or 'buffer' in var_name.lower():
            return {'type': 'sequence'}
        elif 'msg' in var_name.lower() or 'message' in var_name.lower():
            return {'type': 'message'}
        else:
            return {'type': 'value'}

    def _infer_invariants(self):
        """Infer potential invariants from code structure."""
        invariants = []

        # Safety invariants based on variable types
        for var in self.state_variables:
            if 'count' in var.lower():
                invariants.append(f"{var} >= 0")

        return invariants

    def _extract_constants(self, options):
        """Extract constants for the specification."""
        constants = {}

        # Number of processes
        num_processes = options.get('num_processes', 2)
        constants['N'] = num_processes

        return constants
