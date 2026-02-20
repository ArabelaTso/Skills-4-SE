#!/usr/bin/env python3
"""
trace_execution.py - Capture execution traces for behavior comparison

Instruments code to capture:
- Function calls
- Arguments
- Return values
- Execution order
"""

import argparse
import json
import sys
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Callable
import functools
import inspect


class ExecutionTracer:
    """Capture execution traces from Python code."""

    def __init__(self):
        self.traces = []
        self.call_stack = []

    def trace_function(self, func: Callable) -> Callable:
        """Decorator to trace function execution."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Record function entry
            call_info = {
                'function': func.__name__,
                'module': func.__module__,
                'args': self._serialize_args(args),
                'kwargs': self._serialize_args(kwargs),
                'depth': len(self.call_stack)
            }

            self.call_stack.append(func.__name__)

            try:
                result = func(*args, **kwargs)
                call_info['return_value'] = self._serialize_value(result)
                call_info['status'] = 'success'
            except Exception as e:
                call_info['exception'] = str(e)
                call_info['status'] = 'error'
                raise
            finally:
                self.call_stack.pop()
                self.traces.append(call_info)

            return result

        return wrapper

    def _serialize_value(self, value: Any) -> Any:
        """Serialize value for JSON output."""
        if value is None:
            return None
        elif isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value[:10]]  # Limit to 10 items
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in list(value.items())[:10]}
        else:
            return f"<{type(value).__name__}>"

    def _serialize_args(self, args) -> Any:
        """Serialize function arguments."""
        if isinstance(args, dict):
            return {k: self._serialize_value(v) for k, v in args.items()}
        else:
            return [self._serialize_value(arg) for arg in args]

    def instrument_module(self, module_path: str):
        """Instrument all functions in a module."""
        spec = importlib.util.spec_from_file_location("target_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Trace all functions in module
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and obj.__module__ == module.__name__:
                setattr(module, name, self.trace_function(obj))

        return module

    def get_traces(self) -> List[Dict]:
        """Get captured traces."""
        return self.traces

    def save_traces(self, output_file: str):
        """Save traces to JSON file."""
        with open(output_file, 'w') as f:
            json.dump({
                'traces': self.traces,
                'total_calls': len(self.traces)
            }, f, indent=2)


def run_with_tracing(repo_path: str, test_inputs: Dict, output_file: str):
    """Run code with execution tracing."""
    print(f"Tracing execution in {repo_path}...")

    tracer = ExecutionTracer()

    # Add repo to path
    sys.path.insert(0, repo_path)

    try:
        # Load and instrument target module
        main_module = test_inputs.get('module', 'main.py')
        module_path = Path(repo_path) / main_module

        if not module_path.exists():
            raise FileNotFoundError(f"Module not found: {module_path}")

        module = tracer.instrument_module(str(module_path))

        # Execute test cases
        for test_case in test_inputs.get('test_cases', []):
            func_name = test_case.get('function')
            args = test_case.get('args', [])
            kwargs = test_case.get('kwargs', {})

            if hasattr(module, func_name):
                func = getattr(module, func_name)
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing {func_name}: {e}")

        # Save traces
        tracer.save_traces(output_file)
        print(f"Captured {len(tracer.traces)} function calls")
        print(f"Traces saved to: {output_file}")

    finally:
        sys.path.pop(0)


def main():
    parser = argparse.ArgumentParser(
        description='Capture execution traces for behavior comparison'
    )
    parser.add_argument('--repo', required=True,
                       help='Path to repository')
    parser.add_argument('--input', required=True,
                       help='Test inputs file (JSON)')
    parser.add_argument('--output', required=True,
                       help='Output file for traces (JSON)')

    args = parser.parse_args()

    try:
        # Load test inputs
        with open(args.input, 'r') as f:
            test_inputs = json.load(f)

        # Run with tracing
        run_with_tracing(args.repo, test_inputs, args.output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
