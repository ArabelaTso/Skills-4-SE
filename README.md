# Useful Software Engineering (SE) Skills

**A curated, lifecycle-aware Skill library for applying LLMs to real software engineering tasks — from requirements to maintenance.**

---

## 🧠 What is this repository?

This repository is a **collection of reusable, task-oriented Skills** designed to support **software engineering activities across the entire development lifecycle**, including:

> requirements understanding, system design, implementation, testing, verification, deployment, and maintenance.

Unlike prompt collections or ad-hoc demos, each Skill in this repository is:
- **Task-grounded** (solves a concrete software engineering problem)
- **Reusable** (clearly specified inputs and outputs)
- **Composable** (can be chained into larger workflows or pipelines)
- **Tool- and artifact-aware** (operates on real code, tests, specs, configs, logs)

This repo is intended to serve as a **shared skill layer** for:
- LLM-based assistants (e.g., Claude Skills, agents)
- Tool-augmented software engineering workflows
- Research prototypes and empirical studies
- Industrial automation and developer productivity tools

---

## ✨ Why Skills (not just prompts)?

Modern LLMs are powerful, but **raw prompting is fragile**:
- Hard to reproduce
- Hard to evaluate
- Hard to integrate into real workflows

We treat **Skills as first-class engineering artifacts**.

A Skill in this repo is more than a prompt:
- It encodes **procedural knowledge**
- It specifies **expected inputs / outputs**
- It documents **failure modes**
- It can be **evaluated, composed, and reused**

> 🤗 Think of this repo as a *standard library of software engineering capabilities* for LLM-powered systems.


---
## 🔁 SE Lifecycle-Oriented Skills

Skills are primarily organized by **Software Engineering phases**:

- 📕 **Requirements**
    - **Requirement Analysis**
        - [Ambiguity Detector](ambiguity-detector) – Automatically detect ambiguous or vague statements in requirements
        - [Requirement Summarizer](requirement-summarizer) – Extract core features, constraints, and priorities from requirement documents, output markdown files.
        - [Requirement Conflict Analyzer](conflict-analyzer) – Detect conflicts or contradictions among requirements

    - **Traceability & Coverage**
        - [Requirement to Test](req-to-test) – Automatically generate test cases from requirements
        - [Requirement to Contraints](nl-to-constraints) -- Transforms natural language requirements into into formal specifications and constraints (structured, testable specifications with explicit constraints).
        - [Traceability Matrix Generator](traceability-matrix-generator) – Build a traceability matrix connecting requirements → design → implementation → tests
        - [Requirement Coverage Checker](requirement-coverage-checker) – Check whether existing design/code covers all requirements

    - **Documentation & Communication**
        - [Requirement Doc Formatter]() – Generate clear, standardized requirement documents
        - [Requirement Summary]() – Generate a brief summary for quick team understanding

- 💡 **Software Design**
    - **Architecture & High-Level Design**
        - [Architecture Recovery]() – Extract high-level architecture from existing systems or requirements
        - [System Diagram Generator]() – Create visual representations of system structure
        - [Design Pattern Suggestor](design-pattern-suggestor) – Recommend suitable design patterns for a given requirement

    - **Interface & API Design**
        - [API Design Assistant](api-design-assistant) – Suggest API endpoints, parameters, and return types

    - **Design Quality & Analysis**
        - [Design Smell Detector](design-smell-detector) – Identify potential issues like high coupling or low cohesion
        - [Complexity Analyzer]() – Measure and analyze design complexity
        - [Impact Analysis Assistant]() – Evaluate the effect of design changes on the system
        - [Trade-off Evaluator]() – Compare alternative designs and suggest trade-offs

    - **Design Documentation**
        - [Design Doc Formatter]() – Standardize and document design decisions
        - [Design Summary Reporter]() – Summarize design rationale for stakeholders
        - [Design Review Assistant]() – Assist in reviewing and critiquing design artifacts


- ⌨️ **Code Implementation**
    - **Spec-to-Code**
        - [Function/Class Generator](function-class-generator) – Generate functions or classes from formal specifications or design descriptions
        - [Module/Component Generator]() – Build larger components or modules based on interface contracts
        - [Template/Skeleton-based Code Generator](template-code-generator) – Produce boilerplate code or project templates/skeleton automatically

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

- 👩🏽‍💻 **Testing and Validation**
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
        - [Requirement Coverage Checker for Test]() – Check whether existing tests covers all requirements

    - **Failure Analysis**
        - [Regression Root Cause Analyzer](regression-root-cause-analyzer) – Locate root causes of failing regression tests
        - [Error Explanation Generator](error-explanation-generator) – Explain why tests fail and provide actionable guidance
        - [Runtime Error Explanation Generator](runtime-error-explainer) – Explains runtime errors and compilation failures with actionable debugging guidance

    - **Test Documentation & Reporting**
        - [Test Case Documentation](test-case-documentation) – Summarize the documentation for test cases


