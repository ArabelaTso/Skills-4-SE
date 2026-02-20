# Requirement Analysis Framework

## Analysis Dimensions

### 1. Clarity and Precision

**Check for**:
- Vague terms ("fast", "user-friendly", "efficient", "robust")
- Ambiguous pronouns ("it", "they", "this")
- Undefined technical terms
- Missing quantitative metrics
- Unclear scope boundaries

**Questions to ask**:
- What exactly does [vague term] mean in measurable terms?
- What specific value/threshold defines success?
- What is included/excluded from scope?

### 2. Completeness

**Check for**:
- Missing functional requirements
- Missing non-functional requirements (performance, security, usability)
- Undefined inputs/outputs
- Unspecified error handling
- Missing edge cases
- Undefined user roles/permissions

**Questions to ask**:
- What happens when [edge case]?
- Who can perform this action?
- What are the performance requirements?
- How should errors be handled?

### 3. Consistency

**Check for**:
- Conflicting requirements
- Contradictory constraints
- Incompatible assumptions
- Terminology inconsistencies

**Questions to ask**:
- How do requirements X and Y work together?
- Is [term A] the same as [term B]?
- Can both constraints be satisfied simultaneously?

### 4. Feasibility

**Check for**:
- Technical impossibilities
- Resource constraints
- Timeline conflicts
- Dependency issues

**Questions to ask**:
- Is this technically achievable with current technology?
- Are there known limitations?
- What dependencies exist?

### 5. Testability

**Check for**:
- Untestable requirements
- Missing acceptance criteria
- Undefined success metrics
- Unclear verification methods

**Questions to ask**:
- How will we verify this requirement is met?
- What constitutes passing/failing?
- What test scenarios are needed?

## Common Ambiguity Patterns

### Pattern 1: Quantifier Ambiguity

**Vague**: "The system should be fast"
**Issues**: What is "fast"? For whom? Under what conditions?
**Enhanced**: "The system should respond to user queries within 200ms for 95% of requests under normal load (≤1000 concurrent users)"

### Pattern 2: Modal Ambiguity

**Vague**: "The system should support multiple users"
**Issues**: "Should" vs "must"? How many users? Concurrent or total?
**Enhanced**: "The system MUST support at least 10,000 concurrent users with no degradation in response time"

### Pattern 3: Scope Ambiguity

**Vague**: "Users can edit documents"
**Issues**: Which users? What documents? What edits? When?
**Enhanced**: "Authenticated users with 'Editor' role can modify the content, title, and tags of documents they own or have been granted edit permission for"

### Pattern 4: Temporal Ambiguity

**Vague**: "The system should backup data regularly"
**Issues**: How often? When? What data?
**Enhanced**: "The system MUST perform incremental backups of all user data every 6 hours and full backups daily at 2 AM UTC"

### Pattern 5: Conditional Ambiguity

**Vague**: "If the user is inactive, log them out"
**Issues**: What defines "inactive"? How long? What happens to unsaved work?
**Enhanced**: "If a user has no keyboard/mouse activity for 30 minutes, display a warning. If no activity for an additional 5 minutes, save any unsaved work and log them out"

## Domain-Specific Considerations

### Web Applications

**Standard concerns**:
- Authentication and authorization
- Session management
- Data validation
- Error handling
- Browser compatibility
- Responsive design
- Accessibility (WCAG compliance)
- Security (OWASP top 10)

### APIs

**Standard concerns**:
- Request/response formats
- Authentication methods
- Rate limiting
- Versioning strategy
- Error codes and messages
- Documentation
- Backward compatibility

### Data Processing

**Standard concerns**:
- Input data format and validation
- Output data format
- Data transformation rules
- Error handling for malformed data
- Performance requirements
- Data volume limits
- Idempotency

### Real-time Systems

**Standard concerns**:
- Latency requirements
- Throughput requirements
- Consistency guarantees
- Failure handling
- Recovery procedures
- Monitoring and alerting

## Risk Indicators

### High-Risk Patterns

🔴 **Critical ambiguity**: Core functionality undefined
🔴 **Conflicting requirements**: Cannot be satisfied simultaneously
🔴 **Missing constraints**: No bounds on resources/performance
🔴 **Undefined failure modes**: No error handling specified
🔴 **Implicit assumptions**: Unstated dependencies

### Medium-Risk Patterns

🟡 **Vague metrics**: Qualitative instead of quantitative
🟡 **Incomplete edge cases**: Some scenarios unaddressed
🟡 **Unclear priorities**: No indication of must-have vs nice-to-have
🟡 **Missing non-functionals**: Performance/security not specified

### Low-Risk Patterns

🟢 **Minor terminology issues**: Inconsistent naming
🟢 **Formatting issues**: Structure could be improved
🟢 **Missing examples**: Would benefit from illustrations

## Enrichment Strategies

### Strategy 1: Add Standard Constraints

For common requirement types, add industry-standard constraints:

**Example**: "User authentication"
**Add**:
- Password requirements (length, complexity)
- Session timeout
- Failed login attempt limits
- Password reset mechanism
- Multi-factor authentication option

### Strategy 2: Specify Edge Cases

Identify and specify behavior for:
- Empty inputs
- Maximum/minimum values
- Concurrent operations
- Network failures
- Invalid data
- Boundary conditions

### Strategy 3: Add Acceptance Criteria

For each requirement, add:
- Given [precondition]
- When [action]
- Then [expected result]

### Strategy 4: Distinguish Requirement Types

Categorize as:
- **MUST**: Mandatory, non-negotiable
- **SHOULD**: Highly desired, may be deferred
- **MAY**: Optional, nice-to-have
- **MUST NOT**: Explicitly forbidden

### Strategy 5: Add Traceability

Link requirements to:
- Business goals
- User stories
- Use cases
- Test cases
- Design decisions
