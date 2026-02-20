# Code Understanding and Manipulation Suite

Comprehensive toolkit for understanding, analyzing, searching, translating, and manipulating code across languages and frameworks.

## 📋 Overview

This suite provides a complete set of tools for working with codebases at all levels - from understanding legacy code to performing complex migrations, from searching for patterns to optimizing performance.

## 📦 Included Skills (19)

### Code Understanding & Analysis
- **code-summarizer** - Generate concise summaries of code at multiple scales
- **legacy-code-summarizer** - Analyze and document legacy codebases
- **pseudocode-extractor** - Extract language-agnostic pseudocode from source
- **component-boundary-identifier** - Identify module/component boundaries
- **dependency-resolver** - Analyze and resolve software dependencies

### Code Search & Pattern Recognition
- **code-search-assistant** - Search for related code using similarity analysis
- **code-pattern-extractor** - Identify reusable patterns and duplicated code

### Code Translation
- **code-translation** - General-purpose code translation across languages
- **pseudocode-to-java-code** - Convert pseudocode to Java
- **pseudocode-to-python-code** - Convert pseudocode to Python
- **module-level-code-translator** - Translate entire modules between languages

### Code Manipulation & Optimization
- **code-refactoring-assistant** - Suggest and apply refactoring patterns
- **code-optimizer** - Optimize code for performance and efficiency
- **dead-code-eliminator** - Identify and remove unused code

### Framework & System Migration
- **spring-mvc-to-boot-migrator** - Migrate Spring MVC to Spring Boot
- **build-ci-migration-assistant** - Migrate build and CI systems
- **test-guided-migration-assistant** - Use tests to guide safe migrations

### Migration Verification
- **multi-version-behavior-comparator** - Compare behavior across versions
- **behavior-preservation-checker** - Verify behavior is preserved after changes

## 🎯 Use Cases

### 1. Understanding Legacy Code
```bash
# Summarize a legacy codebase
/legacy-code-summarizer --path legacy-app/

# Extract high-level pseudocode
/pseudocode-extractor --source complex_algorithm.cpp

# Identify component boundaries
/component-boundary-identifier --path src/
```

### 2. Code Search & Pattern Analysis
```bash
# Search for similar code
/code-search-assistant --snippet "authentication logic" --repo .

# Extract reusable patterns
/code-pattern-extractor --path src/ --min-occurrences 3

# Analyze dependencies
/dependency-resolver --project-root .
```

### 3. Code Translation & Migration
```bash
# Translate Python to Java
/module-level-code-translator --source auth.py --target-lang java

# Convert pseudocode to production code
/pseudocode-to-python-code --pseudocode algorithm.txt

# Migrate Spring MVC to Spring Boot
/spring-mvc-to-boot-migrator --project legacy-app/
```

### 4. Code Optimization & Refactoring
```bash
# Optimize performance
/code-optimizer --source slow_function.py --focus performance

# Refactor code
/code-refactoring-assistant --path src/services/

# Remove dead code
/dead-code-eliminator --path src/ --safe-mode
```

### 5. Verified Migration
```bash
# Migrate with test guidance
/test-guided-migration-assistant --source old/ --target new/ --tests tests/

# Verify behavior preservation
/behavior-preservation-checker --original v1/ --modified v2/

# Compare multi-version behavior
/multi-version-behavior-comparator --versions v1,v2,v3 --tests tests/
```

## 🚀 Installation

```bash
cd skill-packs/code-understanding-and-manipulation-suite
./install.sh

# Or install to custom location
./install.sh --path ~/.claude/skills
```

## 📊 Complete Workflow

```
┌─────────────────────┐
│   Legacy Codebase   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Understand & Map   │ ← code-summarizer, component-boundary-identifier
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Search & Analyze   │ ← code-search-assistant, code-pattern-extractor
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Refactor & Optimize│ ← code-refactoring-assistant, code-optimizer
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Translate/Migrate  │ ← code-translation, spring-mvc-to-boot-migrator
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Verify & Validate  │ ← behavior-preservation-checker
└─────────────────────┘
```

## 💡 Key Features

### 🔍 Deep Code Understanding
- Multi-scale code summarization (function → file → module → system)
- Legacy code analysis and documentation
- Component boundary detection
- Dependency graph analysis

### 🔎 Intelligent Code Search
- Semantic code search using similarity analysis
- Pattern recognition and extraction
- Duplicate code detection
- Cross-repository search capabilities

### 🔄 Safe Code Transformation
- Test-guided migrations
- Behavior preservation verification
- Multi-version comparison
- Incremental refactoring support

### ⚡ Performance Optimization
- Algorithmic optimization suggestions
- Dead code elimination
- Performance bottleneck identification
- Resource usage optimization

## 📖 Detailed Examples

