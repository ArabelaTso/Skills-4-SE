# SZZ Algorithm Reference

## Overview

The SZZ (Śliwerski-Zimmermann-Zeller) algorithm is a widely-used approach for identifying bug-introducing commits in software repositories. It works by analyzing bug-fixing commits and tracing back through version history to find the commits that introduced the buggy code.

## Core Algorithm Steps

1. **Identify Bug-Fixing Commit**: Start with a commit that fixes a bug (typically identified through commit messages, issue trackers, or manual annotation)

2. **Extract Modified Lines**: Analyze the diff to identify which lines were deleted or modified in the fix

3. **Blame Analysis**: For each deleted/modified line, use `git blame` to trace back to the commit that originally introduced that line

4. **Candidate Identification**: The commits identified through blame are candidates for bug-introducing commits

5. **Filtering**: Apply heuristics to filter false positives

6. **Ranking**: Rank candidates by likelihood of being the actual bug-introducing commit

## False Positive Patterns

Common sources of false positives that should be filtered:

### Code Formatting and Style
- Whitespace changes
- Indentation adjustments
- Bracket placement
- Line breaks

### Non-Functional Changes
- Comment additions/modifications
- Import statement reordering
- Code reorganization without logic changes
- Variable/function renaming

### Refactoring Operations
- Code extraction to methods
- Code movement between files
- Structural changes without behavior modification

## Filtering Heuristics

### Commit Message Analysis
Look for keywords indicating non-bug-introducing changes:
- "refactor", "rename", "format", "style"
- "cleanup", "reorganize", "restructure"
- "reformat", "whitespace", "indent"

### Line Content Analysis
Skip lines that are unlikely to contain bugs:
- Empty lines
- Lines with only braces `{` or `}`
- Import/include statements
- Comments (single-line and multi-line)
- Pure whitespace changes

### Temporal Analysis
- Commits very close in time to the fix may be less likely to be bug-introducing
- Very old commits may have lower confidence if the code has changed significantly

## Confidence Scoring

Factors that increase confidence:
- Multiple lines from the same commit were fixed
- The commit modified functional code (not comments/formatting)
- The commit message doesn't suggest refactoring
- The time gap between introduction and fix is reasonable

Factors that decrease confidence:
- Commit message suggests refactoring/formatting
- Only one line was modified
- The line contains only structural elements
- The commit is very recent or very old relative to the fix

## Limitations

1. **Tangled Changes**: If a commit contains both bug-introducing and unrelated changes, SZZ may incorrectly attribute the entire commit

2. **Indirect Bugs**: Bugs caused by missing code or incorrect assumptions may not be detected

3. **Refactoring**: Heavy refactoring can break the blame chain, making it difficult to trace back to the original introduction

4. **Multi-Commit Bugs**: Bugs introduced across multiple commits may only identify the most recent contributor

5. **False Fixes**: If the "fix" commit doesn't actually fix the bug, the analysis will be incorrect

## Best Practices

1. **Verify Bug-Fix Commits**: Ensure the starting commit actually fixes a bug (check issue trackers, test results)

2. **Manual Review**: Always manually review top candidates, especially for critical bugs

3. **Context Analysis**: Consider the broader context of the code change, not just the specific lines

4. **Multiple Candidates**: Present multiple candidates rather than assuming the top result is always correct

5. **Iterative Refinement**: Use domain knowledge to refine filtering heuristics for specific projects

## Extensions and Variants

- **MA-SZZ**: Meta-data Aware SZZ that uses additional metadata
- **RA-SZZ**: Refactoring-Aware SZZ with improved refactoring detection
- **AG-SZZ**: Annotation Graph SZZ using program dependency graphs
- **PyDriller-based**: Modern implementations using PyDriller library

## References

- Śliwerski, J., Zimmermann, T., & Zeller, A. (2005). "When do changes induce fixes?"
- Kim, S., et al. (2006). "Automatic identification of bug-introducing changes"
- Da Costa, D. A., et al. (2017). "A framework for evaluating the results of the SZZ approach"
