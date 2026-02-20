# Clarification Question Templates

This reference provides templates for generating effective clarifying questions for ambiguous requirements.

## Question Types

### 1. Quantification Questions

**When:** Vague quantities, ranges, or measurements

**Templates:**
- "What is the exact number/amount of [item]?"
- "What is the minimum and maximum acceptable value for [metric]?"
- "How do you define '[vague quantifier]' numerically?"
- "What threshold determines [condition]?"
- "What percentage/ratio constitutes [description]?"

**Examples:**

Requirement: "System should handle many users"
→ "How many concurrent users should the system support? (e.g., 100? 1,000? 10,000?)"
→ "What is the expected peak load?"
→ "What happens when user count exceeds capacity?"

Requirement: "Show recent activity"
→ "How many recent activities should be displayed? (e.g., 5? 10? 20?)"
→ "What time period defines 'recent'? (last hour? day? week?)"
→ "How should activities be sorted?"

### 2. Temporal Questions

**When:** Unclear timing, frequency, or duration

**Templates:**
- "How long should [action] take?"
- "What is the exact time interval for [recurring action]?"
- "When exactly should [event] occur?"
- "What is the acceptable response time/latency?"
- "How often should [action] happen?"
- "What is the timeout duration?"

**Examples:**

Requirement: "Update data frequently"
→ "How often should data be updated? (every second? minute? hour?)"
→ "Should updates happen on a schedule or triggered by events?"
→ "What happens if an update fails?"

Requirement: "Process requests quickly"
→ "What is the maximum acceptable processing time?"
→ "Should this be measured as average, median, or 95th percentile?"
→ "What happens if processing exceeds the time limit?"

### 3. Scope Definition Questions

**When:** Unclear boundaries or extent

**Templates:**
- "Which specific [items/users/entities] are included/excluded?"
- "What are the exact boundaries of [scope]?"
- "Does this apply to all [category] or only [subset]?"
- "What are the exceptions to this rule?"
- "Which [options/formats/types] should be supported?"

**Examples:**

Requirement: "All users can access the dashboard"
→ "Does 'all users' include: (1) Unauthenticated visitors? (2) All authenticated users? (3) Only users with specific roles?"
→ "Are there any user types that should be excluded?"
→ "What should guest users see instead?"

Requirement: "Export to multiple formats"
→ "Which specific file formats should be supported? (CSV, PDF, Excel, JSON, XML?)"
→ "Should all formats support the same data fields?"
→ "Are there any format-specific requirements?"

### 4. Condition and Trigger Questions

**When:** Unclear conditions, triggers, or dependencies

**Templates:**
- "Under what specific conditions does [action] occur?"
- "What triggers [event]?"
- "What must be true before [action] can happen?"
- "When should [condition] be checked?"
- "What happens if [condition] is not met?"

**Examples:**

Requirement: "Send notification when appropriate"
→ "What specific conditions trigger a notification?"
→ "Who should receive the notification?"
→ "What should the notification contain?"
→ "How should notifications be delivered (email, SMS, in-app)?"

Requirement: "Validate user input"
→ "Which specific fields need validation?"
→ "What are the validation rules for each field?"
→ "When should validation occur (on blur, on submit, real-time)?"
→ "What error messages should be displayed for each validation failure?"

### 5. Behavior Specification Questions

**When:** Unclear system behavior or outcomes

**Templates:**
- "What should happen when [scenario]?"
- "What is the expected output given [input]?"
- "How should the system respond to [action]?"
- "What is the desired outcome of [operation]?"
- "What side effects should [action] produce?"

**Examples:**

Requirement: "Calculate total price"
→ "Should the total include: (1) Tax? (2) Shipping? (3) Discounts? (4) Fees?"
→ "How should the price be rounded?"
→ "In what currency should the price be displayed?"
→ "How should multi-currency orders be handled?"

Requirement: "Handle errors gracefully"
→ "What specific errors need to be handled?"
→ "What should be displayed to the user for each error type?"
→ "Should errors be logged? Where and how?"
→ "Should the user be able to retry? How many times?"

### 6. Error and Edge Case Questions

**When:** Missing error handling or edge case specifications

**Templates:**
- "What should happen if [error condition]?"
- "How should [boundary case] be handled?"
- "What happens when [input] is null/empty/invalid?"
- "How should the system behave during [exceptional scenario]?"
- "What if [operation] fails?"

**Examples:**

Requirement: "Allow file uploads"
→ "What file types are allowed?"
→ "What is the maximum file size?"
→ "What happens if the file is too large?"
→ "What happens if the upload fails mid-transfer?"
→ "Should there be virus scanning? Validation?"

