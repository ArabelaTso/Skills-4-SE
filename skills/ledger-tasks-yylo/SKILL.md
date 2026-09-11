---
name: ledger-tasks-yylo
description: Operates a git-native Kanban task board for coding agents from the CLI. Create, search, update, and archive tasks, manage blocked-by dependencies, and resolve safe execution order, with task state stored as hash-chained Markdown inside the repository. Use for task management in agent-driven software engineering workflows.
---

# Ledger Tasks YYLO

Manages a Kanban-style task board for coding-agent projects through the `yy ledger` CLI. Task state lives inside the repository as hash-chained Markdown, so every mutation is reviewable in git and an agent recovers full context from a clean checkout.

Requires the `yy` CLI (`npm install --global '@yylo/cli@latest'`). Works in any agent harness that can run shell commands.

## When to Use This Skill

- Planning or executing multi-task work with a coding agent (create, update, and close tasks from the shell)
- Coordinating parallel work that has dependencies (blocked-by links, ready lists, topological order)
- Keeping an auditable task history next to the code (mutation receipts, revisions, archives)
- Handing off in-progress work between agent sessions with durable, reviewable state

## What This Skill Does

### Step 1: Create and Discover Tasks

```bash
yy ledger create "Implement OAuth login" --status backlog --tags feature,backend
yy ledger list --status todo,in_progress --limit 10
yy ledger search --status todo --tag backend
yy ledger get TASK_ID        # full detail incl. dependencies and related tasks
```

Filters for `search`: `--status`, `--tag`, `--body`, `--response`, `--commit`, `--open`, `--recent`, `--exclude`.

### Step 2: Move Tasks Through Their Lifecycle

```bash
yy ledger mark in_progress --id TASK_ID --response "Starting work on this"
yy ledger mark done --id TASK_ID --response "Completed: implemented X, tested Y" --commit abc123def
yy ledger update TASK_ID --status todo --tags backend,urgent
yy ledger archive TASK_ID   # soft delete; data preserved
```

`mark` requires `--id` and a `--response` message, so every lifecycle change leaves a receipt. `--commit` is recommended when marking done.

### Step 3: Manage Dependencies and Execution Order

```bash
yy ledger deps add --id TASK_ID --blocked-by BLOCKER1 BLOCKER2
yy ledger deps TASK_ID      # blockers, dependents, priority score
yy ledger ready             # tasks whose blockers are all done
yy ledger order --scores    # topological sort of open tasks
```

Cycle detection prevents circular dependencies automatically. Use `ready`/`order` before starting work to avoid blocked tasks.

## How to Use

### Basic Usage

Ask the agent: *"Create a backlog task for adding rate limiting, tag it backend, then show me what's ready to work on."* The agent runs `yy ledger create`, `yy ledger ready`, and reports the task IDs.

### Advanced Usage

- Audit trail: `yy ledger history TASK_ID` returns the task's full revision ledger.
- Cold archives: normal listing is hot-only; `yy ledger archive-search --tag backend --before 2026-01-01 --limit 20` finds archived tasks with bounded output, and `archive-pack plan/create` builds immutable archive packs (explicit owner authorization required; never automate archival).
- Health: `yy ledger doctor` validates board integrity.
- Cross-project routing is opt-in via `.juno_task/config.json` (`kanbanRegistry.enabled` + `allowedProjects`); routing failures never fall back silently.

## Example

```bash
# Plan a small feature with two dependent tasks
yy ledger create "Add POST /tokens endpoint" --status backlog --tags feature,api
yy ledger create "Write integration tests for /tokens" --status backlog --tags test
yy ledger deps add --id TASK_ID_2 --blocked-by TASK_ID_1   # use IDs printed by create

# Pick safe work
yy ledger ready
yy ledger order

# Close out with receipts
yy ledger mark done --id TASK_ID_1 --response "Endpoint shipped, manual check passed" --commit 4f2a91c
```

## Source

Adapted from [yylo-dev/yylo-skills](https://github.com/yylo-dev/yylo-skills) (`skills/ledger-tasks-yylo`), the skill collection for the YYLO CLI. Skill content is MIT licensed.
