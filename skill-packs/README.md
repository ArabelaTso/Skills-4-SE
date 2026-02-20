# Skill Packs

Organized collections of related skills for common software engineering workflows.

## 📦 Available Skill Packs (8 Total)

### 🐛 [Bug Fixing Suite](bug-fixing-suite/)
**12 skills** for bug detection, localization, and automated repair

- Detect and localize bugs
- Generate patches automatically
- Analyze regression root causes
- Debug counterexamples

**Use cases:** Bug fixing, regression analysis, automated repair

[📖 Documentation](bug-fixing-suite/README.md) | [💾 Install](bug-fixing-suite/install.sh)

---

### ✨ [Code Quality Toolkit](code-quality-toolkit/)
**13 skills** for code quality, refactoring, and technical debt management

- Refactor and improve code
- Detect code smells
- Manage technical debt
- Generate documentation

**Use cases:** Code improvement, refactoring, code review, documentation

[📖 Documentation](code-quality-toolkit/README.md) | [💾 Install](code-quality-toolkit/install.sh)

---

### 🧪 [Test Automation Suite](test-automation-suite/)
**18 skills** for comprehensive test generation and optimization

- Generate unit and integration tests
- Mutation testing and optimization
- Test deduplication and prioritization
- Metamorphic testing

**Use cases:** Test generation, test quality improvement, regression testing

[📖 Documentation](test-automation-suite/README.md) | [💾 Install](test-automation-suite/install.sh)

---

### 📋 [Requirements Engineering Suite](requirements-engineering-suite/)
**12 skills** for requirements analysis, formalization, and traceability

- Improve requirements quality
- Generate formal specifications
- Maintain traceability
- Manage requirements evolution

**Use cases:** Requirements analysis, formal specification, traceability management

[📖 Documentation](requirements-engineering-suite/README.md) | [💾 Install](requirements-engineering-suite/install.sh)

---

### 🔄 [Code Understanding and Manipulation Suite](code-understanding-and-manipulation-suite/)
**19 skills** for code understanding, analysis, search, translation, and manipulation

- Understand and analyze legacy code
- Search for code patterns and similarities
- Translate between languages and frameworks
- Refactor and optimize code
- Verify behavior preservation

**Use cases:** Code understanding, code search, language migration, framework migration, code optimization

[📖 Documentation](code-understanding-and-manipulation-suite/README.md) | [💾 Install](code-understanding-and-manipulation-suite/install.sh)

---

### 🚀 [DevOps Automation Toolkit](devops-automation-toolkit/)
**10 skills** for CI/CD pipelines, containerization, and deployment

- Generate CI/CD pipelines
- Create container configurations
- Automate release management
- Scan for security vulnerabilities

**Use cases:** CI/CD setup, containerization, release automation, security scanning

[📖 Documentation](devops-automation-toolkit/README.md) | [💾 Install](devops-automation-toolkit/install.sh)

---

### 🔍 [Formal Verification Toolkit](formal-verification-toolkit/)
**17 skills** for formal verification of software systems

- Generate TLA+ specifications from code
- Verify temporal properties
- Automatically repair violations
- Convert counterexamples to tests

**Use cases:** Concurrent systems, distributed protocols, safety-critical systems

[📖 Documentation](formal-verification-toolkit/README.md) | [⚡ Quick Start](formal-verification-toolkit/demo/verification-workflow.md) | [💾 Install](formal-verification-toolkit/install.sh)

---

### 🔒 [Security Scanner Suite](security-scanner-suite/)
**13 skills** for comprehensive security analysis

- Detect vulnerabilities (injection, overflow, etc.)
- Analyze CVE impact in dependencies
- Generate security patches
- Track untrusted data flow

**Use cases:** Security audits, CVE management, automated patching

[📖 Documentation](security-scanner-suite/README.md) | [⚡ Quick Start](security-scanner-suite/demo/security-audit-workflow.md) | [💾 Install](security-scanner-suite/install.sh)

---

## 🚀 Quick Installation

### Install a Single Pack

```bash
cd formal-verification-toolkit
./install.sh
```

### Install Multiple Packs

```bash
# Install verification and security packs
./install-packs.sh formal-verification-toolkit security-scanner-suite
```

### Install All Packs

```bash
./install-all-packs.sh
```

## 📊 Comparison

