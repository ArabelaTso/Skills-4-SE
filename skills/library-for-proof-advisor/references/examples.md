# Library Usage Examples

This file contains examples of recommending libraries and lemmas for specific proof goals.

## Example 1: List Reversal Property

### Proof Goal
```
Goal: rev (rev xs) = xs
```

### Isabelle/HOL Recommendation

**Library**: Main (automatically imported)

**Relevant lemma**: `rev_rev_ident`
```isabelle
lemma rev_rev_ident: "rev (rev xs) = xs"
```

**Usage**:
```isabelle
lemma "rev (rev xs) = xs"
  by (simp add: rev_rev_ident)
(* Or simply: by simp *)
```

**Alternative approach** (if lemma unknown):
```isabelle
lemma "rev (rev xs) = xs"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  (* Use: rev_append lemma *)
  show ?case by (simp add: rev_append Cons.IH)
qed
```

**Related lemmas**:
- `rev_append`: `rev (xs @ ys) = rev ys @ rev xs`
- `length_rev`: `length (rev xs) = length xs`

### Coq Recommendation

**Library**: `List` (standard library)

**Import**: `Require Import List. Import ListNotations.`

**Relevant lemma**: `rev_involutive`
```coq
Lemma rev_involutive : forall l, rev (rev l) = l.
```

**Usage**:
```coq
Require Import List.
Import ListNotations.

Lemma example : forall l, rev (rev l) = l.
Proof.
  apply rev_involutive.
Qed.
```

**Alternative approach** (manual proof):
```coq
Lemma example : forall l, rev (rev l) = l.
Proof.
  induction l as [| x xs IHxs].
  - (* Base case *)
    simpl. reflexivity.
  - (* Inductive case *)
    simpl.
    rewrite rev_app_distr.  (* Key lemma *)
    simpl.
    rewrite IHxs.
    reflexivity.
Qed.
```

**Related lemmas**:
- `rev_app_distr`: `rev (l1 ++ l2) = rev l2 ++ rev l1`
- `rev_length`: `length (rev l) = length l`

---

## Example 2: Commutativity of Addition

### Proof Goal
```
Goal: n + m = m + n
```

### Isabelle/HOL Recommendation

**Library**: Main (Nat theory)

**Relevant lemma**: `add_commute`
```isabelle
lemma add_commute: "m + n = n + m"
```

**Usage**:
```isabelle
lemma "n + m = m + n"
  by (simp add: add_commute)
(* Or simply: by simp *)
```

**Manual proof** (if needed):
```isabelle
lemma "n + m = m + n"
proof (induction n)
  case 0
  show ?case by simp
next
  case (Suc n)
  (* Use: add_Suc, add_Suc_right *)
  show ?case by (simp add: Suc.IH)
qed
```

**Related lemmas**:
- `add_assoc`: `(m + n) + k = m + (n + k)`
- `add_0`: `0 + n = n`
- `add_0_right`: `n + 0 = n`

### Coq Recommendation

**Library**: `Arith` (standard library)

**Import**: `Require Import Arith.`

**Relevant lemma**: `plus_comm` or `Nat.add_comm`
```coq
Lemma plus_comm : forall n m, n + m = m + n.
```

**Usage**:
```coq
Require Import Arith.

Lemma example : forall n m, n + m = m + n.
Proof.
  apply plus_comm.
Qed.
```

**Alternative** (using lia):
```coq
Require Import Lia.

Lemma example : forall n m, n + m = m + n.
Proof.
  intros. lia.
Qed.
```

**Related lemmas**:
- `plus_assoc`: `(n + m) + p = n + (m + p)`
- `plus_0_l`: `0 + n = n`
- `plus_0_r`: `n + 0 = n`

---

## Example 3: List Membership After Append

### Proof Goal
```
Goal: x ∈ set (xs @ ys) ⟷ x ∈ set xs ∨ x ∈ set ys
```

### Isabelle/HOL Recommendation

**Library**: Main (List theory)

**Relevant lemma**: `set_append`
```isabelle
lemma set_append: "set (xs @ ys) = set xs ∪ set ys"
```

**Usage**:
```isabelle
lemma "x ∈ set (xs @ ys) ⟷ x ∈ set xs ∨ x ∈ set ys"
  by (simp add: set_append)
```

**Related lemmas**:
- `in_set_member`: `x ∈ set xs ⟷ (∃i < length xs. xs ! i = x)`
- `set_rev`: `set (rev xs) = set xs`
- `set_map`: `set (map f xs) = f ` set xs`

### Coq Recommendation

**Library**: `List`

**Import**: `Require Import List. Import ListNotations.`

**Relevant lemma**: `in_app_iff`
```coq
Lemma in_app_iff : forall A (l m : list A) (a : A),
  In a (l ++ m) <-> In a l \/ In a m.
```

**Usage**:
```coq
Require Import List.
Import ListNotations.

Lemma example : forall A (x : A) (l1 l2 : list A),
  In x (l1 ++ l2) <-> In x l1 \/ In x l2.
Proof.
  intros. apply in_app_iff.
