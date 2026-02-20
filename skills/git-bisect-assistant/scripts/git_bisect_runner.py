#!/usr/bin/env python3
"""
Git Bisect Runner - Automates git bisect to find the first bad commit
"""

import subprocess
import sys
import argparse
import os
import time
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class BisectResult:
    """Result of a git bisect operation"""
    bad_commit: str
    bad_commit_message: str
    bisect_log: List[str]
    tested_commits: List[Tuple[str, str, str]]  # (hash, result, message)
    confidence: str
    assumptions: List[str]


def run_command(cmd: List[str], cwd: str, timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def test_commit(test_cmd: str, repo_path: str, retries: int, timeout: Optional[int]) -> Tuple[bool, str]:
    """
    Test a commit by running the test command.
    Returns (is_good, reason)
    """
    results = []

    for attempt in range(retries):
        exit_code, stdout, stderr = run_command(
            ["bash", "-c", test_cmd],
            cwd=repo_path,
            timeout=timeout
        )

        results.append(exit_code == 0)

        if retries > 1:
            time.sleep(0.5)  # Brief pause between retries

    # Determine result based on majority vote
    good_count = sum(results)
    is_good = good_count > len(results) / 2

    if retries > 1:
        reason = f"Test passed {good_count}/{retries} times"
    else:
        reason = "Test passed" if is_good else "Test failed"

    return is_good, reason


def get_commit_info(commit_hash: str, repo_path: str) -> str:
    """Get commit message for a given hash"""
    exit_code, stdout, stderr = run_command(
        ["git", "log", "-1", "--pretty=format:%s", commit_hash],
        cwd=repo_path
    )
    return stdout.strip() if exit_code == 0 else "Unknown commit"


def run_bisect(
    repo_path: str,
    good_rev: str,
    bad_rev: str,
    test_cmd: str,
    retries: int = 1,
    timeout: Optional[int] = None
) -> BisectResult:
    """
    Run git bisect to find the first bad commit
    """
    tested_commits = []
    bisect_log = []
    assumptions = []

    # Validate repository
    exit_code, _, _ = run_command(["git", "rev-parse", "--git-dir"], cwd=repo_path)
    if exit_code != 0:
        raise ValueError(f"Not a git repository: {repo_path}")

    # Start bisect
    bisect_log.append("Starting git bisect...")
    run_command(["git", "bisect", "reset"], cwd=repo_path)  # Clean any previous bisect
    run_command(["git", "bisect", "start"], cwd=repo_path)
    run_command(["git", "bisect", "bad", bad_rev], cwd=repo_path)
    exit_code, _, stderr = run_command(["git", "bisect", "good", good_rev], cwd=repo_path)

    if exit_code != 0:
        raise ValueError(f"Failed to start bisect: {stderr}")

    if retries > 1:
        assumptions.append(f"Using {retries} retries per commit to handle flaky tests")

    if timeout:
        assumptions.append(f"Test timeout set to {timeout} seconds")

    # Bisect loop
    while True:
        # Get current commit
        exit_code, current_commit, _ = run_command(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path
        )
        current_commit = current_commit.strip()

        bisect_log.append(f"\nTesting commit: {current_commit[:8]}")

        # Test the commit
        is_good, reason = test_commit(test_cmd, repo_path, retries, timeout)

        commit_msg = get_commit_info(current_commit, repo_path)
        result_str = "good" if is_good else "bad"
        tested_commits.append((current_commit, result_str, commit_msg))
        bisect_log.append(f"  Result: {result_str} - {reason}")
        bisect_log.append(f"  Message: {commit_msg}")

        # Mark commit as good or bad
        mark_cmd = "good" if is_good else "bad"
        exit_code, stdout, stderr = run_command(
            ["git", "bisect", mark_cmd],
            cwd=repo_path
        )

        # Check if bisect is complete
        if "is the first bad commit" in stdout or "is the first bad commit" in stderr:
            bisect_log.append("\n" + stdout)
            break
        elif exit_code != 0:
            bisect_log.append(f"Bisect completed: {stdout}")
            break

    # Get the bad commit
    exit_code, bad_commit, _ = run_command(
        ["git", "bisect", "bad"],
        cwd=repo_path
    )

    # Extract commit hash from bisect output
    for line in (stdout + stderr).split('\n'):
        if "is the first bad commit" in line:
            bad_commit = line.split()[0]
            break

    bad_commit = bad_commit.strip()
    bad_commit_message = get_commit_info(bad_commit, repo_path)

    # Reset bisect
    run_command(["git", "bisect", "reset"], cwd=repo_path)

    # Determine confidence
    if retries > 1:
        confidence = "High (with retry logic for flaky tests)"
    else:
        confidence = "Medium (no retry logic, assumes deterministic tests)"

    return BisectResult(
        bad_commit=bad_commit,
        bad_commit_message=bad_commit_message,
        bisect_log=bisect_log,
        tested_commits=tested_commits,
        confidence=confidence,
        assumptions=assumptions
    )


def format_report(result: BisectResult) -> str:
    """Format the bisect result as a readable report"""
    report = []
    report.append("=" * 70)
    report.append("GIT BISECT REPORT")
    report.append("=" * 70)
    report.append("")
    report.append(f"First Bad Commit: {result.bad_commit}")
    report.append(f"Commit Message: {result.bad_commit_message}")
    report.append("")
    report.append(f"Confidence Level: {result.confidence}")
    report.append("")

    if result.assumptions:
        report.append("Assumptions:")
        for assumption in result.assumptions:
            report.append(f"  - {assumption}")
        report.append("")

    report.append("Tested Commits:")
    report.append("-" * 70)
    for commit_hash, result_str, message in result.tested_commits:
        report.append(f"  {commit_hash[:8]} [{result_str.upper()}] {message}")
    report.append("")

    report.append("Bisect Log:")
    report.append("-" * 70)
    for line in result.bisect_log:
        report.append(line)
    report.append("")
    report.append("=" * 70)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Automate git bisect to find the first bad commit"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--good",
        required=True,
        help="Known good revision (commit hash, tag, or branch)"
    )
    parser.add_argument(
        "--bad",
        default="HEAD",
        help="Known bad revision (default: HEAD)"
    )
    parser.add_argument(
        "--test",
        required=True,
        help="Test command to determine if commit is good or bad"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Number of times to run test per commit (for flaky tests)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for test execution"
    )

    args = parser.parse_args()

    try:
        print(f"Starting git bisect in {args.repo}")
        print(f"Good revision: {args.good}")
        print(f"Bad revision: {args.bad}")
        print(f"Test command: {args.test}")
        print()

        result = run_bisect(
            repo_path=args.repo,
            good_rev=args.good,
            bad_rev=args.bad,
            test_cmd=args.test,
            retries=args.retries,
            timeout=args.timeout
        )

        print(format_report(result))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
