---
name: markdown-document-structurer
description: "Reorganizes markdown documents into well-structured, consistent format while preserving content and improving readability. Use when Claude needs to: (1) Fix heading hierarchy issues (skipped levels, multiple h1s), (2) Generate or update table of contents, (3) Standardize formatting (lists, code blocks, emphasis, links), (4) Improve grammar and spelling, (5) Add missing standard sections (installation, usage, etc.), (6) Remove redundant or duplicate content, (7) Restructure technical docs, READMEs, or long-form content for better organization and flow."
---

# Markdown Document Structurer

Reorganize and improve markdown documents while preserving content integrity.

## Workflow

### 1. Analyze Current Structure

**Automated analysis:**
```bash
python scripts/analyze_structure.py <markdown_file>
```

**Manual analysis:**
- Read the document to understand content and purpose
- Identify document type (README, technical doc, tutorial, article)
- Note structural issues and inconsistencies

### 2. Identify Issues

Check for:

**Heading Hierarchy:**
- Multiple h1 headings
- Skipped heading levels (h1 → h3)
- Inconsistent heading progression

**Table of Contents:**
- Missing TOC when document has 3+ main sections
- Outdated TOC that doesn't match current structure
- Incorrect anchor links

**Formatting Consistency:**
- Mixed list markers (-, *, +)
- Code blocks without language specification
- Inconsistent emphasis styles (** vs __, * vs _)
- Inconsistent link formats

**Content Issues:**
- Missing standard sections for document type
- Duplicate or redundant sections
- Poor section organization
- Grammar and spelling errors

### 3. Plan Restructuring

Determine:
- Target document structure based on type (see [document-patterns.md](references/document-patterns.md))
- Which sections to add, merge, or reorganize
- Formatting standards to apply (see [markdown-best-practices.md](references/markdown-best-practices.md))
- Content improvements needed

### 4. Apply Restructuring

Follow this order:

**Step 1: Fix Heading Hierarchy**
- Ensure single h1 for document title
- Fix skipped levels
- Maintain logical progression

**Step 2: Reorganize Sections**
- Reorder sections for logical flow
- Merge duplicate sections
- Add missing standard sections
- Remove redundant content

**Step 3: Generate/Update TOC**
- Create TOC if document has 3+ sections
- Update existing TOC to match structure
- Ensure anchor links are correct

**Step 4: Standardize Formatting**
- Use `-` for unordered lists
- Specify language for code blocks
- Use `**bold**` and `*italic*` consistently
- Standardize link formats
- Fix spacing and blank lines

**Step 5: Improve Content**
- Fix grammar and spelling
- Improve clarity where needed
- Preserve all original information
- Maintain author's voice and style

### 5. Verify Results

Check:
- All content preserved
- Heading hierarchy correct
- TOC matches structure
- Formatting consistent
- No broken links
- Grammar improved
- Document flows logically

## Document Type Guidelines

### README Files

**Standard structure:**
1. Title and brief description
2. Table of contents (if 3+ sections)
3. Features/highlights
4. Installation
5. Usage examples
6. Configuration
7. Contributing
8. License

**Required sections:**
- Installation instructions
- Basic usage example
- License information

See [document-patterns.md](references/document-patterns.md) for detailed README patterns.

### Technical Documentation

**Standard structure:**
1. Title
2. Overview
3. Table of contents
4. Prerequisites
5. Installation/setup
6. Basic usage
7. Advanced usage
8. API reference (if applicable)
9. Examples
10. Troubleshooting
11. Additional resources

**Required sections:**
- Prerequisites
- Installation/setup
- Basic usage examples

### Long-Form Content (Articles, Tutorials)

**Standard structure:**
1. Title
2. Introduction/hook
3. Table of contents
4. Main content sections
5. Conclusion
6. References/resources

**For tutorials specifically:**
- Prerequisites section
- Step-by-step structure
- Verification/testing steps
- Next steps

## Formatting Standards

### Headings
- Single h1 (`#`) for title
- Sequential levels (no skipping)
- One blank line before and after

