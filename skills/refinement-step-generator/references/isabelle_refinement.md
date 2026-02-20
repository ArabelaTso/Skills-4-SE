# Isabelle/HOL Refinement Framework

Comprehensive guide for refinement in Isabelle/HOL using the Refinement Framework and Autoref.

## Refinement Framework Basics

### The Refinement Relation (⊑)

The refinement relation `c ⊑ a` means concrete `c` refines abstract `a`.

```isabelle
definition refines :: "'c ⇒ 'a ⇒ bool" (infix "⊑" 50) where
  "c ⊑ a ≡ (∀r. c → r ⟶ a → r)"
```

**Properties:**
- Reflexive: `a ⊑ a`
- Transitive: `a ⊑ b ∧ b ⊑ c ⟹ a ⊑ c`
- Monotonic with respect to operations

### Basic Refinement Example

```isabelle
theory Simple_Refinement
imports Main
begin

(* Abstract specification *)
definition abs_add :: "nat set ⇒ nat ⇒ nat set" where
  "abs_add S x = S ∪ {x}"

(* Concrete implementation *)
definition conc_add :: "nat list ⇒ nat ⇒ nat list" where
  "conc_add xs x = (if x ∈ set xs then xs else x # xs)"

(* Abstraction function *)
definition α :: "nat list ⇒ nat set" where
  "α xs = set xs"

(* Refinement proof *)
lemma conc_add_refines:
  "α (conc_add xs x) = abs_add (α xs) x"
  by (auto simp: conc_add_def abs_add_def α_def)

end
```

## Data Refinement Patterns

### Set Refinement

**Set → List:**
```isabelle
definition set_to_list_α :: "'a list ⇒ 'a set" where
  "set_to_list_α xs = set xs"

lemma set_empty_refines:
  "set_to_list_α [] = {}"
  by (simp add: set_to_list_α_def)

lemma set_insert_refines:
  "set_to_list_α (x # xs) = insert x (set_to_list_α xs)"
  by (simp add: set_to_list_α_def)
```

**Set → Red-Black Tree:**
```isabelle
datatype 'a rbt = Empty | Node color "'a rbt" 'a "'a rbt"

fun rbt_to_set :: "'a::linorder rbt ⇒ 'a set" where
  "rbt_to_set Empty = {}" |
  "rbt_to_set (Node _ l x r) = {x} ∪ rbt_to_set l ∪ rbt_to_set r"

fun rbt_insert :: "'a::linorder ⇒ 'a rbt ⇒ 'a rbt" where
  (* Implementation details *)

lemma rbt_insert_refines:
  "rbt_to_set (rbt_insert x t) = insert x (rbt_to_set t)"
  (* Proof by induction *)
```

### Map Refinement

**Map → Association List:**
```isabelle
type_synonym ('k, 'v) alist = "('k × 'v) list"

definition alist_to_map :: "('k, 'v) alist ⇒ 'k ⇀ 'v" where
  "alist_to_map xs = map_of xs"

definition alist_lookup :: "'k ⇒ ('k, 'v) alist ⇒ 'v option" where
  "alist_lookup k xs = map_of xs k"

definition alist_update :: "'k ⇒ 'v ⇒ ('k, 'v) alist ⇒ ('k, 'v) alist" where
  "alist_update k v xs = (k, v) # filter (λ(k', _). k' ≠ k) xs"

lemma alist_update_refines:
  "alist_to_map (alist_update k v xs) = (alist_to_map xs)(k ↦ v)"
  by (auto simp: alist_update_def alist_to_map_def)
```

## Autoref Framework

Autoref provides automatic refinement for data structures and operations.

### Basic Autoref Usage

```isabelle
theory Autoref_Example
imports "Refine_Monadic.Refine_Monadic"
        "Collections.Collections"
begin

(* Abstract algorithm *)
definition abstract_algo :: "nat set ⇒ nat set" where
  "abstract_algo S = {x ∈ S. x > 5}"

(* Autoref automatically refines to list implementation *)
schematic_goal concrete_algo:
  "(λxs. RETURN ?c) ⊑ (λS. RETURN (abstract_algo S))"
  unfolding abstract_algo_def
  by (autoref (keep_goal))

(* Extract concrete implementation *)
concrete_definition concrete_algo_impl uses concrete_algo
export_code concrete_algo_impl in SML
```

