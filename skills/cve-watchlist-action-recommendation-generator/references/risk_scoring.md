# Risk Scoring Methodology

## Risk Score Calculation

Combine multiple factors to calculate a composite risk score (0-100):

```
Risk Score = (Severity × 0.35) + (Reachability × 0.30) + (Exploitability × 0.20) + (Dependency Criticality × 0.15)
```

### Factor 1: Severity Score (0-100)

Based on CVSS score or severity rating:

| CVSS Score | Severity | Score |
|------------|----------|-------|
| 9.0-10.0   | Critical | 100   |
| 7.0-8.9    | High     | 75    |
| 4.0-6.9    | Medium   | 50    |
| 0.1-3.9    | Low      | 25    |
| 0.0        | None     | 0     |

**Adjustments:**
- If CVE has known exploit: +10 points
- If CVE is trending/actively exploited: +15 points

### Factor 2: Reachability Score (0-100)

Based on whether vulnerable code is actually used:

| Reachability Status | Score | Description |
|---------------------|-------|-------------|
| Direct call         | 100   | Vulnerable function is directly called in application code |
| Indirect call       | 75    | Vulnerable function is called through dependency chain |
| Imported but unused | 25    | Vulnerable code is imported but not executed |
| Not reachable       | 0     | Vulnerable code path is never executed |
| Unknown             | 50    | Reachability analysis not available (assume moderate risk) |

**Detection methods:**
- Static analysis (call graph analysis)
- Dynamic analysis (runtime tracing)
- Dependency tree analysis

### Factor 3: Exploitability Score (0-100)

Based on exploit availability and complexity:

| Exploit Status | Score | Description |
|----------------|-------|-------------|
| Active exploitation in wild | 100 | CVE is being actively exploited |
| Public exploit available | 80 | Exploit code is publicly available (Metasploit, ExploitDB) |
| Proof of concept exists | 60 | PoC code exists but not weaponized |
| Theoretical | 30 | No known exploit, but theoretically exploitable |
| Not exploitable | 0 | Requires physical access or impractical conditions |

**Data sources:**
- CISA KEV (Known Exploited Vulnerabilities)
- Exploit databases (ExploitDB, Metasploit)
- Threat intelligence feeds
- CVE references and advisories

### Factor 4: Dependency Criticality Score (0-100)

Based on how critical the affected dependency is:

| Criticality Level | Score | Description |
|-------------------|-------|-------------|
| Core/Critical     | 100   | Authentication, authorization, data validation, crypto |
| High              | 75    | Database drivers, API frameworks, payment processing |
| Medium            | 50    | Logging, monitoring, utilities |
| Low               | 25    | Development tools, testing frameworks |
| Minimal           | 10    | Documentation generators, linters (dev-only) |

**Indicators of criticality:**
- Handles sensitive data (passwords, PII, financial)
- Exposed to untrusted input (user input, network data)
- Core business logic dependency
- Security-critical functionality
- Production vs development dependency

## Risk Tiers

Based on final risk score:

| Risk Tier | Score Range | Priority | Typical Action |
|-----------|-------------|----------|----------------|
| Critical  | 80-100      | P0       | Immediate action required |
| High      | 60-79       | P1       | Address within days |
| Medium    | 40-59       | P2       | Address within weeks |
| Low       | 20-39       | P3       | Address in next cycle |
| Minimal   | 0-19        | P4       | Monitor or ignore |

## Example Calculations

### Example 1: Critical Risk CVE

```
CVE-2024-1234: SQL Injection in database driver
- Severity: Critical (CVSS 9.8) → 100 points
- Reachability: Direct call → 100 points
- Exploitability: Public exploit available → 80 points
- Dependency Criticality: Core (database driver) → 100 points

Risk Score = (100 × 0.35) + (100 × 0.30) + (80 × 0.20) + (100 × 0.15)
           = 35 + 30 + 16 + 15
           = 96 (Critical Risk)
```

**Recommendation**: Immediate upgrade required

### Example 2: Low Risk CVE

```
CVE-2024-5678: XSS in development-only documentation tool
- Severity: Medium (CVSS 5.4) → 50 points
- Reachability: Not reachable (dev dependency) → 0 points
- Exploitability: Theoretical → 30 points
- Dependency Criticality: Minimal (dev tool) → 10 points

Risk Score = (50 × 0.35) + (0 × 0.30) + (30 × 0.20) + (10 × 0.15)
           = 17.5 + 0 + 6 + 1.5
           = 25 (Low Risk)
```

**Recommendation**: Ignore with justification (dev-only, not reachable)

### Example 3: Medium Risk CVE

```
CVE-2024-9012: Denial of Service in logging library
- Severity: High (CVSS 7.5) → 75 points
- Reachability: Indirect call → 75 points
- Exploitability: Proof of concept exists → 60 points
- Dependency Criticality: Medium (logging) → 50 points

Risk Score = (75 × 0.35) + (75 × 0.30) + (60 × 0.20) + (50 × 0.15)
           = 26.25 + 22.5 + 12 + 7.5
           = 68.25 (High Risk)
```

**Recommendation**: Upgrade within days, or apply rate limiting mitigation

## Special Considerations

### Zero-Day CVEs
- Treat as Critical (score ≥ 80) if reachable
- Immediate action even if no exploit available yet

### Transitive Dependencies
- Score based on actual usage, not just presence
- Consider upgrade path complexity

### False Positives
- Reduce score by 20-30 points if confirmed false positive
- Document justification in report

### Compensating Controls
- Reduce score by 10-20 points if effective mitigations exist
- Examples: WAF rules, network segmentation, input validation
