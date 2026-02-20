---
name: requirement-comparison-reporter
description: "Compares old and new requirement documents, analyzes code repository impact, and generates detailed modification plans. Use when Claude needs to: (1) Compare requirement versions and identify changes, (2) Map requirement changes to code components, (3) Identify components to modify, delete, or add, (4) Analyze dependencies and integration points, (5) Assess test impact, (6) Generate comprehensive modification plans in Markdown format. Supports text/Markdown requirements and analyzes feature-level, functional, and API changes."
---

# Requirement Comparison Reporter

Generate detailed modification plans by comparing requirement documents and analyzing code impact.

## Workflow

### 1. Understand the Inputs

**Gather required inputs:**
- Old requirement document (path or content)
- New requirement document (path or content)
- Repository path

**Verify inputs:**
- Requirements are readable (text/Markdown format)
- Repository path is valid
- Repository contains Python code

### 2. Analyze Requirement Changes

**Read both requirement documents:**
- Extract key sections and features
- Identify structure and organization
- Note any explicit requirement IDs or labels

**Compare requirements:**

**Identify added requirements:**
- Features present in new but not in old
- New functionality descriptions
- New API endpoints or interfaces
- New business rules

**Identify modified requirements:**
- Features with changed descriptions
- Updated acceptance criteria
- Modified API contracts
- Changed business logic

**Identify removed requirements:**
- Features present in old but not in new
- Deprecated functionality
- Removed API endpoints

**Categorize changes:**
- Feature-level changes (new/modified/removed features)
- Functional changes (behavior, logic, workflows)
- API changes (endpoints, parameters, responses)

See [analysis-patterns.md](references/analysis-patterns.md) for detailed comparison strategies.

### 3. Analyze Code Structure

**Automated analysis:**
```bash
python scripts/analyze_code_impact.py <repo_path>
```

**Manual analysis:**
- Identify main modules and packages
- Locate key classes and functions
- Understand code organization
- Find test directory structure

**Build component inventory:**
- List all modules with their classes and functions
- Note public vs private components
- Identify entry points and main functionality
- Map test files to source files

### 4. Map Requirements to Code

**For each requirement change, identify affected code:**

**Name-based mapping:**
- Match requirement terms to class/function names
- Look for modules named after features
- Find components with related naming

**Comment-based mapping:**
- Search for requirement references in comments
- Look for issue/ticket numbers
- Find explicit requirement mentions

**Functionality-based mapping:**
- Analyze what each component does
- Match functionality to requirements
- Use docstrings to understand purpose

**Test-based mapping:**
- Use test names to infer functionality
- Map test files to requirements
- Associate test cases with features

**Example mapping:**
```
Requirement: "Add user authentication"
→ Likely components:
  - auth.py or authentication.py
  - user.py (User class)
  - login-related functions
  - test_auth.py or test_authentication.py
```

### 5. Identify Components to Modify

**For modified requirements:**

**Determine modification type:**
- Behavior change (logic modification)
- Signature change (parameters, return values)
- Integration change (new dependencies)

**Identify affected components:**
- Primary components implementing the feature
- Helper functions used by primary components
- Configuration or constants

**Assess complexity:**
- Simple: Single function/method change
- Medium: Multiple related changes
- Complex: Architectural or widespread changes

**Example:**
```markdown
### Modified Requirement: User login now requires 2FA

**Components to Modify:**
- `auth.py::AuthManager.login()` - Add 2FA verification step
- `user.py::User` - Add 2FA token field
- `config.py` - Add 2FA configuration

**Complexity:** Medium
```

### 6. Identify Components to Delete

**For removed requirements:**

**Find components to delete:**
- Modules implementing removed features
- Classes specific to removed functionality
- Functions no longer needed

**Check for dependencies:**
- Identify components that depend on code to be deleted
- Determine if dependencies can be safely removed
- Plan for updating dependent code

**Example:**
```markdown
### Removed Requirement: Legacy XML export

**Components to Delete:**
- `export/xml_exporter.py` - Entire module
- `utils/xml_helpers.py` - Helper functions

**Dependent Components:**
- `export/exporter.py` - Remove XML export option
```

### 7. Identify Components to Add

**For new requirements:**

**Determine what needs to be created:**
- New modules for new feature areas
- New classes for new entities
- New functions for new operations

**Recommend dependencies:**
- Identify existing components that can be reused
- Suggest appropriate base classes
- Recommend utility functions to use

**Plan integration:**
- Determine where new code fits in architecture
- Identify integration points with existing code
- Plan API or interface design

**Example:**
```markdown
### New Requirement: Email notifications

**Components to Add:**
- `notifications/email_notifier.py` - New module
  - Class: EmailNotifier
  - Methods: send_email(), format_template()

**Recommended Dependencies:**
- `notifications/base_notifier.py` - Base class
- `user.py` - Get user email addresses
- `templates/` - Email templates

**Integration Points:**
- Called by: event handlers in `events.py`
- Configured in: `config.py`
```

See [analysis-patterns.md](references/analysis-patterns.md) for detailed patterns.

### 8. Analyze Test Impact

**For each code change, identify test impact:**

**Tests to modify:**
- Tests for components being modified
- Integration tests involving changed components
- Tests with changed assertions or expectations

**Tests to delete:**
- Tests for removed components
- Tests for deprecated functionality

**Tests to add:**
- Tests for new components
- Tests for new behavior in modified components
- Integration tests for new features

