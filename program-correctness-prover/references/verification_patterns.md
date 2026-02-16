# Verification Patterns and Examples

Common program verification patterns with complete proofs in Isabelle and Coq.

## Table of Contents
- [Simple Assignment](#simple-assignment)
- [Conditional Programs](#conditional-programs)
- [Simple Loops](#simple-loops)
- [Array Operations](#array-operations)
- [Nested Loops](#nested-loops)

## Simple Assignment

### Pattern: Sequential Assignments

**Program**:
```
x := a;
y := b;
z := c
```

**Specification**: `{P} C {Q}`

**Proof Strategy**:
1. Work backwards with weakest precondition
2. Apply assignment rule repeatedly
3. Verify initial precondition

### Example: Swap with Temporary

**Program**:
```
temp := x;
x := y;
y := temp
```

**Specification**: `{x = a ∧ y = b} C {x = b ∧ y = a}`

**Isabelle Proof**:
```isabelle
lemma swap_correct:
  "⦃λs. s ''x'' = a ∧ s ''y'' = b⦄
   temp := (λs. s ''x'');;
   x := (λs. s ''y'');;
   y := (λs. s ''temp'')
   ⦃λs. s ''x'' = b ∧ s ''y'' = a⦄"
proof -
  have "⦃λs. s ''x'' = a ∧ s ''y'' = b⦄
        temp := (λs. s ''x'')
        ⦃λs. s ''temp'' = a ∧ s ''y'' = b⦄"
    by (rule hoare_asgn)
  moreover have "⦃λs. s ''temp'' = a ∧ s ''y'' = b⦄
                 x := (λs. s ''y'')
                 ⦃λs. s ''temp'' = a ∧ s ''x'' = b⦄"
    by (rule hoare_asgn)
  moreover have "⦃λs. s ''temp'' = a ∧ s ''x'' = b⦄
                 y := (λs. s ''temp'')
                 ⦃λs. s ''x'' = b ∧ s ''y'' = a⦄"
    by (rule hoare_asgn)
  ultimately show ?thesis
    by (rule hoare_seq)+
qed
```

**Coq Proof**:
```coq
Example swap_correct : forall a b,
  {{ fun st => st X = a /\ st Y = b }}
  temp ::= X;;
  X ::= Y;;
  Y ::= temp
  {{ fun st => st X = b /\ st Y = a }}.
Proof.
  intros a b.
  eapply hoare_seq.
  - apply hoare_asgn.
  - eapply hoare_seq.
    + apply hoare_asgn.
    + apply hoare_asgn.
Qed.
```

## Conditional Programs

### Pattern: If-Then-Else

**Program**:
```
if B then C1 else C2
```

**Proof Strategy**:
1. Prove `{P ∧ B} C1 {Q}`
2. Prove `{P ∧ ¬B} C2 {Q}`
3. Apply conditional rule

### Example: Maximum of Two Numbers

**Program**:
```
if x >= y then
  max := x
else
  max := y
```

**Specification**: `{true} C {max = max(x, y)}`

**Isabelle Proof**:
```isabelle
lemma max_correct:
  "⦃λs. True⦄
   If (λs. s ''x'' ≥ s ''y'')
   Then max := (λs. s ''x'')
   Else max := (λs. s ''y'')
   ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
proof (rule hoare_if)
  show "⦃λs. s ''x'' ≥ s ''y''⦄
        max := (λs. s ''x'')
        ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
  proof -
    have "⦃λs. s ''x'' = max (s ''x'') (s ''y'')⦄
          max := (λs. s ''x'')
          ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
      by (rule hoare_asgn)
    moreover have "s ''x'' ≥ s ''y'' ⟹ s ''x'' = max (s ''x'') (s ''y'')"
      by simp
    ultimately show ?thesis
      by (rule hoare_conseq)
  qed
next
  show "⦃λs. ¬(s ''x'' ≥ s ''y'')⦄
        max := (λs. s ''y'')
        ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
  proof -
    have "⦃λs. s ''y'' = max (s ''x'') (s ''y'')⦄
          max := (λs. s ''y'')
          ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
      by (rule hoare_asgn)
    moreover have "¬(s ''x'' ≥ s ''y'') ⟹ s ''y'' = max (s ''x'') (s ''y'')"
      by simp
    ultimately show ?thesis
      by (rule hoare_conseq)
  qed
qed
```

**Coq Proof**:
```coq
Example max_correct : forall x y,
  {{ fun st => True }}
  if x >= y then
    max ::= x
  else
    max ::= y
  {{ fun st => st max = max (st x) (st y) }}.
Proof.
  intros x y.
  apply hoare_if.
  - (* Then branch *)
    eapply hoare_consequence_pre.
    + apply hoare_asgn.
    + intros st H. simpl. lia.
  - (* Else branch *)
    eapply hoare_consequence_pre.
    + apply hoare_asgn.
    + intros st H. simpl. lia.
Qed.
```

## Simple Loops

### Pattern: Accumulation Loop

**Program**:
```
result := init;
i := 0;
while i < n do
  result := f(result, a[i]);
  i := i + 1
done
```

**Invariant**: `result = fold(f, init, a[0..i-1]) ∧ 0 ≤ i ≤ n`

### Example: Sum of Array

**Program**:
```
sum := 0;
i := 0;
while i < n do
  sum := sum + a[i];
  i := i + 1
done
```

**Specification**: `{n ≥ 0} C {sum = Σ(a[0..n-1])}`

**Invariant**: `I: sum = Σ(a[0..i-1]) ∧ 0 ≤ i ≤ n`

**Isabelle Proof**:
```isabelle
lemma sum_array_correct:
  assumes "n ≥ 0"
  shows "⦃λs. s ''n'' = n ∧ s ''n'' ≥ 0⦄
         sum := (λs. 0);;
         i := (λs. 0);;
         While (λs. s ''i'' < s ''n'')
         Do (sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
             i := (λs. s ''i'' + 1))
         ⦃λs. s ''sum'' = (∑j<n. s ''a'' j)⦄"
proof -
  (* Define invariant *)
  define I where "I = (λs. s ''sum'' = (∑j<s ''i''. s ''a'' j) ∧
                            0 ≤ s ''i'' ∧ s ''i'' ≤ s ''n'')"

  (* Initialization *)
  have init: "⦃λs. s ''n'' = n ∧ n ≥ 0⦄
              sum := (λs. 0);; i := (λs. 0)
              ⦃I⦄"
  proof -
    have "⦃λs. 0 = (∑j<0. s ''a'' j) ∧ 0 ≤ 0 ∧ 0 ≤ s ''n''⦄
          i := (λs. 0)
          ⦃I⦄"
      unfolding I_def by (rule hoare_asgn) simp
    moreover have "⦃λs. s ''n'' = n ∧ n ≥ 0⦄
                   sum := (λs. 0)
                   ⦃λs. 0 = (∑j<0. s ''a'' j) ∧ 0 ≤ 0 ∧ 0 ≤ s ''n''⦄"
      by (rule hoare_asgn) simp
    ultimately show ?thesis
      by (rule hoare_seq)
  qed

  (* Loop body preserves invariant *)
  have body: "⦃λs. I s ∧ s ''i'' < s ''n''⦄
              sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
              i := (λs. s ''i'' + 1)
              ⦃I⦄"
  proof -
    have "⦃λs. s ''sum'' + s ''a'' (s ''i'') = (∑j<s ''i''+1. s ''a'' j) ∧
               0 ≤ s ''i'' + 1 ∧ s ''i'' + 1 ≤ s ''n''⦄
          i := (λs. s ''i'' + 1)
          ⦃I⦄"
      unfolding I_def by (rule hoare_asgn) simp
    moreover have "⦃λs. I s ∧ s ''i'' < s ''n''⦄
                   sum := (λs. s ''sum'' + s ''a'' (s ''i''))
                   ⦃λs. s ''sum'' + s ''a'' (s ''i'') = (∑j<s ''i''+1. s ''a'' j) ∧
                        0 ≤ s ''i'' + 1 ∧ s ''i'' + 1 ≤ s ''n''⦄"
      unfolding I_def by (rule hoare_asgn) auto
    ultimately show ?thesis
      by (rule hoare_seq)
  qed

  (* Apply while rule *)
  have loop: "⦃I⦄
              While (λs. s ''i'' < s ''n'')
              Do (sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
                  i := (λs. s ''i'' + 1))
              ⦃λs. I s ∧ ¬(s ''i'' < s ''n'')⦄"
    by (rule hoare_while[OF body])

  (* Postcondition *)
  have post: "⦃λs. I s ∧ ¬(s ''i'' < s ''n'')⦄
              Skip
              ⦃λs. s ''sum'' = (∑j<n. s ''a'' j)⦄"
    unfolding I_def using assms by (rule hoare_conseq) auto

  (* Combine *)
  from init loop post show ?thesis
    by (rule hoare_seq)+
qed
```

**Coq Proof**:
```coq
Theorem sum_array_correct : forall n a,
  n >= 0 ->
  {{ fun st => st N = n /\ n >= 0 }}
  sum ::= 0;;
  i ::= 0;;
  while i < N do
    sum ::= sum + a[i];;
    i ::= i + 1
  done
  {{ fun st => st sum = sum_array a n }}.
Proof.
  intros n a Hn.
  (* Define invariant *)
  remember (fun st => st sum = sum_array a (st i) /\
                      0 <= st i /\ st i <= st N) as I.

  (* Initialization *)
  eapply hoare_seq.
  - apply hoare_asgn.
  - eapply hoare_seq.
    + apply hoare_asgn.
    + (* Loop *)
      eapply hoare_consequence_post.
      * apply hoare_while.
        (* Loop body *)
        eapply hoare_seq.
        -- apply hoare_asgn.
        -- eapply hoare_consequence_pre.
           ++ apply hoare_asgn.
           ++ intros st [HI Hcond]. subst I. simpl.
              destruct HI as [Hsum [Hi1 Hi2]].
              split; [|split]; try lia.
              rewrite Hsum. unfold sum_array. lia.
      * intros st [HI Hcond]. subst I.
        destruct HI as [Hsum [Hi1 Hi2]].
        assert (st i = n) by lia.
        rewrite H. exact Hsum.
Qed.
```

## Array Operations

### Pattern: Array Search

**Program**:
```
found := false;
i := 0;
while i < n && !found do
  if a[i] == target then
    found := true
  else
    i := i + 1
done
```

**Specification**: `{n ≥ 0} C {found ⟺ ∃j. 0 ≤ j < n ∧ a[j] = target}`

**Invariant**: `(∀j. 0 ≤ j < i ⟹ a[j] ≠ target) ∧ 0 ≤ i ≤ n ∧ (found ⟹ ∃j. 0 ≤ j < i ∧ a[j] = target)`

### Pattern: Array Maximum

**Program**:
```
max := a[0];
i := 1;
while i < n do
  if a[i] > max then
    max := a[i];
  i := i + 1
done
```

**Specification**: `{n > 0} C {∀j. 0 ≤ j < n ⟹ a[j] ≤ max}`

**Invariant**: `(∀j. 0 ≤ j < i ⟹ a[j] ≤ max) ∧ 1 ≤ i ≤ n ∧ (∃j. 0 ≤ j < i ∧ a[j] = max)`

## Nested Loops

### Pattern: Matrix Operations

**Program**:
```
i := 0;
while i < m do
  j := 0;
  while j < n do
    C[i,j];
    j := j + 1
  done;
  i := i + 1
done
```

**Outer Invariant**: `I_outer: P(0..i-1, 0..n-1) ∧ 0 ≤ i ≤ m`

**Inner Invariant**: `I_inner: P(0..i-1, 0..n-1) ∧ P(i, 0..j-1) ∧ 0 ≤ j ≤ n`

### Example: Matrix Sum

**Program**:
```
sum := 0;
i := 0;
while i < m do
  j := 0;
  while j < n do
    sum := sum + matrix[i][j];
    j := j + 1
  done;
  i := i + 1
done
```

**Specification**: `{m ≥ 0 ∧ n ≥ 0} C {sum = Σ(matrix[0..m-1][0..n-1])}`

**Outer Invariant**: `sum = Σ(matrix[0..i-1][0..n-1]) ∧ 0 ≤ i ≤ m`

**Inner Invariant**: `sum = Σ(matrix[0..i-1][0..n-1]) + Σ(matrix[i][0..j-1]) ∧ 0 ≤ j ≤ n`

## Termination Proofs

### Variant Functions

For total correctness, provide a variant that:
1. Is non-negative when loop condition holds
2. Decreases with each iteration

**Simple loop**: `V = n - i`

**Nested loops**: `V = (m - i) * n + (n - j)`

**Complex conditions**: May need lexicographic ordering

### Example: Euclidean GCD

**Program**:
```
while b != 0 do
  temp := b;
  b := a mod b;
  a := temp
done
```

**Variant**: `V = b` (decreases because `a mod b < b`)

**Termination proof**:
- `b > 0` when loop continues
- `b' = a mod b < b` (property of modulo)
- Eventually `b = 0`
