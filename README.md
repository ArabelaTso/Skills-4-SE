<h1 align="center"><strong>✨ Skills-4-SE</strong>: Useful Skills for Software Engineering</h1>

<p align="center">
<a href="https://platform.composio.dev/?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeSkills">
  <img width="1280" height="640" alt="Composio banner" src="./banner.png">
</a>


[![Welcome Contribution](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![中文](https://img.shields.io/badge/lang-中文-red)](./README-zh.md)
[![English](https://img.shields.io/badge/lang-English-blue)](./README.md)

This repository is **a comprehensive reusable, task-oriented Skills collection** designed to support **software engineering activities across the entire development lifecycle**, including:

> requirements understanding, system design, implementation, testing, verification, deployment, and maintenance.

✅ Unlike prompt collections or ad-hoc demos, each Skill in this repository is:
- **Task-grounded** (solves a concrete software engineering problem)
- **Reusable** (clearly specified inputs and outputs)
- **Composable** (can be chained into larger workflows or pipelines)
- **Tool- and artifact-aware** (operates on real code, tests, specs, configs, logs)

🧰 This repo is intended to serve as a **shared skill layer** for:
- LLM-based assistants (e.g., Claude Skills, agents)
- Tool-augmented software engineering workflows
- Research prototypes and empirical studies
- Industrial automation and developer productivity tools

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

## Table of Contents

- [**Skills by Category**](#skills-by-category)
  - ⌨️ [Code Generation](#code-generation)
  - 👩🏽‍💻 [Testing](#testing)
  - ⚖️ [Code Quality & Analysis](#code-quality--analysis)
  - 📕 [Documentation](#documentation)
  - 💡 [Architecture & Design](#architecture--design)
  - 📗 [Requirements & Specifications](#requirements--specifications)
  - 💻 [DevOps & Deployment](#devops--deployment)
  - 🔨 [Debugging & Error Handling](#debugging--error-handling)
  - ✅ [Formal Methods & Verification](#formal-methods--verification)
  - 🔧 [Maintenance & Refactoring](#maintenance--refactoring)
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

**[Function/Class Generator](./function-class-generator/)**
- Generates functions and classes from specifications
- Supports multiple programming languages
- Includes type hints, documentation, and error handling

**[Module/Component Generator](./module-component-generator/)**
- Builds complete modules from interface contracts
- Generates layered architectures (model, repository, service)
- Supports Python and Java with design patterns

**[Template Code Generator](./template-code-generator/)**
- Creates boilerplate code from templates
- Supports common patterns and frameworks
- Customizable templates for different use cases

**[Specification-Driven Generation](./specification-driven-generation/)**
- Generates code from formal specifications
- Ensures specification compliance
- Validates generated code against requirements

**[Test-Driven Generation](./test-driven-generation/)**
- Generates implementation from test cases
- Follows TDD principles
- Ensures test coverage

**[Incremental Python Programmer](./incremental-python-programmer/)**
- Implements new features in Python repositories from natural language descriptions
- Generates comprehensive unit and integration tests
- Ensures all tests pass and follows existing code patterns

**[Incremental Java Programmer](./incremental-java-programmer/)**
- Implements new features in Java repositories from natural language descriptions
- Supports Maven and Gradle build systems
- Generates JUnit tests and ensures all tests pass successfully

### Testing

**[Unit Test Generator](./unit-test-generator/)**
- Generates unit tests for functions and classes
- Supports multiple testing frameworks
- Includes edge cases and assertions

**[Integration Test Generator](./integration-test-generator/)**
- Creates integration tests for system components
- Tests component interactions
- Includes setup and teardown logic

**[Java Test Updater](./java-test-updater/)**
- Updates Java tests to work with new code versions after refactoring
- Handles signature changes, refactoring, and behavior modifications
- Updates method calls, assertions, mocks, and ensures tests pass

**[Flaky Test Detector](./flaky-test-detector/)**
- Identifies non-deterministic tests
- Analyzes test execution patterns
- Suggests fixes for common flaky patterns

**[Test Oracle Generator](./test-oracle-generator/)**
- Generates expected outputs for test cases
- Creates assertions and validation logic
- Supports property-based testing

**[Edge Case Generator](./edge-case-generator/)**
- Identifies and generates edge case tests
- Covers boundary conditions
- Includes corner cases and error scenarios

**[Directed Test Input Generator](./directed-test-input-generator/)**
- Generates targeted test inputs
- Focuses on specific code paths
- Uses symbolic execution techniques

**[Fuzzing Input Generator](./fuzzing-input-generator/)**
- Creates randomized test inputs
- Discovers unexpected behaviors
- Supports mutation-based fuzzing

**[Test Suite Prioritizer](./test-suite-prioritizer/)**
- Prioritizes test execution order
- Optimizes for early failure detection
- Considers test dependencies and coverage

**[Coverage Enhancer](./coverage-enhancer/)**
- Identifies uncovered code paths
- Generates tests to improve coverage
- Reports coverage metrics

**[Test Case Documentation](./test-case-documentation/)**
- Documents test cases and their purposes
- Explains test scenarios and expected outcomes
- Maintains test documentation

**[Python Test Updater](./python-test-updater/)**
- Updates Python tests to work with new code versions
- Fixes broken tests due to signature and behavior changes
- Analyzes code diffs and updates assertions accordingly

**[Requirement to Test](./req-to-test/)**
- Converts requirements to test cases
- Ensures requirement coverage
- Traces tests back to requirements

### Code Quality & Analysis

**[Code Review Assistant](./code-review-assistant/)**
- Performs automated code reviews
- Identifies issues and suggests improvements
- Checks coding standards compliance

**[Code Smell Detector](./code-smell-detector/)**
- Detects code smells and anti-patterns
- Suggests refactoring opportunities
- Categorizes smells by severity

**[Design Smell Detector](./design-smell-detector/)**
- Identifies architectural and design issues
- Detects violations of design principles
- Suggests design improvements

**[Code Optimizer](./code-optimizer/)**
- Optimizes code for performance
- Identifies bottlenecks
- Suggests algorithmic improvements

**[Dead Code Eliminator](./dead-code-eliminator/)**
- Identifies unused code
- Safely removes dead code
- Reports elimination opportunities

**[Technical Debt Analyzer](./technical-debt-analyzer/)**
- Identifies technical debt
- Quantifies debt impact
- Prioritizes debt reduction

**[Code Pattern Extractor](./code-pattern-extractor/)**
- Analyzes codebases to identify reusable code patterns and duplications
- Generates pattern catalogs with refactoring suggestions
- Creates reusable template code for high-value patterns

**[Code Search Assistant](./code-search-assistant/)**
- Searches repositories for code related to given snippets
- Ranks results by call chain, textual, and functional similarity
- Outputs ranked file lists with matching code snippets

**[Component Boundary Identifier](./component-boundary-identifier/)**
- Identifies module/component boundaries
- Detects boundary violations
- Analyzes architectural separation

### Documentation

**[API Documentation Generator](./api-documentation-generator/)**
- Generates API documentation
- Creates reference documentation
- Includes usage examples

**[Code Comment Generator](./code-comment-generator/)**
- Generates inline code comments
- Explains complex logic
- Follows documentation standards

**[Markdown Document Structurer](./markdown-document-structurer/)**
- Reorganizes markdown documents into well-structured format
- Fixes heading hierarchy and generates table of contents
- Standardizes formatting and improves readability

**[README Generator](./readme-generator/)**
- Generates comprehensive, user-friendly README.md files
- Includes project introduction, prerequisites, and setup instructions
- Provides executable usage examples and repository structure overview

**[Change Log Generator](./change-log-generator/)**
- Creates change logs from commits
- Categorizes changes by type
- Follows semantic versioning

**[Code Change Summarizer](./code-change-summarizer/)**
- Generates structured pull request descriptions from code changes
- Documents breaking changes with migration guides
- Adds testing instructions and context enhancements

**[Release Notes Writer](./release-notes-writer/)**
- Writes release notes
- Highlights new features and fixes
- Targets end users

**[Legacy Code Summarizer](./legacy-code-summarizer/)**
- Summarizes legacy codebases
- Explains code functionality
- Aids in understanding old code

**[Python Repository Quick Start](./python-repo-quickstart/)**
- Quickly analyzes Python repositories
- Identifies project type, entry points, and dependencies
- Generates setup and execution instructions

**[Error Explanation Generator](./error-explanation-generator/)**
- Explains error messages
- Provides context and solutions
- Helps with debugging

### Architecture & Design

**[API Design Assistant](./api-design-assistant/)**
- Assists in API design
- Suggests RESTful patterns
- Validates API consistency

**[Design Pattern Suggestor](./design-pattern-suggestor/)**
- Suggests appropriate design patterns
- Explains pattern applicability
- Provides implementation guidance

**[Configuration Generator](./configuration-generator/)**
- Generates configuration files
- Supports multiple formats (YAML, JSON, XML)
- Validates configuration schemas

**[Dependency Resolver](./dependency-resolver/)**
- Resolves dependency conflicts
- Suggests compatible versions
- Analyzes dependency trees

### Requirements & Specifications

**[Requirement Summarizer](./requirement-summarizer/)**
- Summarizes requirements documents
- Extracts key requirements
- Organizes by priority

**[Requirement Coverage Checker](./requirement-coverage-checker/)**
- Checks requirement coverage
- Identifies gaps in implementation
- Traces requirements to code and test

**[Requirement Comparison Reporter](./requirement-comparison-reporter/)**
- Compares old and new requirement documents
- Maps requirement changes to code components
- Generates detailed modification plans in Markdown format

**[Ambiguity Detector](./ambiguity-detector/)**
- Detects ambiguous requirements
- Highlights unclear specifications
- Suggests clarifications

**[Scenario Generator](./scenario-generator/)**
- Generates usage scenarios
- Creates user stories
- Develops test scenarios

**[Specification Generator](./specification-generator/)**
- Generates formal specifications
- Converts natural language to specs
- Validates specification completeness

**[Natural Language to Constraints](./nl-to-constraints/)**
- Converts NL requirements to formal constraints
- Supports constraint languages
- Validates constraint consistency

### DevOps & Deployment

**[CI Pipeline Synthesizer](./ci-pipeline-synthesizer/)**
- Generates CI pipeline configurations for automated building and testing
- Supports GitHub Actions with dependency caching and matrix testing
- Includes templates for Node.js, Python, Go, and Rust projects

**[CD Pipeline Generator](./cd-pipeline-generator/)**
- Creates CD pipeline configurations for automated deployment
- Supports AWS, GCP, and Azure cloud platforms
- Includes environment separation, approval gates, and rollback capabilities

**[Containerization Assistant](./containerization-assistant/)**
- Creates Dockerfiles and container configs
- Optimizes container images
- Supports multi-stage builds

**[Environment Setup Assistant](./environment-setup-assistant/)**
- Generates environment setup scripts
- Manages dependencies and configurations
- Supports multiple platforms

**[Rollback Strategy Advisor](./rollback-strategy-advisor/)**
- Suggests rollback strategies
- Plans deployment reversions
- Minimizes downtime

### Debugging & Error Handling

**[Bug Localization](./bug-localization/)**
- Localizes bugs in code
- Analyzes stack traces and logs
- Suggests likely bug locations

**[Bug to Patch Generator](./bug-to-patch-generator/)**
- Generates patches for identified bugs
- Creates minimal fixes
- Includes test cases for fixes

**[Runtime Error Explainer](./runtime-error-explainer/)**
- Explains runtime errors
- Provides debugging guidance
- Suggests fixes

**[Regression Root Cause Analyzer](./regression-root-cause-analyzer/)**
- Analyzes regression failures
- Identifies root causes
- Suggests fixes

**[Conflict Analyzer](./conflict-analyzer/)**
- Analyzes merge conflicts
- Suggests conflict resolutions
- Explains conflicting changes

### Formal Methods & Verification

**[ACSL Annotation Assistant](./acsl-annotation-assistant/)**
- Assists with ACSL annotations
- Generates function contracts
- Validates annotation correctness

**[Assertion Synthesizer](./assertion-synthesizer/)**
- Synthesizes program assertions
- Generates invariants and pre/post-conditions
- Validates assertion correctness

**[Invariant Inference](./invariant-inference/)**
- Infers loop and program invariants
- Uses static and dynamic analysis
- Validates inferred invariants

**[Static Reasoning Verifier](./static-reasoning-verifier/)**
- Verifies code using static analysis
- Checks correctness properties
- Reports verification results

**[Symbolic Execution Assistant](./symbolic-execution-assistant/)**
- Assists with symbolic execution
- Generates path constraints
- Explores execution paths

**[Counterexample Generator](./counterexample-generator/)**
- Generates counterexamples for failed proofs
- Creates test cases from counterexamples
- Helps understand verification failures

**[Counterexample Explainer](./counterexample-explainer/)**
- Explains counterexamples
- Provides debugging insights
- Suggests fixes

### Maintenance & Refactoring

**[Code Refactoring Assistant](./code-refactoring-assistant/)**
- Suggests refactoring opportunities
- Applies refactoring patterns
- Ensures behavior preservation

**[Deprecated API Updater](./deprecated-api-updater/)**
- Updates deprecated API usage
- Suggests modern alternatives
- Automates API migration

**[Code Translation](./code-translation/)**
- Translates code between languages
- Preserves functionality
- Adapts to target language idioms

### Visualization

**[System Diagram Generator](./system-diagram-generator/)**
- Creates system architecture diagrams
- Supports Mermaid, PlantUML, Graphviz
- Generates data flow and deployment diagrams


## 🔁 Skills by Stages

> Stages in Software Deveopment Lifecycle (SDLC)

### 📕 **Requirements**
- **Requirement Analysis**
    - [Ambiguity Detector](ambiguity-detector) – Automatically detect ambiguous or vague statements in requirements
    - [Requirement Summarizer (Long)](requirement-summarizer) – Extract core features, constraints, and priorities from requirement documents, output markdown files.
    - [Requirement Summarizer (Short)](requirement-summary) – Generate concise, structured summaries of requirements for quick team understanding.
    - [Requirement Conflict Analyzer](conflict-analyzer) – Detect conflicts or contradictions among requirements

- **Traceability & Coverage**
    - [Requirement to Test](req-to-test) – Automatically generate test cases from requirements
    - [Requirement to Contraints](nl-to-constraints) -- Transforms natural language requirements into into formal specifications and constraints (structured, testable specifications with explicit constraints).
    - [Traceability Matrix Generator](traceability-matrix-generator) – Build a traceability matrix connecting requirements → design → implementation → tests
    - [Requirement Coverage Checker](requirement-coverage-checker) – Check whether existing design/code covers all requirements
    - [Requirement Comparison Reporter](requirement-comparison-reporter) – Compare requirement versions, map changes to code components, and generate modification plans

- **Documentation & Communication**
    - [Requirement Doc Formatter](markdown-document-structurer) – Generate clear, standardized requirement documents


### 💡 **Software Design**
- **Architecture & High-Level Design**
    - [System Diagram Generator](system-diagram-generator) – Create visual representations of system structure
    - [Design Pattern Suggestor](design-pattern-suggestor) – Recommend suitable design patterns for a given requirement

- **Interface & API Design**
    - [API Design Assistant](api-design-assistant) – Suggest API endpoints, parameters, and return types

- **Design Quality & Analysis**
    - [Design Smell Detector](design-smell-detector) – Identify potential issues like high coupling or low cohesion

### ⌨️ **Implementation**
- **Spec-to-Code**
    - [Function/Class Generator](function-class-generator) – Generate functions or classes from formal specifications or design descriptions
    - [Module/Component Generator](module-component-generator) – Build larger components or modules based on interface contracts
    - [Template/Skeleton-based Code Generator](template-code-generator) – Produce boilerplate code or project templates/skeleton automatically
    - [Incremental Python Programmer](incremental-python-programmer) – Implement new features in Python repositories from natural language descriptions with automated testing
    - [Incremental Java Programmer](incremental-java-programmer) – Implement new features in Java repositories (Maven/Gradle) from natural language descriptions with JUnit test generation

- **Refactoring & Optimization**
    - [Refactoring Assistant](code-refactoring-assistant) – Suggest ongoing code improvements to enhance maintainability
    - [Code Optimizer](code-optimizer) – Improve code performance, memory usage, or efficiency
    - [Dead Code Eliminator](dead-code-eliminator) – Identify and remove unused or redundant code
    - [Code Review Assistant](code-review-assistant) - Identify bugs, security issues, performance problems, code quality concerns, and best practice violations
    - [Bad Code Smell Detection](code-smell-detector) - Identifies and reports code smells that may indicate poor design or maintainability issues

- **TDD & SDD**
    - [Test-Driven Code Generator (TDD)](test-driven-generation) – Generate implementation that passes a given set of unit tests (Support Python and Java primarily; Handle simple unit tests (isolated functions/methods))
    - [Specification-Driven Code Generator (SDD)](specification-driven-generation) - Generate implementation according to specification
    
- **Multi-Language & Translation**
    - [Code Translation](code-translation) – Convert code between programming languages while preserving functionality

### 👩🏽‍💻 **Testing**
- **Test Generation**
    - [Unit Test Generator](unit-test-generator) – Automatically generate unit tests for functions or modules
    - [Integration Test Generator](integration-test-generator) – Generate tests for multiple interacting components
    - [Directed Test Input Generator](directed-test-input-generator) – Uses program context and testing objectives to guide LLM-driven test input generation toward hard-to-reach behaviors.
    - [Fuzzing Input Generator](fuzzing-input-generator) -- Produce randomized inputs to detect unexpected failures


- **Assertion & Oracle Synthesis**
    - [Coverage Enhancer](coverage-enhancer) – Suggest additional unit tests to improve test coverage
    - [Assertion Synthesizer](assertion-synthesizer) – Generate assertions for automated test cases (*Scenarios*: Add tests to untested code, Enhance existing tests, and Capture actual behavior. *Complexity*: Simple and complex assertions. *Programming Languages*: Multi-languages.)
    - [Test Oracle Generator](test-oracle-generator) – Create automated oracles to verify correct behavior

- **Test Coverage Analysis and Enhancement**
    - [Scenario Generator](scenario-generator) – Generate test scenarios or user stories based on requirements
    - [Edge Case Generator](edge-case-generator) – Automatically identify potential boundary and exception cases from requirements, and create tests targeting boundary conditions or uncommon scenarios
    - [Test Suite Prioritizer](test-suite-prioritizer) – Suggest which tests to run first based on impact

- **Failure Analysis**
    - [Regression Root Cause Analyzer](regression-root-cause-analyzer) – Locate root causes of failing regression tests
    - [Error Explanation Generator](error-explanation-generator) – Explain why tests fail and provide actionable guidance
    - [Runtime Error Explanation Generator](runtime-error-explainer) – Explains runtime errors and compilation failures with actionable debugging guidance

- **Test Documentation & Reporting**
    - [Test Case Documentation](test-case-documentation) – Summarize the documentation for test cases

- **Test Maintenance**
    - [Python Test Updater](python-test-updater) – Update Python tests to work with new code versions, fixing broken tests and updating assertions
    - [Java Test Updater](java-test-updater) – Update Java tests after code refactoring, handling signature changes, mocks, and assertions


### ✅ **Verification**
- **Specification & Annotation**
    - [Interface Specification Generator](interface-specification-generator) – Produce formal or structured interface specifications
    - [ACSL Annotation Assistant](acsl-annotation-assistant) – Create ACSL or other formal annotations for C/C++ programs
    - [Invariant Inference](invariant-inference) – Automatically infer loop or function invariants
    - [Specification Generator](specification-generator) – Generate formal specifications (pre/postconditions, invariants) from code or requirements

- **Formal Verification**
    - [Static Reasoning Verifier](static-reasoning-verifier) – Check code correctness statically against specifications
    - [Symbolic Execution Assistant](symbolic-execution-assistant) – Perform symbolic execution to detect potential errors

- **Counterexample Analysis**
    - [Counterexample Generator](counterexample-generator) – Produce counterexamples when verification fails
    - [Counterexample Explainer](counterexample-explainer) – Explain why a counterexample violates the specification


### 💻 **Deployment**
- **Deployment Preparation**
    - [Environment Setup Assistant](environment-setup-assistant) – Generate setup scripts or instructions for target environments
    - [Configuration Generator](configuration-generator) – Produce configuration files for applications, services, or infrastructure
    - [Dependency Resolver](dependency-resolver) – Identify and manage software dependencies before deployment
    - [Containerization Assistant](containerization-assistant) – Generate Dockerfiles or containerization scripts

- **Continuous Integration & Delivery (CI/CD)**
    - [CI Pipeline Synthesizer](ci-pipeline-synthesizer) – Create CI pipelines for automated building and testing
    - [CD Pipeline Generator](cd-pipeline-generator) – Produce scripts for automated deployment to staging or production

- **Deployment Verification & Testing**
    - [Rollback Strategy Advisor](rollback-strategy-advisor) – Suggest rollback strategies for failed deployments

- **Documentation & Reporting**
    - [Release Notes Writer](release-notes-writer) – Automatically generate user-facing release notes


### 🔧 **Maintenance**
- **Bug & Issue Handling**
    - [Bug Localization](bug-localization) – Identify the location of bugs in code or modules
    - [Regression Root Cause Analyzer](regression-root-cause-analyzer) – Find root causes of failing regression tests
    - [Runtime Error Explanation Generator](runtime-error-explainer) – Explains runtime errors and compilation failures with actionable debugging guidance
    - [Bug-to-Patch Generator](bug-to-patch-generator) – Generate code fixes from bug reports or failing test cases

- **Legacy & Technical Debt Management**
    - [Legacy Code Summarizer](legacy-code-summarizer) – Produce summaries and insights about legacy code bases
    - [Technical Debt Analyzer](technical-debt-analyzer) – Detect areas with high maintenance cost or poor design
    - [Deprecated API Updater](deprecated-api-updater) – Identify and replace deprecated APIs

- **Performance & Reliability Monitoring**
    - [Flaky Test Detector](flaky-test-detector) – Identify unstable or unreliable test cases

- **Documentation & Knowledge Transfer**
    - [api-documentation-generator](api-documentation-generator) - Summarize API documentation for the given repository
    - [Python Repository Quick Start](python-repo-quickstart) - Quickly analyze Python repositories to understand structure, dependencies, and setup requirements
    - [Markdown Document Structurer](markdown-document-structurer) - Reorganize markdown documents into well-structured, consistent format with improved readability
    - [Code Comment Generator](code-comment-generator) – Produce meaningful comments for maintenance readability
    - [Change Log Generator](change-log-generator) – Automatically generate change logs from commits or patches
    - [Code Change Summarizer](code-change-summarizer) – Generate structured PR descriptions from code changes with testing instructions and context

- **Continuous Improvement**
    - [Refactoring Assistant](code-refactoring-assistant) – Suggest ongoing code improvements to enhance maintainability
    - [Code Pattern Extractor](code-pattern-extractor) – Identify reusable code patterns for future development
    - [Code Search Assistant](code-search-assistant) – Search repositories for related code using multi-dimensional similarity analysis
    


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

Skills are automatically triggered based on user requests that match the skill's description. You can also explicitly invoke a skill:

> Using "requirement-summarizer" to summarize the requirement "path-to-a-doc.md"




## 🤝 Contributing

We welcome contributions from both:
- **Researchers** (new Skills, evaluation methods)
- **Practitioners** (real-world use cases, pipelines)

Please read [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

**Quick Contribution Steps**:
- Ensure your skill is based on a real use case
- Check for duplicates in existing skills
- Follow the skill structure template
- Test your skill across platforms
- Submit a pull request with clear documentation

## 🎯 Vision

Our long-term vision is to build:
> **A shared, open Skill layer for LLM-powered Software Engineering systems** 

- How to submit new skills
- Skill quality standards
- Pull request process
- Code of conduct

🎉 If you are building or studying LLMs for software engineering, this repo is for you.



## Reference

Special thanks for the following links for constructing and enhancing the skills in this repository:

- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/)
- [anthropics-skills](https://github.com/anthropics/skills/)
- [openclaw-skills](https://github.com/openclaw/skills/)