#!/usr/bin/env python3
"""
Test Case Reducer - Automatically reduces test cases to minimal form
Uses delta debugging and other reduction algorithms
"""

import subprocess
import sys
import argparse
import os
import time
from typing import List, Callable, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ReductionStrategy(Enum):
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"


@dataclass
class ReductionResult:
    """Result of test case reduction"""
    original_size: int
    reduced_size: int
    reduction_ratio: float
    removed_elements: List[str]
    iterations: int
    execution_time: float
    final_test: str


class TestOracle:
    """Defines the failure condition"""

    def __init__(self, oracle_type: str, expected_value: str):
        self.oracle_type = oracle_type
        self.expected_value = expected_value

    def check_failure(self, exit_code: int, stdout: str, stderr: str) -> bool:
        """Check if the test exhibits the expected failure"""
        if self.oracle_type == "exit_code":
            return exit_code == int(self.expected_value)
        elif self.oracle_type == "exception":
            return self.expected_value in stderr
        elif self.oracle_type == "output_pattern":
            return self.expected_value in stdout or self.expected_value in stderr
        elif self.oracle_type == "assertion":
            return self.expected_value in stderr
        else:
            return exit_code != 0


class TestCaseReducer:
    """Reduces test cases using delta debugging"""

    def __init__(self,
                 test_command: str,
                 oracle: TestOracle,
                 timeout: Optional[int] = None,
                 strategy: ReductionStrategy = ReductionStrategy.BALANCED):
        self.test_command = test_command
        self.oracle = oracle
        self.timeout = timeout
        self.strategy = strategy
        self.iterations = 0
        self.removed_elements = []

    def run_test(self, test_content: str, test_file: str) -> bool:
        """Run test and check if it still fails as expected"""
        # Write test content to file
        with open(test_file, 'w') as f:
            f.write(test_content)

        # Run test command
        try:
            result = subprocess.run(
                self.test_command.split(),
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            # Check if failure matches oracle
            return self.oracle.check_failure(
                result.returncode,
                result.stdout,
                result.stderr
            )
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def delta_debugging(self, elements: List[str], test_file: str) -> List[str]:
        """Apply delta debugging algorithm to reduce elements"""
        n = 2  # Start with 2 chunks

        while len(elements) > 1:
            chunk_size = len(elements) // n
            if chunk_size == 0:
                chunk_size = 1

            reduced = False

            # Try removing each chunk
            for i in range(n):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, len(elements))

                # Create candidate with chunk removed
                candidate = elements[:start] + elements[end:]

                if len(candidate) == 0:
                    continue

                self.iterations += 1
                test_content = '\n'.join(candidate)

                if self.run_test(test_content, test_file):
                    # Reduction successful
                    removed = elements[start:end]
                    self.removed_elements.extend(removed)
                    elements = candidate
                    reduced = True
                    n = max(2, n - 1)  # Decrease granularity
                    break

            if not reduced:
                # Try with finer granularity
                if n >= len(elements):
                    break
                n = min(n * 2, len(elements))

        return elements

    def greedy_reduction(self, elements: List[str], test_file: str) -> List[str]:
        """Greedy line-by-line reduction"""
        i = 0
        while i < len(elements):
            # Try removing element at position i
            candidate = elements[:i] + elements[i+1:]

            if len(candidate) == 0:
                i += 1
                continue

            self.iterations += 1
            test_content = '\n'.join(candidate)

            if self.run_test(test_content, test_file):
                # Removal successful
                self.removed_elements.append(elements[i])
                elements = candidate
                # Don't increment i, check same position again
            else:
                i += 1

        return elements

    def binary_search_reduction(self, elements: List[str], test_file: str) -> List[str]:
        """Binary search reduction - remove half at a time"""
        while len(elements) > 1:
            mid = len(elements) // 2

            # Try first half
            self.iterations += 1
            candidate = elements[:mid]
            test_content = '\n'.join(candidate)

            if self.run_test(test_content, test_file):
                self.removed_elements.extend(elements[mid:])
                elements = candidate
                continue

            # Try second half
            self.iterations += 1
            candidate = elements[mid:]
            test_content = '\n'.join(candidate)

            if self.run_test(test_content, test_file):
                self.removed_elements.extend(elements[:mid])
                elements = candidate
                continue

            # Can't reduce further with binary search
            break

        return elements

    def reduce(self, test_file: str) -> ReductionResult:
        """Main reduction entry point"""
        start_time = time.time()

        # Read original test
        with open(test_file, 'r') as f:
            original_content = f.read()

        original_lines = original_content.split('\n')
        original_size = len(original_lines)

        # Verify original test fails as expected
        if not self.run_test(original_content, test_file):
            raise ValueError("Original test does not exhibit expected failure")

        # Apply reduction strategy
        if self.strategy == ReductionStrategy.AGGRESSIVE:
            # Binary search first, then greedy
            reduced_lines = self.binary_search_reduction(original_lines, test_file)
            reduced_lines = self.greedy_reduction(reduced_lines, test_file)
        elif self.strategy == ReductionStrategy.BALANCED:
            # Delta debugging
            reduced_lines = self.delta_debugging(original_lines, test_file)
        else:  # CONSERVATIVE
            # Greedy only
            reduced_lines = self.greedy_reduction(original_lines, test_file)

        reduced_content = '\n'.join(reduced_lines)
        reduced_size = len(reduced_lines)

        # Write final reduced test
        with open(test_file, 'w') as f:
            f.write(reduced_content)

        execution_time = time.time() - start_time
        reduction_ratio = (original_size - reduced_size) / original_size * 100

        return ReductionResult(
            original_size=original_size,
            reduced_size=reduced_size,
            reduction_ratio=reduction_ratio,
            removed_elements=self.removed_elements,
            iterations=self.iterations,
            execution_time=execution_time,
            final_test=reduced_content
        )


