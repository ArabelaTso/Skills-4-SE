# Coq Standard Library Guide

## Table of Contents
1. Core Libraries
2. List Library
3. Set Libraries
4. Arithmetic Libraries
5. Logic and Relations
6. Common Lemmas by Category

## 1. Core Libraries

### Init (Automatically Loaded)

**Datatypes**:
- `bool`, `nat`, `option`, `sum`, `prod`

**Logic**:
- `True`, `False`, `and`, `or`, `not`, `iff`

### Logic

**Import**: `Require Import Logic.`

**Key lemmas**:
- `eq_refl`: `x = x`
- `eq_sym`: `x = y -> y = x`
- `eq_trans`: `x = y -> y = z -> x = z`
- `f_equal`: `x = y -> f x = f y`
- `and_intro`: `A -> B -> A /\ B`
- `or_introl`: `A -> A \/ B`
- `or_intror`: `B -> A \/ B`

## 2. List Library

**Import**: `Require Import List. Import ListNotations.`

### Basic Operations

**Constructors**:
- `nil` or `[]`: Empty list
- `cons x xs` or `x :: xs`: Cons

**Functions**:
- `hd : A -> list A -> A`: Head with default
- `tl : list A -> list A`: Tail
- `length : list A -> nat`: Length
- `rev : list A -> list A`: Reverse
- `app : list A -> list A -> list A` or `++`: Append
- `nth : nat -> list A -> A -> A`: Nth element with default
- `map : (A -> B) -> list A -> list B`: Map
- `filter : (A -> bool) -> list A -> list A`: Filter
- `fold_left`, `fold_right`: Fold operations

### Key Lemmas

**Length**:
- `length_nil`: `length [] = 0`
- `length_cons`: `length (x :: xs) = S (length xs)`
- `app_length`: `length (l1 ++ l2) = length l1 + length l2`
- `rev_length`: `length (rev l) = length l`
- `map_length`: `length (map f l) = length l`

**Append**:
- `app_nil_l`: `[] ++ l = l`
- `app_nil_r`: `l ++ [] = l`
- `app_assoc`: `(l1 ++ l2) ++ l3 = l1 ++ (l2 ++ l3)`
- `app_comm_cons`: `(x :: l1) ++ l2 = x :: (l1 ++ l2)`

**Reverse**:
- `rev_involutive`: `rev (rev l) = l`
- `rev_app_distr`: `rev (l1 ++ l2) = rev l2 ++ rev l1`
- `rev_unit`: `rev [x] = [x]`

**Map**:
- `map_app`: `map f (l1 ++ l2) = map f l1 ++ map f l2`
- `map_map`: `map f (map g l) = map (fun x => f (g x)) l`
- `map_id`: `map (fun x => x) l = l`
- `map_rev`: `map f (rev l) = rev (map f l)`

**In (Membership)**:
- `in_eq`: `In x (x :: l)`
- `in_cons`: `In x l -> In x (y :: l)`
- `in_app_iff`: `In x (l1 ++ l2) <-> In x l1 \/ In x l2`
- `in_rev`: `In x (rev l) <-> In x l`
- `in_map_iff`: `In y (map f l) <-> exists x, f x = y /\ In x l`

**Nth**:
- `nth_In`: `n < length l -> In (nth n l d) l`
- `nth_overflow`: `length l <= n -> nth n l d = d`

## 3. Set Libraries

### Sets (MSets)

**Import**: `Require Import MSets.`

**Modules**:
- `MSetWeakList`: Sets as lists
- `MSetAVL`: Sets as AVL trees

**Operations**:
- `empty`: Empty set
- `add`: Add element
- `remove`: Remove element
- `mem`: Membership test
- `union`, `inter`, `diff`: Set operations
- `subset`: Subset test
- `equal`: Equality test

### FSet (Finite Sets)

**Import**: `Require Import FSet.`

Similar to MSets but older interface.

## 4. Arithmetic Libraries

### Arith (Natural Numbers)

**Import**: `Require Import Arith.`

**Operations**:
- `+`, `-`, `*`: Arithmetic operations
- `<`, `<=`, `>`, `>=`: Comparisons
- `min`, `max`: Min/max

**Key Lemmas**:
- `plus_0_l`: `0 + n = n`
- `plus_0_r`: `n + 0 = n`
- `plus_comm`: `n + m = m + n`
- `plus_assoc`: `(n + m) + p = n + (m + p)`
- `mult_0_l`: `0 * n = 0`
- `mult_0_r`: `n * 0 = 0`
- `mult_1_l`: `1 * n = n`
- `mult_1_r`: `n * 1 = n`
- `mult_comm`: `n * m = m * n`
- `mult_assoc`: `(n * m) * p = n * (m * p)`
- `mult_plus_distr_r`: `(n + m) * p = n * p + m * p`

### Lia (Linear Integer Arithmetic)

