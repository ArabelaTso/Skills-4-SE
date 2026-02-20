---
name: time-aware-dependency-cve-scanner
description: "Scan repositories for newly disclosed CVEs in dependencies after a specific cutoff date. Takes a repository path, cutoff date (YYYY-MM-DD), and optional parameters for transitive dependencies. Parses dependency manifests (package.json, pom.xml, requirements.txt, go.mod, Cargo.toml) and lockfiles to extract exact versions. Queries vulnerability databases (OSV.dev, NVD, GitHub Advisory) to identify CVEs disclosed strictly after the cutoff date. Distinguishes between newly disclosed CVEs and previously known CVEs. Use when: (1) Performing security audits to find new vulnerabilities since last review, (2) Checking if new CVEs affect a historical codebase version, (3) Generating compliance reports showing vulnerability status at specific dates, (4) Tracking security posture changes over time. Supports npm, Maven, pip, Go modules, Cargo, and other major ecosystems."
---

# Time-Aware Dependency CVE Scanner

Scan repositories for newly disclosed CVEs affecting dependencies after a specific cutoff date. This skill helps track when vulnerabilities were introduced and distinguish between pre-existing and newly disclosed security issues.

## Quick Start

**Basic scan**:
```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01
```

**Scan only direct dependencies**:
```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01 --no-transitive
```

**Output as JSON**:
```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01 --json > report.json
```

## Workflow

### 1. Parse Dependencies

The scanner automatically detects and parses dependency manifests:

**Supported ecosystems**:
- **npm**: package.json, package-lock.json, yarn.lock
- **Maven**: pom.xml
- **Python**: requirements.txt, Pipfile.lock, poetry.lock
- **Go**: go.mod, go.sum
- **Cargo**: Cargo.toml, Cargo.lock

**Manual parsing** (if needed):
```bash
python scripts/parse_dependencies.py /path/to/repo
```

This extracts:
- Package names and exact versions
- Direct vs transitive dependency classification
- Ecosystem identification

**For detailed manifest formats**, see [references/dependency_formats.md](references/dependency_formats.md)

### 2. Query Vulnerability Databases

The scanner queries multiple databases to find CVEs:

**Primary source**: OSV.dev (Open Source Vulnerabilities)
- No authentication required
- Broad ecosystem coverage (npm, PyPI, Maven, Go, crates.io, etc.)
- Built-in version matching
- Real-time updates

**Additional sources**:
- **NVD** (National Vulnerability Database) - Official CVE records
- **GitHub Security Advisory** - GitHub-curated vulnerabilities

**Manual CVE query** (for testing):
```bash
python scripts/query_cves.py lodash 4.17.20 npm 2023-01-01
```

**For database details and API usage**, see [references/vulnerability_databases.md](references/vulnerability_databases.md)

### 3. Filter by Cutoff Date

The scanner filters CVEs to include only those **disclosed after** the cutoff date:

- Uses the `published` date from vulnerability databases
- Excludes CVEs disclosed before or on the cutoff date
- Distinguishes newly disclosed vulnerabilities from pre-existing ones

**Example**:
- Cutoff date: 2023-01-01
- CVE-2023-12345 published: 2023-06-15 → **Included** ✓
- CVE-2022-98765 published: 2022-11-20 → **Excluded** ✗

### 4. Generate Report

The scanner produces a comprehensive report with:

**Summary statistics**:
- Total dependencies (direct vs transitive)
- Number of new CVEs found
- CVEs affecting direct vs transitive dependencies
- Severity breakdown (CRITICAL, HIGH, MEDIUM, LOW)

**Detailed CVE list**:
For each CVE:
- CVE identifier (CVE-XXXX-XXXXX or GHSA-XXXX-XXXX-XXXX)
- Affected package and ecosystem
- Version range affected
- Severity score
- Disclosure date
- Summary description

**Clear status**: If no new CVEs found, explicitly reports "dependency set is clear since the given date"

## Use Cases

### Security Audit

**Scenario**: Periodic security review to find vulnerabilities disclosed since last audit

```bash
# Last audit was on 2023-06-01, check for new CVEs since then
python scripts/scan_repository.py /path/to/repo 2023-06-01
```

