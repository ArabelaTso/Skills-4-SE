#!/usr/bin/env python3
"""
bisect_wrapper.py - Python wrapper for complex git bisect logic

Provides advanced features:
- Retry logic for flaky tests
- Performance regression detection
- Multiple test execution
- Detailed logging and reporting
- State management across bisect runs

Usage:
    python bisect_wrapper.py --test-command "pytest tests/" --retries 3
    git bisect run python bisect_wrapper.py --test-command "make test"
"""

import argparse
import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List


class BisectRunner:
    """Manages bisect test execution with advanced features."""

    # Exit codes for git bisect
    EXIT_GOOD = 0
    EXIT_BAD = 1
    EXIT_SKIP = 125

    def __init__(self, test_command: str, retries: int = 1, timeout: int = 30,
                 performance_threshold: Optional[float] = None):
        self.test_command = test_command
        self.retries = retries
        self.timeout = timeout
        self.performance_threshold = performance_threshold
        self.commit = self._get_commit_hash()
        self.log_file = f"bisect_log_{self.commit}.json"

    def _get_commit_hash(self) -> str:
        """Get current commit hash."""
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                              capture_output=True, text=True)
        return result.stdout.strip()

    def _get_commit_message(self) -> str:
        """Get current commit message."""
        result = subprocess.run(['git', 'log', '-1', '--format=%s'],
                              capture_output=True, text=True)
        return result.stdout.strip()

    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        print(f"[{timestamp}] {level}: {message}")

    def run_test(self) -> Dict:
        """Run test command and return results."""
        start_time = time.time()

        try:
            result = subprocess.run(
                self.test_command,
                shell=True,
                timeout=self.timeout,
                capture_output=True,
                text=True
            )
            duration = time.time() - start_time

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'timeout': False
            }

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                'success': False,
                'returncode': 124,
                'duration': duration,
                'stdout': '',
                'stderr': f'Test timeout after {self.timeout}s',
                'timeout': True
            }

    def run_with_retries(self) -> Dict:
        """Run test with retry logic for flaky tests."""
        results = []

        for attempt in range(self.retries):
            self.log(f"Attempt {attempt + 1}/{self.retries}")
            result = self.run_test()
            results.append(result)

            if result['timeout']:
                self.log("Test timeout, skipping commit", "WARN")
                return {'decision': 'skip', 'results': results}

            if result['success']:
                self.log(f"Test passed (duration: {result['duration']:.2f}s)")
            else:
                self.log(f"Test failed with code {result['returncode']}")

        # Analyze results
        pass_count = sum(1 for r in results if r['success'])
        fail_count = self.retries - pass_count

        if pass_count == self.retries:
            decision = 'good'
        elif fail_count == self.retries:
            decision = 'bad'
        else:
            # Flaky test - skip this commit
            self.log(f"Flaky test detected ({pass_count}/{self.retries} passed)", "WARN")
            decision = 'skip'

        return {'decision': decision, 'results': results}

    def check_performance(self, duration: float) -> bool:
        """Check if performance meets threshold."""
        if self.performance_threshold is None:
            return True

        if duration > self.performance_threshold:
            self.log(f"Performance regression: {duration:.2f}s > {self.performance_threshold:.2f}s", "WARN")
            return False

        self.log(f"Performance OK: {duration:.2f}s <= {self.performance_threshold:.2f}s")
        return True

    def save_log(self, data: Dict):
        """Save detailed log in JSON format."""
        log_data = {
            'commit': self.commit,
            'message': self._get_commit_message(),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'test_command': self.test_command,
            'retries': self.retries,
            'timeout': self.timeout,
            'performance_threshold': self.performance_threshold,
            **data
        }

        with open(self.log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

        self.log(f"Detailed log saved to {self.log_file}")

    def run(self) -> int:
        """Main execution logic."""
        self.log(f"Testing commit: {self.commit}")
        self.log(f"Message: {self._get_commit_message()}")

        # Check for known broken commits
        commit_msg = self._get_commit_message().lower()
        if any(keyword in commit_msg for keyword in ['wip', 'broken', 'do not merge']):
            self.log("Commit marked as work in progress, skipping", "WARN")
            self.save_log({'decision': 'skip', 'reason': 'WIP commit'})
            return self.EXIT_SKIP

        # Run tests with retries
        result = self.run_with_retries()

        # Check performance if threshold is set
        if result['decision'] == 'good' and self.performance_threshold:
            avg_duration = sum(r['duration'] for r in result['results']) / len(result['results'])
            if not self.check_performance(avg_duration):
                result['decision'] = 'bad'
                result['reason'] = 'performance_regression'

        # Save detailed log
        self.save_log(result)

        # Return appropriate exit code
        if result['decision'] == 'good':
            self.log("✓ GOOD: All tests passed", "SUCCESS")
            return self.EXIT_GOOD
        elif result['decision'] == 'bad':
            self.log("✗ BAD: Tests failed", "ERROR")
            # Print last failure for debugging
            for r in result['results']:
                if not r['success']:
                    print("\nTest output (last 20 lines):")
                    print('\n'.join(r['stderr'].split('\n')[-20:]))
                    break
            return self.EXIT_BAD
        else:
            self.log("⊘ SKIP: Cannot determine result", "WARN")
            return self.EXIT_SKIP


def main():
    parser = argparse.ArgumentParser(
        description='Advanced git bisect test runner with retry logic and performance tracking'
    )
    parser.add_argument('--test-command', required=True,
                       help='Command to run for testing (e.g., "pytest tests/")')
    parser.add_argument('--retries', type=int, default=1,
                       help='Number of times to retry test (default: 1, no retries)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout in seconds for each test run (default: 30)')
    parser.add_argument('--performance-threshold', type=float,
                       help='Maximum acceptable duration in seconds (for performance regression detection)')

    args = parser.parse_args()

    runner = BisectRunner(
        test_command=args.test_command,
        retries=args.retries,
        timeout=args.timeout,
        performance_threshold=args.performance_threshold
    )

    exit_code = runner.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
