#!/usr/bin/env python3
"""
TLA+ specification generator.
Generates pure TLA+ specifications from analyzed program data.
"""


class TLAPlusGenerator:
    """Generates TLA+ specifications from specification data."""

    def __init__(self):
        self.lines = []
        self.indent_level = 0

    def generate(self, spec_data, options):
        """
        Generate TLA+ specification.

        Args:
            spec_data: Dictionary containing specification data
            options: Generation options

        Returns:
            String containing complete TLA+ specification
        """
        self.lines = []
        module_name = options.get('module_name', 'Spec')

        # Module declaration
        self._add_line(f"---- MODULE {module_name} ----")
        self._add_line("")

        # EXTENDS
        self._generate_extends()

        # CONSTANTS
        self._generate_constants(spec_data)

        # VARIABLES
        self._generate_variables(spec_data)

        # Type invariant
        self._generate_type_invariant(spec_data)

        # Initial state
        self._generate_init(spec_data)

        # Actions
        self._generate_actions(spec_data)

        # Next state relation
        self._generate_next(spec_data)

        # Specification
        self._generate_spec(spec_data)

        # Invariants
        self._generate_invariants(spec_data)

        # Module end
        self._add_line("")
        self._add_line("=" * 4)
        self._add_line("")

        return '\n'.join(self.lines)

    def _add_line(self, text="", extra_indent=0):
        """Add a line with proper indentation."""
        indent = "  " * (self.indent_level + extra_indent)
        self.lines.append(indent + text if text else "")

    def _generate_extends(self):
        """Generate EXTENDS clause."""
        self._add_line("EXTENDS Naturals, Sequences, FiniteSets, TLC")
        self._add_line("")

    def _generate_constants(self, spec_data):
        """Generate CONSTANTS section."""
        constants = spec_data.get('constants', {})

        if constants:
            self._add_line("CONSTANTS")
            for const_name, const_value in constants.items():
                self._add_line(f"  {const_name}  \\* Number of processes/nodes", extra_indent=0)
            self._add_line("")

    def _generate_variables(self, spec_data):
        """Generate VARIABLES section."""
        state_vars = spec_data.get('state_variables', {})

        if not state_vars:
            self._add_line("VARIABLES state")
            self._add_line("")
            return

        self._add_line("VARIABLES")
        for var_name in sorted(state_vars.keys()):
            self._add_line(f"  {var_name},", extra_indent=0)

        # Remove trailing comma from last variable
        if self.lines[-1].endswith(','):
            self.lines[-1] = self.lines[-1][:-1]

        self._add_line("")

        # Variable list for convenience
        var_names = sorted(state_vars.keys())
        self._add_line(f"vars == <<{', '.join(var_names)}>>")
        self._add_line("")

    def _generate_type_invariant(self, spec_data):
        """Generate type invariant."""
        state_vars = spec_data.get('state_variables', {})

        if not state_vars:
            return

        self._add_line("TypeOK ==")
        self.indent_level += 1

        for i, (var_name, var_info) in enumerate(sorted(state_vars.items())):
            connector = "/\\" if i > 0 else ""
            type_constraint = self._get_type_constraint(var_name, var_info)
            self._add_line(f"{connector} {type_constraint}")

        self.indent_level -= 1
        self._add_line("")

    def _get_type_constraint(self, var_name, var_info):
        """Generate type constraint for a variable."""
        var_type = var_info.get('type', 'value')

        if var_type == 'boolean':
            return f"{var_name} \\in BOOLEAN"
        elif var_type == 'int':
            range_spec = var_info.get('range', '0..N')
            return f"{var_name} \\in {range_spec}"
        elif var_type == 'enum':
            values = var_info.get('values', ['Init', 'Working', 'Done'])
            value_set = '{' + ', '.join(f'"{v}"' for v in values) + '}'
            return f"{var_name} \\in {value_set}"
        elif var_type == 'sequence':
            return f"{var_name} \\in Seq(Messages)"
        elif var_type == 'message':
            return f"{var_name} \\in Messages \\cup {{NoMessage}}"
        else:
            return f"TRUE  \\* {var_name} type not specified"

    def _generate_init(self, spec_data):
        """Generate initial state predicate."""
        state_vars = spec_data.get('state_variables', {})

        self._add_line("Init ==")
        self.indent_level += 1

        if not state_vars:
            self._add_line("/\\ state = \"Init\"")
        else:
            for i, (var_name, var_info) in enumerate(sorted(state_vars.items())):
                connector = "/\\" if i > 0 else ""
                init_value = self._get_init_value(var_info)
                self._add_line(f"{connector} {var_name} = {init_value}")

        self.indent_level -= 1
        self._add_line("")

    def _get_init_value(self, var_info):
        """Get initial value for a variable."""
        var_type = var_info.get('type', 'value')

        if var_type == 'boolean':
            return "FALSE"
        elif var_type == 'int':
            return "0"
        elif var_type == 'enum':
            values = var_info.get('values', ['Init'])
            return f'"{values[0]}"'
        elif var_type == 'sequence':
            return "<<>>"
        elif var_type == 'message':
            return "NoMessage"
        else:
            return "InitialValue"

    def _generate_actions(self, spec_data):
        """Generate action definitions."""
        actions = spec_data.get('actions', [])

        if not actions:
            # Generate a default action
            self._add_line("Step ==")
            self.indent_level += 1
            self._add_line("/\\ state' = \"Done\"")
            self._add_line("/\\ UNCHANGED <<>>")
            self.indent_level -= 1
            self._add_line("")
            return

        for action in actions:
            action_name = action['name']
            params = action.get('params', [])
            modifies = action.get('modifies', set())

            # Action definition
            if params:
                param_str = ', '.join(params)
                self._add_line(f"{action_name}({param_str}) ==")
            else:
                self._add_line(f"{action_name} ==")

            self.indent_level += 1

            # Action body (simplified - would need more analysis)
            self._add_line("/\\ TRUE  \\* Precondition")

            if modifies:
                for var in sorted(modifies):
                    self._add_line(f"/\\ {var}' = {var}  \\* Update {var}")
            else:
                self._add_line("/\\ TRUE  \\* State update")

            # Unchanged variables
            state_vars = spec_data.get('state_variables', {})
            unchanged_vars = set(state_vars.keys()) - modifies
            if unchanged_vars:
                unchanged_list = ', '.join(sorted(unchanged_vars))
                self._add_line(f"/\\ UNCHANGED <<{unchanged_list}>>")

            self.indent_level -= 1
            self._add_line("")

    def _generate_next(self, spec_data):
        """Generate next-state relation."""
        actions = spec_data.get('actions', [])

        self._add_line("Next ==")
        self.indent_level += 1

        if not actions:
            self._add_line("\\/ Step")
        else:
            for i, action in enumerate(actions):
                connector = "\\/" if i > 0 else ""
                action_name = action['name']
                self._add_line(f"{connector} {action_name}")

        self.indent_level -= 1
        self._add_line("")

    def _generate_spec(self, spec_data):
        """Generate specification formula."""
        state_vars = spec_data.get('state_variables', {})

        self._add_line("Spec == Init /\\ [][Next]_vars")
        self._add_line("")

        # Fairness (optional)
        self._add_line("\\* Fairness ==")
        self._add_line("\\*   /\\ WF_vars(Next)")
        self._add_line("")

    def _generate_invariants(self, spec_data):
        """Generate invariant properties."""
        invariants = spec_data.get('invariants', [])

        # Always include type invariant
        self._add_line("\\* Invariants to check:")
        self._add_line("\\* INVARIANT TypeOK")
        self._add_line("")

        if invariants:
            self._add_line("SafetyInvariant ==")
            self.indent_level += 1

            for i, inv in enumerate(invariants):
                connector = "/\\" if i > 0 else ""
                self._add_line(f"{connector} {inv}")

            self.indent_level -= 1
            self._add_line("")

    def generate_mapping_explanation(self, spec_data):
        """Generate human-readable mapping explanation."""
        lines = []
        lines.append("=" * 70)
        lines.append("PROGRAM-TO-TLA+ MAPPING EXPLANATION")
        lines.append("=" * 70)
        lines.append("")

        # State variables
        lines.append("STATE VARIABLES:")
        lines.append("-" * 70)
        state_vars = spec_data.get('state_variables', {})
        if state_vars:
            for var_name, var_info in sorted(state_vars.items()):
                var_type = var_info.get('type', 'value')
                lines.append(f"  {var_name}: {var_type}")
                if var_type == 'enum':
                    values = var_info.get('values', [])
                    lines.append(f"    Possible values: {', '.join(values)}")
        else:
            lines.append("  (No state variables identified)")
        lines.append("")

        # Actions
        lines.append("ACTIONS:")
        lines.append("-" * 70)
        actions = spec_data.get('actions', [])
        if actions:
            for action in actions:
                action_name = action['name']
                params = action.get('params', [])
                modifies = action.get('modifies', set())

                param_str = f"({', '.join(params)})" if params else ""
                lines.append(f"  {action_name}{param_str}")

                if modifies:
                    lines.append(f"    Modifies: {', '.join(sorted(modifies))}")
        else:
            lines.append("  (No actions identified)")
        lines.append("")

        # Processes
        lines.append("PROCESSES:")
        lines.append("-" * 70)
        processes = spec_data.get('processes', [])
        if processes:
            for proc in processes:
                proc_name = proc['name']
                methods = proc.get('methods', [])
                lines.append(f"  {proc_name}")
                if methods:
                    lines.append(f"    Methods: {', '.join(methods)}")
        else:
            lines.append("  (No processes identified)")
        lines.append("")

        # Constants
        lines.append("CONSTANTS:")
        lines.append("-" * 70)
        constants = spec_data.get('constants', {})
        if constants:
            for const_name, const_value in constants.items():
                lines.append(f"  {const_name} = {const_value}")
        else:
            lines.append("  (No constants defined)")
        lines.append("")

        lines.append("=" * 70)
        lines.append("")
        lines.append("USAGE:")
        lines.append("  1. Review the generated TLA+ specification")
        lines.append("  2. Refine action definitions based on actual program logic")
        lines.append("  3. Add temporal properties (liveness, fairness)")
        lines.append("  4. Run TLC model checker to verify properties")
        lines.append("")

        return '\n'.join(lines)
