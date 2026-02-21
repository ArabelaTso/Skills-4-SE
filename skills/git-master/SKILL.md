---
name: git-master
description: Git expert combining atomic commits, rebase/squash, and history search (blame, bisect, log -S). Use for any git operations requiring structured commit strategies, history rewriting, or code archaeology.
---

# Git Master

A comprehensive git workflow skill with three specializations: Commit Architect, Rebase Surgeon, and History Archaeologist.

## When to Use This Skill

- Committing changes with proper atomic commit discipline
- Rebasing, squashing, or cleaning up branch history
- Searching git history (who wrote X, when was Y added, find the commit that broke Z)
- Resolving merge/rebase conflicts systematically

## What This Skill Does

### 1. Commit Architect — Atomic Commits with Style Detection

**Core Principle: Multiple commits by default.**

```
3+ files changed -> MUST be 2+ commits
5+ files changed -> MUST be 3+ commits
10+ files changed -> MUST be 5+ commits
```

**Workflow:**

1. **Parallel Context Gathering** — Run simultaneously:
   - `git status`, `git diff --staged --stat`, `git diff --stat`
   - `git log -30 --oneline` (for style detection)
   - Branch context: current branch, merge-base, upstream status

2. **Style Detection** — Analyze last 30 commits:
   - Language: Korean vs English (use majority)
   - Style: SEMANTIC (`feat: xxx`), PLAIN (`Add xxx`), SHORT (`format`), SENTENCE
   - All generated commits match detected style + language

3. **Atomic Unit Planning** — Split by:
   - Different directories/modules → different commits
   - Different concerns (UI/logic/config/test) → different commits
   - Implementation + its test → same commit
   - Dependency order: utilities → models → services → API → config

4. **Mandatory Justification** — For each commit with 3+ files, write ONE sentence explaining why they must be together. Invalid reasons: "related to feature X", "part of the same PR".

5. **Execution** — Stage, commit, verify. Support fixup + autosquash for amending existing commits.

### 2. Rebase Surgeon — History Rewriting

**Safety-first approach:**

| Condition | Action |
|-----------|--------|
| On main/master | ABORT — never rebase main |
| Dirty working directory | Stash first |
| Pushed commits | Warn about force-push |
| All commits local | Proceed freely |

**Strategies:**
- `INTERACTIVE_SQUASH` — Combine commits via `git reset --soft` + recommit
- `AUTOSQUASH` — `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $MERGE_BASE`
- `REBASE_ONTO` — Update branch: `git rebase origin/main`
- Conflict resolution: identify → read both versions → resolve → `git rebase --continue`
- Recovery: `git rebase --abort`, `git reflog` for lost commits

### 3. History Archaeologist — Code Archaeology

| Goal | Command |
|------|---------|
| When was "X" added? | `git log -S "X" --oneline` |
| When was "X" removed? | `git log -S "X" --all --oneline` |
| What commits touched "X"? | `git log -G "X" --oneline` |
| Who wrote line N? | `git blame -L N,N file.py` |
| When did bug start? | `git bisect start && git bisect bad && git bisect good <tag>` |
| File history (across renames) | `git log --follow -- path/file.py` |
| Find deleted file | `git log --all --full-history -- "**/filename"` |

**-S vs -G:** `-S` finds commits where count of string changed (added/removed). `-G` finds commits where diff contains the pattern.

## Anti-Patterns

- One giant commit from many files — always split
- Defaulting to semantic commits without detecting repo style
- Separating test from implementation into different commits
- `--force` instead of `--force-with-lease`
- Rebasing main/master
- Vague commit grouping reasons ("related to X")

## Example

**User**: "Commit these 8 changed files"

**Output**: Detects repo uses English + semantic style, produces 4 atomic commits:
```
abc1234 feat: add pricing table component
def5678 feat: update demo browser frame
ghi9012 test: add e2e tests for navbar
jkl3456 chore: update i18n messages
```

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) git-master skill
