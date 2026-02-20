#!/usr/bin/env python3
"""
Python Code Instrumenter for Bug Reproduction Tracing

Instruments Python source code to capture execution traces including function calls,
variable values, and control flow for bug reproduction purposes.
"""

import ast
import sys
import argparse
from pathlib import Path
from typing import Set, List


class TraceInstrumenter(ast.NodeTransformer):
    """AST transformer that adds tracing instrumentation to Python code"""

    def __init__(self, trace_functions: bool = True, trace_variables: bool = True,
                 trace_control_flow: bool = True, exclude_patterns: Set[str] = None):
        self.trace_functions = trace_functions
        self.trace_variables = trace_variables
        self.trace_control_flow = trace_control_flow
        self.exclude_patterns = exclude_patterns or set()
        self.function_depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Instrument function definitions with entry/exit tracing"""
        if not self.trace_functions:
            return node

        # Skip if function name matches exclude patterns
        if any(pattern in node.name for pattern in self.exclude_patterns):
            return node

        self.function_depth += 1

        # Create function entry trace
        entry_trace = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='_trace_function_entry', ctx=ast.Load()),
                args=[
                    ast.Constant(value=node.name),
                    ast.Name(id='locals', ctx=ast.Load()),
                ],
                keywords=[]
            )
        )

        # Create function exit trace
        exit_trace = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='_trace_function_exit', ctx=ast.Load()),
                args=[
                    ast.Constant(value=node.name),
                    ast.Name(id='locals', ctx=ast.Load()),
                ],
                keywords=[]
            )
        )

        # Wrap function body with try-finally to ensure exit trace
        try_finally = ast.Try(
            body=node.body,
            handlers=[],
            orelse=[],
            finalbody=[exit_trace]
        )

        # Insert entry trace at the beginning
        node.body = [entry_trace, try_finally]

        self.generic_visit(node)
        self.function_depth -= 1

        return node

    def visit_Assign(self, node: ast.Assign) -> List[ast.stmt]:
        """Instrument variable assignments with value tracing"""
        if not self.trace_variables:
            return node

        # Get variable names being assigned
        var_names = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_names.append(target.id)

        if not var_names:
            return node

        # Create trace call for each variable
        trace_calls = []
        for var_name in var_names:
            trace_call = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id='_trace_variable', ctx=ast.Load()),
                    args=[
                        ast.Constant(value=var_name),
                        ast.Name(id=var_name, ctx=ast.Load()),
                    ],
                    keywords=[]
                )
            )
            trace_calls.append(trace_call)

        return [node] + trace_calls

    def visit_If(self, node: ast.If) -> ast.If:
        """Instrument if statements with control flow tracing"""
        if not self.trace_control_flow:
            return node

        # Create trace for condition evaluation
        condition_trace = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='_trace_condition', ctx=ast.Load()),
                args=[
                    ast.Constant(value='if'),
                    node.test,
                ],
                keywords=[]
            )
        )

        # Insert trace at the beginning of if body
        node.body.insert(0, condition_trace)

        # Insert trace at the beginning of else body if it exists
        if node.orelse:
            else_trace = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id='_trace_condition', ctx=ast.Load()),
                    args=[
                        ast.Constant(value='else'),
                        ast.Constant(value=True),
                    ],
                    keywords=[]
                )
            )
            if isinstance(node.orelse[0], ast.If):
                # elif case - don't add trace
                pass
            else:
                node.orelse.insert(0, else_trace)

        self.generic_visit(node)
        return node

    def visit_For(self, node: ast.For) -> ast.For:
        """Instrument for loops with iteration tracing"""
        if not self.trace_control_flow:
            return node

        # Create trace for loop entry
        loop_trace = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='_trace_loop', ctx=ast.Load()),
                args=[
                    ast.Constant(value='for'),
                    ast.Name(id=node.target.id if isinstance(node.target, ast.Name) else 'iterator', ctx=ast.Load()),
                ],
                keywords=[]
            )
        )

        node.body.insert(0, loop_trace)
        self.generic_visit(node)
        return node

    def visit_While(self, node: ast.While) -> ast.While:
        """Instrument while loops with iteration tracing"""
        if not self.trace_control_flow:
            return node

        # Create trace for loop condition
        loop_trace = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='_trace_loop', ctx=ast.Load()),
                args=[
                    ast.Constant(value='while'),
                    node.test,
                ],
                keywords=[]
            )
        )

        node.body.insert(0, loop_trace)
        self.generic_visit(node)
        return node


def generate_trace_runtime() -> str:
    """Generate the runtime tracing library code"""
    return '''
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

class TraceRecorder:
    """Records execution traces for bug reproduction"""

    def __init__(self, output_file='trace.json', max_depth=50):
        self.output_file = output_file
        self.max_depth = max_depth
        self.traces = []
        self.call_stack = []
        self.sequence_number = 0

    def record(self, event_type, data):
        """Record a trace event"""
        self.sequence_number += 1
        event = {
            'seq': self.sequence_number,
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'depth': len(self.call_stack),
            'data': data
        }
        self.traces.append(event)

    def save(self):
        """Save traces to file"""
        with open(self.output_file, 'w') as f:
            json.dump({
                'traces': self.traces,
                'metadata': {
                    'total_events': len(self.traces),
                    'max_depth': max(e['depth'] for e in self.traces) if self.traces else 0
                }
            }, f, indent=2, default=str)
        print(f"Trace saved to {self.output_file} ({len(self.traces)} events)")

# Global trace recorder
_recorder = TraceRecorder()

def _trace_function_entry(func_name, local_vars):
    """Trace function entry"""
    if len(_recorder.call_stack) < _recorder.max_depth:
        _recorder.call_stack.append(func_name)
        # Filter out internal variables
        filtered_vars = {k: v for k, v in local_vars().items()
                        if not k.startswith('_')}
        _recorder.record('function_entry', {
            'function': func_name,
            'arguments': filtered_vars
        })

def _trace_function_exit(func_name, local_vars):
    """Trace function exit"""
    if _recorder.call_stack and _recorder.call_stack[-1] == func_name:
        _recorder.call_stack.pop()
    filtered_vars = {k: v for k, v in local_vars().items()
                    if not k.startswith('_')}
    _recorder.record('function_exit', {
        'function': func_name,
        'locals': filtered_vars
    })

def _trace_variable(var_name, value):
    """Trace variable assignment"""
    _recorder.record('variable_assignment', {
        'variable': var_name,
        'value': value,
        'type': type(value).__name__
    })

def _trace_condition(condition_type, result):
    """Trace conditional branch"""
    _recorder.record('control_flow', {
        'type': condition_type,
        'result': bool(result)
    })

def _trace_loop(loop_type, iterator):
    """Trace loop iteration"""
    _recorder.record('control_flow', {
        'type': loop_type,
        'iterator': iterator
    })

def _save_trace():
    """Save trace on program exit"""
    _recorder.save()

import atexit
atexit.register(_save_trace)
'''


def instrument_file(input_path: Path, output_path: Path,
                   trace_functions: bool = True,
                   trace_variables: bool = True,
                   trace_control_flow: bool = True,
                   exclude_patterns: Set[str] = None):
    """Instrument a Python file with tracing code"""

    # Read source code
    with open(input_path, 'r') as f:
        source = f.read()

    # Parse AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Syntax error in {input_path}: {e}", file=sys.stderr)
        return False

    # Apply instrumentation
    instrumenter = TraceInstrumenter(
        trace_functions=trace_functions,
        trace_variables=trace_variables,
        trace_control_flow=trace_control_flow,
        exclude_patterns=exclude_patterns
    )
    instrumented_tree = instrumenter.visit(tree)
    ast.fix_missing_locations(instrumented_tree)

    # Generate instrumented code
    instrumented_code = ast.unparse(instrumented_tree)

    # Add trace runtime at the beginning
    trace_runtime = generate_trace_runtime()
    full_code = trace_runtime + '\n\n' + instrumented_code

    # Write instrumented code
    with open(output_path, 'w') as f:
        f.write(full_code)

    print(f"Instrumented {input_path} -> {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Instrument Python code for bug reproduction tracing'
    )
    parser.add_argument('input', type=Path, help='Input Python file')
    parser.add_argument('-o', '--output', type=Path, help='Output file (default: input_instrumented.py)')
    parser.add_argument('--no-functions', action='store_true', help='Disable function tracing')
    parser.add_argument('--no-variables', action='store_true', help='Disable variable tracing')
    parser.add_argument('--no-control-flow', action='store_true', help='Disable control flow tracing')
    parser.add_argument('--exclude', nargs='+', default=[], help='Patterns to exclude from tracing')

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file {args.input} does not exist", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        args.output = args.input.parent / f"{args.input.stem}_instrumented.py"

    success = instrument_file(
        args.input,
        args.output,
        trace_functions=not args.no_functions,
        trace_variables=not args.no_variables,
        trace_control_flow=not args.no_control_flow,
        exclude_patterns=set(args.exclude)
    )

    if success:
        print(f"\nRun the instrumented code with: python {args.output}")
        print(f"Trace will be saved to: trace.json")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
