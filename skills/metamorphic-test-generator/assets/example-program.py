#!/usr/bin/env python3
"""
Example program for testing: Simple sorting function
Reads JSON input from stdin and outputs sorted result
"""
import json
import sys

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Handle different input types
    if isinstance(input_data, list):
        # Sort list
        result = sorted(input_data)
    elif isinstance(input_data, dict) and 'list' in input_data:
        # Sort list from dict
        result = sorted(input_data['list'])
    elif isinstance(input_data, (int, float)):
        # Return as-is for numeric input
        result = input_data
    else:
        result = input_data

    # Output result as JSON
    print(json.dumps(result))

if __name__ == '__main__':
    main()