Qed.
```

**Related lemmas**:
- `in_eq`: `In x (x :: l)`
- `in_cons`: `In x l -> In x (y :: l)`
- `in_rev`: `In x (rev l) <-> In x l`
- `in_map_iff`: `In y (map f l) <-> exists x, f x = y /\ In x l`

---

## Example 4: Length of Mapped List

### Proof Goal
```
Goal: length (map f xs) = length xs
```

### Isabelle/HOL Recommendation

**Library**: Main (List theory)

**Relevant lemma**: `length_map`
```isabelle
lemma length_map: "length (map f xs) = length xs"
```

**Usage**:
```isabelle
lemma "length (map f xs) = length xs"
  by (simp add: length_map)
```

**Manual proof**:
```isabelle
lemma "length (map f xs) = length xs"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case by (simp add: Cons.IH)
qed
```

### Coq Recommendation

**Library**: `List`

**Relevant lemma**: `map_length`
```coq
Lemma map_length : forall A B (f : A -> B) l,
  length (map f l) = length l.
```

**Usage**:
```coq
Require Import List.

Lemma example : forall A B (f : A -> B) l,
  length (map f l) = length l.
Proof.
  apply map_length.
Qed.
```

---

## Example 5: Arithmetic Inequality

### Proof Goal
```
Goal: n ≤ m ⟹ n + k ≤ m + k
```

### Isabelle/HOL Recommendation

**Library**: Main (Nat theory)

**Relevant lemmas**: Arithmetic simplification

**Usage**:
```isabelle
lemma "n ≤ m ⟹ n + k ≤ m + k"
  by simp
(* Or: by arith *)
```

**Related lemmas**:
- `add_le_mono`: `m ≤ n ⟹ k ≤ l ⟹ m + k ≤ n + l`
- `add_le_mono1`: `m ≤ n ⟹ m + k ≤ n + k`

### Coq Recommendation

**Library**: `Arith` and `Lia`

**Import**: `Require Import Arith Lia.`

**Usage**:
```coq
Require Import Arith Lia.

Lemma example : forall n m k,
  n <= m -> n + k <= m + k.
Proof.
  intros. lia.
Qed.
```

**Alternative** (manual):
```coq
Lemma example : forall n m k,
  n <= m -> n + k <= m + k.
Proof.
  intros n m k H.
  apply plus_le_compat_r.
  exact H.
Qed.
```

**Related lemmas**:
- `plus_le_compat_l`: `n <= m -> p + n <= p + m`
- `plus_le_compat_r`: `n <= m -> n + p <= m + p`
- `plus_le_compat`: `n <= m -> p <= q -> n + p <= m + q`

---

## Example 6: Set Union Commutativity

### Proof Goal
```
Goal: A ∪ B = B ∪ A
```

### Isabelle/HOL Recommendation

**Library**: Main (Set theory)

**Relevant lemma**: `Un_commute`
```isabelle
lemma Un_commute: "A ∪ B = B ∪ A"
```

**Usage**:
```isabelle
lemma "A ∪ B = B ∪ A"
  by (simp add: Un_commute)
(* Or simply: by auto *)
```

**Related lemmas**:
- `Un_assoc`: `(A ∪ B) ∪ C = A ∪ (B ∪ C)`
- `Int_commute`: `A ∩ B = B ∩ A`
- `Un_Int_distrib`: `(A ∪ B) ∩ C = (A ∩ C) ∪ (B ∩ C)`

### Coq Recommendation

**Library**: Sets (MSets or custom)

For finite sets, use extensionality:

**Usage**:
```coq
Require Import MSets.

(* Assuming set operations defined *)
Lemma union_comm : forall A B,
  union A B = union B A.
Proof.
  intros.
  apply set_extensionality.
  intro x.
  split; intro H.
  - (* x in A ∪ B -> x in B ∪ A *)
    destruct H; [right | left]; assumption.
  - (* x in B ∪ A -> x in A ∪ B *)
    destruct H; [right | left]; assumption.
Qed.
```

---

## Recommendation Strategy

### Step 1: Identify the Domain

- **Lists**: Use List theory/library
- **Arithmetic**: Use Nat/Arith/Lia
- **Sets**: Use Set theory/MSets
- **Logic**: Use HOL/Logic basics

### Step 2: Search for Existing Lemmas

**Isabelle**:
```isabelle
find_theorems "rev (rev _)"
find_theorems name: "append" "length"
```

**Coq**:
```coq
Search rev.
Search (_ ++ _).
Search (?x + ?y = ?y + ?x).
```

### Step 3: Check Standard Patterns

- **Commutativity**: `x op y = y op x`
- **Associativity**: `(x op y) op z = x op (y op z)`
- **Identity**: `x op e = x`
- **Distributivity**: `x op (y op' z) = (x op y) op' (x op z)`

### Step 4: Use Automation

**Isabelle**:
- `simp`: Simplification
- `auto`: Automatic proof search
- `blast`: Tableau prover
- `sledgehammer`: External provers

**Coq**:
- `auto`: Automatic tactics
- `lia`: Linear arithmetic
- `nia`: Non-linear arithmetic
- `intuition`: Propositional logic

### Step 5: Manual Proof if Needed

If no lemma exists:
1. Prove by induction
2. Use related lemmas
3. Break into smaller lemmas
