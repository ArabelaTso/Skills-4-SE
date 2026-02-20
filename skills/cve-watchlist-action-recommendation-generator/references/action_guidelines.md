# Action Guidelines

## Decision Tree for CVE Recommendations

Use this decision tree to determine the appropriate action for each CVE.

```
START
  │
  ├─ Risk Score ≥ 80 (Critical)?
  │   └─ YES → IMMEDIATE UPGRADE
  │
  ├─ Risk Score 60-79 (High)?
  │   ├─ Fix available?
  │   │   ├─ YES → UPGRADE WITHIN DAYS
  │   │   └─ NO → APPLY MITIGATION + MONITOR
  │   │
  │   └─ Breaking changes in fix?
  │       ├─ YES → EVALUATE MITIGATION OPTIONS
  │       └─ NO → UPGRADE WITHIN DAYS
  │
  ├─ Risk Score 40-59 (Medium)?
  │   ├─ Reachable?
  │   │   ├─ YES → UPGRADE IN NEXT CYCLE
  │   │   └─ NO → MONITOR
  │   │
  │   └─ Exploit available?
  │       ├─ YES → UPGRADE WITHIN WEEKS
  │       └─ NO → MONITOR
  │
  ├─ Risk Score 20-39 (Low)?
  │   └─ MONITOR OR DEFER
  │
  └─ Risk Score < 20 (Minimal)?
      └─ IGNORE WITH JUSTIFICATION
```

## Action Types

### 1. Immediate Upgrade (P0)

**When to use:**
- Risk score ≥ 80
- Critical severity + reachable + exploit available
- Active exploitation in the wild
- Zero-day with high impact

**Recommendation template:**
```markdown
**Action**: Immediate upgrade required

**Urgency**: Critical - Address within 24-48 hours

**Steps**:
1. Upgrade `<package>` from `<current_version>` to `<fixed_version>`
2. Run full test suite to verify compatibility
3. Deploy to production with rollback plan ready
4. Monitor for any issues post-deployment

**Command**:
```bash
# npm
npm install <package>@<fixed_version>

# pip
pip install <package>==<fixed_version>

# maven
# Update pom.xml: <version><fixed_version></version>
```

**Risk if not addressed**: <specific impact description>
```

### 2. Upgrade Within Days (P1)

**When to use:**
- Risk score 60-79
- High severity + reachable
- Public exploit available but not actively exploited
- Core dependency affected

**Recommendation template:**
```markdown
**Action**: Upgrade within 3-5 days

**Urgency**: High - Schedule upgrade in current sprint

**Steps**:
1. Review changelog for breaking changes
2. Upgrade `<package>` from `<current_version>` to `<fixed_version>`
3. Update dependent code if needed
4. Test thoroughly before deployment

**Breaking changes**: <list any breaking changes>

**Command**:
```bash
<upgrade command>
```

**Alternative**: If upgrade blocked, apply mitigation (see below)
```

### 3. Upgrade in Next Cycle (P2)

**When to use:**
- Risk score 40-59
- Medium severity + reachable
- No immediate exploit threat
- Non-critical dependency

**Recommendation template:**
```markdown
**Action**: Upgrade in next maintenance cycle

**Urgency**: Medium - Include in next release (2-4 weeks)

**Steps**:
1. Add to backlog for next sprint/release
2. Upgrade `<package>` from `<current_version>` to `<fixed_version>`
3. Test as part of regular QA process

**Command**:
```bash
<upgrade command>
```

**Monitoring**: Track for exploit developments
```

### 4. Monitor but Defer (P3)

**When to use:**
- Risk score 20-39
- Low severity or not reachable
- Theoretical vulnerability
- Development-only dependency

**Recommendation template:**
```markdown
**Action**: Monitor but defer upgrade

**Urgency**: Low - Address when convenient

**Rationale**: <why deferring is acceptable>
- Not reachable in production code
- Low severity with no known exploits
- Development-only dependency

**Monitoring plan**:
- Check monthly for exploit developments
- Re-evaluate if exploit becomes available
- Upgrade during next major version bump

**Command** (when ready):
```bash
<upgrade command>
```
```

### 5. Ignore with Justification (P4)

**When to use:**
- Risk score < 20
- Not reachable (confirmed)
- False positive
- Requires impractical attack conditions
- Effective compensating controls in place

