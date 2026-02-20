# Test Templates

This directory contains test framework templates for generating executable test cases from counterexamples.

## Available Templates

- **c_gtest_template.c**: C language with Google Test framework
- **cpp_gtest_template.cpp**: C++ language with Google Test framework
- **java_junit_template.java**: Java with JUnit 5 framework
- **python_pytest_template.py**: Python with pytest framework
- **csharp_nunit_template.cs**: C# with NUnit framework

## Template Structure

Each template includes:

1. **Header comments**: Metadata about the counterexample source and property violated
2. **Trace mapping**: Comments linking counterexample steps to test code lines
3. **Setup phase**: Initialize state to match counterexample initial state
4. **Execution phase**: Replay the counterexample sequence step-by-step
5. **Assertion phase**: Verify that the property violation occurs
6. **Additional tests**: Minimal reproduction and concurrent scenarios (where applicable)

## Placeholders

Templates use placeholders in `[BRACKETS]` that should be replaced with actual values:

- `[MODEL_CHECKER_NAME]`: Name of the model checker (SPIN, CBMC, etc.)
- `[PROPERTY_DESCRIPTION]`: Description of the violated property
- `[TIMESTAMP]`: Generation timestamp
- `[VARIABLE_NAME]`: Variable names from the program
- `[VALUE]`: Concrete values from the counterexample
- `[CODE_FOR_STEP_X]`: Code implementing each counterexample step
- `[ASSERTION_METHOD]`: Appropriate assertion for the test framework
- `[CONDITION]`: Boolean condition to check

## Usage

1. Select the appropriate template based on the program language and available test framework
2. Replace all placeholders with concrete values from the counterexample
3. Ensure the test compiles and runs
4. Verify that the test fails as expected, reproducing the violation
