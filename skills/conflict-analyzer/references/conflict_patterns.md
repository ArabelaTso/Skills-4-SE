# Conflict Type Patterns

This reference provides comprehensive patterns for detecting conflicts in software requirements.

## Table of Contents

1. [Logical Conflicts](#logical-conflicts)
2. [Technical Conflicts](#technical-conflicts)
3. [Resource Conflicts](#resource-conflicts)
4. [Temporal Conflicts](#temporal-conflicts)
5. [Data Conflicts](#data-conflicts)
6. [State Conflicts](#state-conflicts)
7. [Priority Conflicts](#priority-conflicts)
8. [Scope Conflicts](#scope-conflicts)

---

## Logical Conflicts

### Description
Requirements that directly contradict each other or specify mutually exclusive behaviors.

### Detection Patterns

**Direct Contradictions:**
- REQ-A: "System must work offline"
- REQ-B: "System requires continuous internet connection"
→ **Conflict:** Cannot be both offline and require continuous connection

**Mutually Exclusive Features:**
- REQ-A: "All data must be encrypted at rest"
- REQ-B: "Support full-text search across all data fields"
→ **Conflict:** Full-text search typically requires unencrypted searchable indexes

**Opposite Behaviors:**
- REQ-A: "Automatically save changes without user confirmation"
- REQ-B: "Require explicit user confirmation before saving any changes"
→ **Conflict:** Cannot both auto-save and require confirmation

### Resolution Strategies
1. **Prioritize**: Choose the more critical requirement
2. **Conditional**: Apply different rules in different contexts
3. **Compromise**: Find middle ground (e.g., auto-save drafts, confirm final save)
4. **Stakeholder Decision**: Escalate for business decision

---

## Technical Conflicts

### Description
Requirements with incompatible technical constraints, platforms, or technologies.

### Detection Patterns

**Platform Incompatibility:**
- REQ-A: "Support Internet Explorer 11"
- REQ-B: "Use ES2022 JavaScript features"
→ **Conflict:** IE11 doesn't support modern JavaScript

**Technology Stack Conflicts:**
- REQ-A: "Use MySQL database"
- REQ-B: "Store documents with flexible schema"
→ **Conflict:** MySQL is relational; flexible schema suggests NoSQL

**API Version Conflicts:**
- REQ-A: "Integrate with Payment API v1"
- REQ-B: "Use webhook signature validation" (only available in v2)
→ **Conflict:** Feature requires newer API version

**Protocol Incompatibility:**
- REQ-A: "Support real-time collaboration"
- REQ-B: "Use REST API exclusively"
→ **Conflict:** Real-time typically requires WebSockets, not just REST

### Resolution Strategies
1. **Upgrade**: Move to compatible versions/technologies
2. **Polyfill**: Add compatibility layers
3. **Isolate**: Use different tech for different features
4. **Drop**: Remove less critical incompatible requirement

---

## Resource Conflicts

### Description
Requirements competing for limited resources (time, budget, personnel, infrastructure).

### Detection Patterns

**Team Capacity:**
- REQ-A: "Deliver mobile app by Q1" (requires 3 developers, 3 months)
- REQ-B: "Rebuild backend API by Q1" (requires 3 developers, 3 months)
→ **Conflict:** Only 3 developers available, both can't be done simultaneously

**Infrastructure Limits:**
- REQ-A: "Store all user activity logs indefinitely"
- REQ-B: "Operate within $500/month cloud budget"
→ **Conflict:** Unlimited storage exceeds budget

**Performance vs. Features:**
- REQ-A: "Page load time under 1 second"
- REQ-B: "Display 500 items per page"
- REQ-C: "Include high-resolution images for each item"
→ **Conflict:** Loading 500 hi-res images violates performance requirement

**Bandwidth Constraints:**
- REQ-A: "Support 10,000 concurrent video streams"
- REQ-B: "Maximum bandwidth: 1 Gbps"
→ **Conflict:** 10,000 streams exceed bandwidth

### Resolution Strategies
1. **Prioritize**: Sequence features by importance
2. **Phase**: Implement in stages over time
3. **Scale Resources**: Increase budget/team/infrastructure
4. **Optimize**: Find more efficient implementations
5. **Reduce Scope**: Lower targets (e.g., fewer items per page)

---

## Temporal Conflicts

### Description
Requirements with incompatible timelines, sequences, or deadlines.

### Detection Patterns

**Dependency Deadline Conflict:**
- REQ-A: "Launch user dashboard by March 1"
- REQ-B: "User authentication system ready by March 15"
→ **Conflict:** Dashboard depends on auth, but auth is due after dashboard

**Impossible Timeline:**
- REQ-A: "Complete full redesign in 2 weeks"
- REQ-B: "Conduct user research and A/B testing before launch"
→ **Conflict:** Research + testing + redesign cannot fit in 2 weeks

**Frequency Conflicts:**
- REQ-A: "Send daily summary email"
- REQ-B: "Send weekly summary email"
→ **Conflict:** Cannot be both daily and weekly (unless both are needed)

**Processing Time Conflict:**
- REQ-A: "Process all transactions in real-time (< 100ms)"
- REQ-B: "Run fraud detection on all transactions" (requires 500ms)
→ **Conflict:** Fraud detection time exceeds real-time requirement

### Resolution Strategies
1. **Reschedule**: Adjust deadlines to respect dependencies
2. **Parallel Work**: Work on independent parts simultaneously
3. **Fast Track**: Add resources to critical path
4. **Async Processing**: Move time-consuming tasks to background
5. **Relax Constraints**: Extend deadlines or reduce scope

---

## Data Conflicts

### Description
Requirements specifying incompatible data structures, formats, or validation rules.

### Detection Patterns

**Format Conflicts:**
- REQ-A: "Store phone numbers in international format (+1-555-1234)"
- REQ-B: "Accept phone numbers in any format users prefer"
→ **Conflict:** Storage format differs from input format

**Validation Rule Conflicts:**
- REQ-A: "Password must be at least 12 characters"
- REQ-B: "Support legacy accounts with 6-character passwords"
→ **Conflict:** Minimum length differs for new vs. legacy

**Data Type Conflicts:**
- REQ-A: "Store price as integer (cents)"
- REQ-B: "Support fractional cents for tax calculations"
→ **Conflict:** Integer storage can't represent fractional cents

**Uniqueness Conflicts:**
- REQ-A: "Email addresses must be unique across all users"
- REQ-B: "Allow multiple accounts with same email"
→ **Conflict:** Cannot be both unique and non-unique

**Retention Conflicts:**
- REQ-A: "Delete user data immediately upon account closure"
- REQ-B: "Maintain audit logs of all transactions for 7 years"
→ **Conflict:** Audit logs contain user data that should be deleted

### Resolution Strategies
1. **Normalize on Input**: Accept flexible input, normalize to standard format
2. **Versioning**: Support different rules for different versions
3. **Precision Upgrade**: Use more precise data type
4. **Anonymize**: Keep logs but remove PII
5. **Exception Handling**: Define specific exceptions to rules

---

## State Conflicts

### Description
Requirements defining incompatible state machines or state transitions.

### Detection Patterns

**Invalid Transition:**
- REQ-A: "Orders can be cancelled if status is 'pending' or 'processing'"
- REQ-B: "Orders in 'processing' status cannot be modified"
→ **Conflict:** Cancellation is a modification

**State Overlap:**
- REQ-A: "When order is 'shipped', mark as 'complete'"
- REQ-B: "Order status is 'delivered' when customer receives it"
→ **Conflict:** When does 'complete' happen? At shipping or delivery?

**Circular State:**
- REQ-A: "Draft documents can be published"
- REQ-B: "Published documents can be reverted to draft"
- REQ-C: "Draft documents are deleted after 30 days"
→ **Conflict:** Published→Draft→Deleted means published docs can be deleted

**Concurrent State Conflict:**
- REQ-A: "User can be in only one role: Viewer, Editor, or Admin"
- REQ-B: "Users can have Editor role for some projects and Admin for others"
→ **Conflict:** Single role vs. multiple roles per context

### Resolution Strategies
1. **Refine States**: Add intermediate states
2. **Context-Specific**: States apply per context (e.g., per project)
3. **State Hierarchy**: Allow sub-states or composite states
4. **Transition Guards**: Add conditions to transitions
5. **History Tracking**: Keep state history to resolve ambiguities

---

## Priority Conflicts

### Description
Requirements from different stakeholders with competing priorities.

### Detection Patterns

**Feature Priority:**
- Stakeholder A: "Search is critical, must be in v1"
- Stakeholder B: "Export is critical, must be in v1"
- Reality: "Only time/budget for one feature in v1"
→ **Conflict:** Both can't be critical if only one fits

**Performance vs. Security:**
- Security Team: "All API calls require 2FA" (adds latency)
- Product Team: "API response time must be under 200ms"
→ **Conflict:** Security requirement prevents meeting performance target

**User Experience vs. Compliance:**
- UX Team: "Single-click checkout for returning customers"
- Legal Team: "Require explicit consent checkbox for each purchase"
→ **Conflict:** Extra click conflicts with single-click UX

**Cost vs. Reliability:**
- Finance: "Reduce cloud costs by 50%"
- Engineering: "Maintain 99.99% uptime"
→ **Conflict:** Cost reduction may compromise redundancy needed for uptime

### Resolution Strategies
1. **Stakeholder Negotiation**: Facilitate discussion to align priorities
2. **Data-Driven**: Use metrics to objectively prioritize
3. **Phasing**: Address different priorities in different releases
4. **Trade-off Analysis**: Quantify costs/benefits of each option
5. **Executive Decision**: Escalate to decision authority

---

## Scope Conflicts

### Description
Requirements that expand beyond defined project boundaries or contradict scope constraints.

### Detection Patterns

**Scope Creep:**
- Project Scope: "User management for internal employees"
- REQ-A: "Support external partner accounts"
→ **Conflict:** Partners are outside defined scope

**Platform Scope:**
- Project Scope: "Web application only"
- REQ-A: "Users can upload photos from mobile app"
→ **Conflict:** Requires mobile app outside scope

**Integration Scope:**
- Project Scope: "Standalone application"
- REQ-A: "Sync data with ERP system"
→ **Conflict:** Integration outside standalone scope

**Boundary Violations:**
- Component Scope: "Shopping cart handles cart operations only"
- REQ-A: "Shopping cart sends confirmation emails"
→ **Conflict:** Email is outside cart responsibility

### Resolution Strategies
1. **Scope Expansion**: Formally expand scope if critical
2. **Defer**: Move to future phase/project
3. **Reject**: Remove requirement as out of scope
4. **Bridge**: Create minimal integration point
5. **Redefine**: Clarify what's actually in scope

---

## Detection Checklist

For each pair of requirements, check:

- [ ] Do they specify opposite behaviors?
- [ ] Do they require incompatible technologies?
- [ ] Do they compete for the same limited resources?
- [ ] Do they have conflicting deadlines or sequences?
- [ ] Do they specify different data formats/rules?
- [ ] Do they define incompatible state transitions?
- [ ] Do stakeholders prioritize them differently?
- [ ] Does one expand scope beyond the other's boundaries?
- [ ] Are success criteria mutually exclusive?
- [ ] Would satisfying both create technical debt or complexity?

---

## Severity Assessment

**Critical:**
- Impossible to satisfy both requirements
- Fundamental architectural conflict
- Legal/regulatory conflict

**High:**
- Major rework needed to reconcile
- Significant cost or timeline impact
- Affects core functionality

**Medium:**
- Workaround available but not ideal
- Moderate effort to resolve
- Affects secondary features

**Low:**
- Minor inconsistency
- Easy to resolve through clarification
- No significant impact
