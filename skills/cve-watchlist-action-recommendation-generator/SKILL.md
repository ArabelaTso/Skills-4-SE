---
name: cve-watchlist-action-recommendation-generator
description: Generate prioritized CVE watchlists and actionable security recommendations for repositories. Use when analyzing CVE scan results, creating security reports, prioritizing vulnerability remediation, or generating security gate reports for CI/CD. Takes CVE scan results (JSON/SARIF from npm audit, pip-audit, Snyk), reachability analysis, and cutoff date as input. Combines severity, reachability, exploitability, and dependency criticality to rank CVEs by practical risk. Outputs markdown reports with concrete next-step guidance (immediate upgrade, monitor, ignore with justification, apply mitigation) suitable for issue trackers, security reviews, and CI security gates.
---

# CVE Watchlist & Action Recommendation Generator

Generate prioritized CVE watchlists with actionable security recommendations for development and security teams.

## Workflow

### 1. Gather Input Data

Collect required inputs:

**Required:**
- Repository name/path
- CVE scan results (JSON/SARIF format from npm audit, pip-audit, Snyk, etc.)
- Cutoff date (YYYY-MM-DD) for filtering new CVEs

**Optional but recommended:**
- Reachability analysis results (which vulnerable code paths are actually used)
- Exploit intelligence data (CISA KEV, ExploitDB)
- Dependency criticality ratings (how critical each dependency is)

**Parse scan results:**
```bash
python scripts/parse_scan_results.py scan_results.json auto 2024-01-01 > parsed_cves.json
```

### 2. Calculate Risk Scores

Combine multiple risk factors to prioritize CVEs:

```bash
python scripts/calculate_risk_score.py parsed_cves.json reachability.json exploits.json criticality.json > scored_cves.json
```

**Risk scoring formula:**
```
Risk Score = (Severity × 0.35) + (Reachability × 0.30) + (Exploitability × 0.20) + (Dependency Criticality × 0.15)
```

See [risk_scoring.md](references/risk_scoring.md) for detailed methodology.

### 3. Generate Recommendations

For each CVE, determine appropriate action based on risk score and context:

**Decision tree:**
- Risk ≥ 80 (Critical) → Immediate upgrade (24-48h)
- Risk 60-79 (High) → Upgrade within days (3-5 days)
- Risk 40-59 (Medium) → Next maintenance cycle (2-4 weeks)
- Risk 20-39 (Low) → Monitor or defer
- Risk < 20 (Minimal) → Ignore with justification

See [action_guidelines.md](references/action_guidelines.md) for complete decision tree and recommendation templates.

### 4. Generate Report

Create markdown-formatted report using template:

**Report structure:**
1. Executive Summary (CVE counts by risk tier)
2. Prioritized CVE Watchlist (grouped by risk tier)
3. For each CVE:
   - Risk score and breakdown
   - Affected package and versions
   - Reachability status
   - Exploit availability
   - Concrete action recommendation
   - Upgrade commands
   - Mitigation options (if applicable)
4. Summary of Actions (immediate, short-term, medium-term)
5. Dependency Overview
6. Next Steps

Use template from [assets/report_template.md](assets/report_template.md).

## Input Formats

### CVE Scan Results

**npm audit (JSON):**
```json
{
  "vulnerabilities": {
    "package-name": {
      "via": [{
        "cve": ["CVE-2024-1234"],
        "severity": "high",
        "title": "SQL Injection",
        "url": "https://..."
      }],
      "fixAvailable": {"version": "2.0.0"}
    }
  }
}
```

**pip-audit (JSON):**
```json
{
  "dependencies": [{
    "name": "package-name",
    "version": "1.0.0",
    "vulns": [{
      "id": "CVE-2024-1234",
      "fix_versions": ["2.0.0"],
      "description": "..."
    }]
  }]
}
```

**Snyk (JSON):**
```json
{
  "vulnerabilities": [{
    "id": "SNYK-...",
    "identifiers": {"CVE": ["CVE-2024-1234"]},
    "packageName": "package-name",
    "severity": "high",
    "cvssScore": 7.5
  }]
}
```

### Reachability Analysis

```json
{
  "package-name": {
    "status": "direct_call",
    "details": "Called from src/auth.js:42"
  },
  "other-package": {
    "status": "not_reachable",
    "details": "Dev dependency only"
  }
}
```

**Status values:** `direct_call`, `indirect_call`, `imported_unused`, `not_reachable`, `unknown`

### Exploit Intelligence

```json
{
  "CVE-2024-1234": {
    "actively_exploited": true,
    "public_exploit": true,
    "poc_available": true,
    "source": "CISA KEV"
  }
}
```

### Dependency Criticality

```json
{
  "package-name": {
    "level": "critical",
    "reason": "Handles authentication and authorization"
  },
  "dev-tool": {
    "level": "minimal",
    "reason": "Development-only linting tool"
  }
}
```

**Levels:** `critical`, `high`, `medium`, `low`, `minimal`

## Example Output

```markdown
# CVE Security Report

**Repository**: my-app
**Cutoff Date**: 2024-01-01
**New CVEs**: 5

| Risk Tier | Count | Action Required |
|-----------|-------|-----------------|
| 🔴 Critical | 1 | Immediate (24-48h) |
| 🟠 High | 2 | Within days (3-5d) |
| 🟡 Medium | 1 | Next cycle (2-4w) |
| 🟢 Low | 1 | Monitor |

---

### 🔴 Critical Risk

#### CVE-2024-1234: SQL Injection in database-driver

**Risk Score**: 96 / 100 (Critical)

**Affected Package**: database-driver@1.2.3

**Severity**: Critical (CVSS 9.8)

**Reachability**: Direct call from src/db/query.js:42

**Exploitability**: Public exploit available (ExploitDB)

**Action**: Immediate upgrade required

**Steps**:
1. Upgrade database-driver from 1.2.3 to 2.0.0
2. Run full test suite
3. Deploy with rollback plan

**Command**:
```bash
npm install database-driver@2.0.0
```

**Risk if not addressed**: Attackers can execute arbitrary SQL queries, leading to data breach
```

## Tips

- **Always include reachability data** when available - it significantly improves prioritization accuracy
- **Check for breaking changes** in fix versions before recommending immediate upgrades
- **Document assumptions** when data is missing (e.g., "Assuming moderate risk due to unknown reachability")
- **Provide specific commands** for each package manager (npm, pip, maven, etc.)
- **Include mitigation options** for high-risk CVEs when upgrades are blocked
- **Link to CVE details** and security advisories for further investigation
- **Group multiple CVEs** in the same package when a single upgrade fixes all

## Resources

### scripts/
- `parse_scan_results.py` - Parse CVE scan results from npm audit, pip-audit, Snyk, SARIF
- `calculate_risk_score.py` - Calculate composite risk scores from multiple factors

### references/
- `risk_scoring.md` - Risk scoring methodology and factor calculations
- `action_guidelines.md` - Decision tree for generating recommendations

### assets/
- `report_template.md` - Markdown report template structure
