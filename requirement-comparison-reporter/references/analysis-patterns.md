# Requirement Analysis Patterns

## Requirement Change Types

### Feature-Level Changes

**Added Features**
- New functionality not present in old requirements
- New user stories or use cases
- New system capabilities

**Removed Features**
- Functionality present in old but not in new requirements
- Deprecated features
- Sunset capabilities

**Modified Features**
- Features with changed behavior
- Updated acceptance criteria
- Altered functional specifications

### Functional Changes

**Input/Output Changes**
- Modified data formats
- Changed validation rules
- New or removed parameters
- Altered return values

**Behavior Changes**
- Modified business logic
- Changed workflows
- Updated processing rules
- Altered error handling

**Integration Changes**
- New external system integrations
- Modified API contracts
- Changed data exchange formats
- Updated communication protocols

### API Changes

**Endpoint Changes**
- New endpoints
- Removed endpoints
- Modified endpoint paths
- Changed HTTP methods

**Parameter Changes**
- New required parameters
- Removed parameters
- Changed parameter types
- Modified default values

**Response Changes**
- New response fields
- Removed response fields
- Changed response structure
- Modified status codes

## Requirement Comparison Strategies

### Text-Based Comparison

**Section-by-section analysis:**
1. Identify major sections in both documents
2. Compare corresponding sections
3. Note additions, deletions, modifications
4. Extract key differences

**Keyword extraction:**
- Identify key terms and concepts
- Compare term frequency and usage
- Note new terminology
- Identify deprecated terms

**Feature extraction:**
- Extract feature descriptions
- Compare feature lists
- Identify new, removed, modified features
- Map features to requirements

### Structured Comparison

**For user stories:**
```
Old: As a [user], I want [feature] so that [benefit]
New: As a [user], I want [modified feature] so that [benefit]

Change: Feature modified from [old] to [new]
```

**For acceptance criteria:**
```
Old:
- Given [context]
- When [action]
- Then [outcome]

New:
- Given [context]
- When [modified action]
- Then [modified outcome]

Change: Action and outcome modified
```

### Semantic Analysis

**Intent comparison:**
- Understand the purpose of each requirement
- Compare intended outcomes
- Identify semantic changes vs. wording changes
- Focus on meaningful differences

**Dependency analysis:**
- Identify requirement dependencies
- Compare dependency graphs
- Note new dependencies
- Identify removed dependencies

## Code-to-Requirement Mapping

### Mapping Strategies

**Name-based mapping:**
- Match class/function names to requirement terms
- Use naming conventions to infer purpose
- Map module names to feature areas

**Comment-based mapping:**
- Extract requirement references from comments
- Look for issue/ticket numbers
- Find explicit requirement mentions

**Structure-based mapping:**
- Map modules to feature areas
- Associate packages with functional domains
- Link components to system capabilities

**Test-based mapping:**
- Use test names to infer functionality
- Map test suites to requirements
- Associate test cases with acceptance criteria

### Mapping Patterns

**Feature to Module:**
```
Requirement: User authentication
→ Modules: auth.py, user.py, session.py
→ Classes: AuthManager, User, Session
→ Functions: login(), logout(), validate_token()
```

**API Requirement to Endpoint:**
```
Requirement: GET /users/{id} endpoint
→ File: routes/users.py
→ Function: get_user_by_id()
→ Tests: test_get_user_by_id()
```

**Business Logic to Implementation:**
```
Requirement: Calculate order total with tax
→ Module: orders.py
→ Class: Order
→ Method: calculate_total()
→ Tests: test_calculate_total_with_tax()
```

## Impact Analysis Patterns

### Identifying Affected Components

**Direct impact:**
- Components explicitly mentioned in requirements
- Code directly implementing changed features
- APIs with modified contracts

**Indirect impact:**
- Components depending on changed components
- Shared utilities used by affected code
- Integration points with modified systems

**Test impact:**
- Tests for directly affected components
- Integration tests involving changed features
- End-to-end tests covering modified workflows