**Import**: `Require Import Lia.`

**Tactic**: `lia` - Solves linear arithmetic goals

**Use for**:
- Linear inequalities
- Equations over integers/naturals
- Combination of arithmetic facts

### Nia (Non-linear Integer Arithmetic)

**Import**: `Require Import Nia.`

**Tactic**: `nia` - Solves non-linear arithmetic

**Use for**:
- Multiplication in goals
- Polynomial inequalities

### ZArith (Integers)

**Import**: `Require Import ZArith.`

**Type**: `Z` (integers)

**Operations**: Similar to nat but with negative numbers

### QArith (Rationals)

**Import**: `Require Import QArith.`

**Type**: `Q` (rationals)

### Reals

**Import**: `Require Import Reals.`

**Type**: `R` (real numbers)

## 5. Logic and Relations

### Relations

**Import**: `Require Import Relations.`

**Definitions**:
- `reflexive`: `forall x, R x x`
- `symmetric`: `forall x y, R x y -> R y x`
- `transitive`: `forall x y z, R x y -> R y z -> R x z`
- `equivalence`: Reflexive, symmetric, and transitive

### Setoid

**Import**: `Require Import Setoid.`

**Use for**: Rewriting with equivalence relations

## 6. Common Lemmas by Category

### Equality and Rewriting

When proving: `x = y`
- `eq_refl`, `eq_sym`, `eq_trans`
- `f_equal`: `x = y -> f x = f y`
- `f_equal2`: `x1 = y1 -> x2 = y2 -> f x1 x2 = f y1 y2`

When rewriting:
- `rewrite H`: Rewrite using hypothesis
- `rewrite <- H`: Rewrite right-to-left
- `rewrite H in H'`: Rewrite in hypothesis

### Conjunction and Disjunction

When proving: `A /\ B`
- `split`: Split into two goals
- `constructor`: Same as split

When proving: `A \/ B`
- `left`: Prove A
- `right`: Prove B

When using: `A /\ B`
- `destruct H as [HA HB]`: Extract both parts

When using: `A \/ B`
- `destruct H as [HA | HB]`: Case analysis

### Implication

When proving: `A -> B`
- `intro H`: Assume A as H

When using: `A -> B` and `A`
- `apply H`: Apply implication
- `apply H in HA`: Apply to hypothesis

### Quantifiers

When proving: `forall x, P x`
- `intro x` or `intros x`: Introduce variable

When proving: `exists x, P x`
- `exists witness`: Provide witness

When using: `forall x, P x`
- `specialize (H value)`: Instantiate
- `apply H`: Apply to goal

When using: `exists x, P x`
- `destruct H as [x Hx]`: Extract witness

### Induction

For lists:
- `induction l as [| x xs IHxs]`: List induction

For natural numbers:
- `induction n as [| n' IHn']`: Nat induction
- `induction n using lt_wf_ind`: Strong induction

### Arithmetic

For linear arithmetic:
- `lia`: Automatic solver

For non-linear:
- `nia`: Non-linear solver

For simplification:
- `simpl`: Simplify expressions
- `ring`: Ring solver for equations

### Boolean Reflection

**Import**: `Require Import Bool.`

**Lemmas**:
- `eqb_true_iff`: `n =? m = true <-> n = m`
- `leb_le`: `n <=? m = true <-> n <= m`
- `ltb_lt`: `n <? m = true <-> n < m`

## Finding Lemmas

### Using Search

```coq
Search rev.
Search (_ ++ _).
Search (?x + ?y = ?y + ?x).
Search "comm" (_ + _).
```

### Using SearchAbout (deprecated, use Search)

```coq
Search length.
Search In map.
```

### Using Locate

```coq
Locate "++".
Locate "<=".
```

### Using Print

```coq
Print list.
Print length.
```

## Common Library Combinations

### For List Proofs

```coq
Require Import List.
Require Import Arith.
Require Import Lia.
Import ListNotations.
```

### For Arithmetic Proofs

```coq
Require Import Arith.
Require Import Lia.
Require Import Nia.
```

### For Set Proofs

```coq
Require Import MSets.
Require Import List.
Import ListNotations.
```

## Useful Tactics by Goal Type

### List Goals
- `induction l`: List induction
- `simpl`: Simplify list operations
- `rewrite app_assoc`: Associativity
- `rewrite in_app_iff`: Membership in append

### Arithmetic Goals
- `lia`: Linear arithmetic
- `nia`: Non-linear arithmetic
- `ring`: Ring equations
- `omega`: (deprecated, use lia)

### Equality Goals
- `reflexivity`: Prove x = x
- `rewrite`: Rewrite using equality
- `f_equal`: Apply function to both sides

### Boolean Goals
- `destruct b`: Case analysis on boolean
- `rewrite eqb_true_iff`: Reflect to Prop
- `apply Bool.andb_true_iff`: And reflection
