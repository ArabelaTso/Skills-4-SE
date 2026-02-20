# Code Quality Toolkit

Comprehensive toolkit for code quality analysis, refactoring, and technical debt management.

## 📦 Included Skills (13)

### Code Analysis
- **code-smell-detector** - Detect code smells and anti-patterns
- **technical-debt-analyzer** - Identify and quantify technical debt
- **dead-code-eliminator** - Find and remove unused code
- **legacy-code-summarizer** - Understand and document legacy code

### Code Improvement
- **code-refactoring-assistant** - Suggest and apply refactorings
- **code-optimizer** - Optimize code for performance
- **design-pattern-suggestor** - Recommend appropriate design patterns
- **api-design-assistant** - Improve API design

### Code Review
- **code-review-assistant** - Automated code review with best practices
- **behavior-preservation-checker** - Verify refactorings preserve behavior
- **semantic-equivalence-verifier** - Check semantic equivalence of code changes

### Documentation
- **code-comment-generator** - Generate meaningful code comments
- **code-summarizer** - Create high-level code summaries

## 🎯 Use Cases

### 1. Code Quality Audit
```bash
# Detect code smells
/code-smell-detector --path src/

# Analyze technical debt
/technical-debt-analyzer --project .

# Find dead code
/dead-code-eliminator --source src/
```

### 2. Refactoring Workflow
```bash
# Get refactoring suggestions
/code-refactoring-assistant --file src/UserService.java

# Verify behavior is preserved
/behavior-preservation-checker --original old.py --refactored new.py

# Check semantic equivalence
/semantic-equivalence-verifier --v1 before.py --v2 after.py
```

### 3. Code Review
```bash
# Automated code review
/code-review-assistant --pr 123

# Check API design
/api-design-assistant --api-spec openapi.yaml
```

### 4. Legacy Code Modernization
```bash
# Understand legacy code
/legacy-code-summarizer --path legacy/

# Suggest design patterns
/design-pattern-suggestor --code legacy/module.py

# Optimize performance
/code-optimizer --target legacy/slow_function.py
```

## 🚀 Installation

```bash
cd skill-packs/code-quality-toolkit
./install.sh
```

## 📊 Quality Metrics

This toolkit helps improve:
- **Maintainability** - Reduce code smells and technical debt
- **Readability** - Better comments and structure
- **Performance** - Optimize critical paths
- **Design** - Apply appropriate patterns
- **Testability** - Refactor for better testing

## 🔗 Related Skill Packs

- **bug-fixing-suite** - Fix bugs found during quality checks
- **test-automation-suite** - Add tests for refactored code
- **requirements-engineering-suite** - Ensure quality meets requirements

## 📖 Examples

### Example 1: Refactor a God Class

```bash
# Detect the problem
/code-smell-detector --file GodClass.java
# Output: "God Class detected: 2000 lines, 50 methods"

# Get refactoring suggestions
/code-refactoring-assistant --file GodClass.java
# Output: "Suggest Extract Class pattern..."

# Verify after refactoring
/behavior-preservation-checker --original GodClass.java --refactored UserService.java
```

### Example 2: Technical Debt Report

```bash
# Analyze entire project
/technical-debt-analyzer --project . --output debt-report.md

# Focus on high-priority issues
/code-smell-detector --severity high --path src/

# Generate improvement plan
/code-refactoring-assistant --batch --priority high
```

## 🛠️ Requirements

- Claude Code CLI
- Git (for change tracking)
- Language-specific tools (optional, for deeper analysis)

## 📝 License

MIT
