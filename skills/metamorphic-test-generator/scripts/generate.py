#!/usr/bin/env python3
"""
Metamorphic Test Generator
Generates test cases by applying metamorphic transformations to existing tests.
"""

import argparse
import json
import os
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Callable, Tuple
import copy


class MetamorphicProperty:
    """Base class for metamorphic properties"""

    def __init__(self, name: str):
        self.name = name

    def transform_input(self, input_data: Any) -> Any:
        """Transform the input according to the property"""
        raise NotImplementedError

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        """Verify if the metamorphic relation holds"""
        raise NotImplementedError


class PermutationProperty(MetamorphicProperty):
    """Permutation: reordering inputs should not affect output"""

    def __init__(self):
        super().__init__("permutation")

    def transform_input(self, input_data: Any) -> Any:
        if isinstance(input_data, list):
            import random
            transformed = input_data.copy()
            random.shuffle(transformed)
            return transformed
        elif isinstance(input_data, dict) and 'list' in input_data:
            transformed = copy.deepcopy(input_data)
            import random
            random.shuffle(transformed['list'])
            return transformed
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        if isinstance(original_output, (list, set)):
            return sorted(original_output) == sorted(transformed_output), \
                   f"Permutation property: outputs should be equivalent"
        return original_output == transformed_output, \
               f"Permutation property: outputs should be equal"


class AdditionProperty(MetamorphicProperty):
    """Addition: adding elements should increase or maintain result"""

    def __init__(self):
        super().__init__("addition")

    def transform_input(self, input_data: Any) -> Any:
        if isinstance(input_data, list):
            return input_data + [input_data[0]] if input_data else input_data
        elif isinstance(input_data, dict) and 'list' in input_data:
            transformed = copy.deepcopy(input_data)
            if transformed['list']:
                transformed['list'].append(transformed['list'][0])
            return transformed
        elif isinstance(input_data, (int, float)):
            return input_data + 1
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        if isinstance(original_output, (int, float)) and isinstance(transformed_output, (int, float)):
            return transformed_output >= original_output, \
                   f"Addition property: output should increase or stay same"
        elif isinstance(original_output, list):
            return len(transformed_output) >= len(original_output), \
                   f"Addition property: output size should increase or stay same"
        return True, "Addition property: cannot verify for this output type"


class MultiplicationProperty(MetamorphicProperty):
    """Multiplication: scaling inputs should scale outputs proportionally"""

    def __init__(self, factor: float = 2.0):
        super().__init__("multiplication")
        self.factor = factor

    def transform_input(self, input_data: Any) -> Any:
        if isinstance(input_data, (int, float)):
            return input_data * self.factor
        elif isinstance(input_data, list) and all(isinstance(x, (int, float)) for x in input_data):
            return [x * self.factor for x in input_data]
        elif isinstance(input_data, dict):
            transformed = copy.deepcopy(input_data)
            for key, value in transformed.items():
                if isinstance(value, (int, float)):
                    transformed[key] = value * self.factor
            return transformed
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        if isinstance(original_output, (int, float)) and isinstance(transformed_output, (int, float)):
            expected = original_output * self.factor
            tolerance = abs(expected * 0.01)  # 1% tolerance
            return abs(transformed_output - expected) <= tolerance, \
                   f"Multiplication property: output should scale by factor {self.factor}"
        return True, "Multiplication property: cannot verify for this output type"


class InverseProperty(MetamorphicProperty):
    """Inverse: applying inverse operation should return original"""

    def __init__(self):
        super().__init__("inverse")

    def transform_input(self, input_data: Any) -> Any:
        if isinstance(input_data, list):
            return list(reversed(input_data))
        elif isinstance(input_data, str):
            return input_data[::-1]
        elif isinstance(input_data, (int, float)):
            return -input_data
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        # For inverse, we need to apply inverse to output as well
        if isinstance(transformed_output, list):
            return original_output == list(reversed(transformed_output)), \
                   f"Inverse property: applying inverse twice should return original"
        elif isinstance(transformed_output, str):
            return original_output == transformed_output[::-1], \
                   f"Inverse property: applying inverse twice should return original"
        return True, "Inverse property: cannot verify for this output type"


class MonotonicityProperty(MetamorphicProperty):
    """Monotonicity: increasing input should increase or maintain output"""

    def __init__(self):
        super().__init__("monotonicity")

    def transform_input(self, input_data: Any) -> Any:
        if isinstance(input_data, (int, float)):
            return input_data + abs(input_data) * 0.1 + 1
        elif isinstance(input_data, list) and all(isinstance(x, (int, float)) for x in input_data):
            return [x + abs(x) * 0.1 + 1 for x in input_data]
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        if isinstance(original_output, (int, float)) and isinstance(transformed_output, (int, float)):
            return transformed_output >= original_output, \
                   f"Monotonicity property: increasing input should not decrease output"
        return True, "Monotonicity property: cannot verify for this output type"


