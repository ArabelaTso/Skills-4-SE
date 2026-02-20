# Pull Request Templates

## Standard PR Template

```markdown
# [Type] Brief description of changes

## Summary

[2-3 sentence overview of what this PR does and why]

## Changes

### Added
- [New feature or functionality]
- [New file or component]

### Modified
- [Changed behavior or implementation]
- [Updated configuration or settings]

### Removed
- [Deprecated feature or code]
- [Deleted files or components]

### Fixed
- [Bug fix description]
- [Issue resolution]

## Breaking Changes

⚠️ **[Breaking change description]**

**Migration Guide:**
- Step 1: [What users need to do]
- Step 2: [How to update their code]

**Before:**
```[language]
// Old code example
```

**After:**
```[language]
// New code example
```

## Technical Details

### Implementation Approach
[Explain the technical approach taken]

### Key Design Decisions
- **Decision 1:** [Rationale]
- **Decision 2:** [Rationale]

### Architecture Changes
[Describe any architectural changes or impacts]

### Dependencies
- **Added:** `package@version` - [Why needed]
- **Updated:** `package@old-version` → `package@new-version` - [Why updated]
- **Removed:** `package@version` - [Why removed]

## Testing

### How to Test
1. [Step-by-step testing instructions]
2. [Expected behavior]
3. [Edge cases to verify]

### Test Coverage
- Added [X] unit tests
- Added [Y] integration tests
- Current coverage: [Z]%

### Manual Testing Checklist
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test edge case 1

## Security Considerations

[Any security implications or improvements]

## Performance Impact

[Expected performance changes, if any]

## Documentation

- [ ] Updated README
- [ ] Updated API documentation
- [ ] Added inline comments
- [ ] Updated changelog

## Related Issues

Closes #[issue-number]
Related to #[issue-number]

## Screenshots/Videos

[If applicable, add screenshots or videos demonstrating the changes]

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented above)
- [ ] All tests passing
```

## Compact PR Template

For smaller changes:

```markdown
# [Type] Brief description

## What
[What changed]

## Why
[Why it changed]

## Testing
[How to test]

## Notes
[Any additional context]
```

## Feature PR Template

```markdown
# Feature: [Feature Name]

## Overview
[Brief description of the feature]

## Motivation
[Why this feature is needed]

## Implementation

### User-Facing Changes
- [Change 1]
- [Change 2]

### Technical Changes
- [Implementation detail 1]
- [Implementation detail 2]

### API Changes
**New Endpoints:**
- `GET /api/resource` - [Description]

**Modified Endpoints:**
- `POST /api/resource` - [What changed]

## Usage Example

```[language]
// Example of how to use the new feature
```

## Testing
[Testing instructions]

## Documentation
- [ ] User guide updated
- [ ] API docs updated
- [ ] Examples added

## Future Work
[Optional: Related work for future PRs]
```

## Bug Fix PR Template

```markdown
# Fix: [Brief description of bug]

## Problem
[Describe the bug and its impact]

## Root Cause
[Explain what was causing the bug]

## Solution
[Describe how the fix works]

## Testing
[How to verify the fix]

## Regression Prevention
[What was added to prevent this bug from recurring]

Fixes #[issue-number]
```

## Refactoring PR Template

```markdown
# Refactor: [Component/Module name]

## Motivation
[Why this refactoring is needed]

## Changes
[What was refactored]

## Benefits
- [Benefit 1: e.g., improved maintainability]
- [Benefit 2: e.g., better performance]
- [Benefit 3: e.g., reduced complexity]

## Behavior Changes
[Confirm no behavior changes, or list any intentional changes]

## Testing
[How to verify behavior is preserved]

## Metrics
- Lines of code: [Before] → [After]
- Cyclomatic complexity: [Before] → [After]
- Test coverage: [Before] → [After]
```

## Hotfix PR Template

```markdown
# Hotfix: [Critical issue description]

## Severity
🔴 Critical / 🟡 High / 🟢 Medium

## Issue
[Describe the critical issue]

## Impact
[Who/what is affected]

## Fix
[Brief description of the fix]

## Testing
[How this was tested]

## Rollback Plan
[How to rollback if needed]

Fixes #[issue-number]
```

## PR Title Conventions

### Format
```
[Type] Brief description (max 72 characters)
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `chore:` Maintenance tasks
- `perf:` Performance improvements
- `style:` Code style changes
- `ci:` CI/CD changes
- `build:` Build system changes

### Examples
- `feat: Add user authentication with OAuth2`
- `fix: Resolve memory leak in data processor`
- `refactor: Simplify error handling logic`
- `docs: Update API documentation for v2.0`
- `test: Add integration tests for payment flow`

## PR Description Best Practices

### Summary Section
- Start with a clear, concise summary
- Explain the "what" and "why"
- Keep it under 3 sentences
- Use active voice

### Changes Section
- Group changes by type (Added/Modified/Removed/Fixed)
- Be specific but concise
- Use bullet points
- Link to related issues

### Breaking Changes Section
- Clearly mark with ⚠️ emoji
- Provide migration guide
- Show before/after examples
- Explain impact

### Technical Details Section
- Explain implementation approach
- Document key design decisions
- Note architectural changes
- List dependency changes

### Testing Section
- Provide step-by-step instructions
- Include expected results
- List edge cases to test
- Note test coverage changes

### Context Enhancements
- Security implications
- Performance impact
- Accessibility considerations
- Backward compatibility

## Common Patterns

### Pattern: API Change

```markdown
## API Changes

### Breaking Changes
⚠️ **Endpoint signature changed**

**Before:**
```http
POST /api/users
{
  "name": "John",
  "email": "john@example.com"
}
```

**After:**
```http
POST /api/users
{
  "user": {
    "name": "John",
    "email": "john@example.com"
  }
}
```

**Migration:** Wrap user data in a `user` object.
```

### Pattern: Dependency Update

```markdown
## Dependencies

### Updated
- `react@17.0.2` → `react@18.2.0`
  - Reason: Access to new concurrent features
  - Breaking: Requires updating render method
  - Migration: See [React 18 upgrade guide](link)
```

### Pattern: Performance Improvement

```markdown
## Performance Impact

### Improvements
- Database query optimization: 500ms → 50ms (90% faster)
- Memory usage reduced by 30%
- Bundle size decreased from 2.5MB to 1.8MB

### Benchmarks
[Include benchmark results or graphs]
```

### Pattern: Security Enhancement

```markdown
## Security Considerations

### Improvements
- ✅ Added input sanitization for user-generated content
- ✅ Implemented rate limiting on API endpoints
- ✅ Updated dependencies with known vulnerabilities

### Security Review
- [ ] Security team review completed
- [ ] Penetration testing performed
- [ ] Security documentation updated
```

## Review Checklist

### For PR Author
- [ ] Clear, descriptive title
- [ ] Comprehensive summary
- [ ] All changes documented
- [ ] Breaking changes highlighted
- [ ] Testing instructions provided
- [ ] Related issues linked
- [ ] Self-review completed

### For PR Reviewer
- [ ] Changes match description
- [ ] Code quality acceptable
- [ ] Tests adequate
- [ ] Documentation sufficient
- [ ] No security concerns
- [ ] Performance acceptable
- [ ] Breaking changes justified
