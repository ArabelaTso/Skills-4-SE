# Mutation Testing Tool Integration

## Overview

This guide provides detailed instructions for parsing and analyzing mutation testing results from various tools across different programming languages.

## Java - PIT (Pitest)

### Running PIT

**Maven:**
```bash
mvn org.pitest:pitest-maven:mutationCoverage
```

**Gradle:**
```bash
./gradlew pitest
```

### Configuration

**Maven (pom.xml):**
```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <configuration>
        <targetClasses>
            <param>com.example.*</param>
        </targetClasses>
        <targetTests>
            <param>com.example.*</param>
        </targetTests>
        <outputFormats>
            <outputFormat>XML</outputFormat>
            <outputFormat>HTML</outputFormat>
        </outputFormats>
    </configuration>
</plugin>
```

### Parsing PIT Reports

**XML Report Location:**
```
target/pit-reports/YYYYMMDDHHMI/mutations.xml
```

**XML Structure:**
```xml
<mutations>
    <mutation detected="false" status="SURVIVED">
        <sourceFile>Calculator.java</sourceFile>
        <mutatedClass>com.example.Calculator</mutatedClass>
        <mutatedMethod>add</mutatedMethod>
        <methodDescription>(II)I</methodDescription>
        <lineNumber>15</lineNumber>
        <mutator>org.pitest.mutationtest.engine.gregor.mutators.MathMutator</mutator>
        <index>0</index>
        <killingTest/>
        <description>replaced integer addition with subtraction</description>
    </mutation>
</mutations>
```

**Key Fields:**
- `detected`: true/false (killed/survived)
- `status`: KILLED, SURVIVED, NO_COVERAGE, TIMED_OUT, NON_VIABLE_MUTATION
- `sourceFile`: Source file name
- `lineNumber`: Line where mutation occurred
- `mutator`: Mutation operator used
- `description`: Human-readable mutation description
- `killingTest`: Test that killed the mutant (empty if survived)

**Parsing Example (Python):**
```python
import xml.etree.ElementTree as ET

def parse_pit_report(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    surviving_mutants = []

    for mutation in root.findall('mutation'):
        if mutation.get('status') == 'SURVIVED':
            mutant = {
                'id': mutation.get('index'),
                'file': mutation.find('sourceFile').text,
                'line': int(mutation.find('lineNumber').text),
                'method': mutation.find('mutatedMethod').text,
                'mutator': mutation.find('mutator').text.split('.')[-1],
                'description': mutation.find('description').text,
                'class': mutation.find('mutatedClass').text
            }
            surviving_mutants.append(mutant)

    return surviving_mutants
```

### PIT Mutation Operators

**Default Mutators:**
- `CONDITIONALS_BOUNDARY`: `<` ↔ `<=`, `>` ↔ `>=`
- `INCREMENTS`: `++` ↔ `--`
- `INVERT_NEGS`: Invert negations
- `MATH`: `+` → `-`, `*` → `/`, etc.
- `NEGATE_CONDITIONALS`: `==` → `!=`, `<` → `>=`, etc.
- `RETURN_VALS`: Mutate return values
- `VOID_METHOD_CALLS`: Remove void method calls

## JavaScript/TypeScript - Stryker

### Running Stryker

```bash
npx stryker run
```

### Configuration

**stryker.conf.json:**
```json
{
  "mutator": "javascript",
  "packageManager": "npm",
  "reporters": ["html", "json", "clear-text", "progress"],
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.js",
    "!src/**/*.spec.js"
  ]
}
```

### Parsing Stryker Reports

**JSON Report Location:**
```
reports/mutation/mutation.json
```

**JSON Structure:**
```json
{
  "files": {
    "src/calculator.js": {
      "language": "javascript",
      "mutants": [
        {
          "id": "0",
          "mutatorName": "ArithmeticOperator",
          "replacement": "-",
          "location": {
            "start": { "line": 5, "column": 12 },
            "end": { "line": 5, "column": 13 }
          },
          "status": "Survived",
          "statusReason": null,
          "coveredBy": ["test1", "test2"],
          "killedBy": []
        }
      ],
      "source": "..."
    }
  }
}
```

