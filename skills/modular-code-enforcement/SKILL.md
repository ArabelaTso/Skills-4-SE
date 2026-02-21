---
name: modular-code-enforcement
description: Enforces strict modular code architecture with Single Responsibility Principle, file size limits, and anti-pattern detection. Use when reviewing or writing code to maintain clean module boundaries.
---

# Modular Code Enforcement

Zero-tolerance policy for modular code architecture. Violations block further work until resolved.

## When to Use This Skill

- Reviewing code for architectural violations
- Writing new modules with clean boundaries
- Refactoring monolithic files into focused modules
- Enforcing team coding standards on file structure

## Rules

### Rule 1: Entry Points Are Not Dumping Grounds

`index` files (index.ts, __init__.py, etc.) MUST ONLY contain:
- Re-exports (`export { ... } from "./module"`)
- Factory function calls that compose modules
- Top-level wiring/registration

MUST NEVER contain: business logic, helper functions, type definitions beyond re-exports.

### Rule 2: No Catch-All Files

Files named `utils`, `helpers`, `service`, `common` are banned as top-level catch-alls.

| Anti-Pattern | Refactor To |
|--------------|-------------|
| `utils` with `formatDate()`, `slugify()`, `retry()` | `date-formatter`, `slugify`, `retry` |
| `service` handling auth + billing + notifications | `auth-service`, `billing-service`, `notification-service` |
| `helpers` with 15 unrelated exports | One file per logical domain |

Each module should be independently importable, self-contained, and nameable by purpose.

### Rule 3: Single Responsibility Principle — Absolute

Every source file MUST have exactly ONE clear, nameable responsibility.

**Self-test**: If you cannot describe the file's purpose in ONE short phrase, the file does too much. Split it.

| Signal | Action |
|--------|--------|
| File has 2+ unrelated exported functions | SPLIT |
| File mixes I/O with pure logic | SPLIT |
| File has both types and implementation | SPLIT |
| You need to scroll to understand the file | SPLIT |

### Rule 4: 200 LOC Hard Limit

Any source file exceeding 200 lines of code (excluding comments, blank lines, and long string literals like prompts/templates) is an immediate code smell.

**When detected:**
1. STOP current work
2. Identify the multiple responsibilities hiding in the file
3. Extract each responsibility into a focused module
4. Verify each resulting file is < 200 LOC with a single purpose
5. Resume original work

## How to Apply

When reading, writing, or editing any source file:
1. Check the file against all rules above
2. If violations found — refactor FIRST, then proceed
3. If creating a new file — ensure single responsibility and < 200 LOC
4. If adding to existing file — verify the addition doesn't push past limits or add a second responsibility

## Example

**User**: "Review this utils.ts file with 15 functions"

**Output**: Identifies 4 distinct responsibilities, proposes splitting into `date-formatter.ts`, `string-utils.ts`, `retry.ts`, and `validation.ts`, each under 50 LOC with a single clear purpose.

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) modular-code-enforcement rule