- ✅ **Formal Verification**
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


- 💻 **Software Deployment**
    - **Deployment Preparation**
        - [Environment Setup Assistant](environment-setup-assistant) – Generate setup scripts or instructions for target environments
        - [Configuration Generator](configuration-generator) – Produce configuration files for applications, services, or infrastructure
        - [Dependency Resolver](dependency-resolver) – Identify and manage software dependencies before deployment
        - [Containerization Assistant](containerization-assistant) – Generate Dockerfiles or containerization scripts

    - **Continuous Integration & Delivery (CI/CD)**
        - [CI Pipeline Synthesizer]() – Create CI pipelines for automated building and testing
        - [CD Pipeline Generator]() – Produce scripts for automated deployment to staging or production

    - **Deployment Verification & Testing**
        - [Integration Validation Assistant]() – Ensure deployed components integrate correctly
        - [Rollback Strategy Advisor](rollback-strategy-advisor) – Suggest rollback strategies for failed deployments

    - **Monitoring & Maintenance**
        - [Deployment Metrics Analyzer]() – Collect and analyze deployment metrics (uptime, performance, errors)
        - [Failure Pattern Reporter]() – Identify common deployment failures and suggest preventive measures

    - **Documentation & Reporting**
        - [Release Notes Writer](release-notes-writer) – Automatically generate user-facing release notes
        - [Environment Documentation Formatter]() – Standardize documentation for deployment environments


- 🔧 **Software Maintenance**
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
        - [Performance Analyzer]() – Detect performance bottlenecks in code
        - [Resource Usage Optimizer]() – Suggest improvements for memory, CPU, or storage usage
        - [Reliability Assessor]() – Evaluate system reliability and stability issues
        - [Flaky Test Detector]() – Identify unstable or unreliable test cases

    - **Documentation & Knowledge Transfer**
        - [api-documentation-generator](api-documentation-generator) - Summarize API documentation for the given repository
        - [Code Comment Generator](code-comment-generator) – Produce meaningful comments for maintenance readability
        - [Change Log Generator](change-log-generator) – Automatically generate change logs from commits or patches
        - [Maintenance Report Creator]() – Summarize ongoing maintenance tasks and system health

    - **Continuous Improvement**
        - [Refactoring Assistant](code-refactoring-assistant) – Suggest ongoing code improvements to enhance maintainability
        - [Code Pattern Extractor]() – Identify reusable code patterns for future development
        


---

## 🧱 Skill Format

Each Skill follows a **standardized structure**:

```
skill-name/
├── SKILL.md          # Required: Skill instructions and metadata
├── scripts/          # Optional: Helper scripts
├── templates/        # Optional: Document templates
└── resources/        # Optional: Reference files
```

## Basic Skill Template

```
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

Detailed description of the skill's purpose and capabilities.

## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3

## Instructions

[Detailed instructions for Claude on how to execute this skill]

## Examples

[Real-world examples showing the skill in action]
```

---

## 🔗 Pipelines: Skills in Action

Beyond individual Skills, the repo includes **pipelines** that demonstrate how multiple Skills can be composed into end-to-end workflows, such as:

- **Spec → Verified Code**
- **Bug Report → Reproducing Test → Patch**
- **Failing Test → Root Cause → Fix**
- **Legacy Code → Clean Architecture Plan**

Pipelines reflect **real developer workflows**, not toy examples.

---

## 📊 Evaluation & Research Use

This repository is designed with **evaluation in mind**.

We provide:
- Guidelines for Skill-level evaluation
- Case studies on real-world projects
- Hooks for benchmarking LLM-based software engineering systems

The goal is to support **rigorous, reproducible research**, not just demos.

---

## 🛠️ Tooling & Platforms

Skills are designed to be **platform-agnostic**, but we include adapters and examples for:
- Claude (Skills)
- ChatGPT / GPT-style assistants
- Generic LLM agent frameworks

See the `tools/` directory for details.

---

## 🤝 Contributing

We welcome contributions from both:
- **Researchers** (new Skills, evaluation methods)
- **Practitioners** (real-world use cases, pipelines)

Please read `CONTRIBUTING.md` before submitting a pull request.

---

## 🎯 Vision

Our long-term vision is to build:
> **A shared, open Skill layer for LLM-powered software engineering systems** 

one that is:
- Lifecycle-aware
- Evaluation-driven
- Grounded in real engineering tasks

If you are building or studying LLMs for software engineering, this repo is for you.
