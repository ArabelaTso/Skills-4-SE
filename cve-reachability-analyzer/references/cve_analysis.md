# CVE Analysis Guide

## Understanding CVE Information

### Key CVE Fields
- **CVE ID**: Unique identifier (e.g., CVE-2024-12345)
- **Description**: What the vulnerability is
- **Affected versions**: Which versions are vulnerable
- **Fixed versions**: Which versions contain the fix
- **CVSS score**: Severity rating (0-10)
- **CWE**: Weakness type (e.g., CWE-79: XSS, CWE-89: SQL Injection)
- **Attack vector**: Network, Adjacent, Local, Physical
- **Attack complexity**: Low or High
- **Privileges required**: None, Low, High
- **User interaction**: None or Required

### Extracting Vulnerable Components

From CVE description, identify:
1. **Vulnerable package/library**: Exact name and version range
2. **Vulnerable function/class/method**: Specific code entry point
3. **Vulnerability type**: What kind of flaw (injection, overflow, etc.)
4. **Trigger conditions**: What inputs or states trigger the vulnerability

### Example CVE Analysis

**CVE-2024-12345: SQL Injection in MyLib**
```
Description: SQL injection vulnerability in MyLib versions < 2.5.0
in the `query()` function when processing user input.

Affected: MyLib < 2.5.0
Fixed: MyLib >= 2.5.0
CWE: CWE-89 (SQL Injection)
```

**Extracted Information**:
- Package: `MyLib`
- Vulnerable versions: `< 2.5.0`
- Vulnerable component: `query()` function
- Vulnerability type: SQL Injection
- Trigger: User input passed to `query()`

## Reachability Assessment Framework

### Step 1: Dependency Presence
**Question**: Is the vulnerable package present in the project?

- Check dependency files (package.json, requirements.txt, pom.xml, etc.)
- Verify version matches vulnerable range
- Check transitive dependencies

**If NO**: CVE is not applicable → **Not Reachable**
**If YES**: Proceed to Step 2

### Step 2: Import Analysis
**Question**: Is the vulnerable component imported/referenced?

- Search for imports of vulnerable package
- Check if specific vulnerable function/class is imported
- Look for wildcard imports that may include vulnerable component

**If NO**: Likely unreachable (but check dynamic loading)
**If YES**: Proceed to Step 3

### Step 3: Direct Usage
**Question**: Is the vulnerable component directly called?

- Search for call sites of vulnerable function/method
- Check for instantiation of vulnerable classes
- Verify the vulnerable code path is executed

**If NO**: Proceed to Step 4 (indirect usage)
**If YES**: Proceed to Step 5 (data flow)

### Step 4: Indirect Usage
**Question**: Is the vulnerable component used indirectly?

Check for:
- Transitive calls through wrapper functions
- Framework auto-invocation (DI, middleware, event handlers)
- Reflection or dynamic invocation
- Callback registration
- Configuration-based activation

**If NO**: Likely unreachable
**If YES**: Proceed to Step 5

### Step 5: Data Flow Analysis
**Question**: What data reaches the vulnerable component?

Trace data sources:
- **User input**: HTTP requests, file uploads, CLI arguments
- **External data**: Database, APIs, file system
- **Internal data**: Constants, configuration, computed values

**Risk levels**:
- User-controlled data → High risk (exploitable)
- External untrusted data → Medium risk
- Internal trusted data → Lower risk (but still reachable)

### Step 6: Configuration Gates
**Question**: Is the vulnerable code path gated by configuration?

Check for:
- Feature flags
- Environment variables
- Build profiles (dev/prod)
- Conditional compilation
- Runtime configuration

**Assessment**:
- Always enabled → Likely reachable
- Enabled in production → Likely reachable
- Disabled in production → Possibly reachable (if config changes)
- Dev/test only → Likely unreachable in production

### Step 7: Code Path Reachability
**Question**: Is the code path actually executed?

Check for:
- Dead code (commented out, unreachable branches)
- Test-only code
- Deprecated/unused functions
- Error handling paths (rarely executed)

**Assessment**:
- Main code path → Likely reachable
- Error handling → Possibly reachable
- Test code → Unreachable in production
- Dead code → Unreachable

## Classification Criteria

