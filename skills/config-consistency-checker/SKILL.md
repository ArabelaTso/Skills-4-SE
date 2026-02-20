---
name: config-consistency-checker
description: Automatically analyzes configuration files to detect inconsistencies, conflicts, missing keys, and divergent values across environments, versions, or modules. Use when managing multi-environment configurations, detecting config drift, validating configuration changes, or ensuring consistency across microservices. Supports JSON, YAML, TOML, INI, XML, .env, and properties files. Identifies security issues like hardcoded secrets and provides actionable resolution guidance.
---

# Config Consistency Checker

Automatically detect inconsistencies, conflicts, and mismatches in configuration files across environments and modules.

## Workflow

### 1. Parse Configuration Files

Read and parse configuration files in various formats:
- JSON (.json)
- YAML (.yml, .yaml)
- TOML (.toml)
- INI (.ini)
- XML (.xml)
- Environment files (.env)
- Properties files (.properties)

### 2. Extract Structure

Build configuration structure:
- Key-value pairs
- Nested objects/sections
- Arrays/lists
- Data types

### 3. Compare Configurations

Compare across:
- **Environments**: dev vs staging vs production
- **Versions**: v1 vs v2
- **Modules**: service-a vs service-b
- **Templates**: actual vs expected

### 4. Detect Issues

Identify:
- Missing required keys
- Conflicting values
- Type mismatches
- Divergent settings
- Deprecated keys
- Security issues

### 5. Generate Report

Provide:
- Detailed inconsistency list
- Critical issues highlighted
- Resolution guidance
- Suggested fixes

## Quick Examples

### Example 1: Environment Mismatch

**dev.json:**
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "ssl": false
  }
}
```

**prod.json:**
```json
{
  "database": {
    "host": "prod-db.example.com",
    "port": 5432
  }
}
```

**Issues Detected:**
- Missing key: `prod.json` missing `database.ssl`
- **Critical**: SSL disabled in dev but undefined in prod

**Resolution:**
Add `"ssl": true` to prod.json

### Example 2: Type Mismatch

**config-a.yaml:**
```yaml
timeout: 30
```

**config-b.yaml:**
```yaml
timeout: "30"
```

**Issue:** Type mismatch (number vs string)

**Resolution:** Standardize to number: `timeout: 30`

### Example 3: Security Issue

**config.env:**
```
DATABASE_PASSWORD=secret123
API_KEY=hardcoded-key-here
```

**Issues:**
- Hardcoded password
- Hardcoded API key

**Resolution:** Use environment variables or secrets manager

## Detection Patterns

### Missing Keys

Compare key sets across configs:
```
Config A keys: {host, port, ssl}
Config B keys: {host, port}
Missing in B: {ssl}
```

### Conflicting Values

Same key, different values:
```
dev.timeout = 30
prod.timeout = 60
→ Divergent (may be intentional)
```

### Type Mismatches

Same key, different types:
```
config-a.port = 8080 (number)
config-b.port = "8080" (string)
→ Type inconsistency
```

### Security Issues

Detect patterns:
- `password`, `secret`, `key` with hardcoded values
- Weak settings: `ssl: false`, `debug: true` in production
- Exposed credentials

## Report Format

```
Configuration Consistency Report
================================

Files Analyzed:
- dev.json
- staging.json
- prod.json

Summary:
- Total Issues: 5
- Critical: 2
- Warnings: 3

Critical Issues:
1. Missing Key: prod.json missing 'database.ssl'
   Impact: SSL may be disabled in production
   Resolution: Add "ssl": true to prod.json

2. Security Issue: Hardcoded password in dev.json
   Impact: Credentials exposed in config file
   Resolution: Use environment variable ${DB_PASSWORD}

Warnings:
3. Type Mismatch: timeout is number in dev, string in staging
   Resolution: Standardize to number type

4. Divergent Value: max_connections differs (dev:10, prod:100)
   Note: May be intentional for different environments

5. Deprecated Key: 'legacy_mode' is deprecated
   Resolution: Remove or migrate to new setting
```

## Best Practices

- **Environment-specific values**: Document intentional differences
- **Type consistency**: Use same types across environments
- **Required keys**: Define and validate required configuration
- **Security**: Never hardcode secrets
- **Validation**: Use schemas to enforce structure
- **Documentation**: Comment why values differ

## Common Scenarios

### Multi-Environment Setup

Compare dev, staging, prod configs to ensure consistency while allowing intentional differences.

### Microservices

Validate that shared configuration keys are consistent across services.

### Configuration Migration

Detect missing or changed keys when upgrading configuration versions.

### Security Audit

Scan for hardcoded secrets and insecure settings.

## Tips

- Start with critical keys (database, security settings)
- Document intentional differences
- Use configuration schemas for validation
- Automate checks in CI/CD pipeline
- Review security issues immediately
