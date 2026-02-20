# Security Scanner Suite

## 📋 Overview

The Security Scanner Suite is a comprehensive collection of skills for security analysis, vulnerability detection, and automated patching. It helps you identify security issues, analyze their exploitability, and generate fixes.

## 🎯 What's Included

This suite includes **13 skills** covering the complete security analysis workflow:

### Vulnerability Detection
- **static-vulnerability-detector** - Detect security vulnerabilities through static analysis
- **vulnerability-pattern-matcher** - Match code against known vulnerability patterns
- **semantic-bug-detector** - Detect semantic-level security bugs

### Vulnerability Analysis
- **vulnerability-root-cause-analyzer** - Identify root causes of vulnerabilities
- **exploitability-analyzer** - Assess realistic exploitability of vulnerabilities
- **static-bug-detector** - Detect functional bugs that may lead to security issues

### CVE Management
- **cve-reachability-analyzer** - Analyze if CVEs in dependencies are reachable
- **cve-watchlist-action-recommendation-generator** - Generate actionable CVE recommendations
- **time-aware-dependency-cve-scanner** - Scan dependencies with temporal awareness

### Security Patching
- **security-patch-advisor** - Generate secure remediation strategies
- **security-sensitive-path-instrumenter** - Instrument security-critical code paths
- **taint-instrumentation-assistant** - Track untrusted data flow
- **critical-interval-security-checker** - Identify timing vulnerabilities

## 🚀 Quick Start

### Installation

```bash
# Install the entire suite
./install.sh

# Or install to custom location
./install.sh --path ~/.claude/skills
```

### Basic Usage

1. **Scan for vulnerabilities:**
   ```
   Use skill: static-vulnerability-detector
   Input: Your codebase
   Output: List of detected vulnerabilities
   ```

2. **Analyze CVE impact:**
   ```
   Use skill: cve-reachability-analyzer
   Input: Dependency list + CVE database
   Output: Reachable CVEs with priority
   ```

3. **Generate security patches:**
   ```
   Use skill: security-patch-advisor
   Input: Vulnerability report
   Output: Secure fix recommendations
   ```

## 📖 Complete Workflow

See [Security Audit Workflow](demo/security-audit-workflow.md) for a step-by-step guide.

```
┌─────────────┐
│  Codebase   │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│ Scan for Vulnerabilities │ ← static-vulnerability-detector
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Match Known Patterns     │ ← vulnerability-pattern-matcher
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Analyze Root Causes      │ ← vulnerability-root-cause-analyzer
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Assess Exploitability    │ ← exploitability-analyzer
└──────┬───────────────────┘
       │
       ├─── Low risk → Monitor
       │
       └─── High risk
              │
              ▼
       ┌──────────────────────────┐
       │ Generate Patch           │ ← security-patch-advisor
       └──────┬───────────────────┘
              │
              ▼
       ┌──────────────────────────┐
       │ Verify Fix               │
       └──────────────────────────┘
```

## 💡 Use Cases

### 1. Security Audit
Comprehensive security analysis of your codebase to identify vulnerabilities.

**Example:** [SQL Injection Detection](examples/sql-injection-detection)

### 2. CVE Dependency Analysis
Analyze third-party dependencies for known CVEs and assess their impact.

**Example:** [CVE Dependency Analysis](examples/cve-dependency-analysis)

### 3. Automated Security Patching
Generate and apply security patches automatically.

**Example:** [Buffer Overflow Fix](examples/buffer-overflow-fix)

## 📊 Vulnerability Categories Covered

| Category | Detection | Analysis | Patching |
|----------|-----------|----------|----------|
| Injection (SQL, XSS, Command) | ✅ | ✅ | ✅ |
| Buffer Overflow | ✅ | ✅ | ✅ |
| Authentication Issues | ✅ | ✅ | ✅ |
| Cryptographic Failures | ✅ | ✅ | ✅ |
| Insecure Deserialization | ✅ | ✅ | ✅ |
| Race Conditions | ✅ | ✅ | ✅ |
| Resource Leaks | ✅ | ✅ | ✅ |
| CVE Vulnerabilities | ✅ | ✅ | ⚠️ |

## 🔧 Requirements

- Claude Code or compatible LLM system
- (Optional) Static analysis tools (e.g., Bandit, Semgrep)
- (Optional) CVE database access
- (Optional) Dependency scanning tools

## 📖 Documentation

- [Security Audit Workflow](demo/security-audit-workflow.md)
- [Vulnerability Patterns](../../skills/vulnerability-pattern-matcher/references/vulnerability_patterns.md)
- [CVE Analysis Guide](../../skills/cve-reachability-analyzer/references/cve_analysis.md)

## 🤝 Related Skill Packs

- **Formal Verification Toolkit** - For formal security proofs
- **Test Automation Suite** - For security testing
- **Code Quality Toolkit** - For general code quality

## ⚠️ Important Notes

- **False Positives:** Static analysis may produce false positives. Always verify findings.
- **Manual Review:** Automated patches should be reviewed before deployment.
- **Compliance:** Ensure security practices comply with your organization's policies.
- **Responsible Disclosure:** Follow responsible disclosure practices for vulnerabilities.

## 📝 License

Same as the main Skills-4-SE repository.

## 🙋 Support

For issues or questions:
- Open an issue in the main repository
- Check the [Security FAQ](../../docs/SECURITY-FAQ.md)
- Join our community discussions
