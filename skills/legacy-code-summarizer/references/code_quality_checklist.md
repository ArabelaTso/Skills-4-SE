# Code Quality Checklist

Comprehensive checklist for assessing code quality and identifying technical debt in legacy codebases.

## Quick Assessment

Run these commands first for a rapid overview:

```bash
# Lines of code
find . -name "*.py" | xargs wc -l | tail -1
find . -name "*.java" | xargs wc -l | tail -1

# File count
find . -name "*.py" | wc -l
find . -name "*.java" | wc -l

# Largest files (potential god objects)
find . -name "*.py" -exec wc -l {} \; | sort -rn | head -10
find . -name "*.java" -exec wc -l {} \; | sort -rn | head -10

# TODO/FIXME count
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.java" | wc -l

# Test file count
find . -name "test_*.py" -o -name "*_test.py" -o -name "*Test.java" | wc -l
```

---

## Code Structure Quality

### File Size

**Thresholds:**
- ✓ Good: < 300 lines
- ⚠ Warning: 300-500 lines
- ❌ Problem: > 500 lines
- 🚨 Critical: > 1000 lines

**Check:**
```bash
# Find large files
find . -name "*.py" -exec wc -l {} \; | awk '$1 > 500 {print $2 " - " $1 " lines"}' | sort -t- -k2 -rn
```

**Issues:**
- Violates Single Responsibility Principle
- Difficult to understand and maintain
- Usually indicates god object or god class

**Fix:** Refactor into smaller, focused modules

### Function/Method Length

**Thresholds:**
- ✓ Good: < 20 lines
- ⚠ Warning: 20-50 lines
- ❌ Problem: > 50 lines

**Manual Check:**
- Scan for long blocks between `def`...`def` (Python)
- Scan for long blocks between `{` and `}` (Java)

**Tools:**
```bash
# Python - use radon
pip install radon
radon cc src/ -a -nb  # Cyclomatic complexity

# Java - use PMD
# Shows methods exceeding length threshold
```

**Issues:**
- Hard to understand
- Difficult to test
- Often does multiple things

**Fix:** Extract smaller functions with clear names

### Class Size

**Thresholds:**
- ✓ Good: < 200 lines
- ⚠ Warning: 200-400 lines
- ❌ Problem: > 400 lines

**Check:**
```bash
# Find large classes (Python)
grep -n "^class " --include="*.py" -r . | while read line; do
    file=$(echo $line | cut -d: -f1)
    linenum=$(echo $line | cut -d: -f2)
    # Count lines until next class or end of file
done

# Find large classes (Java)
find . -name "*.java" -exec wc -l {} \; | awk '$1 > 400' | sort -rn
```

---

## Code Complexity

### Cyclomatic Complexity

**Thresholds:**
- ✓ Good: 1-10
- ⚠ Warning: 11-20
- ❌ Problem: 21-50
- 🚨 Critical: > 50

**Tools:**

**Python:**
```bash
pip install radon
radon cc src/ -a -nb

# Show only complex functions
radon cc src/ -nc -a
```

**Java:**
```bash
# Use PMD
pmd cpd --minimum-tokens 100 --files src/

# Or Checkstyle
checkstyle -c /google_checks.xml src/
```

**Issues:**
- Too many conditional branches
- Hard to test (need many test cases)
- Likely contains bugs

**Fix:**
- Extract complex conditions to functions
- Use early returns
- Simplify boolean logic

### Nesting Depth

**Thresholds:**
- ✓ Good: ≤ 3 levels
- ⚠ Warning: 4 levels
- ❌ Problem: ≥ 5 levels

**Manual Check:**
Look for deeply nested `if`, `for`, `while` statements

**Issues:**
- Arrow anti-pattern
- Hard to follow logic
- Error-prone

**Fix:**
- Use early returns/continues
- Extract nested logic to functions
- Flatten with guard clauses

---

## Code Duplication

### Finding Duplicates

**Python:**
```bash
# Use pylint
pip install pylint
pylint --disable=all --enable=duplicate-code src/

# Or use PMD Copy/Paste Detector
pmd cpd --minimum-tokens 50 --files src/ --language python
```

**Java:**
```bash
# PMD Copy/Paste Detector
pmd cpd --minimum-tokens 100 --files src/

# Shows duplicate code blocks
```

**Thresholds:**
- ✓ Good: < 3% duplication
- ⚠ Warning: 3-10% duplication
- ❌ Problem: > 10% duplication

**Issues:**
- Bug fixes need multiple updates
- Inconsistent behavior
- Wasted effort

**Fix:**
- Extract to shared function/module
- Use inheritance or composition
- Create utility libraries

---

## Code Smells

### God Object/Class

**Signs:**
- Class > 400 lines
- Many methods (> 20)
- Many fields (> 10)
- Does everything

