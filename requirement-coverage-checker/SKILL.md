---
name: requirement-coverage-checker
description: Verify that design documents, code implementations, and tests fully cover all specified requirements. Use this skill when validating requirement traceability, conducting design reviews, assessing implementation completeness, checking test coverage against requirements, performing compliance audits, or identifying missing functionality. Produces coverage reports showing which requirements are satisfied, partially satisfied, or missing.
---

# Requirement Coverage Checker

Systematically verify that design and implementation cover all specified requirements. Identifies gaps, ensures traceability, and validates that every requirement has corresponding design elements, code, and tests.

## Core Capabilities

### 1. Requirement Extraction

Parse and identify requirements from documents:
- **Functional requirements** - Feature specifications
- **Non-functional requirements** - Performance, security, usability
- **Business rules** - Constraints and policies
- **User stories** - As-a/I-want/So-that format
- **Use cases** - Actor-goal scenarios
- **Acceptance criteria** - Success conditions

### 2. Design Coverage Analysis

Map requirements to design elements:
- **Architecture decisions** - System structure
- **Component specifications** - Module designs
- **Interface definitions** - API contracts
- **Data models** - Database schemas
- **Workflow diagrams** - Process flows
- **UML diagrams** - Class/sequence/state diagrams

### 3. Implementation Coverage Analysis

Verify code implements requirements:
- **Feature implementation** - Functionality exists
- **API endpoints** - Required interfaces present
- **Business logic** - Rules implemented
- **Data persistence** - Storage implemented
- **Error handling** - Edge cases handled
- **Integration points** - Connections implemented

### 4. Test Coverage Analysis

Ensure tests validate requirements:
- **Unit tests** - Component-level validation
- **Integration tests** - Interaction validation
- **Acceptance tests** - Requirement validation
- **Scenario tests** - User story coverage
- **Edge case tests** - Boundary condition coverage
- **Performance tests** - Non-functional validation

## Coverage Checking Workflow

### Step 1: Extract Requirements

Identify all requirements from source documents.

### Step 2: Map to Design Elements

Check if requirements appear in design.

### Step 3: Verify Implementation

Check if code implements design.

### Step 4: Validate Test Coverage

Ensure tests verify requirements.

### Step 5: Generate Coverage Report

Produce comprehensive coverage analysis.

## Best Practices

1. **Start with requirements** - Ensure requirements are clear and complete
2. **Use unique IDs** - Every requirement needs traceable identifier
3. **Check all levels** - Verify design, code, and tests
4. **Be systematic** - Use checklists and matrices
5. **Document gaps** - Record what's missing and why
6. **Prioritize fixes** - Address critical gaps first
7. **Automate when possible** - Use tools for traceability
8. **Update regularly** - Check coverage as project evolves
9. **Include stakeholders** - Review coverage with team
10. **Track over time** - Monitor coverage trends
