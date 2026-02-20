# Bug Fixing Suite

A comprehensive toolkit for bug detection, localization, analysis, and automated repair.

## 📦 Included Skills (12)

### Bug Detection
- **static-bug-detector** - Static analysis to find potential bugs
- **semantic-bug-detector** - Detect semantic-level bugs using program analysis
- **test-guided-bug-detector** - Use test failures to guide bug detection

### Bug Localization
- **bug-localization** - Pinpoint the exact location of bugs in code
- **regression-root-cause-analyzer** - Analyze root causes of regression bugs
- **vulnerability-root-cause-analyzer** - Find root causes of security vulnerabilities

### Bug Analysis
- **szz-bug-identifier** - Identify bug-introducing commits using SZZ algorithm
- **semantic-szz-analyzer** - Enhanced SZZ with semantic analysis
- **counterexample-debugger** - Debug using counterexamples from formal verification
- **runtime-error-explainer** - Explain runtime errors with context

### Bug Repair
- **bug-to-patch-generator** - Automatically generate patches for bugs
- **bug-reproduction-test-generator** - Generate tests that reproduce bugs

## 🎯 Use Cases

### 1. Complete Bug Fix Workflow
```bash
# 1. Detect bugs
/static-bug-detector --path src/

# 2. Localize the bug
/bug-localization --error-log error.txt --source src/

# 3. Generate a patch
/bug-to-patch-generator --bug-report bug.md --source src/module.py

# 4. Generate reproduction test
/bug-reproduction-test-generator --bug-report bug.md
```

### 2. Regression Analysis
```bash
# Find which commit introduced the bug
/szz-bug-identifier --bug-fix-commit abc123

# Analyze root cause
/regression-root-cause-analyzer --old-version v1.0 --new-version v1.1
```

### 3. Security Vulnerability Fix
```bash
# Analyze vulnerability root cause
/vulnerability-root-cause-analyzer --cve CVE-2024-1234

# Generate security patch
/bug-to-patch-generator --vulnerability-report vuln.json
```

## 🚀 Installation

```bash
cd skill-packs/bug-fixing-suite
./install.sh
```

Or install to a custom location:
```bash
./install.sh --target ~/.claude/skills
```

## 📊 Skill Dependencies

```
Bug Detection → Bug Localization → Bug Repair
     ↓              ↓                  ↓
Test Generation ← Root Cause Analysis
```

## 🔗 Related Skill Packs

- **test-automation-suite** - Generate comprehensive tests
- **code-quality-toolkit** - Prevent bugs through quality checks
- **security-scanner-suite** - Detect security vulnerabilities

## 📖 Examples

### Example 1: Fix a Null Pointer Bug

```bash
# Input: error log showing NullPointerException
/bug-localization --error-log npe.log --source src/

# Output: Identifies line 42 in UserService.java
# Then generate patch:
/bug-to-patch-generator --bug-location src/UserService.java:42
```

### Example 2: Regression Bug Hunt

```bash
# Find the commit that introduced the bug
/szz-bug-identifier --bug-fix-commit d4f5e6

# Analyze what changed
/semantic-szz-analyzer --bug-introducing-commit a1b2c3

# Generate fix
/bug-to-patch-generator --regression-analysis regression.json
```

## 🛠️ Requirements

- Claude Code CLI
- Git (for SZZ-based skills)
- Python 3.8+ (for some analysis tools)

## 📝 License

MIT