### Example 1: Understanding a Legacy Codebase

```bash
# Step 1: Get high-level summary
/legacy-code-summarizer --path legacy-app/ --output summary.md

# Step 2: Identify components
/component-boundary-identifier --path legacy-app/src/

# Step 3: Extract patterns
/code-pattern-extractor --path legacy-app/src/ --output patterns.md

# Step 4: Analyze dependencies
/dependency-resolver --project-root legacy-app/
```

### Example 2: Finding and Reusing Code

```bash
# Search for authentication code
/code-search-assistant --query "JWT token validation" --repo .

# Find similar implementations
/code-search-assistant --snippet auth/validate.py --top-k 5

# Extract reusable patterns
/code-pattern-extractor --path src/ --category "authentication"
```

### Example 3: Safe Code Migration

```bash
# Step 1: Analyze current state
/code-summarizer --path old-app/

# Step 2: Migrate with test guidance
/test-guided-migration-assistant \
  --source old-app/ \
  --target new-framework/ \
  --tests tests/

# Step 3: Verify behavior
/behavior-preservation-checker \
  --original old-app/ \
  --migrated new-framework/

# Step 4: Compare versions
/multi-version-behavior-comparator \
  --v1 old-app/ \
  --v2 new-framework/ \
  --tests tests/
```

### Example 4: Code Optimization Pipeline

```bash
# Step 1: Identify dead code
/dead-code-eliminator --path src/ --report dead-code.md

# Step 2: Optimize hot paths
/code-optimizer --path src/core/ --profile performance.json

# Step 3: Refactor for maintainability
/code-refactoring-assistant --path src/ --focus maintainability

# Step 4: Verify no regressions
/behavior-preservation-checker --original backup/ --modified src/
```

### Example 5: Framework Migration (Spring MVC → Spring Boot)

```bash
# Step 1: Analyze current structure
/component-boundary-identifier --path legacy-spring-mvc/

# Step 2: Migrate framework
/spring-mvc-to-boot-migrator --project legacy-spring-mvc/

# Step 3: Migrate build system
/build-ci-migration-assistant --from maven --to gradle

# Step 4: Verify migration
/behavior-preservation-checker \
  --original legacy-spring-mvc/ \
  --migrated spring-boot-app/
```

## 🛠️ Requirements

- Claude Code CLI
- Target language compilers/interpreters (for translation)
- Test frameworks (for verification)
- Build tools (Maven, Gradle, npm, etc.)

## 📝 Best Practices

### Understanding Code
1. **Start with summaries** - Use code-summarizer before diving deep
2. **Map boundaries** - Identify component boundaries early
3. **Document patterns** - Extract and document recurring patterns
4. **Analyze dependencies** - Understand dependency graphs

### Searching Code
1. **Use semantic search** - Leverage code-search-assistant for similarity
2. **Extract patterns** - Find reusable patterns with code-pattern-extractor
3. **Cross-reference** - Search across multiple repositories

### Translating & Migrating
1. **Test first** - Ensure comprehensive test coverage
2. **Migrate incrementally** - Module by module, not all at once
3. **Verify behavior** - Always use behavior-preservation-checker
4. **Compare versions** - Use multi-version-behavior-comparator

### Optimizing & Refactoring
1. **Profile first** - Identify bottlenecks before optimizing
2. **Remove dead code** - Clean up before refactoring
3. **Refactor incrementally** - Small, verified changes
4. **Maintain tests** - Keep tests passing throughout

## 🎯 Supported Operations

### Code Understanding
- Multi-scale summarization (function → system)
- Legacy code analysis
- Pseudocode extraction
- Component boundary detection
- Dependency analysis

### Code Search
- Semantic similarity search
- Pattern recognition
- Duplicate detection
- Cross-repository search

### Code Translation
- Pseudocode → Python/Java
- General language translation
- Module-level translation
- Framework migration

### Code Manipulation
- Refactoring (extract method, inline, etc.)
- Performance optimization
- Dead code elimination
- Code restructuring

### Migration Support
- Spring MVC → Spring Boot
- Build system migration
- CI/CD migration
- Test-guided migration
- Behavior verification

## 🔗 Related Skill Packs

- **formal-verification-toolkit** - For formal verification and proof
- **test-automation-suite** - For comprehensive testing
- **code-quality-toolkit** - For quality analysis and improvement
- **bug-fixing-suite** - For bug detection and repair

## 📚 Additional Resources

- [Code Understanding Best Practices](docs/understanding.md)
- [Migration Guide](docs/migration.md)
- [Optimization Strategies](docs/optimization.md)
- [Pattern Catalog](docs/patterns.md)

## 📝 License

MIT

## 🙋 Support

For issues or questions:
- Open an issue in the main repository
- Check the documentation
- Join our community discussions
