#!/usr/bin/env python3
"""
Trace Replay Script Generator

Generates replay scripts from captured execution traces to reproduce bugs deterministically.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any


class ReplayGenerator:
    """Generates replay scripts from execution traces"""

    def __init__(self, trace_file: Path):
        self.trace_file = trace_file
        self.traces = []
        self.metadata = {}
        self.load_trace()

    def load_trace(self):
        """Load trace data from JSON file"""
        with open(self.trace_file, 'r') as f:
            data = json.load(f)
            self.traces = data.get('traces', [])
            self.metadata = data.get('metadata', {})

    def generate_python_replay(self, output_file: Path):
        """Generate Python replay script"""

        script_lines = [
            '#!/usr/bin/env python3',
            '"""',
            'Bug Reproduction Replay Script',
            f'Generated from trace: {self.trace_file}',
            f'Total events: {len(self.traces)}',
            '"""',
            '',
            'import sys',
            'from typing import Any',
            '',
            'class ReplayEngine:',
            '    """Replays execution trace for bug reproduction"""',
            '    ',
            '    def __init__(self):',
            '        self.current_step = 0',
            '        self.variables = {}',
            '        self.call_stack = []',
            '    ',
            '    def replay(self):',
            '        """Execute replay sequence"""',
            '        print("Starting bug reproduction replay...")',
            '        print(f"Total steps: {len(self.traces)}")',
            '        ',
        ]

        # Generate replay steps
        for i, event in enumerate(self.traces):
            event_type = event.get('type')
            data = event.get('data', {})

            if event_type == 'function_entry':
                func_name = data.get('function', 'unknown')
                args = data.get('arguments', {})
                script_lines.append(f'        # Step {i+1}: Enter function {func_name}')
                script_lines.append(f'        self.call_stack.append("{func_name}")')
                script_lines.append(f'        print(f"[{{self.current_step}}] Entering: {func_name}")')

            elif event_type == 'function_exit':
                func_name = data.get('function', 'unknown')
                script_lines.append(f'        # Step {i+1}: Exit function {func_name}')
                script_lines.append(f'        if self.call_stack: self.call_stack.pop()')
                script_lines.append(f'        print(f"[{{self.current_step}}] Exiting: {func_name}")')

            elif event_type == 'variable_assignment':
                var_name = data.get('variable', 'unknown')
                value = data.get('value')
                var_type = data.get('type', 'unknown')
                script_lines.append(f'        # Step {i+1}: Assign {var_name} = {repr(value)}')
                script_lines.append(f'        self.variables["{var_name}"] = {repr(value)}')
                script_lines.append(f'        print(f"[{{self.current_step}}] {var_name} = {repr(value)}")')

            elif event_type == 'control_flow':
                flow_type = data.get('type', 'unknown')
                result = data.get('result')
                script_lines.append(f'        # Step {i+1}: Control flow - {flow_type}')
                script_lines.append(f'        print(f"[{{self.current_step}}] {flow_type}: {result}")')

            script_lines.append('        self.current_step += 1')
            script_lines.append('        ')

        script_lines.extend([
            '        print("Replay completed successfully!")',
            '        return True',
            '',
            'def main():',
            '    engine = ReplayEngine()',
            '    try:',
            '        engine.replay()',
            '    except Exception as e:',
            '        print(f"Replay failed at step {engine.current_step}: {e}")',
            '        sys.exit(1)',
            '',
            'if __name__ == "__main__":',
            '    main()',
        ])

        # Write replay script
        with open(output_file, 'w') as f:
            f.write('\n'.join(script_lines))

        # Make executable
        output_file.chmod(0o755)

        print(f"Generated replay script: {output_file}")
        print(f"Run with: python {output_file}")

    def generate_summary(self) -> str:
        """Generate human-readable trace summary"""
        summary_lines = [
            "=" * 80,
            "EXECUTION TRACE SUMMARY",
            "=" * 80,
            f"Trace file: {self.trace_file}",
            f"Total events: {len(self.traces)}",
            f"Max call depth: {self.metadata.get('max_depth', 'unknown')}",
            "",
            "Event Distribution:",
        ]

        # Count event types
        event_counts = {}
        for event in self.traces:
            event_type = event.get('type', 'unknown')
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        for event_type, count in sorted(event_counts.items()):
            summary_lines.append(f"  {event_type}: {count}")

        summary_lines.extend([
            "",
            "Call Sequence:",
        ])

        # Extract function call sequence
        function_calls = []
        for event in self.traces:
            if event.get('type') == 'function_entry':
                func_name = event.get('data', {}).get('function', 'unknown')
                depth = event.get('depth', 0)
                function_calls.append((depth, func_name))

        for depth, func_name in function_calls[:20]:  # Show first 20
            indent = "  " * depth
            summary_lines.append(f"  {indent}{func_name}()")

        if len(function_calls) > 20:
            summary_lines.append(f"  ... and {len(function_calls) - 20} more calls")

        summary_lines.append("=" * 80)

        return '\n'.join(summary_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate replay scripts from execution traces'
    )
    parser.add_argument('trace', type=Path, help='Input trace JSON file')
    parser.add_argument('-o', '--output', type=Path, help='Output replay script (default: replay.py)')
    parser.add_argument('--summary', action='store_true', help='Print trace summary')

    args = parser.parse_args()

    if not args.trace.exists():
        print(f"Error: Trace file {args.trace} does not exist", file=sys.stderr)
        sys.exit(1)

    generator = ReplayGenerator(args.trace)

    if args.summary:
        print(generator.generate_summary())

    if args.output is None:
        args.output = Path('replay.py')

    generator.generate_python_replay(args.output)


if __name__ == '__main__':
    main()
