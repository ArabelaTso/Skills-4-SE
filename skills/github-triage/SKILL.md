---
name: github-triage
description: Automated GitHub issue and PR triage. Classifies open items, answers questions from codebase, analyzes bugs, reviews PRs, and produces a structured triage report. Use when processing multiple GitHub issues or PRs in batch.
---

# GitHub Triage

Automated triage orchestrator for GitHub issues and pull requests. Processes all open items in parallel, classifies each one, takes appropriate action, and produces a summary report.

## When to Use This Skill

- Processing a backlog of open GitHub issues
- Batch-reviewing open pull requests
- Answering user questions by searching the codebase
- Analyzing bug reports to identify root causes
- Assessing feature request feasibility

## What This Skill Does

### Phase 1: Fetch All Open Items

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh issue list --repo $REPO --state open --limit 500 \
  --json number,title,state,createdAt,labels,author,body,comments
gh pr list --repo $REPO --state open --limit 500 \
  --json number,title,state,author,body,headRefName,mergeable,reviewDecision,statusCheckRollup
```

### Phase 2: Classify Each Item

**Issues:**

| Type | Detection | Action |
|------|-----------|--------|
| QUESTION | Title contains `?`, body asks "how to" / "why does" | Search codebase, answer with file references, close if resolved |
| BUG | Title contains `Bug:`, body has error messages/stack traces | Trace root cause, confirm or explain correct behavior |
| FEATURE | Title contains `Feature Request`, `Enhancement` | Check if already exists, assess feasibility |
| OTHER | Anything else | Quick assessment, suggest labels |

**PRs:**

| Type | Detection | Action |
|------|-----------|--------|
| BUGFIX | Title starts with `fix`, branch contains `fix/` | Review diff, auto-merge if ALL conditions met |
| OTHER | Everything else | Assess and report, never auto-merge |

### Phase 3: Process Each Item (Parallel)

Each item gets its own background task. For issues:
- Search codebase for relevant code using grep/read tools
- Post helpful comments with specific file paths and code references
- Close resolved questions; never close bug reports

For bugfix PRs, auto-merge only when ALL conditions are met:
1. CI status checks ALL passing
2. Review decision: APPROVED
3. Fix is clearly correct and unambiguous
4. No risky side effects or architectural changes
5. Not a draft PR
6. No merge conflicts

### Phase 4: Summary Report

```markdown
## GitHub Triage Report

| Action | Count |
|--------|-------|
| Issues Answered & Closed | N |
| Bugs Confirmed | N |
| PRs Auto-Merged | N |
| Items Needing Manual Attention | N |
```

## Safety Rules

- Never guess — only answer if codebase clearly supports the answer
- Never close bug issues — only comment
- Never checkout PR branches — read-only via `gh api` and `gh pr view`
- Only merge PRs when 100% certain ALL conditions are met
- Prefix all posted comments with a bot identifier tag

## Example

**User**: "Triage all open issues and PRs"

**Output**: Fetches 12 open issues + 5 PRs, processes all in parallel:
- 4 questions answered and closed (with codebase references)
- 2 bugs confirmed with root cause analysis
- 1 safe bugfix PR auto-merged
- 5 items flagged for manual attention with detailed reports

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) github-triage skill
