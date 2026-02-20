---
name: component-boundary-identifier
description: Identifies boundaries between modules or components in software systems through static code analysis and dependency detection. Use when Claude needs to analyze software architecture, identify module boundaries, detect boundary violations, find circular dependencies, or assess component coupling. Supports Python (packages and imports) and Java (packages and dependencies). Trigger when users ask to "identify boundaries", "find component boundaries", "detect boundary violations", "analyze module structure", "check architecture", or "find circular dependencies".
---

# Component Boundary Identifier

Identify and analyze boundaries between software components to ensure proper architectural separation.

## Quick Start

When a user requests boundary analysis:

1. **Understand the goal**: Identify boundaries, detect violations, or both
2. **Analyze structure**: Examine package/module organization and dependencies
3. **Identify boundaries**: Determine component boundaries based on structure
4. **Detect violations**: Find improper cross-boundary dependencies
5. **Report findings**: Present boundaries and violations with severity levels

## What This Skill Does

### Boundary Identification
Identify component boundaries based on:
- Package/module structure
- Namespace organization
- Architectural patterns (layered, hexagonal, clean)
- Naming conventions
- Dependency clusters

### Violation Detection
Detect boundary violations including:
- Upward dependencies (lower layers depending on higher layers)
- Circular dependencies between components
- Layer skipping (bypassing intermediate layers)
- Domain depending on infrastructure
- Accessing private/internal implementations
- Concrete type dependencies across boundaries

## Analysis Methods

### Static Code Analysis

Analyze code structure without execution.

**Python:**
- Parse import statements
- Analyze package structure
- Identify dependency directions
- Detect circular imports

**Java:**
- Parse import statements
- Analyze package hierarchy
- Check access modifiers
- Identify dependency directions

**Script:** Use `scripts/analyze_boundaries.py` for automated Python analysis

### Manual Code Review

Review code for boundary patterns.

**Process:**
1. Identify top-level packages/modules
2. Map dependencies between components
3. Check against architectural rules
4. Find violations

**See:** [boundary-indicators.md](references/boundary-indicators.md) for patterns

## Architectural Patterns

### Layered Architecture

**Layers (top to bottom):**
1. Presentation/API
2. Application/Service
3. Domain/Business
4. Infrastructure/Data

**Rules:**
- Dependencies flow downward only
- No layer skipping
- No upward dependencies

**Violations:**
- Domain imports from API
- Infrastructure imports from Domain
- API directly uses Infrastructure (skips Service)

### Hexagonal Architecture

**Boundaries:**
- **Core**: Domain logic (center)
- **Ports**: Interfaces for external interaction
- **Adapters**: Implementations (outside)

**Rules:**
- Core has no dependencies on adapters
- Adapters depend on ports
- All external access through ports

**Violations:**
- Core imports adapter implementations
- Core depends on frameworks
- Direct adapter-to-adapter dependencies

### Clean Architecture

**Boundaries (inside to outside):**
1. Entities (domain models)
2. Use Cases (business rules)
3. Interface Adapters
4. Frameworks & Drivers

**Dependency Rule:**
- Dependencies point inward only
- Inner layers independent of outer layers

**Violations:**
- Inner layer imports outer layer
- Domain depends on UI/API
- Use cases depend on frameworks

## Language-Specific Guidance

### Python

**Boundary indicators:**
- Top-level packages (`domain/`, `infrastructure/`, `api/`)
- `__init__.py` with controlled exports
- Protocol/ABC definitions

**Common violations:**
- Domain imports from `infrastructure`
- Circular imports between modules
- Importing private members (`_name`)
- Direct implementation dependencies

**See:** [boundary-indicators.md](references/boundary-indicators.md) for details

### Java

**Boundary indicators:**
- Package hierarchy (`com.example.domain`, `com.example.infrastructure`)
- Access modifiers (public, package-private, private)
- Interface definitions

**Common violations:**
- Domain imports infrastructure packages
- Accessing package-private from different package
- Static coupling across boundaries
- Framework annotations in domain

**See:** [boundary-indicators.md](references/boundary-indicators.md) for details

## Workflow

### 1. Understand the Request

**Questions to clarify:**
- Identify boundaries or detect violations?
- Specific architectural pattern in use?
- Focus on specific components?
- Known problem areas?

### 2. Analyze Project Structure

**For automated analysis:**
```bash
python scripts/analyze_boundaries.py <project_directory>
```

**For manual analysis:**
1. List top-level packages/modules
2. Identify architectural layers
3. Note naming conventions
4. Understand intended architecture