**Output**: List of all CVEs disclosed after June 1, 2023 that affect your dependencies

### Regression Testing

**Scenario**: Check if new CVEs affect a specific historical codebase version

```bash
# Check if any CVEs disclosed after 2023-01-01 affect code from that date
git checkout <commit-from-2023-01-01>
python scripts/scan_repository.py . 2023-01-01
```

**Output**: Shows which vulnerabilities were discovered after the code was written

### Compliance Reporting

**Scenario**: Generate reports showing vulnerability status at specific dates

```bash
# Generate quarterly reports
python scripts/scan_repository.py /path/to/repo 2023-01-01 --json > q1_report.json
python scripts/scan_repository.py /path/to/repo 2023-04-01 --json > q2_report.json
python scripts/scan_repository.py /path/to/repo 2023-07-01 --json > q3_report.json
```

**Output**: Time-series data showing when vulnerabilities were disclosed

### Tracking Security Posture

**Scenario**: Monitor how security posture changes over time

```bash
# Compare vulnerability counts at different dates
python scripts/scan_repository.py /path/to/repo 2022-01-01 | grep "new CVE"
python scripts/scan_repository.py /path/to/repo 2023-01-01 | grep "new CVE"
python scripts/scan_repository.py /path/to/repo 2024-01-01 | grep "new CVE"
```

**Output**: Trend analysis of vulnerability accumulation

## Advanced Options

### Limit Scan Scope

For large repositories, limit the number of dependencies scanned:

```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01 --max-deps 50
```

### Direct Dependencies Only

Skip transitive dependencies to focus on direct dependencies:

```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01 --no-transitive
```

### JSON Output for Automation

Output structured JSON for integration with other tools:

```bash
python scripts/scan_repository.py /path/to/repo 2023-01-01 --json | jq '.summary'
```

## Understanding Results

### Report Structure

```
TIME-AWARE DEPENDENCY CVE SCAN REPORT
======================================================================
Repository: /path/to/repo
Cutoff Date: 2023-01-01
Scan Time: 2024-02-19T10:30:00

DEPENDENCY SUMMARY
----------------------------------------------------------------------
  Total Dependencies: 150
    - Direct: 25
    - Transitive: 125

CVE SUMMARY
----------------------------------------------------------------------
  ⚠ 5 new CVE(s) found after 2023-01-01
    - Affecting direct dependencies: 2
    - Affecting transitive dependencies: 3

  Severity Breakdown:
    - CRITICAL: 1
    - HIGH: 2
    - MEDIUM: 2

DETAILED CVE LIST
----------------------------------------------------------------------

CVE-2023-12345 [CRITICAL]
  Package: lodash (npm)
  Disclosed: 2023-06-15
  Affected Versions: >=4.0.0, <4.17.21
  Summary: Prototype pollution vulnerability...
```

### Interpreting Severity

- **CRITICAL**: Immediate action required, actively exploited
- **HIGH**: Serious vulnerability, patch soon
- **MEDIUM**: Moderate risk, plan remediation
- **LOW**: Minor issue, low priority
- **UNKNOWN**: Severity not yet assessed

### Next Steps After Scan

1. **Review CVEs**: Examine each vulnerability's details
2. **Check exploitability**: Determine if your code uses affected functionality
3. **Update dependencies**: Upgrade to patched versions
4. **Re-scan**: Verify fixes with another scan
5. **Document**: Record findings and remediation actions

## Troubleshooting

### No dependencies found

- Ensure you're in the repository root
- Check that manifest files exist (package.json, pom.xml, etc.)
- Verify file permissions

### API rate limits

- OSV.dev has generous limits, but add delays if hitting limits
- For NVD, get an API key: https://nvd.nist.gov/developers/request-an-api-key
- For GitHub Advisory, set GITHUB_TOKEN environment variable

### Parsing errors

- Ensure manifest files are valid JSON/XML/TOML
- Check for syntax errors in dependency declarations
- Some ecosystems may require additional tools (e.g., `tomli` for Python TOML files)

## Dependencies

The scanner scripts require:
- Python 3.7+
- `requests` library: `pip install requests`
- Optional: `tomli` for TOML parsing: `pip install tomli`
