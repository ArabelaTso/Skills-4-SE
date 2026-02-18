# Dependency Manifest Formats

This reference documents the dependency manifest and lockfile formats for supported ecosystems.

## npm (Node.js/JavaScript)

### package.json

**Purpose**: Declares direct dependencies with version ranges

**Location**: Project root

**Format**:
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "~4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

**Version specifiers**:
- `^4.18.0` - Compatible with 4.18.0 (allows minor/patch updates)
- `~4.17.21` - Approximately 4.17.21 (allows patch updates only)
- `4.18.0` - Exact version
- `>=4.0.0 <5.0.0` - Range

### package-lock.json

**Purpose**: Locks exact versions of all dependencies (direct + transitive)

**Location**: Project root

**Format**:
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "lockfileVersion": 2,
  "dependencies": {
    "express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "requires": {
        "body-parser": "1.20.1"
      }
    },
    "body-parser": {
      "version": "1.20.1"
    }
  }
}
```

**Key fields**:
- `version`: Exact installed version
- `requires`: Direct dependencies of this package

## Maven (Java)

### pom.xml

**Purpose**: Declares dependencies with versions

**Location**: Project root

**Format**:
```xml
<project>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
      <version>2.7.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.13.3</version>
    </dependency>
  </dependencies>
</project>
```

**Dependency format**: `groupId:artifactId:version`

**Transitive dependencies**: Resolved by Maven, can be viewed with `mvn dependency:tree`

## Python

### requirements.txt

**Purpose**: Lists dependencies with version constraints

**Location**: Project root (convention)

**Format**:
```
requests==2.28.1
flask>=2.0.0,<3.0.0
numpy~=1.23.0
pandas
```

**Version specifiers**:
- `==2.28.1` - Exact version
- `>=2.0.0,<3.0.0` - Range
- `~=1.23.0` - Compatible release (>=1.23.0, <1.24.0)
- No version - Latest

### Pipfile.lock

**Purpose**: Locks exact versions (used by Pipenv)

**Location**: Project root

**Format**:
```json
{
  "default": {
    "requests": {
      "version": "==2.28.1",
      "hashes": ["sha256:..."]
    }
  },
  "develop": {}
}
```

### poetry.lock

**Purpose**: Locks exact versions (used by Poetry)

**Location**: Project root

**Format** (TOML):
```toml
[[package]]
name = "requests"
version = "2.28.1"
category = "main"

[[package]]
name = "pytest"
version = "7.1.2"
category = "dev"
```

## Go

### go.mod

**Purpose**: Declares module dependencies

**Location**: Project root

**Format**:
```
module github.com/user/myapp

go 1.19

require (
    github.com/gin-gonic/gin v1.8.1
    github.com/lib/pq v1.10.6
)

require (
    github.com/gin-contrib/sse v0.1.0 // indirect
    github.com/go-playground/validator/v10 v10.11.0 // indirect
)
```

**Key points**:
- Direct dependencies in first `require` block
- Transitive dependencies marked with `// indirect`
- Versions prefixed with `v`

### go.sum

**Purpose**: Checksums for all dependencies

**Location**: Project root

**Format**:
```
github.com/gin-gonic/gin v1.8.1 h1:4+fr/el88TOO3ewCmQr8cx/CtZ/umlIRIs5M4NTNjf8=
github.com/gin-gonic/gin v1.8.1/go.mod h1:ji8BvRH1azfM+SYow9zQ6SZMvR8qOMZHmsCuWR9tTTk=
```

## Rust (Cargo)

### Cargo.toml

**Purpose**: Declares dependencies with version requirements

**Location**: Project root

**Format**:
```toml
[package]
name = "myapp"
version = "0.1.0"

[dependencies]
serde = "1.0"
tokio = { version = "1.20", features = ["full"] }
reqwest = "0.11.11"

[dev-dependencies]
mockito = "0.31"
```

**Version specifiers**:
- `"1.0"` - Caret requirement (^1.0.0)
- `"=1.0.0"` - Exact version
- `">=1.0.0, <2.0.0"` - Range

### Cargo.lock

**Purpose**: Locks exact versions of all dependencies

**Location**: Project root

**Format** (TOML):
```toml
[[package]]
name = "serde"
version = "1.0.144"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "..."

[[package]]
name = "myapp"
version = "0.1.0"
dependencies = [
    "serde",
    "tokio",
]
```

## Parsing Strategy

### Priority Order

For each ecosystem, prefer lockfiles over manifests:

1. **npm**: package-lock.json > package.json
2. **Python**: poetry.lock > Pipfile.lock > requirements.txt
3. **Java**: pom.xml (use `mvn dependency:tree` for transitive)
4. **Go**: go.mod (includes transitive with `// indirect`)
5. **Rust**: Cargo.lock > Cargo.toml

### Extracting Versions

**From manifests** (package.json, pom.xml, etc.):
- Parse version ranges
- Use the minimum version or resolve to latest matching

**From lockfiles** (package-lock.json, Cargo.lock, etc.):
- Use exact versions
- More accurate for vulnerability matching

### Identifying Direct vs Transitive

| Ecosystem | Method |
|-----------|--------|
| npm | Compare package.json deps with package-lock.json |
| Maven | Parse `mvn dependency:tree` output |
| Python | poetry.lock has `category` field; otherwise assume direct |
| Go | Check for `// indirect` comment in go.mod |
| Rust | Compare Cargo.toml with Cargo.lock |

## Common Parsing Challenges

### Version Range Resolution

Manifests often specify ranges (e.g., `^4.0.0`). For CVE scanning:
- Use lockfiles when available (exact versions)
- If only manifest available, query CVE database with range
- Some databases (OSV.dev) support range queries

### Workspace/Monorepo Structures

- **npm**: Look for `workspaces` in package.json
- **Maven**: Multi-module projects with parent POM
- **Python**: Multiple requirements files
- **Go**: Multiple go.mod files in subdirectories
- **Rust**: Workspace in Cargo.toml

Scan each workspace/module separately.

### Private/Internal Dependencies

Skip dependencies that:
- Use `file:` protocol (local paths)
- Point to private registries (unless you have access)
- Are internal company packages (no public CVE data)