Requirement: "Display user profile"
→ "What should be displayed if profile data is missing?"
→ "What if the user has no profile picture?"
→ "How should deleted user profiles appear?"
→ "What privacy controls affect what's displayed?"

### 7. Definition Questions

**When:** Undefined terms or jargon

**Templates:**
- "What does [term] mean specifically in this context?"
- "Which [system/tool/technology] should be used?"
- "Can you provide an example of [concept]?"
- "How is [term] different from [similar term]?"
- "What are the specific characteristics of [entity]?"

**Examples:**

Requirement: "Integrate with the API"
→ "Which specific API (name, version)?"
→ "What authentication method does it use?"
→ "What endpoints need to be integrated?"
→ "What is the expected response format?"

Requirement: "Implement caching"
→ "What caching technology should be used? (Redis, Memcached, in-memory?)"
→ "What data should be cached?"
→ "What is the cache expiration policy?"
→ "How should cache invalidation work?"

### 8. Priority and Constraint Questions

**When:** Unclear importance or limitations

**Templates:**
- "Is this requirement mandatory, recommended, or optional?"
- "What is the priority level (critical, high, medium, low)?"
- "What constraints apply to [requirement]?"
- "What trade-offs are acceptable?"
- "What is the relative importance compared to [other requirement]?"

**Examples:**

Requirement: "The system should be secure"
→ "What specific security requirements are mandatory? (encryption, 2FA, audit logs?)"
→ "What security standards must be met? (SOC 2, ISO 27001, PCI DSS?)"
→ "What are the acceptable security vs. usability trade-offs?"

Requirement: "Support mobile devices"
→ "Which specific devices/OS versions must be supported?"
→ "Is a responsive web design sufficient, or is a native app required?"
→ "What features can be reduced on mobile vs. desktop?"

### 9. Data Format Questions

**When:** Unclear data structure or format

**Templates:**
- "What is the exact format of [data]?"
- "What fields/properties should [entity] contain?"
- "What is the data type for [field]?"
- "What is the expected structure of [input/output]?"
- "Are there any data validation rules?"

**Examples:**

Requirement: "Store user information"
→ "What specific user fields should be stored? (name, email, phone, address?)"
→ "What is the format for each field? (phone: international? email: validated?)"
→ "Which fields are required vs. optional?"
→ "How should names with special characters be handled?"

Requirement: "Accept date input"
→ "What date format should be accepted? (MM/DD/YYYY, DD/MM/YYYY, ISO 8601?)"
→ "Should the system accept multiple formats?"
→ "What timezone should be used?"
→ "What is the valid date range?"

### 10. Success Criteria Questions

**When:** No clear acceptance criteria

**Templates:**
- "How will you know this requirement is successfully implemented?"
- "What would a successful test of this feature demonstrate?"
- "What metrics define success?"
- "What must be true for this to be considered 'done'?"

**Examples:**

Requirement: "Improve performance"
→ "What specific operations should be faster?"
→ "By how much should performance improve? (percentage? absolute time?)"
→ "What metrics will be used to measure improvement?"
→ "What is the target vs. current performance?"

Requirement: "Make the UI intuitive"
→ "What specific usability metrics will be tracked?"
→ "What user testing will validate intuitiveness?"
→ "What is the target task completion rate?"
→ "What is the acceptable learning curve?"

## Question Formulation Guidelines

### DO:
- Ask one clear question at a time
- Provide specific options when possible
- Include examples to illustrate
- Explain why the clarification matters
- Suggest reasonable defaults

### DON'T:
- Ask compound questions
- Use technical jargon without explanation
- Make assumptions in questions
- Ask leading questions
- Overwhelm with too many questions at once

## Prioritizing Questions

When multiple clarifications are needed, prioritize:

1. **Critical path questions** - Blocking core functionality
2. **Risk reduction questions** - High-impact ambiguities
3. **Scope questions** - Define boundaries
4. **Technical feasibility questions** - Can it be built?
5. **Nice-to-have clarifications** - Optimize later

## Response Format

Structure clarifying questions as:

```markdown
**Requirement:** [Original ambiguous requirement]

**Ambiguity Detected:** [What is unclear]

**Questions:**
1. [First clarifying question]
   - Suggested options: [Option A] | [Option B] | [Option C]

2. [Second clarifying question]
   - Example: [Concrete example]

**Suggested Clarification:** [Proposed clear version with assumptions noted]
```
