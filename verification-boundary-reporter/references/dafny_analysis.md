# Dafny Verification Boundary Analysis

Guide for analyzing verification boundaries in Dafny projects.

## Identifying Verified Components

### Verified Methods

**Indicators of verified code:**
```dafny
// VERIFIED: Method with complete verification
method Add(a: int, b: int) returns (sum: int)
  ensures sum == a + b
{
  sum := a + b;
}  // Verifies successfully

// VERIFIED: Function with postcondition
function Max(a: int, b: int): int
  ensures Max(a, b) >= a && Max(a, b) >= b
{
  if a > b then a else b
}
```

### Checking Verification Status

**Dafny output:**
```
Dafny program verifier finished with X verified, Y errors
```

**Successful verification:**
```
Dafny program verifier finished with 10 verified, 0 errors
```

## Identifying Assumptions

### Assume Statements

**Explicit assumptions:**
```dafny
// ASSUMED: Property assumed without proof
method ProcessData(x: int) returns (y: int)
  ensures y > 0
{
  assume x > 0;  // RED FLAG: Assumption
  y := x + 1;
}

// ASSUMED: Precondition not verified by caller
method Caller()
{
  var result := ProcessData(-5);  // Violates assumed precondition
}
```

### Axioms

**Axiom declarations:**
```dafny
// ASSUMED: Axiom without proof
lemma {:axiom} UnprovenProperty(x: int)
  ensures x + 1 > x

// ASSUMED: Opaque function
function {:opaque} MysteryFunction(x: int): int
  // No body, no verification
```

### Unverified Specifications

**Missing specifications:**
```dafny
// UNVERIFIED: No postcondition
method DoSomething(x: int) returns (y: int)
{
  y := x * 2;
}  // What properties does this guarantee?

// UNVERIFIED: Weak specification
method Sort(a: array<int>)
  modifies a
  // No ensures clause - doesn't specify sorting!
{
  // implementation
}
```

## Trusted Computing Base

### Dafny Verifier

**Always in TCB:**
- Dafny verifier
- Boogie intermediate verification language
- Z3 SMT solver
- .NET runtime (for execution)

**Documentation:**
```markdown
### Dafny Verifier
**Type:** Verification Tool
**Description:** Dafny verifier + Boogie + Z3 SMT solver
**Justification:** Core verification infrastructure
**Mitigation:** Widely used, actively maintained
**Risk Level:** Low - but verification is only as good as specifications
```

### External Methods

**Unverified external code:**
```dafny
// TCB: External method
method {:extern} ReadFile(path: string) returns (content: string)

// TCB: External function
function {:extern} SystemTime(): int

// UNVERIFIED: No specification for external code
```

**Report:**
```markdown
### ReadFile (External)
**Type:** External Method
**Description:** Reads file from filesystem
**Justification:** I/O operations cannot be verified in Dafny
**Risk:** HIGH - no verification of file operations
**Recommendation:** Minimize use, add runtime checks
```

### Compilation

**Code generation:**
```dafny
// TCB: Compiled to C#/Java/Go/etc.
// Compilation correctness not verified
```

**Report:**
```markdown
### Dafny Compilation
**Type:** Code Generation
**Description:** Compiles Dafny to target language (C#, Java, Go, etc.)
**Justification:** Enables execution
**Risk:** Medium - compiler correctness not formally verified
**Mitigation:** Compiler is tested, but semantic gaps possible
```

## Unverified Components

### Verification Timeouts

**Timeout issues:**
```dafny
// UNVERIFIED: Verification timeout
method Complex(x: int) returns (y: int)
  ensures y > 0
{
  // Complex implementation
  // Dafny times out trying to verify
}
// Warning: Verification timed out
```

**Report:**
```markdown
### Complex (Timeout)
**Location:** File.dfy:42
**Reason:** Verification timeout
**Risk Assessment:** UNKNOWN - may be correct but unverified
**Recommendation:** Simplify, add intermediate assertions, or increase timeout
```

