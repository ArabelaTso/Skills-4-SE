# Hoare Logic Reference

Reference for Hoare logic rules and verification condition generation.

## Table of Contents
- [Hoare Triple Notation](#hoare-triple-notation)
- [Basic Rules](#basic-rules)
- [Derived Rules](#derived-rules)
- [Loop Invariants](#loop-invariants)
- [Weakest Preconditions](#weakest-preconditions)

## Hoare Triple Notation

A Hoare triple has the form: `{P} C {Q}`

- **P**: Precondition (assertion about state before execution)
- **C**: Command/program
- **Q**: Postcondition (assertion about state after execution)

**Partial correctness**: If P holds before C and C terminates, then Q holds after
**Total correctness**: If P holds before C, then C terminates and Q holds after

### Notation Variants

**Isabelle**: `⦃P⦄ C ⦃Q⦄` or `{P} C {Q}`
**Coq**: `{{ P }} C {{ Q }}`

## Basic Rules

### Skip Rule

```
{P} skip {P}
```

The skip command does nothing, so postcondition equals precondition.

### Assignment Rule

```
{P[E/x]} x := E {P}
```

To prove P after assignment, prove P with E substituted for x before assignment.

**Example**:
```
{y + 1 > 0} x := y + 1 {x > 0}
```

### Sequence Rule

```
{P} C1 {Q}    {Q} C2 {R}
─────────────────────────
    {P} C1; C2 {R}
```

Compose commands by chaining postcondition of first to precondition of second.

### Conditional Rule

```
{P ∧ B} C1 {Q}    {P ∧ ¬B} C2 {Q}
──────────────────────────────────
   {P} if B then C1 else C2 {Q}
```

Prove both branches separately with condition added to precondition.

### While Rule (Partial Correctness)

```
{P ∧ B} C {P}
─────────────────────────
{P} while B do C {P ∧ ¬B}
```

P is the loop invariant:
- Holds before loop
- Preserved by loop body (when B is true)
- Combined with ¬B gives postcondition

### While Rule (Total Correctness)

```
{P ∧ B ∧ V = v} C {P ∧ V < v}
V ≥ 0 when P ∧ B holds
──────────────────────────────
{P} while B do C {P ∧ ¬B}
```

Additionally requires:
- Variant V (decreases each iteration)
- V bounded below (typically V ≥ 0)

## Derived Rules

### Consequence Rule (Strengthening/Weakening)

```
P' ⟹ P    {P} C {Q}    Q ⟹ Q'
────────────────────────────────
        {P'} C {Q'}
```

Can strengthen precondition or weaken postcondition.

### Frame Rule

```
{P} C {Q}
─────────────────────
{P ∧ R} C {Q ∧ R}
```

If R is not modified by C, it's preserved (frame condition).

## Loop Invariants

### What Makes a Good Loop Invariant

A loop invariant I must satisfy:

1. **Initialization**: Precondition implies invariant
   - `P ⟹ I`

2. **Preservation**: Invariant preserved by loop body
   - `{I ∧ B} C {I}`

3. **Termination**: Invariant + negated condition implies postcondition
   - `I ∧ ¬B ⟹ Q`

### Finding Loop Invariants

**Strategy 1: Generalize the postcondition**
- Start with postcondition Q
- Replace constants with variables
- Add relationships that hold throughout

**Example**: Sum of array
- Postcondition: `sum = Σ(a[0..n-1])`
- Invariant: `sum = Σ(a[0..i-1]) ∧ 0 ≤ i ≤ n`

**Strategy 2: State what's been computed**
- Express partial result at iteration i
- Include bounds on loop counter

**Strategy 3: Maintain relationships**
- Identify relationships between variables
- Ensure they hold at each iteration

### Common Loop Invariant Patterns

**Accumulation**:
```
result = f(a[0..i-1]) ∧ 0 ≤ i ≤ n
```

**Search**:
```
(∀j. 0 ≤ j < i ⟹ ¬P(a[j])) ∧ 0 ≤ i ≤ n
```

**Partitioning**:
```
(∀j. 0 ≤ j < i ⟹ P(a[j])) ∧ (∀j. i ≤ j < n ⟹ ¬P(a[j]))
```

## Weakest Preconditions

The weakest precondition wp(C, Q) is the weakest condition that guarantees Q after C.

### WP Rules

**Skip**:
```
wp(skip, Q) = Q
```

**Assignment**:
```
wp(x := E, Q) = Q[E/x]
```

**Sequence**:
```
wp(C1; C2, Q) = wp(C1, wp(C2, Q))
```

**Conditional**:
```
wp(if B then C1 else C2, Q) = (B ⟹ wp(C1, Q)) ∧ (¬B ⟹ wp(C2, Q))
```

**While** (partial correctness):
```
wp(while B do C, Q) = I where:
  I ⟹ (B ⟹ wp(C, I))
  I ∧ ¬B ⟹ Q
```

### Using WP for Verification

1. Start with postcondition Q
2. Work backwards through program
3. Compute wp for each statement
4. Verify precondition P implies final wp

**Example**:
```
{x ≥ 0} y := x + 1; z := y * 2 {z > 0}

wp(z := y * 2, z > 0) = y * 2 > 0 = y > 0
wp(y := x + 1, y > 0) = x + 1 > 0 = x ≥ 0

Verify: x ≥ 0 ⟹ x ≥ 0 ✓
```

## Verification Condition Generation

### Process

1. **Annotate loops** with invariants
2. **Apply Hoare rules** to generate VCs
3. **Prove VCs** using theorem prover

### Example: Sum Program

**Program**:
```
sum := 0; i := 0;
while i < n do
  sum := sum + a[i];
  i := i + 1
done
```

**Specification**:
```
{n ≥ 0} C {sum = Σ(a[0..n-1])}
```

**Invariant**:
```
I: sum = Σ(a[0..i-1]) ∧ 0 ≤ i ≤ n
```

**Verification Conditions**:

1. **Initialization**: `n ≥ 0 ⟹ 0 = Σ(a[0..-1]) ∧ 0 ≤ 0 ≤ n`
   - Simplifies to: `n ≥ 0 ⟹ 0 = 0 ∧ 0 ≤ n` ✓

2. **Preservation**: `{I ∧ i < n} sum := sum + a[i]; i := i + 1 {I}`
   - WP: `sum + a[i] = Σ(a[0..i]) ∧ 0 ≤ i + 1 ≤ n`
   - Verify: `I ∧ i < n ⟹ WP` ✓

3. **Termination**: `I ∧ ¬(i < n) ⟹ sum = Σ(a[0..n-1])`
   - From `I ∧ i ≥ n` and `i ≤ n`, get `i = n`
   - So `sum = Σ(a[0..n-1])` ✓

4. **Variant decreases** (for total correctness): `V = n - i`
   - Initially: `V = n - 0 = n ≥ 0` ✓
   - Decreases: `i := i + 1` makes `V' = n - (i+1) = V - 1 < V` ✓
   - Bounded: `i ≤ n ⟹ V ≥ 0` ✓

## Common Proof Patterns

### Pattern: Simple Assignment Chain

```
{P} x := E1; y := E2; z := E3 {Q}
```

Work backwards with WP:
1. `wp(z := E3, Q) = Q[E3/z]`
2. `wp(y := E2, Q[E3/z]) = Q[E3/z][E2/y]`
3. `wp(x := E1, ...) = Q[E3/z][E2/y][E1/x]`
4. Verify `P ⟹ final_wp`

### Pattern: Conditional Without Else

```
{P} if B then C {Q}
```

Equivalent to:
```
{P} if B then C else skip {Q}
```

VCs:
- `P ∧ B ⟹ wp(C, Q)`
- `P ∧ ¬B ⟹ Q`

### Pattern: Loop with Early Exit

```
while B do
  if C then break
  S
done
```

Invariant must account for both exit conditions.

### Pattern: Nested Loops

```
while B1 do
  while B2 do
    C
  done
done
```

Requires nested invariants:
- Outer invariant I1
- Inner invariant I2 (may depend on outer loop variables)

## Isabelle Syntax

### Hoare Triple
```isabelle
⦃P⦄ C ⦃Q⦄
```

### Common Predicates
```isabelle
⦃λs. P s⦄ C ⦃λs. Q s⦄  (* State-based *)
```

### Verification Condition Lemmas
```isabelle
lemma vc_assign: "⦃P[E/x]⦄ x := E ⦃P⦄"
lemma vc_seq: "⦃P⦄ C1 ⦃Q⦄ ⟹ ⦃Q⦄ C2 ⦃R⦄ ⟹ ⦃P⦄ C1;; C2 ⦃R⦄"
```

## Coq Syntax

### Hoare Triple
```coq
{{ P }} C {{ Q }}
```

### Common Predicates
```coq
{{ fun st => P st }} C {{ fun st => Q st }}
```

### Verification Condition Lemmas
```coq
Theorem hoare_asgn : forall Q X a,
  {{Q [X |-> a]}} X ::= a {{Q}}.

Theorem hoare_seq : forall P Q R c1 c2,
  {{P}} c1 {{Q}} -> {{Q}} c2 {{R}} -> {{P}} c1;;c2 {{R}}.
```