def format_report(result: ReductionResult) -> str:
    """Format reduction result as a report"""
    report = []
    report.append("=" * 70)
    report.append("TEST CASE REDUCTION REPORT")
    report.append("=" * 70)
    report.append("")
    report.append(f"Original size: {result.original_size} lines")
    report.append(f"Reduced size: {result.reduced_size} lines")
    report.append(f"Reduction ratio: {result.reduction_ratio:.1f}%")
    report.append(f"Lines removed: {result.original_size - result.reduced_size}")
    report.append("")
    report.append(f"Iterations: {result.iterations}")
    report.append(f"Execution time: {result.execution_time:.2f} seconds")
    report.append("")
    report.append("Reduced test case:")
    report.append("-" * 70)
    report.append(result.final_test)
    report.append("-" * 70)
    report.append("")

    if result.removed_elements:
        report.append(f"Removed {len(result.removed_elements)} elements")
        report.append("(First 10 shown):")
        for elem in result.removed_elements[:10]:
            report.append(f"  - {elem[:60]}...")

    report.append("")
    report.append("=" * 70)

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Automatically reduce test cases to minimal form"
    )
    parser.add_argument(
        "test_file",
        help="Path to the test file to reduce"
    )
    parser.add_argument(
        "--command",
        required=True,
        help="Command to run the test (e.g., 'python test.py')"
    )
    parser.add_argument(
        "--oracle",
        default="exit_code",
        choices=["exit_code", "exception", "output_pattern", "assertion"],
        help="Type of failure oracle"
    )
    parser.add_argument(
        "--expected",
        default="1",
        help="Expected value for oracle (exit code, exception name, pattern)"
    )
    parser.add_argument(
        "--strategy",
        default="balanced",
        choices=["aggressive", "balanced", "conservative"],
        help="Reduction strategy"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for test execution"
    )

    args = parser.parse_args()

    # Create oracle
    oracle = TestOracle(args.oracle, args.expected)

    # Create reducer
    reducer = TestCaseReducer(
        test_command=args.command,
        oracle=oracle,
        timeout=args.timeout,
        strategy=ReductionStrategy(args.strategy)
    )

    try:
        print(f"Reducing test case: {args.test_file}")
        print(f"Strategy: {args.strategy}")
        print(f"Oracle: {args.oracle} = {args.expected}")
        print()

        result = reducer.reduce(args.test_file)

        print(format_report(result))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