**Example:**
```markdown
### Test Impact for User Authentication Changes

**Tests to Modify:**
- `test_auth.py::test_login()` - Add 2FA verification
- `test_user.py::test_user_creation()` - Add 2FA field

**Tests to Add:**
- `test_auth.py::test_login_with_2fa()` - New test
- `test_auth.py::test_2fa_token_validation()` - New test
```

### 9. Analyze Dependencies

**Build dependency graph:**
- Identify what each component depends on
- Find components that depend on each component
- Map import relationships

**For new components:**
- Recommend existing components to depend on
- Identify reusable utilities
- Suggest appropriate base classes

**For modified components:**
- Check if changes affect dependent components
- Identify ripple effects
- Plan for updating dependents

**For deleted components:**
- Find all components that import deleted code
- Plan for removing or updating imports
- Identify alternative components to use

### 10. Generate Modification Plan

**Create comprehensive report using template:**

See [report-template.md](references/report-template.md) for full template.

**Report structure:**

**1. Executive Summary**
- Total changes count
- Impact summary
- Complexity assessment

**2. Requirement Changes**
- Added requirements with impact
- Modified requirements with changes
- Removed requirements with impact

**3. Code Impact Analysis**
- Components to modify (with details)
- Components to delete (with dependencies)
- Components to add (with recommendations)

**4. Test Impact Analysis**
- Tests to modify
- Tests to delete
- Tests to add

**5. Dependency Analysis**
- New dependencies required
- Dependency changes
- Removed dependencies

**6. Modification Plan**
- Phase 1: Preparation
- Phase 2: Deletions
- Phase 3: Modifications
- Phase 4: Additions
- Phase 5: Integration Testing
- Phase 6: Documentation

**7. Risk Assessment**
- High-risk changes
- Mitigation strategies

**8. Recommendations**
- Implementation recommendations
- Architecture recommendations
- Testing recommendations

**9. Appendix**
- Requirement traceability matrix
- Component dependency graph
- Glossary

### 11. Review and Refine

**Verify completeness:**
- All requirement changes addressed
- All affected components identified
- All dependencies analyzed
- All tests considered

**Check accuracy:**
- Component names and paths correct
- Dependency relationships accurate
- Complexity assessments reasonable
- Recommendations actionable

**Refine report:**
- Clarify ambiguous sections
- Add missing details
- Improve recommendations
- Ensure consistency

## Output Format

Generate a Markdown report with the following sections:

```markdown
# Requirement Comparison Report

## Executive Summary
[High-level overview of changes and impact]

## Requirement Changes
### Added Requirements
[List with impact analysis]

### Modified Requirements
[List with before/after comparison]

### Removed Requirements
[List with deletion impact]

## Code Impact Analysis
### Components to Modify
[Detailed list with reasons and complexity]

### Components to Delete
[List with dependency impact]

### Components to Add
[List with structure and dependencies]

## Test Impact Analysis
[Tests to modify, delete, and add]

## Dependency Analysis
[New, modified, and removed dependencies]

## Modification Plan
[Phased implementation plan]

## Risk Assessment
[Risks and mitigation strategies]

## Recommendations
[Actionable recommendations]

## Appendix
[Traceability matrix, dependency graph, glossary]
```

## Best Practices

### Requirement Analysis
- Read both documents thoroughly
- Focus on meaningful changes, not just wording
- Categorize changes clearly
- Note ambiguities or unclear changes

### Code Mapping
- Use multiple mapping strategies
- Verify mappings with code inspection
- Consider indirect relationships
- Document mapping rationale

### Impact Analysis
- Consider both direct and indirect impact
- Analyze ripple effects
- Assess test coverage impact
- Evaluate dependency changes

### Planning
- Break down into manageable phases
- Prioritize by risk and dependency
- Provide clear, actionable steps
- Include verification checkpoints

### Reporting
- Be specific and detailed
- Use clear, consistent terminology
- Provide code references (file:line)
- Include examples where helpful

## Common Scenarios

### Scenario 1: API Endpoint Changes

**Input:**
- Old req: GET /users returns all fields
- New req: GET /users returns limited fields, add GET /users/detailed

**Analysis:**
- Modified: `routes/users.py::get_users()` - Limit fields
- Added: `routes/users.py::get_users_detailed()` - New endpoint
- Tests: Modify existing, add new tests

### Scenario 2: Feature Removal

**Input:**
- Old req: Support XML export
- New req: XML export removed

**Analysis:**
- Delete: `export/xml_exporter.py`
- Modify: `export/exporter.py` - Remove XML option
- Tests: Delete XML export tests

### Scenario 3: New Feature Addition

**Input:**
- Old req: Basic notifications
- New req: Add email notifications

**Analysis:**
- Add: `notifications/email_notifier.py`
- Depends on: `notifications/base_notifier.py`, `user.py`
- Tests: Add comprehensive email notification tests

## Troubleshooting

### Issue: Can't map requirement to code

**Solution:**
- Search for related keywords in codebase
- Check test files for clues
- Look for similar functionality
- Ask user for guidance

### Issue: Unclear requirement change

**Solution:**
- Highlight ambiguity in report
- Provide multiple interpretations
- Request clarification
- Make reasonable assumptions and document them

### Issue: Complex dependency graph

**Solution:**
- Focus on direct dependencies first
- Identify critical paths
- Simplify visualization
- Provide summary and details separately

### Issue: Large number of changes

**Solution:**
- Prioritize by impact and risk
- Group related changes
- Use summary sections
- Provide detailed appendix