**Key Fields:**
- `status`: Killed, Survived, NoCoverage, Timeout, RuntimeError
- `mutatorName`: Mutation operator
- `replacement`: Mutated code
- `location`: Line and column numbers
- `coveredBy`: Tests that covered the mutant
- `killedBy`: Tests that killed the mutant

**Parsing Example (JavaScript):**
```javascript
const fs = require('fs');

function parseStrykerReport(jsonPath) {
    const report = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    const survivingMutants = [];

    for (const [filePath, fileData] of Object.entries(report.files)) {
        for (const mutant of fileData.mutants) {
            if (mutant.status === 'Survived') {
                survivingMutants.push({
                    id: mutant.id,
                    file: filePath,
                    line: mutant.location.start.line,
                    column: mutant.location.start.column,
                    mutator: mutant.mutatorName,
                    replacement: mutant.replacement,
                    coveredBy: mutant.coveredBy,
                    originalCode: extractOriginalCode(fileData.source, mutant.location)
                });
            }
        }
    }

    return survivingMutants;
}
```

### Stryker Mutators

**Available Mutators:**
- `ArithmeticOperator`: `+`, `-`, `*`, `/`, `%`
- `ArrayDeclaration`: Array literal mutations
- `BlockStatement`: Block removal
- `BooleanLiteral`: `true` ↔ `false`
- `ConditionalExpression`: Ternary mutations
- `EqualityOperator`: `==`, `===`, `!=`, `!==`
- `LogicalOperator`: `&&`, `||`
- `StringLiteral`: String mutations
- `UnaryOperator`: `+`, `-`, `!`, `~`

## Python - mutmut

### Running mutmut

```bash
# Run mutation testing
mutmut run

# Show results
mutmut results

# Show specific mutant
mutmut show <id>

# Apply mutant to see code
mutmut apply <id>
```

### Configuration

**.mutmut-config:**
```ini
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=python -m pytest
```

### Parsing mutmut Results

**Get Results:**
```bash
mutmut results > mutmut_results.txt
mutmut json > mutmut_results.json
```

**JSON Structure:**
```json
{
  "1": {
    "status": "survived",
    "filename": "src/calculator.py",
    "line": 15,
    "description": "--- src/calculator.py\n+++ src/calculator.py\n@@ -15 +15 @@\n-    return a + b\n+    return a - b"
  }
}
```

**Parsing Example (Python):**
```python
import json
import subprocess

def parse_mutmut_results():
    # Get JSON results
    result = subprocess.run(['mutmut', 'json'], capture_output=True, text=True)
    data = json.loads(result.stdout)

    surviving_mutants = []

    for mutant_id, mutant_data in data.items():
        if mutant_data['status'] == 'survived':
            surviving_mutants.append({
                'id': mutant_id,
                'file': mutant_data['filename'],
                'line': mutant_data.get('line'),
                'description': mutant_data['description'],
                'status': mutant_data['status']
            })

    return surviving_mutants

def get_mutant_details(mutant_id):
    """Get detailed diff for a specific mutant"""
    result = subprocess.run(['mutmut', 'show', mutant_id],
                          capture_output=True, text=True)
    return result.stdout
```

### mutmut Mutation Types

**Default Mutations:**
- Arithmetic operators
- Comparison operators
- Boolean operators
- Number literals
- String literals
- Function calls

## Python - Cosmic Ray

### Running Cosmic Ray

```bash
# Initialize session
cosmic-ray init config.toml session.sqlite

# Execute mutations
cosmic-ray exec session.sqlite

# View results
cosmic-ray report session.sqlite
```

### Configuration

**config.toml:**
```toml
[cosmic-ray]
module-path = "src"
test-command = "pytest tests"

[cosmic-ray.execution-engine]
name = "local"

[cosmic-ray.operators]
operators = [
    "core/ReplaceComparisonOperator",
    "core/ReplaceBinaryOperator",
    "core/ReplaceUnaryOperator"
]
```

### Parsing Cosmic Ray Results

**Export Results:**
```bash
cosmic-ray report session.sqlite --show-output > results.txt
cosmic-ray dump session.sqlite > results.json
```

## PHP - Infection

### Running Infection

```bash
./vendor/bin/infection
```

### Configuration

