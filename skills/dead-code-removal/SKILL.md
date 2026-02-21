---
name: dead-code-removal
description: Systematic dead code removal with LSP-verified safety, parallel execution, and atomic commits. Use when cleaning up unused code across a project with zero false positives.
---

# Dead Code Removal

Orchestrated dead code removal using LSP verification, parallel batch processing, and atomic commits. Goes beyond simple detection — this is a complete removal workflow.

## When to Use This Skill

- Cleaning up unused imports, functions, types, or constants
- Removing orphaned files not imported anywhere
- Post-refactoring cleanup of leftover code
- Reducing codebase size with verified safety

## What This Skill Does

### Phase 1: Scan — Find Candidates (Parallel)

Run all scanners simultaneously:

1. **Compiler strict mode** (primary scanner):
   ```bash
   # TypeScript example
   npx tsc --noEmit --noUnusedLocals --noUnusedParameters 2>&1
   # Python example
   vulture src/ --min-confidence 80
   ```

2. **Orphaned file detection**: Find source files not imported by any other file. Exclude entry points, test files, configs.

3. **Unused export detection**: Find exported symbols never imported elsewhere. Cross-reference each export across the codebase.

### Phase 2: Verify — Reference Confirmation (Zero False Positives)

For EACH candidate, verify with grep or language-specific tools:
```bash
# Search for all references (excluding the declaration itself)
grep -rn "symbolName" src/ --include="*.ts" | grep -v "declaration_file.ts"

# Or use language-specific tools:
#   TypeScript: ts-prune, ts-unused-exports
#   Python: vulture --min-confidence 80
#   Go: staticcheck -checks U1000

# 0 references = CONFIRMED dead
# 1+ references = NOT dead, drop from list
```

**False-positive guards — NEVER mark as dead:**
- Symbols in entry point files or barrel re-exports
- Symbols referenced in test files
- Symbols with `@public` / `@api` doc tags
- Factory functions, hook creators, plugin definitions
- Symbols in package exports

### Phase 3: Batch — Group for Conflict-Free Parallelism

1. Group confirmed items by file path
2. All items in the SAME file go to the SAME batch
3. Entire file deletions get their own batch
4. Target 5-15 batches for parallel execution

### Phase 4: Execute — Parallel Removal

For each batch:
1. Read files to understand exact syntax at target lines
2. Re-verify with grep (another batch may have changed things)
3. Apply changes:
   - Unused import (only symbol): remove entire import line
   - Unused import (one of many): remove only that symbol
   - Unused function/type/constant: remove declaration
   - Unused parameter: prefix with `_` (preserve signature)
   - Dead file: delete entirely
4. Run type checker / build to verify
5. If build fails: `git checkout -- [files]` and report failure
6. If build passes: atomic commit for this batch only

### Phase 5: Final Verification

```bash
# Must all pass after removal
typecheck   # language-specific
test        # note NEW failures vs pre-existing
build       # must pass
```

## Safety Rules

- Reference verification is mandatory before ANY removal
- Never remove entry points, test files, or config files
- Stage ONLY your batch's files — never `git add -A` during parallel execution
- If build fails after edits, REVERT all changes and report
- Abort if more than 50 candidates found (ask user to narrow scope)

## Example

**User**: "Remove dead code from this project"

**Output**:
```
Dead Code Removal Complete
- Scanned: 142 source files
- Candidates found: 23
- LSP-verified dead: 18
- Removed: 18 symbols across 12 files
- Commits: 4 atomic commits
- Build: PASS | Tests: 47 passing, 2 pre-existing failures
```

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) remove-deadcode command
