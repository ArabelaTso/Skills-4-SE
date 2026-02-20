# Semantic SZZ Analyzer Skill

A Claude Code skill for identifying bug-introducing commits using semantic analysis that extends the traditional SZZ algorithm.

## Overview

This skill helps identify which commits introduced bugs by analyzing bug-fix commits and tracing back through git history using semantic analysis. It distinguishes actual semantic changes from refactorings or code movements by analyzing control-flow and data-flow similarity across versions.

## Key Features

- **Semantic Change Detection**: Distinguishes semantic changes from refactorings and code movements
- **Control-Flow Analysis**: Uses CFG (Control-Flow Graph) similarity to match code across versions
- **Data-Flow Analysis**: Tracks variable usage patterns to identify semantic changes
- **False Positive Reduction**: Filters out formatting, whitespace, and refactoring changes
- **Multi-Language Support**: Supports Python, Java, C/C++, JavaScript, and more
- **Detailed Explanations**: Provides reasoning for why commits are identified as bug-introducing

## Installation

1. Install the skill in Claude Code:
   ```bash
   # Copy the .skill file to your Claude skills directory
   cp semantic-szz-analyzer.skill ~/.claude/skills/
   ```

2. Install Python dependencies:
   ```bash
   pip install gitpython
   # Optional: for additional language support
   pip install javalang tree-sitter esprima
   ```

## Usage

### Basic Analysis

Analyze a single bug-fix commit:

```bash
python scripts/semantic_szz.py --repo /path/to/repo --fix-commit abc123
```

### Batch Analysis

Analyze multiple bug-fix commits from a file:

```bash
python scripts/batch_analyze.py --repo /path/to/repo --fixes-file bug_fixes.txt --output results.json
```

### With Claude Code

Simply ask Claude to analyze bug-introducing commits:

```
"Analyze the bug-fix commit abc123 and identify which commit introduced the bug"

"Find all bug-introducing commits for the fixes in bug_fixes.txt"

"Explain why commit def456 is considered bug-introducing"
```

## Output Format

Results are provided in JSON format with detailed information:

```json
{
  "fix_commit": "abc123",
  "bug_introducing_commits": [
    {
      "commit": "def456",
      "confidence": 0.85,
      "semantic_change_type": "logic_modification",
      "explanation": "Modified conditional logic in function foo()",
      "similarity_scores": {
        "cfg": 0.72,
        "dfg": 0.68,
        "ast": 0.81
      }
    }
  ]
}
```

## Configuration

Adjust similarity thresholds in `scripts/semantic_analyzer.py`:

```python
CFG_THRESHOLD = 0.7  # Control-flow similarity
DFG_THRESHOLD = 0.6  # Data-flow similarity
AST_THRESHOLD = 0.8  # AST structural similarity
```

## Documentation

- **SKILL.md**: Complete skill documentation and workflow
- **references/szz_algorithm.md**: Traditional SZZ algorithm explanation
- **references/semantic_analysis.md**: Semantic analysis techniques
- **references/language_support.md**: Language-specific support details

## Requirements

- Python 3.7+
- Git repository
- Optional: Language-specific parsers (javalang, tree-sitter, etc.)

## License

This skill is provided as-is for research and development purposes.

## References

- Śliwerski, J., Zimmermann, T., & Zeller, A. (2005). "When do changes induce fixes?"
- Kim, S., et al. (2006). "Automatic identification of bug-introducing changes"
- Da Costa, D. A., et al. (2017). "A framework for evaluating the results of the SZZ approach"