**infection.json:**
```json
{
    "source": {
        "directories": ["src"]
    },
    "logs": {
        "text": "infection.log",
        "json": "infection.json"
    },
    "mutators": {
        "@default": true
    }
}
```

### Parsing Infection Reports

**JSON Report:**
```json
{
    "escaped": [
        {
            "mutator": "Plus",
            "file": "src/Calculator.php",
            "line": 10,
            "diff": "--- Original\n+++ New\n@@ @@\n- return $a + $b;\n+ return $a - $b;"
        }
    ]
}
```

## C# - Stryker.NET

### Running Stryker.NET

```bash
dotnet stryker
```

### Configuration

**stryker-config.json:**
```json
{
  "stryker-config": {
    "project": "MyProject.csproj",
    "reporters": ["html", "json"],
    "mutation-level": "complete"
  }
}
```

## Cross-Tool Analysis

### Unified Mutant Format

Normalize different tool outputs to common format:

```python
class Mutant:
    def __init__(self, id, file, line, mutator, original, mutated, status, tests_covered=None):
        self.id = id
        self.file = file
        self.line = line
        self.mutator = mutator
        self.original = original
        self.mutated = mutated
        self.status = status  # survived, killed, no_coverage, timeout
        self.tests_covered = tests_covered or []

def normalize_pit_mutant(pit_mutant):
    return Mutant(
        id=pit_mutant['index'],
        file=pit_mutant['sourceFile'],
        line=pit_mutant['lineNumber'],
        mutator=pit_mutant['mutator'].split('.')[-1],
        original=None,  # Extract from source
        mutated=pit_mutant['description'],
        status='survived' if pit_mutant['status'] == 'SURVIVED' else 'killed'
    )

def normalize_stryker_mutant(stryker_mutant, file_path):
    return Mutant(
        id=stryker_mutant['id'],
        file=file_path,
        line=stryker_mutant['location']['start']['line'],
        mutator=stryker_mutant['mutatorName'],
        original=None,  # Extract from source
        mutated=stryker_mutant['replacement'],
        status=stryker_mutant['status'].lower(),
        tests_covered=stryker_mutant.get('coveredBy', [])
    )
```

### Coverage Integration

Combine mutation results with coverage data:

**Java (JaCoCo):**
```bash
mvn jacoco:report
# Parse target/site/jacoco/jacoco.xml
```

**JavaScript (Istanbul/NYC):**
```bash
npm test -- --coverage
# Parse coverage/coverage-final.json
```

**Python (Coverage.py):**
```bash
coverage run -m pytest
coverage json
# Parse coverage.json
```

### Mutation Score Calculation

```python
def calculate_mutation_score(mutants):
    total = len(mutants)
    killed = sum(1 for m in mutants if m.status == 'killed')
    survived = sum(1 for m in mutants if m.status == 'survived')
    no_coverage = sum(1 for m in mutants if m.status == 'no_coverage')
    timeout = sum(1 for m in mutants if m.status == 'timeout')

    # Standard mutation score
    mutation_score = (killed / total) * 100 if total > 0 else 0

    # Adjusted score (excluding no_coverage)
    covered = total - no_coverage
    adjusted_score = (killed / covered) * 100 if covered > 0 else 0

    return {
        'total': total,
        'killed': killed,
        'survived': survived,
        'no_coverage': no_coverage,
        'timeout': timeout,
        'mutation_score': mutation_score,
        'adjusted_score': adjusted_score
    }
```

## Best Practices

**Tool Selection:**
- Java: PIT (most mature)
- JavaScript/TypeScript: Stryker (excellent IDE integration)
- Python: mutmut (fast) or Cosmic Ray (configurable)
- C#: Stryker.NET
- PHP: Infection

**Performance Optimization:**
- Use incremental mode (only mutate changed code)
- Enable coverage analysis to skip uncovered code
- Parallelize mutation execution
- Set reasonable timeouts

**CI/CD Integration:**
- Run mutation testing on pull requests
- Set mutation score thresholds
- Cache mutation results
- Run incrementally on changed files only

**Report Storage:**
- Store JSON reports for programmatic analysis
- Generate HTML reports for human review
- Track mutation scores over time
- Archive results for trend analysis