**Recommendation template:**
```markdown
**Action**: Ignore (with justification)

**Rationale**: <specific reason>
- Vulnerable code path is not reachable
- Requires physical access / impractical conditions
- False positive (confirmed by security team)
- Effective mitigations already in place

**Compensating controls** (if applicable):
- <list existing mitigations>

**Documentation**: Add to security exceptions log
```

### 6. Apply Mitigation or Workaround (Alternative to Upgrade)

**When to use:**
- Upgrade blocked (breaking changes, compatibility issues)
- No fix available yet
- Temporary measure while planning upgrade

**Recommendation template:**
```markdown
**Action**: Apply mitigation (temporary)

**Urgency**: <based on risk score>

**Mitigation options**:

1. **Configuration change**:
   ```
   <specific config changes>
   ```

2. **Code-level workaround**:
   ```
   <code changes to avoid vulnerable path>
   ```

3. **Network-level protection**:
   - Add WAF rule: <rule details>
   - Restrict access: <access control changes>

4. **Input validation**:
   ```
   <validation code>
   ```

**Effectiveness**: <how well this mitigates the risk>

**Long-term plan**: Upgrade to `<fixed_version>` when feasible
```

## Special Cases

### Case 1: No Fix Available

```markdown
**Action**: Apply mitigation + Monitor for fix

**Status**: No fix available yet

**Mitigation**:
<temporary mitigation steps>

**Monitoring**:
- Check weekly for security updates
- Subscribe to security advisories
- Consider alternative packages if fix delayed

**Escalation**: If no fix within 30 days, evaluate alternatives
```

### Case 2: Breaking Changes in Fix

```markdown
**Action**: Evaluate upgrade path

**Issue**: Fix version contains breaking changes

**Options**:
1. **Accept breaking changes**: Upgrade and refactor code
   - Estimated effort: <hours/days>
   - Risk: <refactoring risks>

2. **Apply mitigation**: Keep current version with workaround
   - Mitigation: <specific mitigation>
   - Risk: <residual risk>

3. **Partial upgrade**: Upgrade to intermediate version
   - Version: <intermediate_version>
   - Trade-offs: <what's gained/lost>

**Recommendation**: <preferred option with rationale>
```

### Case 3: Transitive Dependency

```markdown
**Action**: Upgrade parent dependency

**Issue**: CVE in transitive dependency `<package>`

**Root cause**: Pulled in by `<parent_package>@<version>`

**Solution**:
1. Upgrade `<parent_package>` to `<fixed_version>` (includes fixed transitive dep)
2. Or: Add explicit dependency override
   ```bash
   # npm
   npm install <package>@<fixed_version>

   # pip requirements.txt
   <package>==<fixed_version>  # override transitive
   ```

**Verification**:
```bash
# Check resolved version
npm ls <package>
pip show <package>
```
```

### Case 4: Multiple CVEs in Same Package

```markdown
**Action**: Single upgrade addresses multiple CVEs

**CVEs addressed**: CVE-XXXX-YYYY, CVE-XXXX-ZZZZ, ...

**Upgrade**: `<package>` from `<current>` to `<fixed>`

**Combined risk score**: <highest individual score>

**Priority**: <based on highest risk CVE>

**Note**: Single upgrade resolves all listed CVEs
```

## Recommendation Priority Matrix

| Risk Score | Reachable | Exploit Available | Recommended Action | Timeline |
|------------|-----------|-------------------|-------------------|----------|
| 80-100     | Yes       | Yes               | Immediate upgrade | 24-48h   |
| 80-100     | Yes       | No                | Immediate upgrade | 24-48h   |
| 80-100     | No        | Yes               | Upgrade within days | 3-5 days |
| 60-79      | Yes       | Yes               | Upgrade within days | 3-5 days |
| 60-79      | Yes       | No                | Upgrade within days | 3-5 days |
| 60-79      | No        | Any               | Monitor or defer | 2-4 weeks |
| 40-59      | Yes       | Any               | Next cycle | 2-4 weeks |
| 40-59      | No        | Any               | Monitor | As convenient |
| 20-39      | Any       | Any               | Monitor or defer | As convenient |
| 0-19       | Any       | Any               | Ignore with justification | N/A |

## Validation Checklist

Before finalizing recommendation:

- [ ] Risk score calculated correctly
- [ ] Reachability confirmed (not assumed)
- [ ] Fix version verified to address CVE
- [ ] Breaking changes documented
- [ ] Upgrade command tested (if possible)
- [ ] Mitigation effectiveness validated
- [ ] Timeline realistic for team capacity
- [ ] Justification clear and documented