**Detection:**
```bash
# Count methods per class
grep -A 100 "^class" file.py | grep "def " | wc -l
```

**Fix:** Split into multiple focused classes

### Feature Envy

**Signs:**
- Method uses another object's data more than its own
- Lots of getters from other objects

**Example:**
```python
# BAD - feature envy
class Order:
    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.product.price * item.quantity  # Using product's data
        return total

# BETTER - move to Product
class Item:
    def get_subtotal(self):
        return self.product.price * self.quantity

class Order:
    def calculate_total(self):
        return sum(item.get_subtotal() for item in self.items)
```

### Dead Code

**Find unused code:**

**Python:**
```bash
# Find unused imports
pip install autoflake
autoflake --check --remove-all-unused-imports src/

# Find unused functions (requires vulture)
pip install vulture
vulture src/
```

**Java:**
```bash
# Use UCDetector (Eclipse plugin) or
# PMD with unused code rules
```

**Fix:** Delete unused code (if confirmed)

### Magic Numbers

**Example:**
```python
# BAD
if temperature > 273.15:
    status = "liquid"

# GOOD
WATER_FREEZING_POINT_KELVIN = 273.15
if temperature > WATER_FREEZING_POINT_KELVIN:
    status = "liquid"
```

**Detection:**
```bash
# Find hardcoded numbers (crude)
grep -rn "[0-9]\{3,\}" --include="*.py" src/
```

---

## Documentation Quality

### Missing Docstrings

**Python:**
```bash
# Find functions without docstrings
grep -A 1 "^def " --include="*.py" -r src/ | grep -v '"""' | grep -v "'''" | wc -l

# Or use pydocstyle
pip install pydocstyle
pydocstyle src/
```

**Java:**
```bash
# Find classes without Javadoc
grep -B 1 "^public class" --include="*.java" -r src/ | grep -v "/\*\*" | wc -l
```

**Threshold:**
- ✓ Good: > 80% documented
- ⚠ Warning: 50-80% documented
- ❌ Problem: < 50% documented

### Comment Quality

**Good Comments:**
- Explain WHY, not WHAT
- Document complex algorithms
- Note non-obvious decisions

**Bad Comments:**
- Obvious statements
- Commented-out code
- Outdated information

**Check for commented code:**
```bash
# Find commented code blocks
grep -rn "^#.*=\|^#.*def\|^#.*if" --include="*.py" src/
grep -rn "^//.*=\|^//.*public" --include="*.java" src/
```

---

## Naming Conventions

### Consistency Check

**Python:**
```bash
# Check for inconsistent naming
# PEP 8: snake_case for functions/variables
grep -rn "def [A-Z]" --include="*.py" src/  # camelCase functions (wrong)

# PEP 8: PascalCase for classes
grep -rn "class [a-z]" --include="*.py" src/  # lowercase classes (wrong)
```

**Java:**
```bash
# Check for inconsistent naming
# Should be camelCase for methods
grep -rn "public.*_" --include="*.java" src/  # snake_case methods (wrong)
```

### Naming Quality

**Bad Names:**
- Single letters (except loop counters)
- Abbreviations
- Generic names (data, info, manager)

**Detection:**
```bash
# Find short variable names
grep -rn " [a-z] =" --include="*.py" src/

# Find generic names
grep -rn "data\|info\|manager\|handler\|util" --include="*.py" src/
```

---

## Error Handling

### Missing Error Handling

**Python:**
```bash
# Find functions without try/except
# (crude - checks if file has any try blocks)
for file in $(find src/ -name "*.py"); do
    if ! grep -q "try:" $file; then
        echo "$file - no error handling"
    fi
done
```

**Java:**
```bash
# Find methods that throw checked exceptions but don't handle them
grep -rn "throws.*Exception" --include="*.java" src/
```

### Empty Catch Blocks

**Detection:**
```python
# BAD - swallowing exceptions
try:
    risky_operation()
except Exception:
    pass  # Silent failure!

# GOOD
try:
    risky_operation()
except SpecificException as e:
    logger.error(f"Failed: {e}")
    raise
```

```bash
# Find empty except blocks (Python)
grep -A 1 "except.*:" --include="*.py" -r src/ | grep "pass"

# Find empty catch blocks (Java)
grep -A 2 "catch.*{" --include="*.java" -r src/ | grep "^$"
```

---

## Security Issues

### Hardcoded Credentials

```bash
# Find potential credentials
grep -rni "password\|secret\|api_key" --include="*.py" --include="*.java" src/ | \
  grep -v "input\|env\|config"
```

### SQL Injection

**Detection:**
```bash
# Find string concatenation in SQL (dangerous)
grep -rn "SELECT.*+\|INSERT.*+" --include="*.py" --include="*.java" src/
```

