#!/usr/bin/env python3
"""
Runtime library for capturing state snapshots in Python programs.

This module is imported by instrumented Python code to capture snapshots.
"""

import json
import inspect
import traceback
import sys
import os
from datetime import datetime
from typing import Any, Dict, List


class SnapshotRuntime:
    """Runtime for capturing and managing snapshots."""

    def __init__(self, output_file: str = None):
        self.snapshots = []
        self.output_file = output_file or os.environ.get('SNAPSHOT_OUTPUT', 'snapshots.json')
        self.enabled = True

    def capture_snapshot(self, snapshot_id: int, location: str, snapshot_type: str,
                        local_vars: Dict, global_vars: Dict):
        """Capture a snapshot of current program state."""
        if not self.enabled:
            return

        # Get call stack
        stack = []
        for frame_info in inspect.stack()[2:]:  # Skip this function and the instrumented call
            stack.append({
                'function': frame_info.function,
                'filename': frame_info.filename,
                'lineno': frame_info.lineno
            })

        # Filter and serialize variables
        local_vars_serialized = self._serialize_variables(local_vars)

        # Create snapshot
        snapshot = {
            'snapshot_id': snapshot_id,
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'type': snapshot_type,
            'call_stack': stack,
            'local_variables': local_vars_serialized,
            'thread_id': None  # Could add threading.get_ident() if needed
        }

        self.snapshots.append(snapshot)

    def _serialize_variables(self, variables: Dict) -> Dict[str, Any]:
        """Serialize variables to JSON-compatible format."""
        serialized = {}

        # Filter out internal variables and modules
        filtered_vars = {k: v for k, v in variables.items()
                        if not k.startswith('__') and not inspect.ismodule(v)}

        for name, value in filtered_vars.items():
            try:
                # Try to serialize the value
                serialized[name] = self._serialize_value(value)
            except Exception as e:
                serialized[name] = {
                    '__type__': type(value).__name__,
                    '__repr__': repr(value)[:100],
                    '__error__': str(e)
                }

        return serialized

    def _serialize_value(self, value: Any) -> Any:
        """Serialize a single value."""
        # Handle basic types
        if value is None or isinstance(value, (bool, int, float, str)):
            return value

        # Handle collections
        if isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value[:100]]  # Limit size

        if isinstance(value, dict):
            return {str(k): self._serialize_value(v) for k, v in list(value.items())[:100]}

        if isinstance(value, set):
            return list(value)[:100]

        # Handle objects
        if hasattr(value, '__dict__'):
            return {
                '__type__': type(value).__name__,
                '__attributes__': {k: self._serialize_value(v)
                                  for k, v in value.__dict__.items()
                                  if not k.startswith('_')}
            }

        # Fallback
        return {
            '__type__': type(value).__name__,
            '__repr__': repr(value)[:100]
        }

    def save_snapshots(self):
        """Save all snapshots to file."""
        output = {
            'format_version': '1.0',
            'language': 'python',
            'total_snapshots': len(self.snapshots),
            'snapshots': self.snapshots
        }

        with open(self.output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"Saved {len(self.snapshots)} snapshots to {self.output_file}", file=sys.stderr)

    def __del__(self):
        """Save snapshots when runtime is destroyed."""
        if self.snapshots:
            self.save_snapshots()


# Global runtime instance
_runtime = SnapshotRuntime()


def capture_snapshot(snapshot_id: int, location: str, snapshot_type: str,
                    local_vars: Dict, global_vars: Dict):
    """Global function for capturing snapshots."""
    _runtime.capture_snapshot(snapshot_id, location, snapshot_type, local_vars, global_vars)


def save_snapshots():
    """Manually save snapshots."""
    _runtime.save_snapshots()


def set_output_file(filename: str):
    """Set output file for snapshots."""
    _runtime.output_file = filename


def enable():
    """Enable snapshot capture."""
    _runtime.enabled = True


def disable():
    """Disable snapshot capture."""
    _runtime.enabled = False