### Incomplete Specifications

**Under-specified code:**
```dafny
// UNVERIFIED: Specification incomplete
method ProcessArray(a: array<int>)
  requires a.Length > 0
  modifies a
  // Missing: What does this method do to the array?
{
  a[0] := 0;
}
```

### Unverified Loops

**Missing loop invariants:**
```dafny
// UNVERIFIED: Loop without invariant
method Sum(a: array<int>) returns (sum: int)
{
  sum := 0;
  var i := 0;
  while i < a.Length
    // Missing: loop invariant
  {
    sum := sum + a[i];
    i := i + 1;
  }
}
// Dafny cannot verify without invariant
```

## Verification Depth

### Shallow vs Deep Verification

**Shallow (type safety only):**
```dafny
// SHALLOW: Only type-checked
method Add(a: int, b: int) returns (sum: int)
{
  sum := a + b;
}
// No specification - only type safety verified
```

**Deep (functional correctness):**
```dafny
// DEEP: Functional correctness verified
method Add(a: int, b: int) returns (sum: int)
  ensures sum == a + b
  ensures sum >= a && sum >= b  // Additional properties
{
  sum := a + b;
}
```

## Dependency Analysis

### Specification Dependencies

**Tracking dependencies:**
```dafny
lemma Helper(x: int)
  requires x > 0
  ensures x + 1 > 1
{
  // proof
}

method UseHelper(y: int) returns (z: int)
  requires y > 0
  ensures z > 1
{
  Helper(y);  // Depends on Helper lemma
  z := y + 1;
}
```

### Assumption Propagation

**Example:**
```dafny
method Base(x: int) returns (y: int)
  ensures y > 0
{
  assume x > 0;  // ASSUMPTION
  y := x;
}

method Derived(a: int) returns (b: int)
  ensures b > 0
{
  b := Base(a);  // Inherits assumption
}
```

**Report:**
```markdown
### Assumption Propagation

assume x > 0 (in Base)
  ↓ (propagates to)
method Derived

**Impact:** Derived's correctness depends on unverified assumption
**Risk Level:** HIGH
```

## Coverage Analysis

### Calculating Coverage

**Metrics:**
```
Total methods: Count all methods
Verified methods: Methods with ensures clauses that verify
Unverified methods: Methods without ensures or with timeouts
Assumed statements: Count assume statements
External methods: Count {:extern} methods
```

**Example:**
```markdown
## Verification Statistics

- Total methods: 25
- Verified methods: 18 (72%)
- Unverified methods: 5 (20%)
- External methods: 2 (8%)
- Assume statements: 3
- Verification timeouts: 1
```

## Red Flags

### Critical Issues

**High-priority red flags:**
```dafny
// RED FLAG: Assume in critical method
method CriticalOperation(x: int) returns (y: int)
  ensures y > 0
{
  assume x > 0;  // RED FLAG
  y := x;
}

// RED FLAG: No specification
method ImportantFunction(a: array<int>)
  modifies a
  // No ensures - what does this do?
{
  // implementation
}

// RED FLAG: Verification timeout
method ComplexAlgorithm(x: int) returns (y: int)
  ensures y == ComputeExpected(x)
{
  // Complex code
}
// Dafny: Verification timed out
```

### Warning Signs

**Medium-priority warnings:**
```dafny
// WARNING: Weak specification
method Sort(a: array<int>)
  modifies a
  ensures a.Length == old(a.Length)
  // Missing: sorted property, permutation property

// WARNING: External method without specification
method {:extern} ExternalOp(x: int) returns (y: int)
  // No ensures clause

// WARNING: Opaque function
function {:opaque} Mystery(x: int): int
  // No body, no properties
```

## Report Generation

### Section: Verified Components

