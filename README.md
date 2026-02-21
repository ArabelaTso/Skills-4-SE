<h1 align="center"><strong>✨ Skills-4-SE</strong>: Useful Skills for Software Engineering</h1>

[![Welcome Contribution](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/CONTRIBUTING.md)
[![中文](https://img.shields.io/badge/lang-中文-red)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/README-zh.md)
[![English](https://img.shields.io/badge/lang-English-blue)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/README.md)

This repository is **a comprehensive, reusable, task-oriented Skills collection** designed to support **software engineering activities across the entire development lifecycle**, including:

> *Requirement understanding, system design, implementation, testing, verification, deployment, and maintenance*.


**We provide**:
- 🌐 [**Website**](https://ArabelaTso.github.io/Skills-4-SE/) to quick browse skills
- 📦 8 [**Core Skill Packs**](#-skill-packs)
- 🚀 170+ [**Coding Skills**](#list-of-skills)


## 🌐 Skills Manager Web Interface

**[🚀 Visit Skills Manager](https://ArabelaTso.github.io/Skills-4-SE/)**

> You can also deploy the website locally. 👉 [Guideline](https://github.com/ArabelaTso/Skills-4-SE/blob/main/skill-manager/README.md)

<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/skill-manager-image.png" alt="Skills Manager Interface" width="100%">
</p>

Browse, search, and install skills through our interactive web interface. The Skills Manager provides:
- 📦 One-click installation of all 170+ skills
- ✅ Selective installation of specific skills
- 🔍 Search and filter by category
- 📖 Bilingual help documentation (English/中文)
- 🎨 Modern, responsive interface

<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/zh-image.png" alt="Skills Manager Interface" width="100%">
</p>



## 📦 Skill Packs

Organized collections of related skills for common software engineering workflows. Instead of installing skills individually, you can install curated skill packs that bundle related capabilities together.

<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/skill-pack-image.png" alt="Skills Manager Interface" width="100%">
</p>

### 🚀 Available Skill Packs (8 Total)

- **🐛 [Bug Fixing Suite](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/bug-fixing-suite/)** - 12 skills for bug detection, localization, and automated repair
- **✨ [Code Quality Toolkit](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/code-quality-toolkit/)** - 13 skills for code quality, refactoring, and technical debt management
- **🧪 [Test Automation Suite](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/test-automation-suite/)** - 18 skills for comprehensive test generation and optimization
- **📋 [Requirements Engineering Suite](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/requirements-engineering-suite/)** - 12 skills for requirements analysis, formalization, and traceability
- **🔄 [Code Understanding and Manipulation Suite](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/code-understanding-and-manipulation-suite/)** - 19 skills for code understanding, analysis, search, translation, and manipulation
- **🚀 [DevOps Automation Toolkit](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/devops-automation-toolkit/)** - 10 skills for CI/CD pipelines, containerization, and deployment
- **🔍 [Formal Verification Toolkit](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/formal-verification-toolkit/)** - 17 skills for formal verification of software systems
- **🔒 [Security Scanner Suite](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/security-scanner-suite/)** - 13 skills for comprehensive security analysis

### Quick Installation

```bash
# Install a single pack
cd skill-packs/formal-verification-toolkit
./install.sh

# Install multiple packs
cd skill-packs
./install-packs.sh formal-verification-toolkit security-scanner-suite

# Install all packs
cd skill-packs
./install-all-packs.sh
```

👉 [Learn more about Skill Packs](https://github.com/ArabelaTso/Skills-4-SE/blob/main/skill-packs/README.md)


## ✨ Why Skills (not just prompts)?

Modern LLMs are powerful, but **raw prompting is fragile**:
- Hard to reproduce
- Hard to evaluate
- Hard to integrate into real workflows

We treat **Skills as first-class engineering artifacts**, in preparation for the **future metaprogramming**.

A Skill in this repo is more than a prompt:
- It encodes **procedural knowledge**
- It specifies **expected inputs / outputs**
- It documents **failure modes**
- It can be **evaluated, composed, and reused**

> 🤗 Think of this repo as a *standard library of software engineering capabilities* for LLM-powered systems.

## List of Skills 

- [**Skills by Category**](#skills-by-category)
  - ⌨️ [Code Generation](#code-generation)
  - 👩🏽‍💻 [Testing](#testing)
  - ⚖️ [Code Quality & Analysis](#code-quality--analysis)
  - 📕 [Documentation](#documentation)
  - 💡 [Architecture & Design](#architecture--design)
  - 📗 [Requirements & Specifications](#requirements--specifications)
  - 💻 [DevOps & Deployment](#devops--deployment)
  - 🔀 [Version Control & Collaboration](#version-control--collaboration)
  - 📋 [Project Management & Issue Tracking](#project-management--issue-tracking)
  - 💬 [Team Communication](#team-communication)
  - 📊 [Monitoring & Error Tracking](#monitoring--error-tracking)
  - 🗄️ [Database & Backend Services](#database--backend-services)
  - 🛠️ [Development Tools & Builders](#development-tools--builders)
  - 🔗 [Integration & Webhooks](#integration--webhooks)
  - 🔨 [Debugging & Error Handling](#debugging--error-handling)
  - ✅ [Formal Methods & Verification](#formal-methods--verification)
  - 🔧 [Maintenance & Refactoring](#maintenance--refactoring)
  - 🎨 [UI/UX Design](#uiux-design)
  - 👀 [Visualization](#visualization)
- [**Skills by Stages**](#-skills-by-stages)
  - 📕 [Requirement Analysis](#-requirements)
  - 💡[Software Design](#-software-design)
  - ⌨️ [Implementation](#️-implementation)
  - 👩🏽‍💻 [Testing](#-testing)
  - ✅ [Verification](#-verification)
  - 💻 [Deployment](#-deployment)
  - 🔧 [Maintenance](#-maintenance)
- 📖 [Usage](#usage)
- 🫶 [Contributing](#contributing)
- 🎯 [Vision](#-vision)
- 🙏 [Reference](#reference)


## Skills by Category

### Code Generation

**[Function/Class Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/function-class-generator/)**
- Generates functions and classes from specifications
- Supports multiple programming languages
- Includes type hints, documentation, and error handling

**[Module/Component Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-component-generator/)**
- Builds complete modules from interface contracts
- Generates layered architectures (model, repository, service)
- Supports Python and Java with design patterns

**[Template Code Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/template-code-generator/)**
- Creates boilerplate code from templates
- Supports common patterns and frameworks
- Customizable templates for different use cases

**[Specification-Driven Generation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-driven-generation/)**
- Generates code from formal specifications
- Ensures specification compliance
- Validates generated code against requirements

**[Test-Driven Generation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-driven-generation/)**
- Generates implementation from test cases
- Follows TDD principles
- Ensures test coverage

**[Incremental Python Programmer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-python-programmer/)**
- Implements new features in Python repositories from natural language descriptions
- Generates comprehensive unit and integration tests
- Ensures all tests pass and follows existing code patterns

**[Incremental Java Programmer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-java-programmer/)**
- Implements new features in Java repositories from natural language descriptions
- Supports Maven and Gradle build systems
- Generates JUnit tests and ensures all tests pass successfully

**[Pseudocode Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-extractor/)**
- Extracts programming-language-agnostic pseudocode from source code
- Preserves control flow and logical structure
- Filters out implementation details for clarity

**[Module-Level Code Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-level-code-translator/)**
- Translates source code between programming languages at module level
- Preserves behavior and adapts to target language idioms
- Generates verification tests for translated code

**[Pseudocode to Java Code](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-java-code/)**
- Converts pseudocode descriptions into complete, executable Java programs
- Preserves original logic and control flow
- Applies appropriate Java idioms and best practices

**[Pseudocode to Python Code](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-python-code/)**
- Converts pseudocode and algorithm descriptions into executable Python code
- Provides proper structure, documentation, and tests
- Maintains algorithmic logic while following Python conventions

### Testing

**[Unit Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/unit-test-generator/)**
- Generates unit tests for functions and classes
- Supports multiple testing frameworks
- Includes edge cases and assertions

**[Integration Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/integration-test-generator/)**
- Creates integration tests for system components
- Tests component interactions
- Includes setup and teardown logic

**[Java Test Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-test-updater/)**
- Updates Java tests to work with new code versions after refactoring
- Handles signature changes, refactoring, and behavior modifications
- Updates method calls, assertions, mocks, and ensures tests pass

**[Flaky Test Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector/)**
- Identifies non-deterministic tests
- Analyzes test execution patterns
- Suggests fixes for common flaky patterns

**[Test Oracle Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-oracle-generator/)**
- Generates expected outputs for test cases
- Creates assertions and validation logic
- Supports property-based testing

**[Edge Case Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/edge-case-generator/)**
- Identifies and generates edge case tests
- Covers boundary conditions
- Includes corner cases and error scenarios

**[Directed Test Input Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/directed-test-input-generator/)**
- Generates targeted test inputs
- Focuses on specific code paths
- Uses symbolic execution techniques

**[Fuzzing Input Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/fuzzing-input-generator/)**
- Creates randomized test inputs
- Discovers unexpected behaviors
- Supports mutation-based fuzzing

**[Test Suite Prioritizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-suite-prioritizer/)**
- Prioritizes test execution order
- Optimizes for early failure detection
- Considers test dependencies and coverage

**[Coverage Enhancer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/coverage-enhancer/)**
- Identifies uncovered code paths
- Generates tests to improve coverage
- Reports coverage metrics

**[Test Case Documentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-documentation/)**
- Documents test cases and their purposes
- Explains test scenarios and expected outcomes
- Maintains test documentation

**[Python Test Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-test-updater/)**
- Updates Python tests to work with new code versions
- Fixes broken tests due to signature and behavior changes
- Analyzes code diffs and updates assertions accordingly

**[Bug Reproduction Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-reproduction-test-generator/)**
- Automatically generates tests that reproduce reported bugs from issue reports
- Analyzes bug symptoms, stack traces, and triggering conditions
- Creates minimal, focused tests that reliably trigger the bug
- Supports Python, Java, and JavaScript test frameworks

**[Interval-Guided Regression Test Update](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-guided-regression-test-update/)**
- Updates regression tests based on interval analysis

**[Requirement to Test](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/req-to-test/)**
- Converts requirements to test cases
- Ensures requirement coverage
- Traces tests back to requirements

**[Test Case Reducer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-reducer/)**
- Reduces test cases to minimal form using delta debugging

**[Java Regression Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-regression-test-generator/)**
- Automatically generates regression tests for Java codebases
- Analyzes changes between old and new code versions
- Ensures tests cover refactored or modified functionality

**[Python Regression Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-regression-test-generator/)**
- Automatically generates regression tests for Python codebases
- Analyzes changes between code versions and migrates existing tests
- Generates tests for new functionality

**[Mocking Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mocking-test-generator/)**
- Generates unit tests with proper mocking for Python and Java
- Supports unittest.mock/pytest for Python and Mockito/JUnit for Java
- Handles external dependencies and complex interactions

**[Test-Guided Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-bug-detector/)**
- Analyzes failing tests to detect functional bugs in code
- Examines execution behavior, assertions, and stack traces
- Identifies suspicious code regions causing test failures

**[Behavioral Mutation Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavioral-mutation-analyzer/)**
- Systematically analyzes surviving mutants from mutation testing
- Identifies test suite weaknesses and generates improvements
- Categorizes why mutants survived and suggests test enhancements

**[Metamorphic Property Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-property-extractor/)**
- Automatically identifies metamorphic properties from programs
- Enables metamorphic testing without explicit test oracles
- Discovers input-output relationships for test generation

**[Metamorphic Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-test-generator/)**
- Generates test cases using metamorphic testing principles
- Applies transformations based on metamorphic properties
- Expands test suites and detects bugs through input-output relationships

**[Counterexample to Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator/)**
- Converts formal verification counterexamples into executable test cases
- Transforms model checker outputs into unit or integration tests
- Bridges formal verification and testing workflows

**[Mutation Test Suite Optimizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mutation-test-suite-optimizer/)**
- Optimizes test suites using mutation testing analysis
- Selects minimal subset of tests maximizing mutation kill rate
- Reduces execution time and eliminates redundancy

**[Test Deduplicator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-deduplicator/)**
- Analyzes test suites to identify redundant or duplicate tests
- Examines code coverage, semantic similarity, and execution behavior
- Groups equivalent tests and explains deduplication rationale

**[Java API Consistency Validator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-api-consistency-validator/)**
- Validates API consistency between two versions of Java libraries
- Compares signatures, behavior, and exceptions
- Identifies breaking changes and incompatible modifications

**[Python API Consistency Validator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-api-consistency-validator/)**
- Validates API consistency between two versions of Python libraries
- Compares signatures, behavior, and exceptions
- Identifies breaking changes and provides migration guidance

### Code Quality & Analysis

**[Code Review Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-review-assistant/)**
- Performs automated code reviews
- Identifies issues and suggests improvements
- Checks coding standards compliance

**[Code Smell Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-smell-detector/)**
- Detects code smells and anti-patterns
- Suggests refactoring opportunities
- Categorizes smells by severity

**[Design Smell Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-smell-detector/)**
- Identifies architectural and design issues
- Detects violations of design principles
- Suggests design improvements

**[Code Optimizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-optimizer/)**
- Optimizes code for performance
- Identifies bottlenecks
- Suggests algorithmic improvements

**[Dead Code Eliminator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dead-code-eliminator/)**
- Identifies unused code
- Safely removes dead code
- Reports elimination opportunities

**[Technical Debt Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer/)**
- Identifies technical debt
- Quantifies debt impact
- Prioritizes debt reduction

**[Code Pattern Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor/)**
- Analyzes codebases to identify reusable code patterns and duplications
- Generates pattern catalogs with refactoring suggestions
- Creates reusable template code for high-value patterns

**[Code Search Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant/)**
- Searches repositories for code related to given snippets
- Ranks results by call chain, textual, and functional similarity
- Outputs ranked file lists with matching code snippets

**[Component Boundary Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier/)**
- Identifies module/component boundaries
- Detects boundary violations
- Analyzes architectural separation

**[Code Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-summarizer/)**
- Generates concise summaries of source code at multiple scales
- Explains code functionality from functions to entire codebases
- Helps understand complex code structures quickly

**[Static Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-bug-detector/)**
- Analyzes source code statically to detect potential functional bugs
- Identifies null dereferences, incorrect conditions, unreachable code
- Detects logic errors, resource leaks, and inconsistent state updates

**[Static Vulnerability Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-vulnerability-detector/)**
- Statically analyzes code to detect security vulnerabilities
- Identifies buffer overflows, injection risks, insecure deserialization
- Detects improper authentication and unsafe cryptographic usage

**[Vulnerability Pattern Matcher](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-pattern-matcher/)**
- Detects security vulnerabilities by matching known patterns
- Identifies insecure coding idioms and CVE-style patterns
- Explains why patterns are risky and conditions for exploitation

**[Vulnerability Root Cause Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-root-cause-analyzer/)**
- Analyzes vulnerable code to identify underlying root causes
- Identifies violated assumptions, incorrect invariants, missing validation
- Detects unsafe component interactions

**[Exploitability Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/exploitability-analyzer/)**
- Assesses realistic exploitability of detected vulnerabilities
- Examines control flow, input sources, and sanitization logic
- Determines if vulnerabilities are practically exploitable

**[Security Patch Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-patch-advisor/)**
- Proposes secure remediation strategies for security vulnerabilities
- Addresses buffer overflows, injection risks, insecure deserialization
- Provides fixes for improper authentication and unsafe cryptographic usage

**[CVE Reachability Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-reachability-analyzer/)**
- Analyzes whether CVE vulnerabilities in dependencies are reachable from application code
- Performs static and dynamic reachability analysis
- Prioritizes CVE remediation based on actual exploitability

**[CVE Watchlist Action Recommendation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-watchlist-action-recommendation-generator/)**
- Generates actionable recommendations for CVEs in dependency watchlists
- Prioritizes CVEs based on severity, exploitability, and impact
- Suggests patching, mitigation, or monitoring strategies

**[Time-Aware Dependency CVE Scanner](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/time-aware-dependency-cve-scanner/)**
- Scans dependencies for CVEs with temporal context awareness
- Tracks CVE disclosure timelines and patch availability
- Provides time-sensitive vulnerability management recommendations

**[Semantic Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-bug-detector/)**
- Detects semantic-level bugs by analyzing code behavior vs. intent
- Infers intended purpose from names, comments, and documentation
- Identifies mismatches between implementation and expected behavior

**[Behavior Preservation Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavior-preservation-checker/)**
- Validates that migrated or refactored codebase preserves original behavior
- Compares runtime behavior, test results, and execution traces
- Identifies behavioral divergences between code versions

**[Semantic Equivalence Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-equivalence-verifier/)**
- Analyzes semantic equivalence between two code artifacts
- Compares control flow, data flow, and observable behavior
- Provides rigorous equivalence analysis for functions, classes, or modules

**[Multi-Version Behavior Comparator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/multi-version-behavior-comparator/)**
- Compares behavior across multiple versions of programs
- Identifies functional changes, regressions, and behavioral divergences
- Guides safe upgrades and validation processes

**[Regression Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-consistency-checker/)**
- Checks whether new version preserves behavior observed by tests on old version
- Validates behavioral consistency across versions
- Identifies unexpected behavioral changes

**[Interval Difference Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-difference-analyzer/)**
- Analyzes differences in program intervals (variable value ranges) between versions
- Detects behavioral changes and identifies potential bugs
- Guides testing efforts based on interval analysis

**[Interval Profiling Performance Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-profiling-performance-analyzer/)**
- Profiles programs to identify performance bottlenecks
- Generates optimization recommendations with visualizations
- Uses interval analysis for performance insights

**[Modular Code Enforcement](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/modular-code-enforcement/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Enforces strict modular architecture with SRP and 200 LOC limits
- Bans catch-all files (utils.ts, helpers.ts) in favor of focused modules
- Detects and splits files with multiple responsibilities

**[Dead Code Removal](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dead-code-removal/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Systematic dead code removal with LSP-verified safety
- Parallel batch processing with conflict-free execution
- Atomic commits per batch with automatic rollback on failure

### Documentation

**[API Documentation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-documentation-generator/)**
- Generates API documentation
- Creates reference documentation
- Includes usage examples

**[Code Comment Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-comment-generator/)**
- Generates inline code comments
- Explains complex logic
- Follows documentation standards

**[Markdown Document Structurer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer/)**
- Reorganizes markdown documents into well-structured format
- Fixes heading hierarchy and generates table of contents
- Standardizes formatting and improves readability

**[README Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/readme-generator/)**
- Generates comprehensive, user-friendly README.md files
- Includes project introduction, prerequisites, and setup instructions
- Provides executable usage examples and repository structure overview

**[Change Log Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/change-log-generator/)**
- Creates change logs from commits
- Categorizes changes by type
- Follows semantic versioning

**[Code Change Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-change-summarizer/)**
- Generates structured pull request descriptions from code changes
- Documents breaking changes with migration guides
- Adds testing instructions and context enhancements

**[Release Notes Writer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/release-notes-writer/)**
- Writes release notes
- Highlights new features and fixes
- Targets end users

**[Legacy Code Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/legacy-code-summarizer/)**
- Summarizes legacy codebases
- Explains code functionality
- Aids in understanding old code

**[Python Repository Quick Start](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-repo-quickstart/)**
- Quickly analyzes Python repositories
- Identifies project type, entry points, and dependencies
- Generates setup and execution instructions

**[Error Explanation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/error-explanation-generator/)**
- Explains error messages
- Provides context and solutions
- Helps with debugging

**[Init Deep](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/init-deep/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Generates hierarchical AGENTS.md context files throughout a project tree
- Provides AI agents with directory-specific knowledge automatically
- Supports max-depth control and incremental generation

**[Session Handoff](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/session-handoff/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Creates structured context summaries for cross-session continuation
- Captures completed work, remaining tasks, key files, and gotchas
- Enables seamless handoff between AI sessions or teammates

### Architecture & Design

**[API Design Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-design-assistant/)**
- Assists in API design
- Suggests RESTful patterns
- Validates API consistency

**[Design Pattern Suggestor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-pattern-suggestor/)**
- Suggests appropriate design patterns
- Explains pattern applicability
- Provides implementation guidance

**[Configuration Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator/)**
- Generates configuration files
- Supports multiple formats (YAML, JSON, XML)
- Validates configuration schemas

**[Dependency Resolver](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver/)**
- Resolves dependency conflicts
- Suggests compatible versions
- Analyzes dependency trees

### Requirements & Specifications

**[Requirement Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summarizer/)**
- Summarizes requirements documents
- Extracts key requirements
- Organizes by priority

**[Requirement Coverage Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-coverage-checker/)**
- Checks requirement coverage
- Identifies gaps in implementation
- Traces requirements to code and test

**[Requirement Comparison Reporter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-comparison-reporter/)**
- Compares old and new requirement documents
- Maps requirement changes to code components
- Generates detailed modification plans in Markdown format

**[Ambiguity Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ambiguity-detector/)**
- Detects ambiguous requirements
- Highlights unclear specifications
- Suggests clarifications

**[Scenario Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator/)**
- Generates usage scenarios
- Creates user stories
- Develops test scenarios

**[Specification Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-generator/)**
- Generates formal specifications
- Converts natural language to specs
- Validates specification completeness

**[Natural Language to Constraints](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/nl-to-constraints/)**
- Converts NL requirements to formal constraints
- Supports constraint languages
- Validates constraint consistency

**[Strategic Planner](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/strategic-planner/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Interview-based strategic planning for complex software tasks
- Conducts gap analysis to catch hidden intentions and ambiguities
- Generates detailed work plans with acceptance criteria and test strategy

### DevOps & Deployment



**[Build/CI Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/build-ci-migration-assistant/)**
- Migrates build systems and CI/CD configurations


**[CD Pipeline Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cd-pipeline-generator/)**
- Creates CD pipeline configurations for automated deployment
- Supports AWS, GCP, and Azure cloud platforms
- Includes environment separation, approval gates, and rollback capabilities

**[CI Pipeline Synthesizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ci-pipeline-synthesizer/)**
- Generates CI pipeline configurations for automated building and testing
- Supports GitHub Actions with dependency caching and matrix testing
- Includes templates for Node.js, Python, Go, and Rust projects



**[Config Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/config-consistency-checker/)**
- Detects configuration inconsistencies across environments

**[Containerization Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/containerization-assistant/)**
- Creates Dockerfiles and container configs
- Optimizes container images
- Supports multi-stage builds



**[Environment Setup Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/environment-setup-assistant/)**
- Generates environment setup scripts
- Manages dependencies and configurations
- Supports multiple platforms


**[Rollback Strategy Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rollback-strategy-advisor/)**
- Suggests rollback strategies
- Plans deployment reversions
- Minimizes downtime


**[Docker Hub Automation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/docker_hub-automation/)**
- Automates Docker Hub tasks via Rube MCP (Composio)
- Manages repositories, images, tags, and container registry
- Supports Docker Hub operations




**[Code Instrumentation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-instrumentation-generator/)**
- Automatically instruments source code to collect runtime information
- Preserves program semantics while adding instrumentation
- Supports various instrumentation strategies for debugging and analysis

**[Security-Sensitive Path Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-sensitive-path-instrumenter/)**
- Adds structured logging instrumentation to security-critical code paths
- Monitors authentication, authorization, input validation, and session management
- Enables runtime monitoring of security-relevant events

**[Taint Instrumentation Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/taint-instrumentation-assistant/)**
- Instruments code to track untrusted and sensitive data flow
- Detects security vulnerabilities through taint analysis
- Identifies potential injection points and data leaks

**[Critical Interval Security Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/critical-interval-security-checker/)**
- Analyzes code to identify security-critical time intervals
- Detects timing vulnerabilities that could compromise security
- Identifies race conditions and time-of-check-time-of-use issues

**[Release Change Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/release-change-analyzer/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Compares HEAD with latest published version to analyze real changes
- Groups changes by type (feat/fix/refactor) with actual diff descriptions
- Recommends version bump (major/minor/patch) with reasoning



### Debugging & Error Handling

**[Bug Localization](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-localization/)**
- Localizes bugs in code
- Analyzes stack traces and logs
- Suggests likely bug locations

**[Bug to Patch Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-to-patch-generator/)**
- Generates patches for identified bugs
- Creates minimal fixes
- Includes test cases for fixes

**[Conflict Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer/)**
- Analyzes merge conflicts
- Suggests conflict resolutions
- Explains conflicting changes

**[Failure-Oriented Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/failure-oriented-instrumentation/)**
- Selectively instruments code to capture runtime data for debugging

**[Git Bisect Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/git-bisect-assistant/)**
- Automates git bisect to find the first bad commit

**[Regression Root Cause Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer/)**
- Analyzes regression failures
- Identifies root causes
- Suggests fixes

**[Replay-Oriented Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/replay-oriented-instrumentation/)**
- Records execution for deterministic replay debugging

**[Runtime Error Explainer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer/)**
- Explains runtime errors
- Provides debugging guidance
- Suggests fixes

**[Issue Report Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/issue-report-generator/)**
- Automatically generates clear, actionable issue reports from failing tests
- Analyzes test failures to understand expected vs. actual behavior
- Identifies affected code components and suggests fixes

**[Bug History Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-history-summarizer/)**
- Traces and summarizes the complete lifecycle of a bug across code versions
- Provides historical context for bug evolution
- Helps understand bug patterns and resolution strategies

**[Bisect-Aware Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bisect-aware-instrumentation/)**
- Instruments code to support efficient git bisect operations
- Produces deterministic pass/fail signals and concise runtime summaries
- Creates robust test scripts for bisect workflows

**[Reproduction Trace Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/reproduction-trace-instrumenter/)**
- Instruments source code to capture detailed execution traces for bug reproduction
- Records function calls, variable values, control flow, and program state
- Generates replay scripts for deterministic bug reproduction

**[State Snapshot Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/state-snapshot-instrumenter/)**
- Instruments programs to capture snapshots of key program states at runtime
- Includes variable values, memory state, call stacks, and execution context
- Saves snapshots in structured JSON format for analysis

**[Trace Collection Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/trace-collection-assistant/)**
- Collects, normalizes, and structures execution traces from instrumented programs
- Processes strace, ltrace, and custom trace formats
- Makes traces suitable for debugging, reproduction, or performance analysis

**[SZZ Bug Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/szz-bug-identifier/)**
- Performs SZZ algorithm analysis to identify bug-introducing commits
- Traces modified lines back through version history
- Links bug fixes to their originating changes

**[Semantic SZZ Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-szz-analyzer/)**
- Extends traditional SZZ algorithm with semantic analysis
- Distinguishes actual bug-introducing changes from refactoring
- Provides more accurate identification of bug origins

### Formal Methods & Verification

**[ACSL Annotation Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/acsl-annotation-assistant/)**
- Assists with ACSL annotations
- Generates function contracts
- Validates annotation correctness

**[Assertion Synthesizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/assertion-synthesizer/)**
- Synthesizes program assertions
- Generates invariants and pre/post-conditions
- Validates assertion correctness

**[Invariant Inference](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/invariant-inference/)**
- Infers loop and program invariants
- Uses static and dynamic analysis
- Validates inferred invariants

**[Static Reasoning Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-reasoning-verifier/)**
- Verifies code using static analysis
- Checks correctness properties
- Reports verification results

**[Symbolic Execution Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/symbolic-execution-assistant/)**
- Assists with symbolic execution
- Generates path constraints
- Explores execution paths

**[Counterexample Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-generator/)**
- Generates counterexamples for failed proofs
- Creates test cases from counterexamples
- Helps understand verification failures

**[Counterexample Explainer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-explainer/)**
- Explains counterexamples
- Provides debugging insights
- Suggests fixes

**[Counterexample Debugger](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-debugger/)**
- Debugs proof failures using counterexamples from Nitpick or QuickChick
- Identifies specification errors and missing preconditions
- Helps resolve proof strategy issues

**[Abstract Domain Explorer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-domain-explorer/)**
- Applies abstract interpretation using different abstract domains
- Supports intervals, octagons, polyhedra, sign, and congruence domains
- Infers invariants, value ranges, and relationships

**[Abstract Invariant Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-invariant-generator/)**
- Uses abstract interpretation to infer loop invariants automatically
- Generates function preconditions and postconditions
- Supports formal verification workflows

**[Abstract State Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-state-analyzer/)**
- Performs abstract interpretation to infer program states
- Analyzes variable ranges and data properties without execution
- Reports potential runtime errors

**[Abstract Trace Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-trace-summarizer/)**
- Produces summarized execution traces using abstract interpretation
- Highlights key control flow paths and variable relationships
- Generates high-level program behavior representations

**[Control Flow Abstraction Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/control-flow-abstraction-generator/)**
- Generates abstract Control Flow Graph (CFG) representations
- Shows loops, branches, and function calls for static analysis
- Supports verification and program understanding

**[Formal Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/formal-spec-generator/)**
- Generates formal specifications in Isabelle/HOL or Coq
- Converts informal requirements to formal definitions and predicates
- Creates invariants, pre/post-conditions from natural language

**[C/C++ to Lean4 Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/c-cpp-to-lean4-translator/)**
- Translates C or C++ programs into equivalent Lean4 code
- Preserves program semantics and ensures type safety
- Generates well-typed, executable, and verifiable code

**[C++ to Dafny Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cpp-to-dafny-translator/)**
- Translates C/C++ programs to equivalent Dafny code
- Preserves semantics and ensures verification
- Supports formal verification workflows

**[Python to Dafny Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-dafny-translator/)**
- Translates Python programs into equivalent Dafny code
- Preserves program semantics and ensures verifiability
- Generates well-typed, executable Dafny code

**[Python to Lean4 Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-lean4-translator/)**
- Translates Python programs to equivalent Lean4 code
- Preserves semantics and ensures type safety
- Supports formal verification in Lean4

**[Imperative to Coq Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/imperative-to-coq-model-extractor/)**
- Extracts abstract mathematical models from imperative code
- Supports C, C++, Python, Java for Coq formal reasoning
- Creates Coq specifications suitable for verification

**[Program to Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-model-extractor/)**
- Extracts abstract mathematical models from functional code
- Supports Haskell, OCaml, F# to Isabelle/HOL conversion
- Enables formal reasoning about functional programs

**[Program Correctness Prover](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-correctness-prover/)**
- Generates Isabelle or Coq proofs for program correctness
- Establishes partial or total correctness from specifications
- Uses Hoare logic and weakest precondition calculus

**[Proof Carrying Code Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-carrying-code-generator/)**
- Generates executable code with formal correctness proofs
- Certifies safety and correctness properties in Isabelle/HOL or Coq
- Supports verified software and safety-critical systems

**[Proof Skeleton Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-skeleton-generator/)**
- Generates structured proof skeletons with tactics and strategies
- Creates intermediate lemmas for theorems in Isabelle/HOL or Coq
- Provides proof outlines for complex theorems

**[Proof Trace Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-trace-summarizer/)**
- Summarizes long Isabelle or Coq proof scripts
- Extracts high-level logical steps and reasoning flow
- Documents proof strategies for understanding

**[Proof Failure Explainer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-failure-explainer/)**
- Analyzes and explains why Isabelle or Coq proofs fail
- Identifies type mismatches, missing assumptions, incorrect goals
- Detects unification failures and inapplicable tactics

**[Proof Refactoring Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-refactoring-assistant/)**
- Restructures Isabelle or Coq proofs for better readability
- Enhances modularity and maintainability without changing semantics
- Eliminates repeated patterns and improves proof structure

**[Lemma Discovery Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/lemma-discovery-assistant/)**
- Analyzes failed or stuck proofs to propose auxiliary lemmas
- Helps complete proofs in Isabelle/HOL or Coq
- Addresses unprovable subgoals and stuck proof states

**[Library Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/library-for-proof-advisor/)**
- Recommends relevant Isabelle/HOL or Coq standard library resources
- Suggests theories, lemmas, and tactics based on proof goals
- Helps find existing library support for proofs

**[Tactic Suggestion Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tactic-suggestion-assistant/)**
- Analyzes proof states in Isabelle or Coq
- Suggests applicable tactics to make progress
- Helps choose next steps in interactive proofs

**[Refinement Step Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/refinement-step-generator/)**
- Generates systematic refinement steps from specifications to implementations
- Works in Isabelle/HOL or Coq with correctness obligations
- Supports formal verification through refinement

**[Verification Boundary Reporter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verification-boundary-reporter/)**
- Analyzes formal verification artifacts (Isabelle, Coq, Dafny)
- Identifies boundaries between verified, assumed, and unverified components
- Produces structured reports on verification coverage

**[Verified Pseudocode Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-pseudocode-extractor/)**
- Extracts language-agnostic pseudocode from verified programs
- Preserves verified control flow and data dependencies
- Maintains algorithmic logic from Isabelle/HOL or Coq code

**[Verified Spec Code Mapper](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-spec-code-mapper/)**
- Establishes traceability between formal specifications and verified code
- Maps preconditions, postconditions, invariants to code components
- Produces structured Markdown mapping with correctness proofs

**[Requirement Enhancer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-enhancer/)**
- Iteratively enhances user requirements into clear specifications
- Analyzes and clarifies incomplete or ambiguous requirements
- Produces actionable, complete specifications

**[Interface Contract Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-contract-verifier/)**
- Verifies that formal contracts (preconditions, postconditions, invariants) are preserved
- Validates contract compliance when updating to new program versions
- Ensures interface specifications remain consistent

**[Code Completion Semantic Constraints](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-completion-semantic-constraints/)**
- Completes partial code snippets while satisfying semantic constraints
- Produces compilable code with verification tests
- Explains how each constraint was satisfied

**[Model-Guided Code Repair](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/model-guided-code-repair/)**
- Automatically repairs code violations of temporal properties using counterexamples
- Reasons about model-level causes and proposes minimal fixes
- Validates repairs through re-verification or test generation

**[TLA+ Guided Code Repair](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-guided-code-repair/)**
- Repairs code based on TLA+ specification violations
- Uses TLA+ model checking results to guide repair strategies
- Ensures repaired code satisfies temporal properties

**[Program to TLA+ Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-tlaplus-spec-generator/)**
- Automatically generates TLA+ specifications from program code
- Identifies state variables, actions, and invariants
- Creates formal models for verification

**[TLA+ Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-spec-generator/)**
- Generates TLA+ specifications from requirements or designs
- Creates formal specifications with proper syntax
- Supports concurrent and distributed system modeling

**[Requirement to TLA+ Property Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-to-tlaplus-property-generator/)**
- Converts natural language requirements to TLA+ temporal properties
- Formalizes safety and liveness properties
- Generates verifiable specifications from informal descriptions

**[Specification to Temporal Logic Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-to-temporal-logic-generator/)**
- Translates specifications into temporal logic formulas (LTL, CTL)
- Supports multiple temporal logic notations
- Enables formal verification of system properties

**[TLA+ Model Reduction](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-model-reduction/)**
- Reduces TLA+ model complexity while preserving properties
- Applies abstraction and symmetry reduction techniques
- Improves model checking performance

**[SMV Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smv-model-extractor/)**
- Extracts SMV models from program code or specifications
- Generates models suitable for symbolic model checking
- Supports NuSMV and nuXmv verification tools

**[RTL Specification Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-specification-consistency-checker/)**
- Checks behavioral consistency between RTL and specifications
- Identifies satisfied, violated, underspecified, and uncheckable requirements
- Provides detailed violation reports with execution traces

**[RTL Equivalence Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-equivalence-checker/)**
- Verifies equivalence between two RTL implementations
- Detects functional differences in hardware designs
- Supports formal equivalence checking workflows

**[RTL Property Inference](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-property-inference/)**
- Automatically infers temporal properties from RTL code
- Discovers invariants and protocol properties
- Generates assertions for hardware verification

### Maintenance & Refactoring

**[Code Refactoring Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant/)**
- Suggests refactoring opportunities
- Applies refactoring patterns
- Ensures behavior preservation

**[Deprecated API Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/deprecated-api-updater/)**
- Updates deprecated API usage
- Suggests modern alternatives
- Automates API migration

**[Code Translation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-translation/)**
- Translates code between languages
- Preserves functionality
- Adapts to target language idioms

**[Framework Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/framework-migration-assistant/)**
- Automatically migrates Python web applications between frameworks
- Transforms code, configuration, and tests while preserving functionality
- Handles route migration and request/response patterns

**[Spring MVC to Boot Migrator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/spring-mvc-to-boot-migrator/)**
- Automatically migrates Spring MVC applications to Spring Boot
- Transforms build configuration, annotations, and XML configuration
- Preserves existing functionality while modernizing architecture

**[Test-Guided Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-migration-assistant/)**
- Automatically updates codebase to new language or framework versions
- Ensures all tests continue to pass during migration
- Provides safe, test-driven migration path

**[Test-Guided Debloating](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-debloating/)**
- Removes unnecessary code from repository while preserving test-exercised behavior
- Identifies and eliminates dead code safely
- Maintains exactly the functionality covered by test suite

**[Smart Mutation Operator Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smart-mutation-operator-generator/)**
- Generates customized mutation operators tailored to specific codebase
- Maximizes mutation testing effectiveness
- Creates domain-specific mutations for better test evaluation

**[Code Repair Generation Combo](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-repair-generation-combo/)**
- Automatically repairs buggy code and generates comprehensive tests
- Supports Python, Java, and C++ programs
- Diagnoses bugs, generates fixes, and creates tests to prevent regressions

**[LSP Refactoring](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/lsp-refactoring/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Intelligent refactoring using LSP tools (rename, find-references, go-to-definition)
- AST-aware pattern matching and replacement across 25 languages
- TDD verification workflow with automatic rollback on failure

### Visualization

**[System Diagram Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/system-diagram-generator/)**
- Creates system architecture diagrams
- Supports Mermaid, PlantUML, Graphviz
- Generates data flow and deployment diagrams

### Version Control & Collaboration

**[Git Master](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/git-master/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Atomic commit discipline with automatic style detection from repo history
- Rebase surgeon for history rewriting, conflict resolution, and branch cleanup
- History archaeologist using git blame, bisect, log -S for code archaeology

### Project Management & Issue Tracking

**[GitHub Triage](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/github-triage/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Automated GitHub issue and PR triage with parallel processing
- Classifies issues (question/bug/feature), answers questions from codebase
- Reviews bugfix PRs and auto-merges when all safety conditions are met

### Development Tools & Builders

**[Playwright Automation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/playwright-automation/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Browser automation via Playwright for testing, screenshots, and scraping
- Persistent page state with incremental script-based workflow
- Supports accessibility snapshots, network interception, and device emulation

**[Agent Browser](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/agent-browser/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- CLI-based browser automation with ref-based element interaction
- Snapshot-driven workflow: discover elements, interact by ref, re-snapshot
- Supports form filling, screenshots, PDFs, cookies, and network control

**[Reference Searcher](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/reference-searcher/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Systematic external reference searching across docs, OSS repos, and web
- Three-layer strategy: official docs, GitHub examples, web search
- Synthesizes findings into actionable recommendations

### UI/UX Design

**[Frontend UI/UX](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/frontend-ui-ux/)** (Inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode))
- Designer-turned-developer approach to crafting stunning UI without mockups
- Bold aesthetic direction with distinctive typography, color, and motion
- Anti-pattern enforcement against generic fonts and cookie-cutter design


## 🔁 Skills by Stages

> Stages in Software Development Lifecycle (SDLC)

### 📕 **Requirements**
- **Requirement Analysis**
    - [Ambiguity Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ambiguity-detector) – Automatically detect ambiguous or vague statements in requirements
    - [Requirement Summarizer (Long)](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summarizer) – Extract core features, constraints, and priorities from requirement documents, output markdown files.
    - [Requirement Summarizer (Short)](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summary) – Generate concise, structured summaries of requirements for quick team understanding.
    - [Requirement Conflict Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer) – Detect conflicts or contradictions among requirements

- **Traceability & Coverage**
    - [Requirement to Test](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/req-to-test) – Automatically generate test cases from requirements
    - [Requirement to Constraints](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/nl-to-constraints) -- Transforms natural language requirements into formal specifications and constraints (structured, testable specifications with explicit constraints).
    - [Traceability Matrix Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/traceability-matrix-generator) – Build a traceability matrix connecting requirements → design → implementation → tests
    - [Requirement Coverage Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-coverage-checker) – Check whether the existing design/code covers all requirements
    - [Requirement Comparison Reporter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-comparison-reporter) – Compare requirement versions, map changes to code components, and generate modification plans

- **Documentation & Communication**
    - [Requirement Doc Formatter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer) – Generate clear, standardized requirement documents

- **Scenario & User Story Generation**
    - [Scenario Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator) – Generate usage scenarios and user stories based on requirements
    - [Requirement Enhancer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-enhancer) – Iteratively enhance user requirements into clear, complete, actionable specifications through analysis and clarification

- **Project Management & Issue Tracking**


### 💡 **Software Design**
- **Architecture & High-Level Design**
    - [System Diagram Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/system-diagram-generator) – Create visual representations of system structure
    - [Design Pattern Suggestor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-pattern-suggestor) – Recommend suitable design patterns for a given requirement

- **Interface & API Design**
    - [API Design Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-design-assistant) – Suggest API endpoints, parameters, and return types

- **Design Quality & Analysis**
    - [Design Smell Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-smell-detector) – Identify potential issues like high coupling or low cohesion
    - [Component Boundary Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – Identify module/component boundaries and detect boundary violations
    - [Configuration Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator) – Generate configuration files for applications, services, or infrastructure
    - [Dependency Resolver](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver) – Identify and manage software dependencies

### ⌨️ **Implementation**
- **Spec-to-Code**
    - [Function/Class Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/function-class-generator) – Generate functions or classes from formal specifications or design descriptions
    - [Module/Component Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-component-generator) – Build larger components or modules based on interface contracts
    - [Template/Skeleton-based Code Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/template-code-generator) – Produce boilerplate code or project templates/skeleton automatically
    - [Incremental Python Programmer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-python-programmer) – Implement new features in Python repositories from natural language descriptions with automated testing
    - [Incremental Java Programmer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-java-programmer) – Implement new features in Java repositories (Maven/Gradle) from natural language descriptions with JUnit test generation

- **Refactoring & Optimization**
    - [Refactoring Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant) – Suggest ongoing code improvements to enhance maintainability
    - [Code Optimizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-optimizer) – Improve code performance, memory usage, or efficiency
    - [Dead Code Eliminator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dead-code-eliminator) – Identify and remove unused or redundant code
    - [Code Review Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-review-assistant) - Identify bugs, security issues, performance problems, code quality concerns, and best practice violations
    - [Bad Code Smell Detection](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-smell-detector) - Identifies and reports code smells that may indicate poor design or maintainability issues
    - [Technical Debt Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer) – Identify technical debt and quantify debt impact
    - [Code Pattern Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor) – Analyze codebases to identify reusable code patterns and duplications
    - [Code Search Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant) – Search repositories for code related to given snippets using similarity analysis
    - [Component Boundary Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – Identify module/component boundaries and analyze architectural separation
    - [Code Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-summarizer) – Generate concise summaries of source code at multiple scales to explain and understand code functionality
    - [Pseudocode Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-extractor) – Extract programming-language-agnostic pseudocode from source code, preserving control flow and logical structure
    - [Module-Level Code Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-level-code-translator) – Translate source code between programming languages at module level while preserving behavior
    - [Pseudocode to Java Code](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-java-code) – Convert pseudocode descriptions into complete, executable Java programs
    - [Pseudocode to Python Code](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-python-code) – Convert pseudocode and algorithm descriptions into executable Python code
    - [Code Instrumentation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-instrumentation-generator) – Automatically instrument source code to collect runtime information while preserving semantics
    - [Code Completion Semantic Constraints](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-completion-semantic-constraints) – Complete partial code snippets while satisfying specified semantic constraints

- **TDD & SDD**
    - [Test-Driven Code Generator (TDD)](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-driven-generation) – Generate implementation that passes a given set of unit tests (Support Python and Java primarily; Handle simple unit tests (isolated functions/methods))
    - [Specification-Driven Code Generator (SDD)](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-driven-generation) - Generate implementation according to specification
    
- **Multi-Language & Translation**
    - [Code Translation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-translation) – Convert code between programming languages while preserving functionality



### 👩🏽‍💻 **Testing**
- **Test Generation**
    - [Unit Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/unit-test-generator) – Automatically generate unit tests for functions or modules
    - [Integration Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/integration-test-generator) – Generate tests for multiple interacting components
    - [Directed Test Input Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/directed-test-input-generator) – Uses program context and testing objectives to guide LLM-driven test input generation toward hard-to-reach behaviors.
    - [Fuzzing Input Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/fuzzing-input-generator) -- Produce randomized inputs to detect unexpected failures
    - [Bug Reproduction Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-reproduction-test-generator) – Automatically generate tests that reproduce reported bugs from issue reports and stack traces
    - [Java Regression Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-regression-test-generator) – Automatically generate regression tests for Java codebases by analyzing changes between old and new code versions
    - [Python Regression Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-regression-test-generator) – Automatically generate regression tests for Python codebases by analyzing changes between code versions and migrating existing tests
    - [Mocking Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mocking-test-generator) – Generate unit tests with proper mocking for Python (unittest.mock/pytest) or Java (Mockito/JUnit) code with external dependencies
    - [Metamorphic Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-test-generator) – Generate test cases using metamorphic testing principles by applying transformations based on metamorphic properties
    - [Counterexample to Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator) – Convert formal verification counterexamples into executable test cases for bridging verification and testing


- **Assertion & Oracle Synthesis**
    - [Coverage Enhancer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/coverage-enhancer) – Suggest additional unit tests to improve test coverage
    - [Assertion Synthesizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/assertion-synthesizer) – Generate assertions for automated test cases (*Scenarios*: Add tests to untested code, Enhance existing tests, and Capture actual behavior. *Complexity*: Simple and complex assertions. *Programming Languages*: Multi-languages.)
    - [Test Oracle Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-oracle-generator) – Create automated oracles to verify correct behavior

- **Test Coverage Analysis and Enhancement**
    - [Scenario Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator) – Generate test scenarios or user stories based on requirements
    - [Edge Case Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/edge-case-generator) – Automatically identify potential boundary and exception cases from requirements, and create tests targeting boundary conditions or uncommon scenarios
    - [Test Suite Prioritizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-suite-prioritizer) – Suggest which tests to run first based on impact
    - [Metamorphic Property Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-property-extractor) – Automatically identify metamorphic properties from programs to enable metamorphic testing without explicit test oracles

- **Test Quality & Optimization**
    - [Behavioral Mutation Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavioral-mutation-analyzer) – Systematically analyze surviving mutants from mutation testing to identify test suite weaknesses
    - [Mutation Test Suite Optimizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mutation-test-suite-optimizer) – Optimize test suites using mutation testing to select minimal subset maximizing mutation kill rate
    - [Test Deduplicator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-deduplicator) – Analyze test suites to identify redundant or duplicate tests by examining coverage and semantic similarity
    - [Java API Consistency Validator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-api-consistency-validator) – Validate API consistency between two versions of Java libraries
    - [Python API Consistency Validator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-api-consistency-validator) – Validate API consistency between two versions of Python libraries

- **Failure Analysis**
    - [Regression Root Cause Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer) – Locate root causes of failing regression tests
    - [Error Explanation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/error-explanation-generator) – Explain why tests fail and provide actionable guidance
    - [Runtime Error Explanation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer) – Explains runtime errors and compilation failures with actionable debugging guidance
    - [Failure-Oriented Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/failure-oriented-instrumentation) – Selectively instruments code to capture runtime data for debugging
    - [Replay-Oriented Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/replay-oriented-instrumentation) – Records execution for deterministic replay debugging
    - [Test-Guided Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-bug-detector) – Analyze failing tests to detect functional bugs in code by examining execution behavior, assertions, and stack traces

- **Test Documentation & Reporting**
    - [Test Case Documentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-documentation) – Summarize the documentation for test cases

- **Test Maintenance**
    - [Python Test Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-test-updater) – Update Python tests to work with new code versions, fixing broken tests and updating assertions
    - [Java Test Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-test-updater) – Update Java tests after code refactoring, handling signature changes, mocks, and assertions
    - [Flaky Test Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector) – Identify non-deterministic tests and suggest fixes for common flaky patterns
    - [Interval-Guided Regression Test Update](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-guided-regression-test-update) – Updates regression tests based on interval analysis
    - [Test Case Reducer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-reducer) – Reduces test cases to minimal form using delta debugging



### ✅ **Verification**
- **Specification & Annotation**
    - [Interface Specification Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-specification-generator) – Produce formal or structured interface specifications
    - [ACSL Annotation Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/acsl-annotation-assistant) – Create ACSL or other formal annotations for C/C++ programs
    - [Invariant Inference](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/invariant-inference) – Automatically infer loop or function invariants
    - [Specification Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-generator) – Generate formal specifications (pre/postconditions, invariants) from code or requirements
    - [Formal Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/formal-spec-generator) – Generate formal specifications (definitions, predicates, invariants, pre/post-conditions) in Isabelle/HOL or Coq from informal requirements
    - [Abstract Invariant Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-invariant-generator) – Use abstract interpretation to automatically infer loop invariants, function preconditions, and postconditions for formal verification

- **Abstract Interpretation & Analysis**
    - [Abstract Domain Explorer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-domain-explorer) – Apply abstract interpretation using different abstract domains (intervals, octagons, polyhedra, sign, congruence) to analyze program variables
    - [Abstract State Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-state-analyzer) – Perform abstract interpretation to infer possible program states, variable ranges, and data properties without executing the program
    - [Abstract Trace Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-trace-summarizer) – Perform abstract interpretation to produce summarized execution traces and high-level program behavior representations
    - [Control Flow Abstraction Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/control-flow-abstraction-generator) – Generate abstract Control Flow Graph (CFG) representations showing loops, branches, and function calls for static analysis

- **Code Translation for Verification**
    - [C/C++ to Lean4 Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/c-cpp-to-lean4-translator) – Translate C or C++ programs into equivalent Lean4 code, preserving program semantics and ensuring type safety
    - [C++ to Dafny Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cpp-to-dafny-translator) – Translate C/C++ programs to equivalent Dafny code while preserving semantics and ensuring verification
    - [Python to Dafny Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-dafny-translator) – Translate Python programs into equivalent Dafny code, preserving program semantics and ensuring verifiability
    - [Python to Lean4 Translator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-lean4-translator) – Translate Python programs to equivalent Lean4 code while preserving semantics and ensuring type safety
    - [Imperative to Coq Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/imperative-to-coq-model-extractor) – Extract abstract mathematical models from imperative code (C, C++, Python, Java) suitable for formal reasoning in Coq
    - [Program to Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-model-extractor) – Extract abstract mathematical models from functional code (Haskell, OCaml, F#) for formal reasoning in Isabelle/HOL

- **Formal Verification**
    - [Static Reasoning Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-reasoning-verifier) – Check code correctness statically against specifications
    - [Symbolic Execution Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/symbolic-execution-assistant) – Perform symbolic execution to detect potential errors
    - [Program Correctness Prover](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-correctness-prover) – Generate Isabelle or Coq proofs establishing partial or total correctness of imperative programs from code and formal specifications
    - [Proof Carrying Code Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-carrying-code-generator) – Generate executable code together with formal proofs certifying safety and correctness properties in Isabelle/HOL or Coq

- **Proof Development & Assistance**
    - [Proof Skeleton Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-skeleton-generator) – Generate structured proof skeletons with tactics, strategies, and intermediate lemmas for theorems in Isabelle/HOL or Coq
    - [Proof Trace Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-trace-summarizer) – Summarize long Isabelle or Coq proof scripts into high-level logical steps and reasoning flow
    - [Proof Refactoring Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-refactoring-assistant) – Restructure and improve Isabelle or Coq proofs to enhance readability, modularity, and maintainability without changing semantics
    - [Lemma Discovery Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/lemma-discovery-assistant) – Analyze failed or stuck proofs and propose auxiliary lemmas to help complete the proof in Isabelle/HOL or Coq
    - [Library Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/library-for-proof-advisor) – Recommend relevant Isabelle/HOL or Coq standard library theories, lemmas, and tactics based on proof goals
    - [Tactic Suggestion Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tactic-suggestion-assistant) – Analyze proof states in Isabelle or Coq and suggest applicable tactics to make progress
    - [Refinement Step Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/refinement-step-generator) – Generate systematic refinement steps from high-level specifications to concrete implementations in Isabelle/HOL or Coq

- **Counterexample Analysis**
    - [Counterexample Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-generator) – Produce counterexamples when verification fails
    - [Counterexample Explainer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-explainer) – Explain why a counterexample violates the specification
    - [Counterexample Debugger](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-debugger) – Debug proof failures using counterexamples from Nitpick (Isabelle) or QuickChick (Coq) to identify specification errors and missing preconditions
    - [Proof Failure Explainer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-failure-explainer) – Analyze and explain why Isabelle or Coq proofs fail, identifying root causes such as type mismatches, missing assumptions, and incorrect goals

- **Verification Reporting & Traceability**
    - [Verification Boundary Reporter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verification-boundary-reporter) – Analyze formal verification artifacts (Isabelle, Coq, Dafny) and produce structured reports identifying boundaries between verified, assumed, and unverified components
    - [Verified Pseudocode Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-pseudocode-extractor) – Extract language-agnostic pseudocode from formally verified programs (Isabelle/HOL, Coq) while preserving verified control flow and data dependencies
    - [Verified Spec Code Mapper](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-spec-code-mapper) – Establish explicit traceability between formal specifications (preconditions, postconditions, invariants) and verified code components with their correctness proofs
    - [Interface Contract Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-contract-verifier) – Verify that formal contracts are preserved when updating to new program versions
    - [Behavior Preservation Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavior-preservation-checker) – Validate that migrated or refactored codebase preserves original behavior
    - [Semantic Equivalence Verifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-equivalence-verifier) – Analyze semantic equivalence between two code artifacts
    - [Regression Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-consistency-checker) – Check whether new version preserves behavior observed by tests on old version

- **TLA+ Specification & Verification**
    - [Program to TLA+ Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-tlaplus-spec-generator) – Automatically generate TLA+ specifications from program code by identifying state variables, actions, and invariants
    - [TLA+ Spec Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-spec-generator) – Generate TLA+ specifications from requirements or designs for concurrent and distributed system modeling
    - [Requirement to TLA+ Property Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-to-tlaplus-property-generator) – Convert natural language requirements to TLA+ temporal properties and formal specifications
    - [Specification to Temporal Logic Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-to-temporal-logic-generator) – Translate specifications into temporal logic formulas (LTL, CTL) for formal verification
    - [TLA+ Model Reduction](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-model-reduction) – Reduce TLA+ model complexity while preserving properties using abstraction and symmetry reduction
    - [TLA+ Guided Code Repair](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-guided-code-repair) – Repair code based on TLA+ specification violations using model checking results
    - [Model-Guided Code Repair](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/model-guided-code-repair) – Automatically repair code violations of temporal properties using counterexamples and model-level reasoning

- **Hardware Verification**
    - [RTL Specification Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-specification-consistency-checker) – Check behavioral consistency between RTL and specifications with detailed violation reports
    - [RTL Equivalence Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-equivalence-checker) – Verify equivalence between two RTL implementations and detect functional differences
    - [RTL Property Inference](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-property-inference) – Automatically infer temporal properties and invariants from RTL code

- **Model Checking & Extraction**
    - [SMV Model Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smv-model-extractor) – Extract SMV models from program code or specifications for symbolic model checking
    - [Counterexample to Test Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator) – Convert formal verification counterexamples into executable test cases


### 💻 **Deployment**
- **Deployment Preparation**
    - [Environment Setup Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/environment-setup-assistant) – Generate setup scripts or instructions for target environments
    - [Configuration Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator) – Produce configuration files for applications, services, or infrastructure
    - [Dependency Resolver](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver) – Identify and manage software dependencies before deployment
    - [Containerization Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/containerization-assistant) – Generate Dockerfiles or containerization scripts
    - [Config Consistency Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/config-consistency-checker) – Detects configuration inconsistencies across environments
    - [Security-Sensitive Path Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-sensitive-path-instrumenter) – Add structured logging instrumentation to security-critical code paths for runtime monitoring
    - [Taint Instrumentation Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/taint-instrumentation-assistant) – Instrument code to track untrusted and sensitive data flow for security vulnerability detection
    - [Critical Interval Security Checker](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/critical-interval-security-checker) – Analyze code to identify security-critical time intervals and timing vulnerabilities

- **Continuous Integration & Delivery (CI/CD)**
    - [CI Pipeline Synthesizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ci-pipeline-synthesizer) – Create CI pipelines for automated building and testing
    - [CD Pipeline Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cd-pipeline-generator) – Produce scripts for automated deployment to staging or production
    - [Build/CI Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/build-ci-migration-assistant) – Migrates build systems and CI/CD configurations

- **Cloud & Infrastructure Deployment**
    - [Docker Hub Automation](docker_hub-automation) – Automate Docker Hub tasks via Rube MCP (Composio) for repositories, images, tags, and container registry management

- **Deployment Verification & Testing**
    - [Rollback Strategy Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rollback-strategy-advisor) – Suggest rollback strategies for failed deployments

- **Documentation & Reporting**
    - [Release Notes Writer](release-notes-writer) – Automatically generate user-facing release notes


### 🔧 **Maintenance**
- **Bug & Issue Handling**
    - [Bug Localization](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-localization) – Identify the location of bugs in code or modules
    - [Regression Root Cause Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer) – Find root causes of failing regression tests
    - [Runtime Error Explanation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer) – Explains runtime errors and compilation failures with actionable debugging guidance
    - [Bug-to-Patch Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-to-patch-generator) – Generate code fixes from bug reports or failing test cases
    - [Git Bisect Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/git-bisect-assistant) – Automates git bisect to find the first bad commit
    - [Issue Report Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/issue-report-generator) – Automatically generate clear, actionable issue reports from failing tests and repository analysis
    - [Bug History Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-history-summarizer) – Trace and summarize the complete lifecycle of a bug across code versions
    - [Bisect-Aware Instrumentation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bisect-aware-instrumentation) – Instrument code to support efficient git bisect operations
    - [Reproduction Trace Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/reproduction-trace-instrumenter) – Instrument source code to capture detailed execution traces for bug reproduction
    - [State Snapshot Instrumenter](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/state-snapshot-instrumenter) – Instrument programs to capture snapshots of key program states at runtime
    - [Trace Collection Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/trace-collection-assistant) – Collect, normalize, and structure execution traces from instrumented programs
    - [SZZ Bug Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/szz-bug-identifier) – Perform SZZ algorithm analysis to identify bug-introducing commits
    - [Semantic SZZ Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-szz-analyzer) – Extend traditional SZZ algorithm with semantic analysis for more accurate bug origin identification
    - [Code Repair Generation Combo](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-repair-generation-combo) – Automatically repair buggy code and generate comprehensive tests to verify correctness

- **Security & Vulnerability Management**
    - [Static Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-bug-detector) – Analyze source code statically to detect potential functional bugs including null dereferences, incorrect conditions, and logic errors
    - [Static Vulnerability Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-vulnerability-detector) – Statically analyze code to detect security vulnerabilities including buffer overflows, injection risks, and insecure deserialization
    - [Vulnerability Pattern Matcher](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-pattern-matcher) – Detect security vulnerabilities by matching code against known vulnerability patterns and insecure coding idioms
    - [Vulnerability Root Cause Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-root-cause-analyzer) – Analyze vulnerable code to identify underlying root causes such as violated assumptions and missing validation checks
    - [Exploitability Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/exploitability-analyzer) – Assess realistic exploitability of detected vulnerabilities by examining control flow, input sources, and sanitization logic
    - [Security Patch Advisor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-patch-advisor) – Propose secure remediation strategies for detected security vulnerabilities
    - [Semantic Bug Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-bug-detector) – Detect semantic-level bugs by analyzing whether code behavior matches its intended purpose inferred from names, comments, and documentation
    - [CVE Reachability Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-reachability-analyzer) – Analyze whether CVE vulnerabilities in dependencies are reachable from application code
    - [CVE Watchlist Action Recommendation Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-watchlist-action-recommendation-generator) – Generate actionable recommendations for CVEs in dependency watchlists
    - [Time-Aware Dependency CVE Scanner](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/time-aware-dependency-cve-scanner) – Scan dependencies for CVEs with temporal context awareness and time-sensitive recommendations

- **Legacy & Technical Debt Management**
    - [Legacy Code Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/legacy-code-summarizer) – Produce summaries and insights about legacy code bases
    - [Technical Debt Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer) – Detect areas with high maintenance cost or poor design
    - [Deprecated API Updater](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/deprecated-api-updater) – Identify and replace deprecated APIs

- **Performance & Reliability Monitoring**
    - [Flaky Test Detector](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector) – Identify unstable or unreliable test cases

- **Version Control & Merge Conflicts**
    - [Conflict Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer) – Analyze merge conflicts and suggest conflict resolutions

- **Documentation & Knowledge Transfer**
    - [api-documentation-generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-documentation-generator) - Summarize API documentation for the given repository
    - [README Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/readme-generator) – Generate comprehensive, user-friendly README.md files with setup instructions and usage examples
    - [Python Repository Quick Start](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-repo-quickstart) - Quickly analyze Python repositories to understand structure, dependencies, and setup requirements
    - [Markdown Document Structurer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer) - Reorganize markdown documents into well-structured, consistent format with improved readability
    - [Code Comment Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-comment-generator) – Produce meaningful comments for maintenance readability
    - [Change Log Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/change-log-generator) – Automatically generate change logs from commits or patches
    - [Code Change Summarizer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-change-summarizer) – Generate structured PR descriptions from code changes with testing instructions and context

- **Continuous Improvement**
    - [Refactoring Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant) – Suggest ongoing code improvements to enhance maintainability
    - [Code Pattern Extractor](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor) – Identify reusable code patterns for future development
    - [Code Search Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant) – Search repositories for related code using multi-dimensional similarity analysis
    - [Component Boundary Identifier](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – Identify module/component boundaries and detect boundary violations
    - [Framework Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/framework-migration-assistant) – Automatically migrate Python web applications between frameworks
    - [Spring MVC to Boot Migrator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/spring-mvc-to-boot-migrator) – Automatically migrate Spring MVC applications to Spring Boot
    - [Test-Guided Migration Assistant](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-migration-assistant) – Automatically update codebase to new language or framework versions while ensuring tests pass
    - [Test-Guided Debloating](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-debloating) – Remove unnecessary code while preserving test-exercised behavior
    - [Smart Mutation Operator Generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smart-mutation-operator-generator) – Generate customized mutation operators tailored to specific codebase
    - [Multi-Version Behavior Comparator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/multi-version-behavior-comparator) – Compare behavior across multiple versions of programs
    - [Interval Difference Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-difference-analyzer) – Analyze differences in program intervals between versions to detect behavioral changes
    - [Interval Profiling Performance Analyzer](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-profiling-performance-analyzer) – Profile programs to identify performance bottlenecks
    

## Usage

Each skill is packaged as a skill folder containing a `SKILL.md` file and other necessary scripts/references that can be loaded into Claude Code or other compatible LLM systems.

### Setup a Skill

```bash
# Copy the skill folder to your skills directory
cp -r skill-folder ~/.claude/skills
```

You may also need to make a direction if `~/.claude/skills` does not exist:

```bash
mkdir ~/.claude/skills
```

More details of [**how Claude store skills and other configurations**](https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md#Claude-Code-Local-Storage-Layout)


### Using a Skill

See [here](https://ArabelaTso.github.io/Skills-4-SE/) "How to use".


## ⚡ Risk Disclosure
To prevent potential **security risks** that skills may pose when running locally (such as accessing SSH keys, API keys, sending data to external servers, executing arbitrary system commands, or modifying global dependencies), all skills in this project have undergone **security scans** via [Skill-Security-Scanner](https://github.com/huifer/skill-security-scan). The summarized report is provided below, and the full report can be accessed at [here](https://github.com/ArabelaTso/Skills-4-SE/tree/main/_report/):

📊 Risk Level Statistical Report 

- Risk distribution (Total: 174 skills scanned):

- 🔴 CRITICAL: 16 Skills (9.2%)
    > Trying to access `\tmp` or other system dirs, installing packages
    - framework-migration-assistant
    - vulnerability-pattern-matcher
    - code-smell-detector
    - req-to-test
    - traceability-matrix-generator
    - python-test-updater
    - requirement-enhancer
    - security-sensitive-path-instrumenter
    - critical-interval-security-checker
    - static-vulnerability-detector
    - environment-setup-assistant
    - scenario-generator
    - security-patch-advisor
    - api-documentation-generator
    - test-case-documentation
    - symbolic-execution-assistant
- 🟠 HIGH: 5 Skills (2.9%)
    > Using `os.system`, `subprocess`, `eval`, `exec`
    - containerization-assistant
    - bisect-aware-instrumentation
    - code-change-summarizer
    - configuration-generator
    - code-comment-generator
- 🟡 MEDIUM: 9 Skills (5.2%)
    > Requesting network
- 🟢 LOW: 21 Skills (12.1%)
- ✅ SAFE: 123 Skills (70.7%)

⚠️ **Note**: High false positive rate; please carefully verify. For example, if the description contains words like "password," it is considered a high-risk skill. Decide for yourself whether to use it.

For more details, please see the [log](https://github.com/ArabelaTso/Skills-4-SE/tree/main/_report/security_scan_raw.log).



## 🤝 Contributing

We welcome contributions from both:
- **Researchers** (new Skills, evaluation methods)
- **Practitioners** (real-world use cases, pipelines)

to:
- **Contribute new skills** 
- **Improving existing skills** (serving as baseline, improving procedures, triggering conditions, scripts, and example codes)
- **Suggesting new skill packs** (packing existing skills to suit new task scenarios)


Please read [Contributing Guidelines](https://github.com/ArabelaTso/Skills-4-SE/blob/main/CONTRIBUTING.md) before submitting a pull request.

**Quick Contribution Steps**:
- Ensure your skill is based on a real use case
- Check for duplicates in existing skills
- Follow the skill structure template
- Test your skill across platforms
- Submit a pull request with clear documentation

## 🎯 Vision

Our long-term vision is to build:
> **A shared, open Skill layer for LLM-powered Software Engineering systems** 

✅ Unlike prompt collections or ad-hoc demos, each Skill in this repository is:
- **Task-grounded** (solves a concrete software engineering problem)
- **Reusable** (clearly specified inputs and outputs)
- **Composable** (can be chained into larger workflows or pipelines)
- **Tool- and artifact-aware** (operates on real code, tests, specs, configs, logs)

🧰 This repo is intended to serve as a **shared skill layer** for:
- AI assistants (e.g., Claude Skills, agents)
- Tool-augmented software engineering workflows
- Research prototypes and empirical studies
- Industrial automation and developer productivity tools


🎉 If you are building or studying AI Agent for software engineering, this repo is for you.




## Reference

Special thanks to the following links for constructing and enhancing the skills in this repository:

- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/)
- [anthropics-skills](https://github.com/anthropics/skills/)
- [openclaw-skills](https://github.com/openclaw/skills/)
