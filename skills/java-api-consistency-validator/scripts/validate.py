#!/usr/bin/env python3
"""
Main validator for comparing API behavior between two Java library versions.

Usage:
    python validate.py <old_version_path> <new_version_path> [--output <report.json>]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


class JavaAPIValidator:
    """Validates API consistency between two Java library versions."""

    def __init__(self, old_path: Path, new_path: Path):
        self.old_path = old_path
        self.new_path = new_path
        self.differences = []
        self.breaking_changes = []
        self.warnings = []

    def validate(self) -> Dict[str, Any]:
        """Run complete validation."""
        print("=== Java API Behavior Consistency Validator ===\n")

        print("Analyzing old version...")
        old_api = self._extract_api(self.old_path)

        print("Analyzing new version...")
        new_api = self._extract_api(self.new_path)

        print("\nComparing APIs...")
        self._compare_apis(old_api, new_api)

        report = self._generate_report(old_api, new_api)
        return report

    def _extract_api(self, path: Path) -> Dict[str, Any]:
        """Extract API definitions from Java code."""
        api = {'classes': {}, 'interfaces': {}, 'methods': {}}

        for java_file in path.rglob("*.java"):
            if "test" in str(java_file).lower():
                continue

            try:
                content = java_file.read_text()
                self._parse_java_file(content, api)
            except Exception as e:
                print(f"Warning: Could not parse {java_file}: {e}")

        return api

    def _parse_java_file(self, content: str, api: Dict):
        """Parse Java file for API definitions."""
        # Extract public classes
        class_pattern = r'public\s+(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            api['classes'][class_name] = {
                'name': class_name,
                'extends': match.group(2),
                'implements': match.group(3),
                'methods': self._extract_methods(content, class_name)
            }

        # Extract public interfaces
        interface_pattern = r'public\s+interface\s+(\w+)(?:\s+extends\s+([\w,\s]+))?'
        for match in re.finditer(interface_pattern, content):
            interface_name = match.group(1)
            api['interfaces'][interface_name] = {
                'name': interface_name,
                'extends': match.group(2),
                'methods': self._extract_methods(content, interface_name)
            }

    def _extract_methods(self, content: str, class_name: str) -> Dict[str, Any]:
        """Extract public methods from class/interface."""
        methods = {}
        method_pattern = r'public\s+(?:static\s+)?(?:final\s+)?(\w+(?:<[\w,\s]+>)?)\s+(\w+)\s*\((.*?)\)(?:\s+throws\s+([\w,\s]+))?'

        for match in re.finditer(method_pattern, content):
            return_type = match.group(1)
            method_name = match.group(2)
            params = match.group(3)
            throws = match.group(4)

            methods[method_name] = {
                'name': method_name,
                'return_type': return_type,
                'parameters': self._parse_parameters(params),
                'throws': throws.split(',') if throws else []
            }

        return methods

    def _parse_parameters(self, params_str: str) -> List[Dict[str, str]]:
        """Parse method parameters."""
        if not params_str.strip():
            return []

        params = []
        for param in params_str.split(','):
            param = param.strip()
            if param:
                parts = param.rsplit(' ', 1)
                if len(parts) == 2:
                    params.append({'type': parts[0], 'name': parts[1]})

        return params

    def _compare_apis(self, old_api: Dict, new_api: Dict):
        """Compare two API definitions."""
        self._compare_classes(old_api['classes'], new_api['classes'])
        self._compare_interfaces(old_api['interfaces'], new_api['interfaces'])

    def _compare_classes(self, old_classes: Dict, new_classes: Dict):
        """Compare class definitions."""
        for name in old_classes:
            if name not in new_classes:
                self.breaking_changes.append({
                    'type': 'class_removed',
                    'name': name,
                    'severity': 'breaking',
                    'message': f"Class '{name}' was removed"
                })
            else:
                self._compare_methods(name, old_classes[name]['methods'], new_classes[name]['methods'])

        for name in new_classes:
            if name not in old_classes:
                self.differences.append({
                    'type': 'class_added',
                    'name': name,
                    'severity': 'info',
                    'message': f"New class '{name}' was added"
                })

    def _compare_interfaces(self, old_interfaces: Dict, new_interfaces: Dict):
        """Compare interface definitions."""
        for name in old_interfaces:
            if name not in new_interfaces:
                self.breaking_changes.append({
                    'type': 'interface_removed',
                    'name': name,
                    'severity': 'breaking',
                    'message': f"Interface '{name}' was removed"
                })

    def _compare_methods(self, class_name: str, old_methods: Dict, new_methods: Dict):
        """Compare methods in a class."""
        for method_name in old_methods:
            if method_name not in new_methods:
                self.breaking_changes.append({
                    'type': 'method_removed',
                    'class': class_name,
                    'method': method_name,
                    'severity': 'breaking',
                    'message': f"Method '{class_name}.{method_name}' was removed"
                })
            else:
                self._compare_method_signatures(class_name, method_name,
                                               old_methods[method_name],
                                               new_methods[method_name])

    def _compare_method_signatures(self, class_name: str, method_name: str,
                                   old_method: Dict, new_method: Dict):
        """Compare method signatures."""
        if old_method['return_type'] != new_method['return_type']:
            self.breaking_changes.append({
                'type': 'return_type_changed',
                'class': class_name,
                'method': method_name,
                'old_type': old_method['return_type'],
                'new_type': new_method['return_type'],
                'severity': 'breaking',
                'message': f"Return type changed in '{class_name}.{method_name}'"
            })

        if len(old_method['parameters']) != len(new_method['parameters']):
            self.breaking_changes.append({
                'type': 'parameter_count_changed',
                'class': class_name,
                'method': method_name,
                'severity': 'breaking',
                'message': f"Parameter count changed in '{class_name}.{method_name}'"
            })

    def _generate_report(self, old_api: Dict, new_api: Dict) -> Dict[str, Any]:
        """Generate validation report."""
        return {
            'summary': {
                'breaking_changes': len(self.breaking_changes),
                'warnings': len(self.warnings),
                'info': len(self.differences),
                'total_issues': len(self.breaking_changes) + len(self.warnings) + len(self.differences)
            },
            'breaking_changes': self.breaking_changes,
            'warnings': self.warnings,
            'differences': self.differences,
            'old_api_summary': {
                'classes': len(old_api['classes']),
                'interfaces': len(old_api['interfaces'])
            },
            'new_api_summary': {
                'classes': len(new_api['classes']),
                'interfaces': len(new_api['interfaces'])
            }
        }


def main():
    parser = argparse.ArgumentParser(description='Java API Consistency Validator')
    parser.add_argument('old_version', help='Path to old version')
    parser.add_argument('new_version', help='Path to new version')
    parser.add_argument('--output', '-o', default='api_validation_report.json')

    args = parser.parse_args()

    validator = JavaAPIValidator(Path(args.old_version), Path(args.new_version))
    report = validator.validate()

    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n=== Validation Summary ===")
    print(f"Breaking changes: {report['summary']['breaking_changes']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Info: {report['summary']['info']}")
    print(f"\nReport saved to: {args.output}")

    sys.exit(1 if report['summary']['breaking_changes'] > 0 else 0)


if __name__ == '__main__':
    main()
