#!/usr/bin/env python3
"""
Run TLC model checker to validate TLA+ specifications.

This script provides a convenient interface to run TLC and capture results.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tlc(spec_file: str, config_file: str = None, workers: int = 1,
            depth: int = None, timeout: int = None) -> dict:
    """
    Run TLC model checker on a specification.

    Args:
        spec_file: Path to .tla specification file
        config_file: Path to .cfg configuration file (optional)
        workers: Number of worker threads (default: 1)
        depth: Maximum search depth (optional)
        timeout: Timeout in seconds (optional)

    Returns:
        Dictionary with:
        - success: Boolean indicating if model checking passed
        - output: Full TLC output
        - error: Error message if failed
        - counterexample: Path to counterexample file if violation found
    """
    result = {
        "success": False,
        "output": "",
        "error": None,
        "counterexample": None
    }

    # Build TLC command
    cmd = ["tlc2", spec_file]

    if config_file:
        cmd.extend(["-config", config_file])

    cmd.extend(["-workers", str(workers)])

    if depth:
        cmd.extend(["-depth", str(depth)])

    if timeout:
        cmd.extend(["-timeout", str(timeout)])

    try:
        # Run TLC
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout if timeout else None
        )

        result["output"] = process.stdout + process.stderr

        # Check if model checking succeeded
        if process.returncode == 0:
            result["success"] = True
        else:
            result["error"] = "Model checking failed - violation found"

            # Look for counterexample in output
            if "Error: Invariant" in result["output"] or "Deadlock" in result["output"]:
                result["counterexample"] = result["output"]

    except subprocess.TimeoutExpired:
        result["error"] = f"TLC timed out after {timeout} seconds"
    except FileNotFoundError:
        result["error"] = "TLC not found. Please install TLA+ Toolbox or tlc2 command."
    except Exception as e:
        result["error"] = f"Error running TLC: {str(e)}"

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: run_tlc.py <spec_file> [options]")
        print("\nOptions:")
        print("  --config <file>    Configuration file")
        print("  --workers <n>      Number of workers (default: 1)")
        print("  --depth <n>        Maximum search depth")
        print("  --timeout <sec>    Timeout in seconds")
        sys.exit(1)

    spec_file = sys.argv[1]

    if not os.path.exists(spec_file):
        print(f"Error: Specification file '{spec_file}' not found")
        sys.exit(1)

    # Parse options
    config_file = None
    workers = 1
    depth = None
    timeout = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--config" and i + 1 < len(sys.argv):
            config_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--workers" and i + 1 < len(sys.argv):
            workers = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--depth" and i + 1 < len(sys.argv):
            depth = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Run TLC
    result = run_tlc(spec_file, config_file, workers, depth, timeout)

    # Print results
    print(result["output"])

    if result["success"]:
        print("\n✓ Model checking passed - no violations found")
        sys.exit(0)
    else:
        print(f"\n✗ Model checking failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