### Autoref Data Structure Annotations

```isabelle
(* Specify implementation types *)
context
  fixes S :: "nat set"
  assumes [autoref_rules]: "(Si, S) ∈ ⟨nat_rel⟩list_set_rel"
begin

(* Operations are automatically refined *)
definition filtered :: "nat set" where
  "filtered = {x ∈ S. x mod 2 = 0}"

schematic_goal filtered_impl:
  "(λSi. RETURN ?c, λS. RETURN filtered) ∈ ⟨nat_rel⟩list_set_rel → ⟨⟨nat_rel⟩list_set_rel⟩nres_rel"
  unfolding filtered_def
  by autoref

end
```

### Custom Autoref Rules

```isabelle
(* Define custom data structure *)
datatype 'a my_set = MySet "'a list"

(* Define abstraction relation *)
definition my_set_rel :: "('a × 'a) set ⇒ ('a my_set × 'a set) set" where
  "my_set_rel R = {(MySet xs, S). (xs, S) ∈ ⟨R⟩list_set_rel}"

(* Register operations *)
definition my_set_empty :: "'a my_set" where
  "my_set_empty = MySet []"

definition my_set_insert :: "'a ⇒ 'a my_set ⇒ 'a my_set" where
  "my_set_insert x (MySet xs) = MySet (x # xs)"

(* Autoref rules *)
lemma [autoref_rules]:
  "(my_set_empty, {}) ∈ ⟨R⟩my_set_rel"
  by (auto simp: my_set_rel_def my_set_empty_def list_set_rel_def)

lemma [autoref_rules]:
  "(my_set_insert, insert) ∈ R → ⟨R⟩my_set_rel → ⟨R⟩my_set_rel"
  by (auto simp: my_set_rel_def my_set_insert_def list_set_rel_def)
```

## Sepref: Imperative Refinement

Sepref refines functional programs to imperative programs with arrays and mutable state.

### Basic Sepref Example

```isabelle
theory Sepref_Example
imports "Refine_Imperative_HOL.IICF"
begin

(* Functional specification *)
definition sum_list :: "nat list ⇒ nat" where
  "sum_list xs = fold (+) xs 0"

(* Imperative implementation *)
sepref_definition sum_list_impl is
  "uncurry0 (RETURN (sum_list xs))" :: "unit_assn⇧k →⇩a nat_assn"
  unfolding sum_list_def
  by sepref

(* Export to Imperative/HOL *)
export_code sum_list_impl in SML
```

### Array Operations with Sepref

```isabelle
(* Swap array elements *)
definition swap_spec :: "nat list ⇒ nat ⇒ nat ⇒ nat list" where
  "swap_spec xs i j = xs[i := xs ! j, j := xs ! i]"

sepref_definition swap_impl is
  "uncurry2 (λxs i j. RETURN (swap_spec xs i j))"
  :: "(array_assn nat_assn)⇧d *⇩a nat_assn⇧k *⇩a nat_assn⇧k →⇩a array_assn nat_assn"
  unfolding swap_spec_def
  by sepref

(* In-place array modification *)
definition increment_all :: "nat list ⇒ nat list" where
  "increment_all xs = map (λx. x + 1) xs"

sepref_definition increment_all_impl is
  "RETURN ∘ increment_all" :: "(array_assn nat_assn)⇧d →⇩a array_assn nat_assn"
  unfolding increment_all_def
  by sepref
```

## Monadic Refinement

Use the Refine_Monadic framework for nondeterministic and monadic refinement.

### Nondeterministic Specifications