### Likely Reachable
All of the following must be true:
- Vulnerable package is a direct dependency
- Vulnerable component is explicitly imported
- Vulnerable function/class is directly called
- Code path is in production code (not tests)
- No configuration gates, or gates are enabled in production

**Confidence**: High

### Possibly Reachable
One or more of the following:
- Vulnerable component used indirectly (transitive calls)
- Dynamic invocation (reflection, eval, dynamic imports)
- Configuration-gated (unclear if enabled in production)
- Framework auto-invocation (DI, middleware)
- Transitive dependency (not direct)

**Confidence**: Medium

### Likely Unreachable
One or more of the following:
- Vulnerable package imported but vulnerable component not used
- Code path is in test files only
- Code path is dead/unreachable
- Configuration gate is disabled in production
- Vulnerable component is in a different module not imported

**Confidence**: High

## Special Cases

### Transitive Dependencies
```
Your Project → LibA → LibB (vulnerable)
```

**Analysis**:
1. Check if LibA uses the vulnerable part of LibB
2. Check if your project uses the part of LibA that uses LibB
3. Reachability depends on both links in the chain

**Classification**: Usually "Possibly Reachable" (requires deeper analysis)

### Framework Auto-Invocation
```java
@Autowired
private VulnerableService service;  // Framework injects and may call
```

**Analysis**:
1. Check if vulnerable component is registered with framework
2. Check if framework auto-invokes vulnerable methods
3. Check lifecycle hooks (init, destroy, etc.)

**Classification**: Usually "Likely Reachable" if registered

### Dynamic Loading
```python
module = importlib.import_module(config.get('module_name'))
```

**Analysis**:
1. Check configuration values
2. Check if vulnerable module is in possible values
3. Assess likelihood based on configuration

**Classification**: Usually "Possibly Reachable" (uncertain)

### Reflection/Metaprogramming
```java
Method method = clazz.getMethod(methodName);
method.invoke(obj, args);
```

**Analysis**:
1. Try to determine possible values of `methodName`
2. Check if vulnerable method is in the set
3. Assess based on how constrained the values are

**Classification**: Usually "Possibly Reachable" (uncertain)

## Evidence Collection

### Strong Evidence (High Confidence)
- Direct import statement with line number
- Direct function call with line number
- Call chain from entry point to vulnerable code
- Configuration showing feature is enabled

### Moderate Evidence (Medium Confidence)
- Indirect usage through wrapper
- Framework registration
- Configuration file exists but unclear if used
- Dynamic invocation with limited possible values

### Weak Evidence (Low Confidence)
- Package is present but no usage found
- Wildcard import but no specific usage
- Dynamic invocation with many possible values
- Unclear configuration

## Uncertainty Factors

### When to Mark as "Uncertain"
- Dynamic code execution (eval, reflection)
- Configuration-dependent behavior (unclear config state)
- Complex framework magic (auto-wiring, AOP)
- Incomplete codebase (missing files, obfuscated code)
- Transitive dependencies (multiple hops)

### How to Express Uncertainty
- State what is known vs. unknown
- List assumptions made
- Suggest additional investigation steps
- Provide confidence level (High/Medium/Low)

### Example Uncertainty Statement
```
Classification: Possibly Reachable
Confidence: Medium

The vulnerable function is imported and called through a wrapper.
However, the wrapper is only invoked when feature flag 'enable_feature_x'
is true. The production configuration file was not found in the repository,
so it's unclear if this flag is enabled in production.

Recommendation: Check production configuration to determine if
'enable_feature_x' is enabled.
```

## Common Pitfalls

### Pitfall 1: Assuming Presence = Reachability
Just because a package is in dependencies doesn't mean vulnerable code is reached.

### Pitfall 2: Ignoring Configuration
Code may be present but gated by configuration that's disabled in production.

### Pitfall 3: Missing Transitive Calls
Vulnerable code may be reached through multiple layers of indirection.

### Pitfall 4: Overlooking Framework Magic
Frameworks may auto-invoke code through DI, annotations, or conventions.

### Pitfall 5: Confusing Reachability with Exploitability
Reachable code may not be exploitable if inputs are sanitized or constrained.

### Pitfall 6: Test Code False Positives
Usage in test files doesn't mean production reachability.

### Pitfall 7: Dead Code False Positives
Commented out or unreachable code shouldn't count as reachable.