**Example:**
```python
# BAD - SQL injection risk
query = "SELECT * FROM users WHERE username = '" + username + "'"

# GOOD - parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

---

## Testing Quality

### Test Coverage

**Python:**
```bash
pip install pytest pytest-cov
pytest --cov=src --cov-report=term-missing

# Target: > 70% coverage for critical modules
```

**Java:**
```bash
mvn test jacoco:report
# View target/site/jacoco/index.html
```

### Test-to-Code Ratio

**Calculate:**
```bash
SRC_LINES=$(find src/ -name "*.py" | xargs wc -l | tail -1 | awk '{print $1}')
TEST_LINES=$(find tests/ -name "*.py" | xargs wc -l | tail -1 | awk '{print $1}')
echo "Test-to-code ratio: $(echo "scale=2; $TEST_LINES / $SRC_LINES" | bc)"
```

**Threshold:**
- ✓ Good: > 1.0 (more test code than source)
- ⚠ Warning: 0.5-1.0
- ❌ Problem: < 0.5

---

## Dependencies

### Outdated Dependencies

**Python:**
```bash
pip list --outdated

# Or use pip-audit for security
pip install pip-audit
pip-audit
```

**Java:**
```bash
# Maven
mvn versions:display-dependency-updates

# Check for security vulnerabilities
mvn dependency-check:check
```

**Node.js:**
```bash
npm outdated
npm audit
```

### Dependency Count

**Thresholds:**
- ✓ Good: < 20 direct dependencies
- ⚠ Warning: 20-50 dependencies
- ❌ Problem: > 50 dependencies

**Check:**
```bash
# Python
cat requirements.txt | wc -l

# Java
grep "<dependency>" pom.xml | wc -l

# Node.js
cat package.json | grep -A 100 "dependencies" | grep ":" | wc -l
```

---

## Performance

### N+1 Query Problem

**Detection (requires runtime analysis):**
```bash
# Enable SQL logging and look for repeated queries
# Python/Django: Check django.db.backends log
# Java/Hibernate: Enable SQL logging
```

**Example:**
```python
# BAD - N+1 queries
users = User.objects.all()  # 1 query
for user in users:
    posts = user.posts.all()  # N queries!

# GOOD - single query with join
users = User.objects.prefetch_related('posts').all()
```

### Inefficient Algorithms

Look for:
- Nested loops (O(n²))
- Linear search in loops (should use dict/set)
- Repeated calculations

**Detection:**
```bash
# Find nested loops
grep -A 5 "for.*:" --include="*.py" src/ | grep "for.*:"
```

---

## Code Quality Tools

### Python

```bash
# Linting
pip install pylint flake8 black

pylint src/
flake8 src/
black --check src/

# Type checking
pip install mypy
mypy src/

# Security
pip install bandit
bandit -r src/

# Complexity
pip install radon
radon cc src/ -a -nb
radon mi src/  # Maintainability index
```

### Java

```bash
# Static analysis
# PMD, Checkstyle, SpotBugs

# Code coverage
mvn test jacoco:report

# Dependency analysis
mvn dependency:analyze
```

### JavaScript

```bash
# Linting
npx eslint src/

# Type checking (TypeScript)
npx tsc --noEmit

# Dependencies
npm audit
```

---

## Quality Score

Create a composite quality score:

```python
def calculate_quality_score(metrics):
    """Calculate overall quality score (0-100)."""
    score = 100

    # Deduct for issues
    score -= metrics['files_over_500_lines'] * 5
    score -= metrics['functions_over_50_lines'] * 2
    score -= metrics['duplicate_code_percent'] * 10
    score -= metrics['missing_tests'] * 3
    score -= metrics['complexity_violations'] * 2

    # Deduct for low coverage
    if metrics['test_coverage'] < 70:
        score -= (70 - metrics['test_coverage'])

    return max(0, score)
```

**Interpretation:**
- 90-100: Excellent
- 70-89: Good
- 50-69: Fair (needs improvement)
- < 50: Poor (requires refactoring)

---

## Checklist Summary

- [ ] File sizes reasonable (< 500 lines)
- [ ] Function/method lengths reasonable (< 50 lines)
- [ ] Cyclomatic complexity low (< 10)
- [ ] Nesting depth reasonable (≤ 3 levels)
- [ ] Code duplication minimal (< 3%)
- [ ] No god objects/classes
- [ ] No dead code
- [ ] Magic numbers eliminated
- [ ] Functions documented (> 80%)
- [ ] Naming conventions consistent
- [ ] Error handling present
- [ ] No hardcoded credentials
- [ ] No SQL injection risks
- [ ] Test coverage adequate (> 70%)
- [ ] Dependencies up to date
- [ ] No known security vulnerabilities
