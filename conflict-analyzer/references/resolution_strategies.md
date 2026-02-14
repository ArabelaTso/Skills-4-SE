# Resolution Strategy Guide

This reference provides detailed strategies for resolving different types of requirement conflicts.

## Resolution Framework

### Step 1: Understand the Conflict
- Identify conflicting requirements precisely
- Understand stakeholder perspectives
- Assess business impact of each requirement
- Determine root cause of conflict

### Step 2: Evaluate Options
- Generate multiple resolution alternatives
- Analyze pros/cons of each option
- Estimate cost, time, and complexity
- Consider long-term implications

### Step 3: Select Strategy
- Choose appropriate resolution approach
- Document decision rationale
- Get stakeholder buy-in
- Update requirements accordingly

### Step 4: Implement Resolution
- Update conflicting requirements
- Communicate changes to team
- Update related documentation
- Verify conflict is resolved

---

## Resolution Strategies by Conflict Type

### 1. Prioritization

**When to Use:**
- Resource conflicts (can't do both)
- Timeline conflicts
- Priority conflicts
- Budget constraints

**Approach:**
- Rank requirements by business value
- Consider criticality and urgency
- Implement high-priority first
- Defer or drop low-priority

**Example:**
```
Conflict: Both "Mobile app" and "API redesign" needed by Q1, only one fits timeline

Resolution: Prioritize by business value
- Mobile app: High customer demand, competitive pressure → Priority 1
- API redesign: Internal improvement, technical debt → Priority 2
→ Decision: Ship mobile app Q1, API redesign Q2
```

---

### 2. Sequencing

**When to Use:**
- Temporal conflicts with dependencies
- Resource conflicts over time
- Dependency chains

**Approach:**
- Create dependency graph
- Identify critical path
- Schedule in correct order
- Adjust timelines to accommodate sequence

**Example:**
```
Conflict: Dashboard due March 1, Authentication due March 15, but dashboard needs auth

Resolution: Sequence properly
- Authentication: Feb 1 - Feb 28 (moved earlier)
- Dashboard: March 1 - March 15 (starts after auth complete)
→ Decision: Reschedule auth to complete before dashboard
```

---

### 3. Decomposition

**When to Use:**
- Large features with conflicting aspects
- Scope conflicts
- Complex requirements with separable parts

**Approach:**
- Break requirement into smaller pieces
- Satisfy non-conflicting parts
- Address conflicting parts separately
- Phase implementation

**Example:**
```
Conflict: "Support offline mode" vs "Real-time collaboration"

Resolution: Decompose into modes
- Online mode: Full real-time collaboration
- Offline mode: Local editing, sync when reconnected
- Conflict detection: Handle merge conflicts on reconnection
→ Decision: Support both modes with clear transitions
```

---

### 4. Compromise

**When to Use:**
- Both requirements have merit
- Middle ground exists
- Stakeholders willing to negotiate

**Approach:**
- Find acceptable middle ground
- Each side gives up something
- Achieve partial satisfaction of both
- Document trade-offs

**Example:**
```
Conflict: "Auto-save every keystroke" vs "Require explicit save confirmation"

Resolution: Compromise approach
- Auto-save drafts every 30 seconds (background)
- Require confirmation for final "Publish" action
- Show "Draft saved" indicator
→ Decision: Auto-save drafts, confirm publish
```

---

### 5. Conditional Logic

**When to Use:**
- Context-dependent requirements
- Different users need different behaviors
- Mode-based conflicts

**Approach:**
- Apply different rules in different contexts
- Use feature flags or configuration
- Implement if/else logic
- Document conditions clearly

**Example:**
```
Conflict: "Password must be 12+ characters" vs "Support legacy 6-character passwords"

Resolution: Conditional rules
- New accounts: Require 12+ characters
- Legacy accounts: Accept 6+ characters, prompt to upgrade
- After upgrade: Enforce 12+ characters for all
→ Decision: Different rules for new vs legacy, migration path
```

---

### 6. Technical Solution

**When to Use:**
- Technical conflicts with engineering solutions
- Performance conflicts
- Platform conflicts

**Approach:**
- Apply technical pattern or architecture
- Use appropriate technology
- Add abstraction layer
- Optimize implementation

**Example:**
```
Conflict: "Real-time updates" vs "REST API only"

Resolution: Technical solution
- Keep REST API for primary operations
- Add WebSocket endpoint for real-time events
- Server pushes updates via WebSocket
- Fallback to polling if WebSocket unavailable
→ Decision: Hybrid approach with REST + WebSocket
```

---

### 7. Scope Adjustment

**When to Use:**
- Scope conflicts
- Feature creep
- Out-of-boundary requirements

**Approach:**
- Clarify project boundaries
- Move out-of-scope items to backlog
- Define what's included/excluded
- Create future roadmap for deferred items

**Example:**
```
Conflict: "Internal user management" vs "Support external partner accounts"

Resolution: Scope clarification
- Phase 1 (current scope): Internal users only
- Phase 2 (future roadmap): External partner support
- Document partner requirements for future
→ Decision: Partners out of scope for v1, planned for v2
```

---

### 8. Stakeholder Negotiation

**When to Use:**
- Priority conflicts between stakeholders
- Political conflicts
- Business vs technical conflicts

**Approach:**
- Facilitate stakeholder meeting
- Present conflict and impact clearly
- Explore options together
- Reach consensus or escalate decision
- Document agreement

**Example:**
```
Conflict: Marketing wants features, Security wants restrictions

Resolution: Joint decision session
- Present: Feature value vs security risk
- Discuss: Acceptable risk levels
- Agree: Implement feature with security controls
→ Decision: Feature approved with MFA requirement
```

---

### 9. Relaxation

**When to Use:**
- Over-constrained requirements
- Conflicting constraints
- Performance vs completeness

**Approach:**
- Identify which constraint can be relaxed
- Adjust threshold or target
- Accept "good enough" vs perfect
- Document acceptable range

**Example:**
```
Conflict: "Page load < 1 second" vs "Display 500 items with images"

Resolution: Relax constraints
- Reduce items per page: 50 instead of 500
- Or relax timing: < 2 seconds instead of < 1 second
- Or lazy load: Initial view < 1s, scroll loads more
→ Decision: Show 50 items initially, lazy load rest
```

---

### 10. Parallel Tracks

**When to Use:**
- Resource conflicts with available capacity
- Independent features
- Can work simultaneously

**Approach:**
- Allocate separate teams/resources
- Work on both in parallel
- Coordinate integration points
- Merge at completion

**Example:**
```
Conflict: "Mobile app" and "Admin dashboard" both needed, same timeline

Resolution: Parallel development
- Team A: Mobile app (3 developers)
- Team B: Admin dashboard (2 developers)
- Shared: Backend API (coordinated)
→ Decision: Develop both simultaneously with separate teams
```

---

## Resolution Decision Matrix

| Conflict Type | Recommended Strategies |
|---------------|------------------------|
| Logical | Prioritization, Conditional Logic, Stakeholder Negotiation |
| Technical | Technical Solution, Decomposition, Scope Adjustment |
| Resource | Prioritization, Sequencing, Parallel Tracks |
| Temporal | Sequencing, Relaxation, Scope Adjustment |
| Data | Technical Solution, Conditional Logic, Decomposition |
| State | Decomposition, Conditional Logic, Technical Solution |
| Priority | Stakeholder Negotiation, Prioritization, Compromise |
| Scope | Scope Adjustment, Prioritization, Sequencing |

---

## Communication Templates

### Presenting Conflict to Stakeholders

```
Subject: Requirement Conflict: [Brief Description]

Conflict Summary:
- REQ-A: [Requirement A]
- REQ-B: [Requirement B]
- Issue: [Why they conflict]

Impact if Unresolved:
- [Consequence 1]
- [Consequence 2]

Proposed Options:
1. Option A: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Impact: [Time/cost/scope]

2. Option B: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Impact: [Time/cost/scope]

Recommendation: [Your recommendation with rationale]

Decision Needed By: [Date]
```

### Documenting Resolution

```
Conflict ID: CONF-001
Date Resolved: [Date]
Resolved By: [Names]

Original Conflict:
- REQ-A: [Requirement A]
- REQ-B: [Requirement B]

Resolution Strategy: [Strategy name]

Resolution Details:
[Specific resolution]

Updated Requirements:
- REQ-A (Updated): [New version]
- REQ-B (Updated): [New version]

Trade-offs Accepted:
- [Trade-off 1]
- [Trade-off 2]

Action Items:
- [ ] Update requirements document
- [ ] Notify affected teams
- [ ] Update project timeline
- [ ] Update budget/resources
```

---

## Best Practices

1. **Act Early**: Resolve conflicts as soon as detected
2. **Involve Stakeholders**: Get input from affected parties
3. **Document Everything**: Record conflicts, decisions, rationale
4. **Consider Long-term**: Think beyond immediate resolution
5. **Validate Resolution**: Ensure conflict is actually resolved
6. **Communicate Widely**: Notify all affected parties
7. **Learn**: Track conflict patterns to prevent future issues
8. **Be Transparent**: Explain trade-offs clearly
9. **Get Sign-off**: Confirm stakeholder acceptance
10. **Follow Up**: Verify resolution works in practice
