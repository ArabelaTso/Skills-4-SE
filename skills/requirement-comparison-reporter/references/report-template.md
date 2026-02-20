# Report Template

## Standard Report Template

```markdown
# Requirement Comparison Report

**Generated:** [Date]
**Old Requirements:** [Document name/path]
**New Requirements:** [Document name/path]
**Repository:** [Repository path]

---

## Executive Summary

### Overview
- **Total Requirement Changes:** [number]
- **New Requirements:** [number]
- **Modified Requirements:** [number]
- **Removed Requirements:** [number]

### Impact Summary
- **Components to Modify:** [number]
- **Components to Delete:** [number]
- **Components to Add:** [number]
- **Tests Affected:** [number]

### Complexity Assessment
- **Simple Changes:** [number]
- **Medium Changes:** [number]
- **Complex Changes:** [number]

---

## Requirement Changes

### 1. Added Requirements

#### REQ-NEW-001: [Requirement Title]

**Description:**
[Detailed description of the new requirement]

**Rationale:**
[Why this requirement was added]

**Impact:**
- **New Components:** [list]
- **Dependencies:** [list]
- **Priority:** [High/Medium/Low]
- **Complexity:** [Simple/Medium/Complex]

---

#### REQ-NEW-002: [Requirement Title]
...

### 2. Modified Requirements

#### REQ-MOD-001: [Requirement Title]

**Old Version:**
[Description of old requirement]

**New Version:**
[Description of new requirement]

**Changes:**
- [Change 1]
- [Change 2]

**Impact:**
- **Components to Modify:** [list]
- **Tests to Update:** [list]
- **Priority:** [High/Medium/Low]
- **Complexity:** [Simple/Medium/Complex]

---

#### REQ-MOD-002: [Requirement Title]
...

### 3. Removed Requirements

#### REQ-DEL-001: [Requirement Title]

**Description:**
[Description of removed requirement]

**Rationale:**
[Why this requirement was removed]

**Impact:**
- **Components to Delete:** [list]
- **Tests to Remove:** [list]
- **Priority:** [High/Medium/Low]

---

## Code Impact Analysis

### Components to Modify

#### 1. `module_name.py`

**Location:** `src/module_name.py`

**Affected Elements:**
- **Class:** `ClassName`
  - **Method:** `method_name()`
    - **Reason:** [Why modification needed]
    - **Change Type:** [Behavior/Signature/Logic]
    - **Complexity:** [Simple/Medium/Complex]
    - **Related Requirement:** REQ-MOD-001

**Dependencies:**
- Depends on: `dependency1.py`, `dependency2.py`
- Used by: `consumer1.py`, `consumer2.py`

**Recommendation:**
[Specific guidance on how to modify]

---

#### 2. `another_module.py`
...

### Components to Delete

#### 1. `old_module.py`

**Location:** `src/old_module.py`

**Reason:** Feature removed (REQ-DEL-001)

**Impact:**
- **Dependent Components:** [list components that use this]
- **Action Required:** Remove imports and update dependent code

**Recommendation:**
[Guidance on safe deletion]

---

### Components to Add

#### 1. `new_feature_module.py`

**Purpose:** Implement [feature description]

**Related Requirement:** REQ-NEW-001

**Suggested Structure:**
```python
# new_feature_module.py
"""
Module for [feature description].
"""

class NewFeatureClass:
    """[Class description]"""

    def __init__(self):
        pass

    def main_method(self):
        """[Method description]"""
        pass