### Lists
- Use `-` for unordered lists
- Proper indentation (2 or 4 spaces)
- One blank line before and after

### Code Blocks
- Always specify language: ```python
- One blank line before and after

### Emphasis
- Use `**bold**` for strong emphasis
- Use `*italic*` for emphasis
- Avoid mixing styles

### Links
- Use inline format: `[text](url)`
- Use reference format for repeated links

### Spacing
- One blank line between sections
- No trailing whitespace
- Consistent blank line usage

See [markdown-best-practices.md](references/markdown-best-practices.md) for complete formatting guidelines.

## Content Preservation Rules

**Always preserve:**
- All factual information
- Code examples
- Technical details
- Links and references
- Author's key points

**Safe to modify:**
- Grammar and spelling
- Sentence structure for clarity
- Section organization
- Formatting consistency

**Never:**
- Remove content without user approval
- Change technical accuracy
- Alter code examples (except formatting)
- Modify links or URLs

## Handling Redundancy

### Identifying Duplicates
- Same section headings
- Repeated installation instructions
- Duplicate code examples
- Overlapping explanations

### Consolidation Strategy
1. Identify all duplicate content
2. Keep the most complete version
3. Merge complementary information
4. Add cross-references if needed
5. Remove redundant sections

### Example
**Before:**
```markdown
## Installation
npm install package

## Installing the Package
Run npm install package

## Setup
Install with npm install package
```

**After:**
```markdown
## Installation

Install the package using npm:

```bash
npm install package
```
```

## Adding Missing Sections

### Detection
Check document type and identify missing standard sections:
- README: Installation, Usage, License
- Technical docs: Prerequisites, Examples, Troubleshooting
- Tutorials: Prerequisites, Verification steps, Next steps

### Adding Sections
1. Determine appropriate location in document flow
2. Add section with appropriate heading level
3. Include placeholder content or note that section needs completion
4. Inform user about added sections

### Example
```markdown
## Installation

*Installation instructions to be added*

## Usage

*Usage examples to be added*
```

## Table of Contents Generation

### When to Generate
- Document has 3+ main sections (h2)
- Technical documentation
- Long-form content (>500 lines)

### Placement
- After title and description
- Before main content
- Use h2: `## Table of Contents`

### Format
```markdown
## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
  - [Subsection 2.1](#subsection-21)
  - [Subsection 2.2](#subsection-22)
- [Section 3](#section-3)
```

### Anchor Generation
- Lowercase all text
- Replace spaces with hyphens
- Remove special characters except hyphens
- Example: "API Reference Guide" → `#api-reference-guide`

## Grammar and Spelling

### Approach
- Fix obvious errors
- Improve clarity without changing meaning
- Maintain author's voice and style
- Preserve technical terminology

### Common Fixes
- Subject-verb agreement
- Tense consistency
- Article usage (a, an, the)
- Common spelling errors
- Punctuation

### Caution
- Don't change technical terms
- Preserve code-related text exactly
- Keep domain-specific language
- Maintain intentional informal tone

## Output Format

After restructuring, provide:

1. **Summary of changes:**
   - Structural improvements
   - Sections added/removed/merged
   - Formatting fixes
   - Content improvements

2. **Restructured document:**
   - Complete markdown with all changes applied

3. **Notes:**
   - Any sections needing user input
   - Recommendations for further improvement
   - Warnings about significant changes

## Best Practices

### Analysis
- Understand document purpose before restructuring
- Identify document type to apply appropriate structure
- Use automated analysis script for quick assessment
- Note all issues before making changes

### Restructuring
- Make one type of change at a time
- Preserve all content unless clearly redundant
- Maintain logical flow and readability
- Follow established patterns for document type

### Quality
- Verify all links work
- Ensure TOC matches structure
- Check heading hierarchy
- Confirm formatting consistency
- Test code blocks if possible

### Communication
- Explain significant structural changes
- Highlight added or removed sections
- Note any content needing user input
- Provide rationale for major reorganization