**Template:**
```markdown
### [Method/Function Name]

**Location:** [File.dfy:Line]
**Type:** [Method/Function/Lemma]
**Signature:** ```dafny [signature] ```
**Preconditions:** [List requires clauses]
**Postconditions:** [List ensures clauses]
**Verification Status:** ✓ Verified
**Verification Time:** [seconds]
**Dependencies:** [Methods/lemmas used]
```

### Section: Assumptions

**Template:**
```markdown
### [Assume Statement/Axiom]

**Location:** [File.dfy:Line]
**Type:** [assume/axiom]
**Statement:** ```dafny [statement] ```
**Context:** [Where it appears]
**Justification:** [Why assumed - if documented]
**Impact:** [Methods affected]
**Risk Level:** [Low/Medium/High]
**Recommendation:** [Can this be proven?]
```

### Section: Unverified Components

**Template:**
```markdown
### [Method Name]

**Location:** [File.dfy:Line]
**Reason:** [No specification/Timeout/External/etc.]
**Risk Assessment:** [Impact if incorrect]
**Current Specification:** [What is specified, if anything]
**Missing Specification:** [What should be specified]
**Recommendation:** [Add specification/Fix timeout/etc.]
```

## Example Analysis

**Input:**
```dafny
method BinarySearch(a: array<int>, key: int) returns (index: int)
  requires forall i, j :: 0 <= i < j < a.Length ==> a[i] <= a[j]
  ensures index == -1 || (0 <= index < a.Length && a[index] == key)
{
  var low := 0;
  var high := a.Length;
  while low < high
    invariant 0 <= low <= high <= a.Length
    invariant forall i :: 0 <= i < low ==> a[i] < key
    invariant forall i :: high <= i < a.Length ==> a[i] > key
  {
    var mid := (low + high) / 2;
    if a[mid] < key {
      low := mid + 1;
    } else if a[mid] > key {
      high := mid;
    } else {
      return mid;
    }
  }
  return -1;
}

method Main()
{
  var arr := new int[5];
  assume arr[0] == 1 && arr[1] == 3 && arr[2] == 5;  // RED FLAG
  var idx := BinarySearch(arr, 3);
  print idx;
}
```

**Output report excerpt:**
```markdown
## Verification Statistics

- Total methods: 2
- Verified methods: 1 (50%)
- Unverified methods: 1 (50%)
- Assume statements: 1

## Verified Components

### BinarySearch
**Location:** Example.dfy:1
**Type:** Method
**Preconditions:**
- Array is sorted: `forall i, j :: 0 <= i < j < a.Length ==> a[i] <= a[j]`
**Postconditions:**
- Returns -1 or valid index: `index == -1 || (0 <= index < a.Length && a[index] == key)`
**Verification Status:** ✓ Verified
**Loop Invariants:** 3 invariants maintain search space correctness
**Properties Verified:**
- Correctness: Returns correct index or -1
- Safety: No array out-of-bounds access
- Termination: Loop terminates (search space shrinks)

## Assumptions

### Array initialization (assume)
**Location:** Example.dfy:24
**Statement:** `assume arr[0] == 1 && arr[1] == 3 && arr[2] == 5`
**Context:** Main method
**Justification:** None provided
**Impact:** Main method correctness depends on this
**Risk Level:** MEDIUM - test code, but assumption not verified
**Recommendation:** Replace with explicit assignments:
```dafny
arr[0] := 1;
arr[1] := 3;
arr[2] := 5;
```

## Unverified Components

### Main
**Location:** Example.dfy:22
**Reason:** Contains unverified assumption
**Risk Assessment:** LOW - test/demo code
**Recommendation:** Remove assume, use assignments

## Verification Gaps

1. **Array initialization:** Main uses assume instead of verified initialization
2. **Remaining array elements:** arr[3] and arr[4] uninitialized

## Limitations

1. **Sortedness assumption:** BinarySearch requires sorted array; caller
   must ensure this precondition
2. **Integer overflow:** Division (low + high) / 2 could overflow for
   very large arrays (not verified in Dafny)
```