### Change Classification

**Modification (M):**
- Existing component needs changes
- Behavior must be updated
- Logic requires modification

**Deletion (D):**
- Component no longer needed
- Feature being removed
- Deprecated functionality

**Addition (A):**
- New component required
- New feature implementation
- New integration point

**No Change (-):**
- Component unaffected
- No modification needed
- Remains as-is

## Dependency Analysis Patterns

### Analyzing Dependencies

**Import analysis:**
```python
# Identify what a module depends on
import module_a
from module_b import ClassB

# Dependencies: module_a, module_b
```

**Call graph analysis:**
```python
# Function A calls Function B
def function_a():
    result = function_b()
    return result

# Dependency: function_a → function_b
```

**Inheritance analysis:**
```python
# Class A inherits from Class B
class ClassA(ClassB):
    pass

# Dependency: ClassA → ClassB
```

### Dependency Recommendations

**For new modules:**
1. Identify similar existing functionality
2. Find reusable components
3. Recommend appropriate dependencies
4. Suggest integration points

**Example:**
```
New Requirement: Email notification system
Existing Components:
- notification.py (base notification)
- user.py (user management)
- template.py (template rendering)

Recommendation:
- Create email_notification.py
- Depend on: notification.py (base class)
- Depend on: user.py (get user email)
- Depend on: template.py (email templates)
```

## Modification Planning Patterns

### Planning Structure

**For each change:**
1. Identify affected components
2. Determine change type (M/D/A)
3. Assess complexity
4. Identify dependencies
5. Note test impact
6. Provide recommendations

### Complexity Assessment

**Simple:**
- Single file modification
- Isolated change
- No dependency impact
- Straightforward implementation

**Medium:**
- Multiple file modifications
- Some dependency impact
- Requires coordination
- Moderate implementation effort

**Complex:**
- Many file modifications
- Significant dependency impact
- Requires architectural changes
- High implementation effort

### Priority Assessment

**High Priority:**
- Breaking changes
- Security-related changes
- Critical functionality
- Blocking other changes

**Medium Priority:**
- Feature enhancements
- Non-breaking changes
- Performance improvements
- Usability updates

**Low Priority:**
- Minor tweaks
- Cosmetic changes
- Optional features
- Nice-to-have improvements

## Report Generation Patterns

### Markdown Report Structure

```markdown
# Requirement Comparison Report

## Executive Summary
- Total changes: X
- New features: Y
- Modified features: Z
- Removed features: W

## Requirement Changes

### Added Requirements
1. [Requirement description]
   - Impact: [components affected]
   - Priority: [High/Medium/Low]

### Modified Requirements
1. [Requirement description]
   - Old: [old version]
   - New: [new version]
   - Impact: [components affected]

### Removed Requirements
1. [Requirement description]
   - Impact: [components to remove]

## Code Impact Analysis

### Components to Modify
- `module.py::ClassName.method_name()`
  - Reason: [why modification needed]
  - Complexity: [Simple/Medium/Complex]

### Components to Delete
- `old_module.py`
  - Reason: [why deletion needed]

### Components to Add
- `new_module.py`
  - Purpose: [what it will do]
  - Dependencies: [what it depends on]

## Test Impact

### Tests to Modify
- `test_module.py::test_function()`

### Tests to Add
- `test_new_feature.py`

## Modification Plan

### Phase 1: Preparation
1. [Step 1]
2. [Step 2]

### Phase 2: Implementation
1. [Step 1]
2. [Step 2]

### Phase 3: Testing
1. [Step 1]
2. [Step 2]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

### Detail Levels

**High-level report:**
- Focus on major changes
- Summarize impact
- Provide overview

**Detailed report:**
- List all changes
- Specify exact components
- Include code references
- Provide implementation guidance

**Technical report:**
- Include code snippets
- Show dependency graphs
- Provide detailed analysis
- Include complexity metrics