### 3. Identify Boundaries

**Look for:**
- Package/module groupings
- Architectural layer separation
- Domain vs infrastructure separation
- API vs business logic separation

**Document:**
- Boundary names and purposes
- Components within each boundary
- Intended dependency directions

### 4. Detect Violations

**Check for:**
- Upward dependencies
- Circular dependencies
- Layer skipping
- Concrete type dependencies
- Private/internal access

**See:** [violation-patterns.md](references/violation-patterns.md) for patterns

### 5. Report Findings

**Structure:**
```
IDENTIFIED BOUNDARIES
- boundary1/ (N modules)
- boundary2/ (M modules)

BOUNDARY VIOLATIONS
[CRITICAL] module_a depends on higher layer module_b
[HIGH] Circular dependency: module_c -> module_d -> module_c
[MEDIUM] module_e accesses private implementation

RECOMMENDATIONS
- Fix critical violations first
- Introduce interfaces for concrete dependencies
- Refactor circular dependencies
```

## Violation Severity Levels

### Critical
- Domain depends on infrastructure
- Upward dependencies in layered architecture
- Circular dependencies between major components

**Impact:** Breaks architectural principles, prevents proper separation

**Priority:** Fix immediately

### High
- Layer skipping
- Concrete type dependencies across boundaries
- Framework coupling in domain

**Impact:** Reduces flexibility, complicates testing

**Priority:** Fix soon

### Medium
- Accessing private/internal members
- Static coupling across boundaries
- Missing interfaces at boundaries

**Impact:** Breaks encapsulation, reduces maintainability

**Priority:** Fix when refactoring

### Low
- Suboptimal package structure
- Inconsistent naming
- Missing documentation

**Impact:** Reduces code clarity

**Priority:** Fix opportunistically

## Detection Patterns

### Upward Dependency

**Pattern:**
```python
# domain/services.py
from api.serializers import UserSerializer  # VIOLATION
```

**Detection:** Lower layer imports from higher layer

**Fix:** Move serialization to API layer

### Circular Dependency

**Pattern:**
```python
# module_a.py
from module_b import ClassB

# module_b.py
from module_a import ClassA  # VIOLATION
```

**Detection:** A imports B, B imports A

**Fix:** Extract shared interface, use dependency injection

### Layer Skipping

**Pattern:**
```python
# api/routes.py
from infrastructure.repositories import UserRepository  # VIOLATION
```

**Detection:** API directly uses infrastructure (skips service layer)

**Fix:** Use service layer as intermediary

### Concrete Dependency

**Pattern:**
```python
# domain/services.py
from infrastructure.email import SMTPEmailSender  # VIOLATION

class NotificationService:
    def __init__(self):
        self.sender = SMTPEmailSender()
```

**Detection:** Domain depends on concrete infrastructure class

**Fix:** Depend on interface, inject implementation

## Best Practices

### Boundary Definition
- Use clear package/module names
- Follow architectural patterns consistently
- Document boundary purposes
- Establish dependency rules

### Dependency Management
- Depend on interfaces, not implementations
- Use dependency injection
- Follow dependency inversion principle
- Avoid static coupling

### Violation Prevention
- Code reviews focusing on imports
- Automated dependency analysis in CI/CD
- Architecture decision records
- Team training on patterns

### Refactoring Strategy
- Fix critical violations first
- Introduce interfaces gradually
- Extract shared code carefully
- Test after each change

## Example Usage Patterns

**User:** "Identify the component boundaries in this codebase"
→ Analyze structure, identify boundaries, report findings

**User:** "Check if there are any boundary violations"
→ Analyze dependencies, detect violations, report with severity

**User:** "Is my domain layer properly isolated?"
→ Check domain dependencies, verify no infrastructure/API imports

**User:** "Find circular dependencies in the project"
→ Analyze import graph, identify cycles, report

**User:** "Does this follow clean architecture?"
→ Identify layers, check dependency directions, report violations

**User:** "Why is this module hard to test?"
→ Analyze dependencies, identify concrete couplings, suggest fixes

## Automated Analysis

Use the provided script for Python projects:

```bash
python scripts/analyze_boundaries.py /path/to/project
```

**Output:**
- Identified boundaries
- Boundary violations with severity
- Circular dependencies
- Recommendations

**Limitations:**
- Python only (for automated analysis)
- Requires valid Python syntax
- May miss dynamic imports
- Heuristic-based layer detection

For Java or manual analysis, follow the workflow using reference patterns.