```isabelle
theory Monadic_Refinement
imports "Refine_Monadic.Refine_Monadic"
begin

(* Nondeterministic specification *)
definition find_any :: "nat list ⇒ (nat ⇒ bool) ⇒ nat option nres" where
  "find_any xs P = SPEC (λr. case r of
    None ⇒ ∀x ∈ set xs. ¬P x |
    Some x ⇒ x ∈ set xs ∧ P x)"

(* Deterministic refinement *)
definition find_first :: "nat list ⇒ (nat ⇒ bool) ⇒ nat option nres" where
  "find_first xs P = RETURN (List.find P xs)"

lemma find_first_refines:
  "find_first xs P ⊑ find_any xs P"
  unfolding find_any_def find_first_def
  by (auto simp: RETURN_def SPEC_def find_Some_iff)
```

### Monadic Combinators

```isabelle
(* Sequential composition *)
definition seq_example :: "nat ⇒ nat nres" where
  "seq_example n = do {
    x ← RETURN (n + 1);
    y ← RETURN (x * 2);
    RETURN (y - 1)
  }"

(* Conditional *)
definition cond_example :: "nat ⇒ nat nres" where
  "cond_example n = do {
    if n > 10 then
      RETURN (n * 2)
    else
      RETURN (n + 5)
  }"

(* Loops *)
definition loop_example :: "nat ⇒ nat nres" where
  "loop_example n = do {
    (i, acc) ← WHILEIT
      (λ(i, acc). i ≤ n ∧ acc = sum_upto i)
      (λ(i, acc). i < n)
      (λ(i, acc). RETURN (i + 1, acc + i + 1))
      (0, 0);
    RETURN acc
  }"
```

## Code Generation

Generate executable code from refined specifications.

### Basic Code Export

```isabelle
(* Define function *)
fun fibonacci :: "nat ⇒ nat" where
  "fibonacci 0 = 0" |
  "fibonacci (Suc 0) = 1" |
  "fibonacci (Suc (Suc n)) = fibonacci n + fibonacci (Suc n)"

(* Export to various languages *)
export_code fibonacci in SML file "fib.sml"
export_code fibonacci in OCaml file "fib.ml"
export_code fibonacci in Haskell file "Fib.hs"
export_code fibonacci in Scala file "Fib.scala"
```

### Code Equations

```isabelle
(* Inefficient definition *)
fun slow_reverse :: "'a list ⇒ 'a list" where
  "slow_reverse [] = []" |
  "slow_reverse (x # xs) = slow_reverse xs @ [x]"

(* Efficient implementation *)
fun fast_reverse_aux :: "'a list ⇒ 'a list ⇒ 'a list" where
  "fast_reverse_aux [] acc = acc" |
  "fast_reverse_aux (x # xs) acc = fast_reverse_aux xs (x # acc)"

definition fast_reverse :: "'a list ⇒ 'a list" where
  "fast_reverse xs = fast_reverse_aux xs []"

(* Prove equivalence *)
lemma fast_reverse_correct:
  "fast_reverse xs = slow_reverse xs"
  (* Proof *)

(* Use efficient version for code generation *)
declare fast_reverse_def[code]
declare slow_reverse.simps[code del]
```

## Complete Refinement Example

```isabelle
theory Complete_Example
imports "Refine_Monadic.Refine_Monadic" "Collections.Collections"
begin

(* Abstract specification: find maximum in set *)
definition find_max_spec :: "nat set ⇒ nat option" where
  "find_max_spec S = (if S = {} then None else Some (Max S))"

(* Refinement 1: List-based algorithm *)
definition find_max_list :: "nat list ⇒ nat option nres" where
  "find_max_list xs = SPEC (λr. r = find_max_spec (set xs))"

(* Refinement 2: Concrete algorithm *)
fun find_max_impl :: "nat list ⇒ nat option" where
  "find_max_impl [] = None" |
  "find_max_impl (x # xs) = (case find_max_impl xs of
    None ⇒ Some x |
    Some m ⇒ Some (max x m))"

(* Correctness proof *)
lemma find_max_impl_correct:
  "find_max_impl xs = find_max_spec (set xs)"
  by (induction xs) (auto simp: find_max_spec_def)

(* Autoref refinement *)
schematic_goal find_max_autoref:
  "(λxs. RETURN (find_max_impl xs), λS. RETURN (find_max_spec S))
   ∈ ⟨nat_rel⟩list_set_rel → ⟨⟨Id⟩option_rel⟩nres_rel"
  by (autoref (keep_goal))

end
```
