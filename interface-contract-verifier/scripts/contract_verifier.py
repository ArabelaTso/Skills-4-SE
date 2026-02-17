#!/usr/bin/env python3
"""
contract_verifier.py - Verify contract preservation between versions

Checks:
- Preconditions not strengthened
- Postconditions not weakened
- Invariants maintained
"""

import argparse
import json
import sys
from typing import Dict, List


class ContractVerifier:
    """Verify contract preservation."""

    def __init__(self, old_file: str, new_file: str):
        self.old_file = old_file
        self.new_file = new_file

    def load_contracts(self, file_path: str) -> Dict:
        """Load contracts from JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def verify(self) -> Dict:
        """Verify contract preservation."""
        print(f"Loading old contracts from {self.old_file}...")
        old_data = self.load_contracts(self.old_file)
        old_contracts = old_data.get('contracts', {})

        print(f"Loading new contracts from {self.new_file}...")
        new_data = self.load_contracts(self.new_file)
        new_contracts = new_data.get('contracts', {})

        violations = []

        # Verify class contracts
        for class_name in old_contracts.get('classes', {}):
            old_class = old_contracts['classes'][class_name]
            new_class = new_contracts.get('classes', ).get(class_name)

            if not new_class:
                violations.append({
                    'type': 'missing_class',
                    'severity': 'error',
                    'class': class_name,
                    'message': f'Class {class_name} removed'
                })
                continue

            # Verify invariants
            violations.extend(self._verify_invariants(class_name, old_class, new_class))

            # Verify methods
            for method_name in old_class.get('methods', {}):
                old_method = old_class['methods'][method_name]
                new_method = new_class.get('methods', {}).get(method_name)

                if not new_method:
                    violations.append({
                        'type': 'missing_method',
                        'severity': 'error',
                        'class': class_name,
                        'method': method_name,
                        'message': f'Method {method_name} removed'
                    })
                    continue

                violations.extend(self._verify_method(class_name, method_name, old_method, new_method))

        # Verify function contracts
        for func_name in old_contracts.get('functions', {}):
            old_func = old_contracts['functions'][func_name]
            new_func = new_contracts.get('functions', {}).get(func_name)

            if not new_func:
                violations.append({
                    'type': 'missing_function',
                    'severity': 'error',
                    'function': func_name,
                    'message': f'Function {func_name} removed'
                })
                continue

            violations.extend(self._verify_method(None, func_name, old_func, new_func))

        # Generate summary
        summary = {
            'total_violations': len(violations),
            'critical': sum(1 for v in violations if v.get('severity') == 'critical'),
            'errors': sum(1 for v in violations if v.get('severity') == 'error'),
            'warnings': sum(1 for v in violations if v.get('severity') == 'warning')
        }

        return {
            'summary': summary,
            'violations': violations,
            'recommendations': self._generate_recommendations(violations)
        }

    def _verify_invariants(self, class_name: str, old_class: Dict, new_class: Dict) -> List[Dict]:
        """Verify class invariants are maintained."""
        violations = []
        old_invariants = set(old_class.get('invariants', []))
        new_invariants = set(new_class.get('invariants', []))

        # Check for removed invariants
        removed = old_invariants - new_invariants
        for inv in removed:
            violations.append({
                'type': 'broken_invariant',
                'severity': 'critical',
                'class': class_name,
                'invariant': inv,
                'message': f'Invariant removed: {inv}',
                'guidance': 'Restore invariant or verify all methods maintain it'
            })

        return violations

    def _verify_method(self, class_name: str, method_name: str,
                      old_method: Dict, new_method: Dict) -> List[Dict]:
        """Verify method contracts."""
        violations = []

        # Verify preconditions (must not be strengthened)
        old_pre = set(old_method.get('preconditions', []))
        new_pre = set(new_method.get('preconditions', []))

        # New preconditions that weren't in old (potentially strengthened)
        added_pre = new_pre - old_pre
        if added_pre:
            for pre in added_pre:
                violations.append({
                    'type': 'strengthened_precondition',
                    'severity': 'error',
                    'class': class_name,
                    'method': method_name,
                    'old_preconditions': list(old_pre),
                    'new_precondition': pre,
                    'message': f'New precondition added: {pre}',
                    'guidance': 'Remove precondition or verify it accepts all previously valid inputs'
                })

        # Verify postconditions (must not be weakened)
        old_post = set(old_method.get('postconditions', []))
        new_post = set(new_method.get('postconditions', []))

        # Old postconditions that aren't in new (potentially weakened)
        removed_post = old_post - new_post
        if removed_post:
            for post in removed_post:
                violations.append({
                    'type': 'weakened_postcondition',
                    'severity': 'error',
                    'class': class_name,
                    'method': method_name,
                    'old_postcondition': post,
                    'new_postconditions': list(new_post),
                    'message': f'Postcondition removed: {post}',
                    'guidance': 'Restore postcondition or strengthen implementation'
                })

        return violations

    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate recommendations based on violations."""
        recommendations = []

        critical_count = sum(1 for v in violations if v.get('severity') == 'critical')
        error_count = sum(1 for v in violations if v.get('severity') == 'error')

        if critical_count > 0:
            recommendations.append(f'CRITICAL: Fix {critical_count} broken invariant(s) immediately')

        if error_count > 0:
            recommendations.append(f'Fix {error_count} contract violation(s) before deployment')

        recommendations.append('Review all violations and apply suggested guidance')
        recommendations.append('Add contract tests to prevent future violations')

        return recommendations

    def print_report(self, report: Dict):
        """Print verification report."""
        print("\n" + "="*80)
        print("CONTRACT VERIFICATION REPORT")
        print("="*80)

        summary = report['summary']
        print(f"\nTotal violations: {summary['total_violations']}")
        print(f"Critical: {summary['critical']}")
        print(f"Errors: {summary['errors']}")
        print(f"Warnings: {summary['warnings']}")

        # Print critical violations
        critical = [v for v in report['violations'] if v.get('severity') == 'critical']
        if critical:
            print("\n" + "="*80)
            print("CRITICAL VIOLATIONS")
            print("="*80)
            for v in critical:
                print(f"\n✗ {v['class']}: {v.get('invariant', 'N/A')}")
                print(f"  {v['message']}")
                print(f"  Guidance: {v.get('guidance', 'N/A')}")

        # Print error violations
        errors = [v for v in report['violations'] if v.get('severity') == 'error']
        if errors:
            print("\n" + "="*80)
            print("ERROR VIOLATIONS")
            print("="*80)
            for v in errors[:5]:  # Show first 5
                location = f"{v.get('class', '')}.{v.get('method', v.get('function', ''))}"
                print(f"\n✗ {location}")
                print(f"  Type: {v['type']}")
                print(f"  {v['message']}")
                if v.get('guidance'):
                    print(f"  Guidance: {v['guidance']}")

        # Print recommendations
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")


def main():
    parser = argparse.ArgumentParser(
        description='Verify contract preservation between versions'
    )
    parser.add_argument('--old', required=True,
                       help='Old contracts JSON file')
    parser.add_argument('--new', required=True,
                       help='New contracts JSON file')
    parser.add_argument('--output', required=True,
                       help='Output file for verification report')

    args = parser.parse_args()

    try:
        verifier = ContractVerifier(args.old, args.new)
        report = verifier.verify()
        verifier.print_report(report)

        # Save report
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to: {args.output}")

        # Exit with error if violations found
        if report['summary']['total_violations'] > 0:
            print(f"\n⚠ Found {report['summary']['total_violations']} violation(s)")
            sys.exit(1)
        else:
            print("\n✓ No contract violations found")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