```

**Recommended Dependencies:**
- `existing_module1.py` - [Why needed]
- `existing_module2.py` - [Why needed]

**Integration Points:**
- Called by: [list]
- Integrates with: [list]

**Complexity:** [Simple/Medium/Complex]

---

## Test Impact Analysis

### Tests to Modify

#### 1. `test_module.py::TestClassName::test_method_name`

**Location:** `tests/test_module.py`

**Reason:** Method signature changed (REQ-MOD-001)

**Required Changes:**
- Update test parameters
- Modify assertions
- Add new test cases for new behavior

**Complexity:** [Simple/Medium/Complex]

---

### Tests to Delete

#### 1. `test_old_feature.py`

**Location:** `tests/test_old_feature.py`

**Reason:** Feature removed (REQ-DEL-001)

**Action:** Delete entire test file

---

### Tests to Add

#### 1. `test_new_feature.py`

**Purpose:** Test new feature (REQ-NEW-001)

**Suggested Test Cases:**
- `test_basic_functionality()` - Test core feature
- `test_edge_cases()` - Test boundary conditions
- `test_error_handling()` - Test error scenarios
- `test_integration()` - Test integration with existing code

**Complexity:** [Simple/Medium/Complex]

---

## Dependency Analysis

### New Dependencies Required

#### External Dependencies
- `package_name==version` - [Why needed]

#### Internal Dependencies
- `existing_module.py` - [Why needed]

### Dependency Changes

#### Modified Dependencies
- `module_a.py` now depends on `module_b.py` - [Reason]

#### Removed Dependencies
- `old_dependency.py` no longer needed - [Reason]

---

## Modification Plan

### Phase 1: Preparation (Estimated: [time])

**Objective:** Prepare codebase for changes

**Tasks:**
1. **Backup current state**
   - Create feature branch
   - Tag current version

2. **Review dependencies**
   - Verify all dependencies available
   - Update requirements.txt if needed

3. **Set up test environment**
   - Ensure all tests pass before changes
   - Document baseline metrics

**Deliverables:**
- Clean baseline
- Updated dependencies
- Passing test suite

---

### Phase 2: Deletions (Estimated: [time])

**Objective:** Remove deprecated components

**Tasks:**
1. **Remove deprecated features**
   - Delete `old_module.py`
   - Remove related tests
   - Update documentation

2. **Update dependent code**
   - Remove imports
   - Update calling code
   - Fix broken references

3. **Verify deletions**
   - Run test suite
   - Check for broken imports
   - Verify no regressions

**Deliverables:**
- Cleaned codebase
- Updated tests
- Passing test suite

---

### Phase 3: Modifications (Estimated: [time])

**Objective:** Modify existing components

**Tasks:**
1. **Modify `module_name.py`**
   - Update `ClassName.method_name()`
   - Add new parameters
   - Update logic

2. **Update tests**
   - Modify `test_module.py`
   - Update assertions
   - Add new test cases

3. **Verify modifications**
   - Run affected tests
   - Check integration points
   - Verify backward compatibility

**Deliverables:**
- Modified components
- Updated tests
- Passing test suite

---

### Phase 4: Additions (Estimated: [time])

**Objective:** Add new components

**Tasks:**
1. **Create `new_feature_module.py`**
   - Implement core functionality
   - Add error handling
   - Write documentation

2. **Create tests**
   - Write `test_new_feature.py`
   - Implement test cases
   - Verify coverage

3. **Integrate with existing code**
   - Add imports where needed
   - Update calling code
   - Test integration points

**Deliverables:**
- New components
- Comprehensive tests
- Integrated functionality

---

### Phase 5: Integration Testing (Estimated: [time])

**Objective:** Verify all changes work together

**Tasks:**
1. **Run full test suite**
   - Unit tests
   - Integration tests
   - End-to-end tests

2. **Verify requirements**
   - Check all new requirements implemented
   - Verify modified requirements updated
   - Confirm removed requirements deleted

3. **Performance testing**
   - Run performance benchmarks
   - Compare with baseline
   - Address any regressions

**Deliverables:**
- Passing test suite
- Verified requirements
- Performance report

---

### Phase 6: Documentation (Estimated: [time])

**Objective:** Update all documentation

**Tasks:**
1. **Update code documentation**
   - Update docstrings
   - Add inline comments
   - Update type hints

2. **Update user documentation**
   - Update README
   - Update API documentation
   - Update user guides

3. **Update developer documentation**
   - Update architecture docs
   - Update contribution guide
   - Update changelog

**Deliverables:**
- Updated documentation
- Changelog entry
- Migration guide (if needed)

---

## Risk Assessment

### High-Risk Changes

#### 1. [Change description]

**Risk:** [What could go wrong]

**Mitigation:**
- [Mitigation strategy 1]
- [Mitigation strategy 2]

**Contingency:**
- [Fallback plan]

---

### Medium-Risk Changes

#### 1. [Change description]

**Risk:** [What could go wrong]

**Mitigation:**
- [Mitigation strategy]

---

## Recommendations

### Implementation Recommendations

1. **[Recommendation 1]**
   - Rationale: [Why]
   - Benefit: [What it achieves]

2. **[Recommendation 2]**
   - Rationale: [Why]
   - Benefit: [What it achieves]

### Architecture Recommendations

1. **[Recommendation 1]**
   - Current state: [Description]
   - Proposed change: [Description]
   - Benefit: [What it achieves]

### Testing Recommendations

1. **[Recommendation 1]**
   - Current coverage: [X%]
   - Target coverage: [Y%]
   - Action: [What to do]

---

## Appendix

### A. Requirement Traceability Matrix

| Requirement ID | Type | Component(s) | Test(s) | Status |
|---------------|------|--------------|---------|--------|
| REQ-NEW-001 | Add | new_module.py | test_new.py | Planned |
| REQ-MOD-001 | Modify | module.py | test_module.py | Planned |
| REQ-DEL-001 | Delete | old_module.py | test_old.py | Planned |

### B. Component Dependency Graph

```
new_module.py
├── depends on: existing_module1.py
├── depends on: existing_module2.py
└── used by: main.py

modified_module.py
├── depends on: base_module.py
└── used by: consumer1.py, consumer2.py
```

### C. Glossary

- **Component:** A module, class, or function in the codebase
- **Requirement:** A specification of desired functionality
- **Impact:** The effect of a requirement change on the codebase
- **Complexity:** The difficulty of implementing a change

---

**End of Report**
```

## Compact Report Template

For simpler cases, use a more compact format:

```markdown
# Requirement Comparison Report

## Summary
- New: [X] | Modified: [Y] | Removed: [Z]
- Components: Modify [A] | Delete [B] | Add [C]

## Changes

### Added
1. **[Feature]** → Add `new_module.py` (depends on: `existing.py`)

### Modified
2. **[Feature]** → Modify `module.py::Class.method()` (Complexity: Medium)

### Removed
3. **[Feature]** → Delete `old_module.py`

## Plan
1. Phase 1: Delete old components
2. Phase 2: Modify existing components
3. Phase 3: Add new components
4. Phase 4: Update tests

## Tests
- Modify: `test_module.py`
- Add: `test_new_feature.py`
- Delete: `test_old.py`
```