| Feature | Bug Fixing | Code Quality | Test Automation | Requirements | Code Understanding | DevOps | Formal Verification | Security |
|---------|-----------|--------------|-----------------|--------------|-------------------|--------|-------------------|----------|
| Skills | 12 | 13 | 18 | 12 | 19 | 10 | 17 | 13 |
| Difficulty | Intermediate | Beginner | Beginner | Intermediate | Intermediate | Intermediate | Advanced | Intermediate |
| Time to Learn | 1-2 hours | 30-60 min | 30-60 min | 1-2 hours | 1-2 hours | 1-2 hours | 2-3 hours | 1-2 hours |
| Prerequisites | Debugging basics | None | Testing basics | None | Language knowledge | CI/CD basics | Temporal logic | Security basics |

## 🎯 Which Pack Should I Use?

### Choose **Bug Fixing Suite** if you need to:
- ✅ Detect and localize bugs
- ✅ Generate patches automatically
- ✅ Analyze regression root causes
- ✅ Debug counterexamples

### Choose **Code Quality Toolkit** if you need to:
- ✅ Refactor and improve code
- ✅ Detect code smells
- ✅ Manage technical debt
- ✅ Generate documentation

### Choose **Test Automation Suite** if you need to:
- ✅ Generate comprehensive test suites
- ✅ Improve test quality
- ✅ Optimize test execution
- ✅ Detect flaky tests

### Choose **Requirements Engineering Suite** if you need to:
- ✅ Improve requirements quality
- ✅ Generate formal specifications
- ✅ Maintain traceability
- ✅ Manage requirements evolution

### Choose **Code Understanding and Manipulation Suite** if you need to:
- ✅ Understand and analyze legacy code
- ✅ Search for code patterns and similarities
- ✅ Translate between languages and frameworks
- ✅ Refactor and optimize code
- ✅ Verify behavior preservation

### Choose **DevOps Automation Toolkit** if you need to:
- ✅ Generate CI/CD pipelines
- ✅ Create container configurations
- ✅ Automate release management
- ✅ Scan dependencies for CVEs

### Choose **Formal Verification Toolkit** if you need to:
- ✅ Verify concurrent or distributed systems
- ✅ Prove correctness properties
- ✅ Detect race conditions and deadlocks
- ✅ Generate formal specifications

### Choose **Security Scanner Suite** if you need to:
- ✅ Find security vulnerabilities
- ✅ Manage CVE dependencies
- ✅ Generate security patches
- ✅ Track data flow for security

## 💡 Combining Skill Packs

Skill packs can be used together for comprehensive analysis:

### Example 1: Complete Software Development Lifecycle
```
1. Use Requirements Engineering Suite to formalize requirements
2. Use Code Understanding and Manipulation Suite to implement from specifications
3. Use Test Automation Suite to generate comprehensive tests
4. Use Code Quality Toolkit to improve code quality
5. Use DevOps Automation Toolkit to set up CI/CD
```

### Example 2: Secure Concurrent System
```
1. Use Formal Verification Toolkit to verify concurrency correctness
2. Use Security Scanner Suite to detect security vulnerabilities
3. Use Test Automation Suite to generate comprehensive tests
4. Use Bug Fixing Suite to fix any detected issues
```

### Example 3: Legacy System Modernization
```
1. Use Code Understanding and Manipulation Suite to analyze and understand legacy code
2. Use Code Quality Toolkit to analyze technical debt
3. Use Code Understanding and Manipulation Suite to migrate to modern frameworks
4. Use Test Automation Suite to ensure behavior preservation
5. Use DevOps Automation Toolkit to modernize deployment
```

### Example 4: Production-Ready Feature Development
``` 
1. Use Requirements Engineering Suite to clarify requirements
2. Use Test Automation Suite to write tests first (TDD)
3. Use Code Quality Toolkit to maintain code quality
4. Use Bug Fixing Suite to fix issues
5. Use DevOps Automation Toolkit to deploy
```

## 📖 Documentation

- [Creating Custom Skill Packs](../docs/CREATING-SKILL-PACKS.md)
- [Skill Pack Development Guide](../docs/SKILL-PACK-DEV.md)
- [Contributing New Packs](../CONTRIBUTING.md)

## 🤝 Contributing

We welcome contributions of new skill packs! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Suggested Future Packs
- 🔧 Hardware Verification Toolkit (RTL verification, FPGA design)
- 📊 Data Analysis Toolkit (data processing, visualization, ML pipelines)
- 🌐 API Development Suite (API design, documentation, testing)
- 🎨 Frontend Development Kit (UI components, accessibility, performance)
- 📱 Mobile App Testing Suite (mobile-specific testing, device compatibility)
- ☁️ Cloud Infrastructure Toolkit (IaC, cloud deployment, monitoring)

## 📝 License

Same as the main Skills-4-SE repository.
