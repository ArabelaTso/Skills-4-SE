---
name: agent-browser
description: CLI-based browser automation with persistent page state using ref-based element interaction. Use for web testing, form filling, screenshots, scraping, and browser workflows via command-line interface.
---

# Agent Browser — CLI Browser Automation

Command-line browser automation tool with persistent page state and ref-based element interaction. Ideal for quick browser tasks without writing scripts.

## When to Use This Skill

- Quick browser interactions via CLI commands
- Form filling and submission
- Taking screenshots and PDFs
- Web scraping and data extraction
- Testing web applications interactively

## Core Workflow

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

1. Navigate to a URL
2. Take a snapshot to discover elements (returns refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Commands

### Navigation
```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (Page Analysis)
```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interactions (Use @refs from Snapshot)
```bash
agent-browser click @e1           # Click
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser hover @e1           # Hover
agent-browser select @e1 "value"  # Select dropdown
agent-browser upload @e1 file.pdf # Upload files
agent-browser scroll down 500     # Scroll page
```

### Get Information
```bash
agent-browser get text @e1        # Get element text
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
```

### Screenshots and PDF
```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser screenshot --full   # Full page
agent-browser pdf output.pdf      # Save as PDF
```

### Wait
```bash
agent-browser wait @e1                  # Wait for element
agent-browser wait 2000                 # Wait milliseconds
agent-browser wait --text "Success"     # Wait for text
agent-browser wait --url "**/dashboard" # Wait for URL pattern
agent-browser wait --load networkidle   # Wait for network idle
```

## Example: Form Submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Tips

- Always use `snapshot -i` (interactive only) for cleaner output
- Re-snapshot after any navigation or major DOM change
- Use `--json` flag for machine-readable output
- Sessions persist page state — reconnect to continue where you left off

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) agent-browser skill. Based on [agent-browser](https://github.com/vercel-labs/agent-browser) by Vercel.