class EquivalenceProperty(MetamorphicProperty):
    """Equivalence: different representations should yield same result"""

    def __init__(self):
        super().__init__("equivalence")

    def transform_input(self, input_data: Any) -> Any:
        # Transform to equivalent representation
        if isinstance(input_data, str):
            return input_data.strip()
        elif isinstance(input_data, list):
            return tuple(input_data)
        elif isinstance(input_data, tuple):
            return list(input_data)
        return input_data

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        # Outputs should be equivalent
        if type(original_output) != type(transformed_output):
            if isinstance(original_output, (list, tuple)) and isinstance(transformed_output, (list, tuple)):
                return list(original_output) == list(transformed_output), \
                       f"Equivalence property: different representations should yield same result"
        return original_output == transformed_output, \
               f"Equivalence property: outputs should be equal"


class MetamorphicTestGenerator:
    """Main class for generating metamorphic tests"""

    def __init__(self, program_path: str, test_dir: str, properties: List[str]):
        self.program_path = program_path
        self.test_dir = test_dir
        self.properties = self._initialize_properties(properties)
        self.original_tests = []
        self.generated_tests = []
        self.violations = []
        self.anomalies = []

    def _initialize_properties(self, property_names: List[str]) -> List[MetamorphicProperty]:
        """Initialize metamorphic properties from names"""
        property_map = {
            'permutation': PermutationProperty(),
            'addition': AdditionProperty(),
            'multiplication': MultiplicationProperty(),
            'inverse': InverseProperty(),
            'monotonicity': MonotonicityProperty(),
            'equivalence': EquivalenceProperty()
        }

        properties = []
        for name in property_names:
            if name.lower() in property_map:
                properties.append(property_map[name.lower()])
            else:
                print(f"Warning: Unknown property '{name}', skipping")

        return properties

    def load_tests(self):
        """Load original test cases from test directory"""
        test_path = Path(self.test_dir)

        if test_path.is_file() and test_path.suffix == '.json':
            # Load from JSON file
            with open(test_path, 'r') as f:
                data = json.load(f)
                self.original_tests = data if isinstance(data, list) else [data]
        elif test_path.is_dir():
            # Load from directory of JSON files
            for test_file in test_path.glob('*.json'):
                with open(test_file, 'r') as f:
                    test_data = json.load(f)
                    if isinstance(test_data, list):
                        self.original_tests.extend(test_data)
                    else:
                        self.original_tests.append(test_data)
        else:
            raise ValueError(f"Test path must be a JSON file or directory: {self.test_dir}")

        print(f"Loaded {len(self.original_tests)} original test cases")

    def execute_program(self, input_data: Any) -> Any:
        """Execute the program with given input and return output"""
        program_ext = Path(self.program_path).suffix

        # Prepare input
        input_json = json.dumps(input_data)

        try:
            if program_ext == '.py':
                # Python program
                result = subprocess.run(
                    ['python3', self.program_path],
                    input=input_json,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10
                )
            elif program_ext == '.js':
                # JavaScript program
                result = subprocess.run(
                    ['node', self.program_path],
                    input=input_json,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10
                )
            elif program_ext == '.java':
                # Java program (assumes compiled)
                class_name = Path(self.program_path).stem
                result = subprocess.run(
                    ['java', class_name],
                    input=input_json,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10,
                    cwd=Path(self.program_path).parent
                )
            else:
                # Try to execute directly
                result = subprocess.run(
                    [self.program_path],
                    input=input_json,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10
                )

            if result.returncode != 0:
                return {'error': result.stderr}

            # Try to parse output as JSON
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                return result.stdout.strip()

        except subprocess.TimeoutExpired:
            return {'error': 'Execution timeout'}
        except Exception as e:
            return {'error': str(e)}

    def generate_tests(self):
        """Generate new test cases using metamorphic properties"""
        print(f"\nGenerating tests using {len(self.properties)} properties...")

        for test_idx, original_test in enumerate(self.original_tests):
            input_data = original_test.get('input', original_test)

            # Execute original test
            original_output = self.execute_program(input_data)

            # Apply each property
            for prop in self.properties:
                try:
                    # Transform input
                    transformed_input = prop.transform_input(input_data)

                    # Skip if transformation didn't change input
                    if transformed_input == input_data:
                        continue

                    # Execute with transformed input
                    transformed_output = self.execute_program(transformed_input)

                    # Verify metamorphic relation
                    is_valid, message = prop.verify_output(
                        original_output, transformed_output,
                        input_data, transformed_input
                    )

                    # Record generated test
                    generated_test = {
                        'original_test_id': test_idx,
                        'property': prop.name,
                        'input': transformed_input,
                        'expected_relation': message,
                        'output': transformed_output,
                        'valid': is_valid
                    }
                    self.generated_tests.append(generated_test)

                    # Record violation if property doesn't hold
                    if not is_valid:
                        violation = {
                            'test_id': test_idx,
                            'property': prop.name,
                            'message': message,
                            'original_input': input_data,
                            'original_output': original_output,
                            'transformed_input': transformed_input,
                            'transformed_output': transformed_output
                        }
                        self.violations.append(violation)

                    # Detect anomalies (errors in execution)
                    if isinstance(transformed_output, dict) and 'error' in transformed_output:
                        self.anomalies.append({
                            'test_id': test_idx,
                            'property': prop.name,
                            'error': transformed_output['error'],
                            'input': transformed_input
                        })

                except Exception as e:
                    self.anomalies.append({
                        'test_id': test_idx,
                        'property': prop.name,
                        'error': str(e),
                        'input': input_data
                    })

        print(f"Generated {len(self.generated_tests)} new test cases")
        print(f"Found {len(self.violations)} property violations")
        print(f"Found {len(self.anomalies)} anomalies")

    def calculate_coverage(self) -> Dict[str, Any]:
        """Calculate property coverage statistics"""
        total_tests = len(self.generated_tests)
        if total_tests == 0:
            return {'coverage': 0.0, 'by_property': {}}

        valid_tests = sum(1 for test in self.generated_tests if test['valid'])
        coverage = (valid_tests / total_tests) * 100

        # Coverage by property
        by_property = {}
        for prop in self.properties:
            prop_tests = [t for t in self.generated_tests if t['property'] == prop.name]
            prop_valid = sum(1 for t in prop_tests if t['valid'])
            by_property[prop.name] = {
                'total': len(prop_tests),
                'valid': prop_valid,
                'coverage': (prop_valid / len(prop_tests) * 100) if prop_tests else 0.0
            }

        return {
            'overall_coverage': coverage,
            'by_property': by_property
        }

    def generate_report(self, output_path: str = None) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        coverage = self.calculate_coverage()

        report = {
            'summary': {
                'original_tests': len(self.original_tests),
                'generated_tests': len(self.generated_tests),
                'properties_applied': [prop.name for prop in self.properties],
                'violations': len(self.violations),
                'anomalies': len(self.anomalies),
                'property_coverage': coverage['overall_coverage']
            },
            'coverage_by_property': coverage['by_property'],
            'violations': self.violations,
            'anomalies': self.anomalies,
            'generated_tests': self.generated_tests
        }

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nReport saved to: {output_path}")

        return report

    def save_expanded_test_suite(self, output_path: str):
        """Save the expanded test suite (original + generated)"""
        expanded_suite = {
            'original_tests': self.original_tests,
            'generated_tests': [
                {
                    'input': test['input'],
                    'property': test['property'],
                    'expected_relation': test['expected_relation']
                }
                for test in self.generated_tests
            ]
        }

        with open(output_path, 'w') as f:
            json.dump(expanded_suite, f, indent=2)
        print(f"Expanded test suite saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate metamorphic tests for a program'
    )
    parser.add_argument('program', help='Path to the program to test')
    parser.add_argument('--tests', required=True,
                       help='Path to test directory or JSON file with test cases')
    parser.add_argument('--properties', required=True,
                       help='Comma-separated list of properties or path to properties JSON file')
    parser.add_argument('--output', help='Path to save the report (JSON)')
    parser.add_argument('--suite-output', help='Path to save expanded test suite')

    args = parser.parse_args()

    # Parse properties
    if args.properties.endswith('.json'):
        with open(args.properties, 'r') as f:
            properties_data = json.load(f)
            if isinstance(properties_data, list):
                properties = properties_data
            elif isinstance(properties_data, dict) and 'properties' in properties_data:
                properties = properties_data['properties']
            else:
                properties = list(properties_data.keys())
    else:
        properties = [p.strip() for p in args.properties.split(',')]

    # Create generator
    generator = MetamorphicTestGenerator(args.program, args.tests, properties)

    # Load tests
    generator.load_tests()

    # Generate metamorphic tests
    generator.generate_tests()

    # Generate report
    report = generator.generate_report(args.output)

    # Print summary
    print("\n" + "="*60)
    print("METAMORPHIC TEST GENERATION SUMMARY")
    print("="*60)
    print(f"Original tests:      {report['summary']['original_tests']}")
    print(f"Generated tests:     {report['summary']['generated_tests']}")
    print(f"Properties applied:  {', '.join(report['summary']['properties_applied'])}")
    print(f"Violations found:    {report['summary']['violations']}")
    print(f"Anomalies found:     {report['summary']['anomalies']}")
    print(f"Property coverage:   {report['summary']['property_coverage']:.1f}%")
    print("="*60)

    if report['summary']['violations'] > 0:
        print("\n⚠️  VIOLATIONS DETECTED:")
        for v in report['violations'][:5]:  # Show first 5
            print(f"  - Test {v['test_id']}, Property: {v['property']}")
            print(f"    {v['message']}")

    if report['summary']['anomalies'] > 0:
        print("\n⚠️  ANOMALIES DETECTED:")
        for a in report['anomalies'][:5]:  # Show first 5
            print(f"  - Test {a['test_id']}, Property: {a['property']}")
            print(f"    Error: {a['error']}")

    # Save expanded test suite
    if args.suite_output:
        generator.save_expanded_test_suite(args.suite_output)

    return 0 if report['summary']['violations'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
