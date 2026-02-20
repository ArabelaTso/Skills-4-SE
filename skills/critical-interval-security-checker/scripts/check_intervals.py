#!/usr/bin/env python3
"""
Analyze code for security-critical time interval issues.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class IntervalSecurityChecker:
    """Check code for timing security vulnerabilities."""

    def __init__(self):
        self.issues = defaultdict(list)

        # Patterns for detecting time-related code
        self.time_patterns = {
            'python': {
                'timedelta': r'timedelta\s*\(\s*(?:days|hours|minutes|seconds)\s*=\s*(\d+)',
                'jwt_decode': r'jwt\.decode\([^,]+,\s*[^,]+(?:,\s*(?:verify|options)\s*=\s*(?:False|\{[^}]*verify[^}]*False[^}]*\}))?',
                'expiration_field': r'["\'](?:exp|expires_at|expiry|valid_until|expires)["\']',
                'datetime_now': r'datetime\.(?:now|utcnow)\(\)',
                'rate_limit': r'@(?:limiter\.limit|RateLimit)',
                'sleep': r'time\.sleep\(',
            },
            'javascript': {
                'timeout': r'(?:setTimeout|setInterval)\s*\([^,]+,\s*(\d+)',
                'date_now': r'Date\.now\(\)',
                'jwt_decode': r'jwt\.(?:decode|verify)\(',
                'expiration_field': r'["\'](?:exp|expiresAt|expiry|validUntil|expires)["\']',
                'rate_limit': r'rateLimit\s*\(',
            },
            'java': {
                'duration': r'Duration\.of(?:Days|Hours|Minutes|Seconds)\s*\(\s*(\d+)',
                'jwt_parse': r'Jwts\.parser\(\)',
                'expiration': r'setExpiration\s*\(',
                'current_time': r'System\.currentTimeMillis\(\)',
            }
        }

    def check_file(self, filepath: Path, language: str) -> List[Dict]:
        """Check a single file for timing security issues."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return []

        lines = content.split('\n')
        file_issues = []

        # Check for various patterns
        file_issues.extend(self._check_missing_expiration(filepath, lines, language))
        file_issues.extend(self._check_excessive_timeouts(filepath, lines, language))
        file_issues.extend(self._check_no_rate_limiting(filepath, lines, language))
        file_issues.extend(self._check_client_side_only(filepath, lines, language))
        file_issues.extend(self._check_hardcoded_timeouts(filepath, lines, language))

        return file_issues

    def _check_missing_expiration(self, filepath: Path, lines: List[str], language: str) -> List[Dict]:
        """Check for expiration fields that are set but never validated."""
        issues = []

        # Find lines that set expiration
        expiration_sets = []
        for i, line in enumerate(lines, 1):
            if re.search(self.time_patterns[language].get('expiration_field', ''), line):
                expiration_sets.append(i)

        # Check if there are validation checks nearby
        for line_num in expiration_sets:
            # Look in surrounding context (±20 lines)
            context_start = max(0, line_num - 20)
            context_end = min(len(lines), line_num + 20)
            context = '\n'.join(lines[context_start:context_end])

            # Look for expiration checks
            has_check = False
            if language == 'python':
                has_check = bool(re.search(r'(?:exp|expires_at|expiry)\s*[<>]', context))
            elif language == 'javascript':
                has_check = bool(re.search(r'(?:exp|expiresAt|expiry)\s*[<>]', context))
            elif language == 'java':
                has_check = bool(re.search(r'(?:isExpired|getExpiration|before|after)', context))

            if not has_check:
                issues.append({
                    'type': 'missing_expiration_check',
                    'severity': 'high',
                    'file': str(filepath),
                    'line': line_num,
                    'message': 'Expiration field set but no validation found nearby',
                    'recommendation': 'Add expiration check before using token/session'
                })

        return issues

    def _check_excessive_timeouts(self, filepath: Path, lines: List[str], language: str) -> List[Dict]:
        """Check for unreasonably long timeout values."""
        issues = []

        # Thresholds (in seconds)
        thresholds = {
            'reset_token': 3600,  # 1 hour
            'session': 86400,  # 24 hours
            'access_token': 900,  # 15 minutes
        }

        for i, line in enumerate(lines, 1):
            # Check for timedelta/duration patterns
            if language == 'python':
                match = re.search(r'timedelta\s*\(\s*days\s*=\s*(\d+)', line)
                if match:
                    days = int(match.group(1))
                    if days > 1 and ('reset' in line.lower() or 'token' in line.lower()):
                        issues.append({
                            'type': 'excessive_timeout',
                            'severity': 'medium',
                            'file': str(filepath),
                            'line': i,
                            'message': f'Reset token timeout too long: {days} days',
                            'recommendation': 'Use 15-60 minutes for reset tokens'
                        })

                match = re.search(r'timedelta\s*\(\s*hours\s*=\s*(\d+)', line)
                if match:
                    hours = int(match.group(1))
                    if hours > 24 and 'session' in line.lower():
                        issues.append({
                            'type': 'excessive_timeout',
                            'severity': 'medium',
                            'file': str(filepath),
                            'line': i,
                            'message': f'Session timeout too long: {hours} hours',
                            'recommendation': 'Use 8-12 hours for session timeout'
                        })

            elif language == 'javascript':
                # Check for millisecond values
                match = re.search(r'(\d+)\s*\*\s*24\s*\*\s*60\s*\*\s*60\s*\*\s*1000', line)
                if match:
                    days = int(match.group(1))
                    if days > 30:
                        issues.append({
                            'type': 'excessive_timeout',
                            'severity': 'medium',
                            'file': str(filepath),
                            'line': i,
                            'message': f'Timeout too long: {days} days',
                            'recommendation': 'Review if this timeout is appropriate'
                        })

        return issues

    def _check_no_rate_limiting(self, filepath: Path, lines: List[str], language: str) -> List[Dict]:
        """Check for authentication endpoints without rate limiting."""
        issues = []

        # Look for authentication-related functions/routes
        auth_keywords = ['login', 'authenticate', 'reset', 'password', 'register', 'signup']

        for i, line in enumerate(lines, 1):
            # Check if this is an auth endpoint
            is_auth_endpoint = False
            for keyword in auth_keywords:
                if keyword in line.lower() and ('def ' in line or 'function ' in line or '@app.route' in line or 'app.post' in line):
                    is_auth_endpoint = True
                    break

            if is_auth_endpoint:
                # Check if rate limiting is applied (look in surrounding lines)
                context_start = max(0, i - 5)
                context_end = min(len(lines), i + 1)
                context = '\n'.join(lines[context_start:context_end])

                has_rate_limit = False
                if language == 'python':
                    has_rate_limit = bool(re.search(r'@limiter\.limit|@RateLimit', context))
                elif language == 'javascript':
                    has_rate_limit = bool(re.search(r'rateLimit|rateLimiter', context))

                if not has_rate_limit:
                    issues.append({
                        'type': 'no_rate_limiting',
                        'severity': 'high',
                        'file': str(filepath),
                        'line': i,
                        'message': 'Authentication endpoint without rate limiting',
                        'recommendation': 'Add rate limiting (e.g., 5 attempts per 15 minutes)'
                    })

        return issues

    def _check_client_side_only(self, filepath: Path, lines: List[str], language: str) -> List[Dict]:
        """Check for client-side only expiration checks."""
        issues = []

        for i, line in enumerate(lines, 1):
            # Look for JWT decode without verification
            if language == 'python':
                if 'jwt.decode' in line and ('verify=False' in line or 'verify_signature' in line):
                    issues.append({
                        'type': 'client_side_only',
                        'severity': 'critical',
                        'file': str(filepath),
                        'line': i,
                        'message': 'JWT decoded without signature verification',
                        'recommendation': 'Remove verify=False to enable expiration checking'
                    })

        return issues

    def _check_hardcoded_timeouts(self, filepath: Path, lines: List[str], language: str) -> List[Dict]:
        """Check for magic number timeouts."""
        issues = []

        # Common magic numbers (in seconds)
        magic_numbers = {
            '3600': '1 hour',
            '86400': '1 day',
            '604800': '1 week',
            '2592000': '30 days',
        }

        for i, line in enumerate(lines, 1):
            for number, description in magic_numbers.items():
                if number in line and not re.search(r'[A-Z_]+\s*=\s*' + number, line):
                    # Found magic number not in a constant definition
                    issues.append({
                        'type': 'hardcoded_timeout',
                        'severity': 'low',
                        'file': str(filepath),
                        'line': i,
                        'message': f'Magic number timeout: {number} ({description})',
                        'recommendation': 'Use named constant for timeout value'
                    })

        return issues


