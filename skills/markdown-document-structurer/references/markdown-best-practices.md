# Markdown Best Practices

## Heading Hierarchy

### Rules
- Start with single h1 (`#`) for document title
- Use sequential heading levels (don't skip levels)
- h2 (`##`) for main sections
- h3 (`###`) for subsections
- h4 (`####`) and beyond for deeper nesting

### Common Issues
- Skipping levels: h1 → h3 (missing h2)
- Multiple h1 headings in one document
- Inconsistent heading styles

### Fix Pattern
```
Bad:
# Title
### Subsection (skips h2)

Good:
# Title
## Main Section
### Subsection
```

## Table of Contents

### When to Include
- Documents longer than 3 sections
- Technical documentation
- README files with multiple sections
- Long-form content

### Format
```markdown
## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
  - [Subsection 2.1](#subsection-21)
- [Section 3](#section-3)
```

### Anchor Generation
- Lowercase all text
- Replace spaces with hyphens
- Remove special characters except hyphens
- Example: "API Reference Guide" → `#api-reference-guide`

## List Formatting

### Unordered Lists
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3
```

### Ordered Lists
```markdown
1. First item
2. Second item
   1. Nested item
   2. Another nested item
3. Third item
```

### Consistency Rules
- Use `-` for unordered lists (not `*` or `+`)
- Use proper indentation (2 or 4 spaces)
- Maintain consistent spacing

## Code Blocks

### Inline Code
Use backticks for inline code: `variable_name`

### Fenced Code Blocks
Always specify language for syntax highlighting:

```python
def example():
    return "Hello"
```

### Common Languages
- `python`, `javascript`, `java`, `bash`, `json`, `yaml`, `markdown`

## Emphasis and Strong

### Consistency
- Use `**bold**` for strong emphasis (not `__bold__`)
- Use `*italic*` for emphasis (not `_italic_`)

## Links

### Inline Links
```markdown
[Link text](https://example.com)
```

### Reference Links
```markdown
[Link text][ref]

[ref]: https://example.com
```

### Internal Links
```markdown
[See section](#section-name)
```

## Standard Document Sections

### README Files
1. Title and description
2. Table of contents (if long)
3. Features
4. Installation
5. Usage
6. Configuration
7. Contributing
8. License

### Technical Documentation
1. Title
2. Table of contents
3. Overview/Introduction
4. Prerequisites
5. Main content sections
6. Examples
7. API reference (if applicable)
8. Troubleshooting
9. Additional resources

### Long-Form Content
1. Title
2. Table of contents
3. Introduction
4. Main sections
5. Conclusion
6. References

## Spacing and Blank Lines

### Rules
- One blank line between sections
- One blank line before and after headings
- One blank line before and after code blocks
- One blank line before and after lists
- No trailing whitespace

## Common Redundancy Patterns

### Duplicate Sections
- Multiple "Introduction" sections
- Repeated installation instructions
- Duplicate examples

### Overlapping Content
- Similar information in different sections
- Redundant explanations
- Duplicate code examples

### Consolidation Strategy
- Identify duplicate content
- Keep the most complete version
- Add cross-references if needed
- Remove or merge redundant sections
