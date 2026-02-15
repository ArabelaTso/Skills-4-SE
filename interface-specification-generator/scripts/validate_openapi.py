#!/usr/bin/env python3
"""
OpenAPI Specification Validator

Validates OpenAPI 3.0 specifications for correctness and best practices.
"""

import sys
import json
import yaml
from pathlib import Path


def load_spec(file_path):
    """Load OpenAPI spec from YAML or JSON file."""
    path = Path(file_path)

    if not path.exists():
        return None, f"File not found: {file_path}"

    try:
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                spec = yaml.safe_load(f)
            elif path.suffix == '.json':
                spec = json.load(f)
            else:
                return None, f"Unsupported file format: {path.suffix}"
        return spec, None
    except Exception as e:
        return None, f"Error loading file: {str(e)}"


def validate_spec(spec):
    """Validate OpenAPI specification structure."""
    errors = []
    warnings = []

    # Check required root fields
    if 'openapi' not in spec:
        errors.append("Missing required field: 'openapi'")
    elif not spec['openapi'].startswith('3.0'):
        warnings.append(f"OpenAPI version {spec['openapi']} - this validator is optimized for 3.0.x")

    if 'info' not in spec:
        errors.append("Missing required field: 'info'")
    else:
        info = spec['info']
        if 'title' not in info:
            errors.append("Missing required field: 'info.title'")
        if 'version' not in info:
            errors.append("Missing required field: 'info.version'")
        if 'description' not in info:
            warnings.append("Consider adding 'info.description' for better documentation")

    if 'paths' not in spec:
        errors.append("Missing required field: 'paths'")
    else:
        validate_paths(spec['paths'], errors, warnings)

    # Check for components
    if 'components' in spec:
        validate_components(spec['components'], errors, warnings)

    return errors, warnings


def validate_paths(paths, errors, warnings):
    """Validate paths section."""
    if not paths:
        warnings.append("No paths defined in the specification")
        return

    for path, path_item in paths.items():
        if not path.startswith('/'):
            errors.append(f"Path '{path}' must start with '/'")

        # Check for HTTP methods
        http_methods = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace']
        has_operation = False

        for method in http_methods:
            if method in path_item:
                has_operation = True
                validate_operation(path, method, path_item[method], errors, warnings)

        if not has_operation and 'parameters' not in path_item:
            warnings.append(f"Path '{path}' has no operations defined")


def validate_operation(path, method, operation, errors, warnings):
    """Validate an operation (HTTP method)."""
    if 'responses' not in operation:
        errors.append(f"{method.upper()} {path}: Missing required field 'responses'")
    else:
        if not operation['responses']:
            warnings.append(f"{method.upper()} {path}: No responses defined")

        # Check for success response
        success_codes = ['200', '201', '202', '204']
        has_success = any(code in operation['responses'] for code in success_codes)
        if not has_success:
            warnings.append(f"{method.upper()} {path}: No success response (2xx) defined")

    if 'summary' not in operation and 'description' not in operation:
        warnings.append(f"{method.upper()} {path}: Consider adding 'summary' or 'description'")

    # Check request body for POST/PUT/PATCH
    if method in ['post', 'put', 'patch']:
        if 'requestBody' not in operation:
            warnings.append(f"{method.upper()} {path}: Consider adding 'requestBody'")


def validate_components(components, errors, warnings):
    """Validate components section."""
    if 'schemas' in components:
        for schema_name, schema in components['schemas'].items():
            if 'type' not in schema and '$ref' not in schema and 'allOf' not in schema and 'oneOf' not in schema and 'anyOf' not in schema:
                warnings.append(f"Schema '{schema_name}': Consider specifying 'type'")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_openapi.py <openapi-spec-file>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Validating OpenAPI specification: {file_path}")
    print("-" * 60)

    spec, error = load_spec(file_path)
    if error:
        print(f"❌ Error: {error}")
        sys.exit(1)

    errors, warnings = validate_spec(spec)

    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")

    if not errors and not warnings:
        print("✅ Specification is valid!")
    elif not errors:
        print("\n✅ Specification is valid (with warnings)")
    else:
        print(f"\n❌ Validation failed with {len(errors)} error(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