def print_report(issues: List[Dict]):
    """Print security check report."""
    if not issues:
        print("✅ No timing security issues found!")
        return

    print("=" * 80)
    print("CRITICAL INTERVAL SECURITY CHECK REPORT")
    print("=" * 80)
    print()

    # Group by severity
    by_severity = defaultdict(list)
    for issue in issues:
        by_severity[issue['severity']].append(issue)

    severity_order = ['critical', 'high', 'medium', 'low']
    severity_icons = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🔵'
    }

    for severity in severity_order:
        if severity not in by_severity:
            continue

        issues_list = by_severity[severity]
        print(f"{severity_icons[severity]} {severity.upper()} ({len(issues_list)} issues)")
        print("-" * 80)

        for issue in issues_list:
            print(f"\n  {issue['file']}:{issue['line']}")
            print(f"  Issue: {issue['message']}")
            print(f"  Fix: {issue['recommendation']}")

        print()

    print("=" * 80)
    print(f"Total issues found: {len(issues)}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Check code for security-critical time interval issues'
    )
    parser.add_argument(
        'path',
        type=Path,
        help='File or directory to check'
    )
    parser.add_argument(
        '--language',
        choices=['python', 'javascript', 'java', 'auto'],
        default='auto',
        help='Programming language (default: auto-detect)'
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        return 1

    checker = IntervalSecurityChecker()
    all_issues = []

    # Determine files to check
    if args.path.is_file():
        files = [args.path]
    else:
        # Scan directory
        extensions = {
            'python': ['.py'],
            'javascript': ['.js', '.ts', '.jsx', '.tsx'],
            'java': ['.java']
        }

        files = []
        for lang, exts in extensions.items():
            for ext in exts:
                files.extend(args.path.rglob(f'*{ext}'))

    # Check each file
    for filepath in files:
        # Auto-detect language
        language = args.language
        if language == 'auto':
            ext = filepath.suffix
            if ext == '.py':
                language = 'python'
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                language = 'javascript'
            elif ext == '.java':
                language = 'java'
            else:
                continue

        issues = checker.check_file(filepath, language)
        all_issues.extend(issues)

    # Print report
    print_report(all_issues)

    return 0 if not all_issues else 1


if __name__ == '__main__':
    sys.exit(main())
