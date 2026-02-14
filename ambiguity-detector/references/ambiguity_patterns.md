# Ambiguity Patterns in Requirements

This reference provides comprehensive patterns for detecting ambiguous language in software requirements.

## Table of Contents

1. [Vague Quantifiers](#vague-quantifiers)
2. [Temporal Ambiguity](#temporal-ambiguity)
3. [Unclear Scope and Boundaries](#unclear-scope-and-boundaries)
4. [Weak Verbs and Conditionals](#weak-verbs-and-conditionals)
5. [Undefined Terms](#undefined-terms)
6. [Incomplete Specifications](#incomplete-specifications)
7. [Subjective Language](#subjective-language)
8. [Implicit Assumptions](#implicit-assumptions)
9. [Pronouns and References](#pronouns-and-references)
10. [Missing Edge Cases](#missing-edge-cases)

---

## Vague Quantifiers

### Problem
Imprecise quantities that mean different things to different people.

### Patterns to Flag

**Vague quantity words:**
- "some", "many", "few", "several", "most", "numerous"
- "a lot", "a bunch", "various", "multiple", "enough"
- "reasonable", "adequate", "sufficient", "minimal", "maximum"
- "appropriate", "typical", "normal", "usual", "regular"

**Examples:**

❌ Ambiguous: "The system should handle many concurrent users"
- How many is "many"? 10? 100? 10,000?

✅ Clear: "The system should handle at least 1,000 concurrent users"

❌ Ambiguous: "Show a few recent orders"
- How many is "a few"? 3? 5? 10?

✅ Clear: "Show the 5 most recent orders"

❌ Ambiguous: "Response time should be reasonable"
- What is "reasonable"? 1 second? 5 seconds? 1 minute?

✅ Clear: "Response time should be under 2 seconds for 95% of requests"

### Clarifying Questions
- "Exactly how many/much?"
- "What is the minimum/maximum acceptable value?"
- "What numeric threshold defines [vague term]?"

---

## Temporal Ambiguity

### Problem
Unclear timing, sequences, or durations.

### Patterns to Flag

**Vague temporal words:**
- "soon", "later", "eventually", "quickly", "slowly"
- "recently", "frequently", "occasionally", "rarely", "periodically"
- "as soon as possible", "timely", "promptly", "immediately"
- "before", "after" (without specific reference)
- "real-time", "near real-time" (without definition)

**Examples:**

❌ Ambiguous: "The system should update frequently"
- How often? Every second? Minute? Hour?

✅ Clear: "The system should update every 5 minutes"

❌ Ambiguous: "Process the request immediately"
- How fast is "immediately"? Milliseconds? Seconds?

✅ Clear: "Process the request within 100 milliseconds"

❌ Ambiguous: "Backup data regularly"
- Daily? Weekly? Monthly?

✅ Clear: "Backup data daily at 2:00 AM UTC"

### Clarifying Questions
- "How long should this take?"
- "What is the exact time interval?"
- "When exactly should this happen?"
- "What is the deadline or timeout?"

---

## Unclear Scope and Boundaries

### Problem
Undefined extent, ranges, or limits.

### Patterns to Flag

**Scope ambiguity words:**
- "all", "any", "everything", "nothing" (without qualification)
- "the system", "the user", "the data" (which one?)
- "etc.", "and so on", "and more"
- "relevant", "applicable", "appropriate"
- "where applicable", "as needed", "when necessary"

**Examples:**

❌ Ambiguous: "All users can view the dashboard"
- All users including guests? Only authenticated users? Admin users?

✅ Clear: "All authenticated users with 'viewer' role or higher can view the dashboard"

❌ Ambiguous: "Export data to various formats"
- Which formats? PDF, CSV, JSON, XML, Excel? All of them?

✅ Clear: "Export data to CSV, PDF, and Excel formats"

❌ Ambiguous: "Validate user input"
- Which inputs? All form fields? Specific fields? What validation rules?

✅ Clear: "Validate email format, password strength (min 8 chars, 1 number, 1 special char), and required fields (name, email, password)"

### Clarifying Questions
- "Which specific items/users/data are included?"
- "What are the exact boundaries?"
- "Are there any exceptions?"
- "What is excluded from this requirement?"

---

## Weak Verbs and Conditionals

### Problem
Unclear obligation levels or conditional language without clear conditions.

### Patterns to Flag

**Weak modal verbs:**
- "might", "could", "may", "can"
- "should" (without clear priority)
- "would be nice", "ideally", "preferably"
- "try to", "attempt to", "aim to"

**Unclear conditionals:**
- "if possible", "if needed", "if applicable"
- "where appropriate", "as required"
- "depending on", "based on" (without specifics)

**Examples:**

❌ Ambiguous: "The system might send a notification"
- When? Under what conditions? Is this optional?

✅ Clear: "The system must send an email notification when an order is placed"

❌ Ambiguous: "Users should be able to edit their profile"
- Is this required or optional? What priority?

✅ Clear: "Users must be able to edit their name, email, and phone number in their profile [CRITICAL]"

❌ Ambiguous: "Display results if available"
- When are results available? What to show when not available?

✅ Clear: "Display search results if the query returns data; otherwise, display 'No results found' message"

### Clarifying Questions
- "Is this mandatory, optional, or conditional?"
- "Under what specific conditions does this apply?"
- "What is the priority level?"

---

## Undefined Terms

### Problem
Domain-specific jargon, acronyms, or technical terms without definition.

### Patterns to Flag

**Undefined domain terms:**
- Industry jargon without definition
- Acronyms not spelled out
- Technical terms assumed to be understood
- Company-specific terminology
- Ambiguous technical terms (e.g., "database" - SQL? NoSQL? Which one?)

**Examples:**

❌ Ambiguous: "Integrate with the CRM"
- Which CRM? Salesforce? HubSpot? Custom system?

✅ Clear: "Integrate with Salesforce CRM using the REST API v52.0"

❌ Ambiguous: "Store data in the database"
- Which database? PostgreSQL? MongoDB? MySQL? Redis?

✅ Clear: "Store user data in PostgreSQL 14 using the 'users' table"

❌ Ambiguous: "Implement SSO"
- Which SSO protocol? SAML? OAuth 2.0? OpenID Connect?

✅ Clear: "Implement Single Sign-On using OAuth 2.0 with Google as the identity provider"

### Clarifying Questions
- "What does [term] mean specifically?"
- "Which [system/tool/technology] exactly?"
- "Can you provide a definition or example?"

---

## Incomplete Specifications

### Problem
Missing critical details about behavior, inputs, outputs, or error handling.

### Patterns to Flag

**Incomplete requirement indicators:**
- No mention of error conditions
- No validation rules specified
- No data format specified
- No success criteria
- No constraints or limits
- "..." or implied continuation
- No specification of what happens when...

**Examples:**

❌ Ambiguous: "Users can upload files"
- What file types? Size limits? What happens if upload fails? Where are files stored?

✅ Clear: "Users can upload PDF, DOCX, and TXT files up to 10MB. Files are stored in AWS S3. Display error 'File too large' if over 10MB, 'Invalid file type' if not PDF/DOCX/TXT, 'Upload failed' if network error occurs."

❌ Ambiguous: "Calculate the total price"
- Include tax? Shipping? Discounts? Currency? Rounding?

✅ Clear: "Calculate total price as: (item_price × quantity) + shipping - discount + tax. Round to 2 decimal places. Display in USD format ($XX.XX)."

❌ Ambiguous: "Search for products"
- Search which fields? Case-sensitive? Partial match? Sort order?

✅ Clear: "Search product name and description fields (case-insensitive, partial match). Return results sorted by relevance score, then by price (low to high). Limit to 50 results per page."

### Clarifying Questions
- "What happens if [error condition]?"
- "What are the validation rules?"
- "What is the expected format?"
- "What are the constraints or limits?"
- "How should this behave in edge cases?"

---

## Subjective Language

### Problem
Qualitative descriptions that vary by interpretation.

### Patterns to Flag

**Subjective quality terms:**
- "user-friendly", "intuitive", "easy to use"
- "fast", "slow", "quick", "responsive"
- "simple", "complex", "sophisticated"
- "clean", "elegant", "professional", "modern"
- "good", "bad", "better", "best", "optimal"
- "efficient", "robust", "scalable", "reliable"

**Examples:**

❌ Ambiguous: "The interface should be user-friendly"
- What makes it user-friendly? Specific usability criteria?

✅ Clear: "The interface should: (1) Complete common tasks in max 3 clicks, (2) Display clear error messages, (3) Support keyboard navigation, (4) Pass WCAG 2.1 AA accessibility standards"

❌ Ambiguous: "The system should be fast"
- How fast? What operations? What metric?

✅ Clear: "Page load time must be under 2 seconds, API response time under 500ms for 95th percentile"

❌ Ambiguous: "Use a modern design"
- What does "modern" mean? Specific design patterns?

✅ Clear: "Use Material Design 3 components with the specified color palette (primary: #1976D2, secondary: #424242)"

### Clarifying Questions
- "What specific, measurable criteria define [subjective term]?"
- "How would you verify this quality?"
- "What are the concrete success metrics?"

---

## Implicit Assumptions

### Problem
Unstated assumptions about system behavior, user knowledge, or context.

### Patterns to Flag

**Assumption indicators:**
- "Obviously", "clearly", "of course", "naturally"
- "As usual", "like normal", "standard"
- "Everyone knows", "it's common knowledge"
- Implied workflows without stating them
- Assumed infrastructure or dependencies

**Examples:**

❌ Ambiguous: "Send a password reset email"
- Assumes email is configured. What if user has no email? Expired link handling? Link format?

✅ Clear: "Send password reset email to user's registered email address. Email contains a unique token valid for 24 hours. Link format: https://app.com/reset?token=XXX. If user has no email, display error 'No email on file'."

❌ Ambiguous: "Archive old records"
- How old is "old"? Where to archive? Delete or move? Can archived records be retrieved?

✅ Clear: "Move records older than 90 days to archive database. Archived records remain queryable in 'Archive' section. Deletion requires admin approval and happens after 7 years."

❌ Ambiguous: "Process credit card payments"
- Assumes payment gateway. Which one? Test mode? PCI compliance? Retry logic?

✅ Clear: "Process payments using Stripe API v2023-10-16. Support Visa, MasterCard, Amex. Retry failed payments 3 times with exponential backoff. Store only tokenized card data (no raw card numbers). Implement 3D Secure for transactions over $100."

### Clarifying Questions
- "What assumptions are being made?"
- "What prerequisites must be in place?"
- "What happens in the absence of [assumed condition]?"

---

## Pronouns and References

### Problem
Unclear pronoun references or ambiguous "it/this/that" usage.

### Patterns to Flag

**Ambiguous pronouns:**
- "it", "this", "that", "these", "those" (unclear antecedent)
- "they", "them", "their" (unclear reference)
- "the system", "the user", "the data" (which one?)
- "same", "similar", "like the other one"

**Examples:**

❌ Ambiguous: "When the user submits the form, validate it"
- Validate the form or the user?

✅ Clear: "When the user submits the form, validate all form fields before processing"

❌ Ambiguous: "The order contains items. Display them on the page"
- Display the orders or the items?

✅ Clear: "The order contains items. Display all items in the order on the order details page"

❌ Ambiguous: "Similar to the existing feature"
- Which feature? How similar? What differs?

✅ Clear: "Implement user notifications similar to the 'Order Status Updates' feature, but for wishlist items instead of orders"

### Clarifying Questions
- "What does [pronoun] refer to specifically?"
- "Which [noun] exactly?"
- "Can you name the specific entity?"

---

## Missing Edge Cases

### Problem
No specification for boundary conditions, error states, or exceptional scenarios.

### Patterns to Flag

**Missing edge case indicators:**
- Only happy path described
- No error handling specified
- No null/empty handling
- No boundary value handling
- No concurrent access handling
- No mention of "what if..."

**Examples:**

❌ Ambiguous: "Display user's age based on birthdate"
- What if birthdate is in the future? Missing? Invalid format? User is 0 years old?

✅ Clear: "Calculate age from birthdate. If birthdate is in future, show error 'Invalid birthdate'. If birthdate is missing, show 'N/A'. If age < 13, show 'Minor account' badge. If age > 120, request verification."

❌ Ambiguous: "Divide total by count"
- What if count is 0? What if total is null?

✅ Clear: "Divide total by count. If count is 0 or null, display 'N/A'. If total is null, treat as 0."

❌ Ambiguous: "Allow users to delete their account"
- What about their data? Orders? Subscriptions? Can they undo? Cascade deletes?

✅ Clear: "Allow users to delete their account. Before deletion: (1) Cancel active subscriptions, (2) Archive order history for 7 years (regulatory), (3) Anonymize user data in analytics, (4) Send confirmation email, (5) Allow 30-day grace period to undo deletion."

### Clarifying Questions
- "What happens when [boundary condition]?"
- "How should the system handle [error scenario]?"
- "What if [edge case]?"
- "Are there any exceptional cases?"

---

## Detection Scoring

When analyzing requirements, assign ambiguity severity:

**Critical (Must Fix):**
- Core functionality unclear
- No acceptance criteria
- Multiple valid interpretations with conflicting outcomes

**High (Should Fix):**
- Missing important details
- Subjective quality without metrics
- Undefined technical terms

**Medium (Recommend Fixing):**
- Vague quantifiers for non-critical features
- Minor edge cases not covered
- Weak verbs without priority

**Low (Consider Fixing):**
- Optional features with unclear scope
- Stylistic improvements
- Nice-to-have clarifications
