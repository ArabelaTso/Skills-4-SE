# Isabelle/HOL Proof-Carrying Code

Comprehensive guide for generating proof-carrying code in Isabelle/HOL.

## Code Generation Basics

### Export Code Command

**Basic export:**
```isabelle
export_code function_name in SML file "output.sml"
```

**Multiple targets:**
```isabelle
export_code function_name in SML file "output.sml"
export_code function_name in OCaml file "output.ml"
export_code function_name in Haskell file "Output.hs"
export_code function_name in Scala file "Output.scala"
```

**Multiple functions:**
```isabelle
export_code func1 func2 func3 in SML file "output.sml"
```

### Code Equations

Control how definitions are translated to code.

**Default code equations:**
```isabelle
fun factorial :: "nat ⇒ nat" where
  "factorial 0 = 1" |
  "factorial (Suc n) = Suc n * factorial n"

(* Automatically generates code equations *)
```

**Custom code equations:**
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
  (* proof *)

(* Use efficient version for code *)
lemmas [code] = fast_reverse_def
declare slow_reverse.simps [code del]
```

## Verified Implementations

### Pattern 1: Direct Implementation with Proof

**Workflow:**
1. Implement function
2. State correctness property
3. Prove property
4. Export code

**Example: Verified sorting**
```isabelle
theory VerifiedSort
imports Main "HOL-Library.Multiset"
begin

(* Implementation *)
fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

(* Correctness properties *)
lemma insert_sorted:
  "sorted xs ⟹ sorted (insert x xs)"
  by (induction xs) auto

lemma mset_insert:
  "mset (insert x xs) = {#x#} + mset xs"
  by (induction xs) (auto simp: ac_simps)

theorem insertion_sort_correct:
  "sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs"
  by (induction xs) (auto simp: insert_sorted mset_insert)

(* Export certified code *)
export_code insertion_sort in SML file "insertion_sort.sml"

end
```

### Pattern 2: Refinement-Based

**Workflow:**
1. Abstract specification
2. Concrete implementation
3. Prove refinement
4. Export code

**Example: Verified search**
```isabelle
theory VerifiedSearch
imports Main
begin

(* Abstract specification *)
definition find_spec :: "'a list ⇒ ('a ⇒ bool) ⇒ 'a option" where
  "find_spec xs P = (if ∃x ∈ set xs. P x
                     then Some (SOME x. x ∈ set xs ∧ P x)
                     else None)"

(* Concrete implementation *)
fun find_impl :: "'a list ⇒ ('a ⇒ bool) ⇒ 'a option" where
  "find_impl [] P = None" |
  "find_impl (x # xs) P = (if P x then Some x else find_impl xs P)"

(* Refinement proof *)
theorem find_impl_refines:
  "find_impl xs P = find_spec xs P"
proof (induction xs)
  case Nil
  then show ?case by (simp add: find_spec_def)
next
  case (Cons x xs)
  then show ?case
    by (auto simp: find_spec_def split: if_splits)
       (metis (mono_tags, lifting) someI_ex)
qed

(* Export *)
export_code find_impl in OCaml file "find.ml"

end
```

## Safety Certification

### Memory Safety

**Pattern: Bounds-checked array access**
```isabelle
theory SafeArray
imports Main
begin

(* Safe array access *)
definition safe_nth :: "'a list ⇒ nat ⇒ 'a option" where
  "safe_nth xs i = (if i < length xs then Some (xs ! i) else None)"

(* Safety property *)
lemma safe_nth_bounds:
  "safe_nth xs i = Some v ⟹ i < length xs ∧ xs ! i = v"
  by (simp add: safe_nth_def split: if_splits)

lemma safe_nth_no_crash:
  "∀i. ∃result. safe_nth xs i = result"
  by auto

(* Export *)
export_code safe_nth in SML file "safe_array.sml"

end
```

### Null Safety

**Pattern: Non-empty list operations**
```isabelle
theory SafeList
imports Main
begin

(* Type for non-empty lists *)
typedef 'a nonempty_list = "{xs :: 'a list. xs ≠ []}"
  by (rule exI[of _ "[undefined]"]) simp

(* Safe head *)
definition ne_head :: "'a nonempty_list ⇒ 'a" where
  "ne_head xs = hd (Rep_nonempty_list xs)"

(* Safety property *)
lemma ne_head_safe:
  "∃v. ne_head xs = v"
  by (simp add: ne_head_def Rep_nonempty_list)

(* Constructor *)
definition ne_cons :: "'a ⇒ 'a list ⇒ 'a nonempty_list" where
  "ne_cons x xs = Abs_nonempty_list (x # xs)"

lemma ne_cons_nonempty:
  "Rep_nonempty_list (ne_cons x xs) = x # xs"
  by (simp add: ne_cons_def Abs_nonempty_list_inverse)

(* Export *)
export_code ne_head ne_cons in OCaml file "safe_list.ml"

end
```

### Division Safety

**Pattern: Non-zero divisor**
```isabelle
theory SafeArith
imports Main
begin

(* Safe division *)
definition safe_div :: "nat ⇒ nat ⇒ nat option" where
  "safe_div a b = (if b ≠ 0 then Some (a div b) else None)"

(* Safety property *)
lemma safe_div_no_error:
  "safe_div a b = Some q ⟹ b ≠ 0 ∧ a div b = q"
  by (simp add: safe_div_def split: if_splits)

(* Alternative: dependent type *)
definition safe_div_dep :: "nat ⇒ nat ⇒ nat" where
  "safe_div_dep a b = (if b = 0 then 0 else a div b)"

lemma safe_div_dep_correct:
  "b ≠ 0 ⟹ safe_div_dep a b = a div b"
  by (simp add: safe_div_dep_def)

(* Export *)
export_code safe_div in Haskell file "SafeArith.hs"

end
```

## Functional Correctness

### Specification-Based Verification

**Pattern: Prove implementation meets specification**
```isabelle
theory VerifiedGCD
imports Main
begin

(* Specification *)
definition gcd_spec :: "nat ⇒ nat ⇒ nat ⇒ bool" where
  "gcd_spec a b g ≡ g dvd a ∧ g dvd b ∧ (∀d. d dvd a ∧ d dvd b ⟶ d dvd g)"

(* Implementation *)
function gcd_impl :: "nat ⇒ nat ⇒ nat" where
  "gcd_impl a 0 = a" |
  "gcd_impl a b = gcd_impl b (a mod b)"
  by auto
termination
  by (relation "measure (λ(a, b). b)") auto

(* Correctness proof *)
theorem gcd_impl_correct:
  "gcd_spec a b (gcd_impl a b)"
proof (induction a b rule: gcd_impl.induct)
  case (1 a)
  then show ?case by (simp add: gcd_spec_def)
next
  case (2 a b)
  then show ?case
    by (auto simp: gcd_spec_def dvd_mod_iff)
qed

(* Export *)
export_code gcd_impl in SML file "gcd.sml"

end
```

### Invariant Preservation

**Pattern: Data structure invariants**
```isabelle
theory VerifiedBST
imports Main
begin

(* Binary search tree *)
datatype 'a tree = Leaf | Node "'a tree" 'a "'a tree"

(* BST invariant *)
fun bst :: "nat tree ⇒ bool" where
  "bst Leaf = True" |
  "bst (Node l x r) = (bst l ∧ bst r ∧
    (∀y ∈ set_tree l. y < x) ∧
    (∀y ∈ set_tree r. x < y))"

(* Insert operation *)
fun insert_bst :: "nat ⇒ nat tree ⇒ nat tree" where
  "insert_bst x Leaf = Node Leaf x Leaf" |
  "insert_bst x (Node l y r) =
    (if x < y then Node (insert_bst x l) y r
     else if y < x then Node l y (insert_bst x r)
     else Node l y r)"

(* Invariant preservation *)
theorem insert_preserves_bst:
  "bst t ⟹ bst (insert_bst x t)"
proof (induction t)
  case Leaf
  then show ?case by simp
next
  case (Node l y r)
  then show ?case by auto
qed

(* Export *)
export_code insert_bst in OCaml file "bst.ml"

end
```

## Code Generation with Refinement Framework

### Using Autoref

**Pattern: Automatic refinement to efficient data structures**
```isabelle
theory AutorefExample
imports "Refine_Monadic.Refine_Monadic"
        "Collections.Collections"
begin

(* Abstract algorithm on sets *)
definition abstract_filter :: "nat set ⇒ nat set" where
  "abstract_filter S = {x ∈ S. x > 5}"

(* Autoref automatically refines to list *)
schematic_goal concrete_filter:
  "(λxs. RETURN ?c, λS. RETURN (abstract_filter S))
   ∈ ⟨nat_rel⟩list_set_rel → ⟨⟨nat_rel⟩list_set_rel⟩nres_rel"
  unfolding abstract_filter_def
  by autoref

(* Extract concrete implementation *)
concrete_definition filter_impl uses concrete_filter
export_code filter_impl in SML file "filter.sml"

end
```

### Using Sepref

**Pattern: Imperative code with arrays**
```isabelle
theory SeprefExample
imports "Refine_Imperative_HOL.IICF"
begin

(* Functional specification *)
definition array_sum :: "nat list ⇒ nat" where
  "array_sum xs = fold (+) xs 0"

(* Imperative implementation *)
sepref_definition array_sum_impl is
  "RETURN ∘ array_sum" :: "(array_assn nat_assn)⇧k →⇩a nat_assn"
  unfolding array_sum_def
  by sepref

(* Export *)
export_code array_sum_impl in SML file "array_sum.sml"

end
```

## Termination Proofs

### Well-Founded Recursion

**Pattern: Prove termination with decreasing measure**
```isabelle
theory TerminationExample
imports Main
begin

(* Ackermann function *)
function ackermann :: "nat ⇒ nat ⇒ nat" where
  "ackermann 0 n = n + 1" |
  "ackermann (Suc m) 0 = ackermann m 1" |
  "ackermann (Suc m) (Suc n) = ackermann m (ackermann (Suc m) n)"
  by auto
termination
  by (relation "measure (λ(m, n). m) <*lex*> measure (λ(m, n). n)") auto

(* Termination certificate *)
lemma ackermann_terminates:
  "∃result. ackermann m n = result"
  by auto

(* Export *)
export_code ackermann in Haskell file "Ackermann.hs"

end
```

## Complete Example: Verified Quicksort

```isabelle
theory VerifiedQuicksort
imports Main "HOL-Library.Multiset"
begin

(* Partition function *)
fun partition :: "nat ⇒ nat list ⇒ nat list × nat list" where
  "partition p [] = ([], [])" |
  "partition p (x # xs) =
    (let (ls, rs) = partition p xs in
     if x ≤ p then (x # ls, rs) else (ls, x # rs))"

(* Quicksort *)
function quicksort :: "nat list ⇒ nat list" where
  "quicksort [] = []" |
  "quicksort (p # xs) =
    (let (ls, rs) = partition p xs in
     quicksort ls @ [p] @ quicksort rs)"
  by auto
termination
  by (relation "measure length") auto

(* Partition properties *)
lemma partition_mset:
  "partition p xs = (ls, rs) ⟹
   mset ls + mset rs = mset xs"
  by (induction xs arbitrary: ls rs) (auto split: prod.splits)

lemma partition_bounds:
  "partition p xs = (ls, rs) ⟹
   (∀x ∈ set ls. x ≤ p) ∧ (∀x ∈ set rs. x > p)"
  by (induction xs arbitrary: ls rs) (auto split: prod.splits)

(* Correctness *)
theorem quicksort_sorted:
  "sorted (quicksort xs)"
proof (induction xs rule: quicksort.induct)
  case 1
  then show ?case by simp
next
  case (2 p xs)
  obtain ls rs where part: "partition p xs = (ls, rs)"
    by (cases "partition p xs") auto
  have "sorted (quicksort ls)" using 2 part by simp
  moreover have "sorted (quicksort rs)" using 2 part by simp
  moreover have "∀x ∈ set (quicksort ls). x ≤ p"
    using partition_bounds[OF part] by auto
  moreover have "∀x ∈ set (quicksort rs). x > p"
    using partition_bounds[OF part] by auto
  ultimately show ?case
    by (simp add: part sorted_append)
qed

theorem quicksort_mset:
  "mset (quicksort xs) = mset xs"
proof (induction xs rule: quicksort.induct)
  case 1
  then show ?case by simp
next
  case (2 p xs)
  obtain ls rs where part: "partition p xs = (ls, rs)"
    by (cases "partition p xs") auto
  have "mset (quicksort ls) = mset ls" using 2 part by simp
  moreover have "mset (quicksort rs) = mset rs" using 2 part by simp
  moreover have "mset ls + mset rs = mset xs"
    using partition_mset[OF part] by simp
  ultimately show ?case
    by (simp add: part ac_simps)
qed

(* Combined correctness *)
theorem quicksort_correct:
  "sorted (quicksort xs) ∧ mset (quicksort xs) = mset xs"
  using quicksort_sorted quicksort_mset by blast

(* Export certified code *)
export_code quicksort in SML file "quicksort.sml"
export_code quicksort in OCaml file "quicksort.ml"
export_code quicksort in Haskell file "Quicksort.hs"

end
```

## Code Generation Options

### Optimization

**Efficient data structures:**
```isabelle
(* Use efficient set implementation *)
code_printing
  type_constructor set ⇀ (SML) "_ Set.set"

(* Use efficient map implementation *)
code_printing
  type_constructor map ⇀ (SML) "(_, _) Map.map"
```

### Custom Serialization

**Control code generation:**
```isabelle
code_printing
  constant my_function ⇀ (SML) "MyModule.my_function"
```

## Testing Extracted Code

**Pattern: Generate test harness**
```isabelle
(* Test function *)
definition test_sort :: "nat list list ⇒ bool" where
  "test_sort tests = list_all (λxs. sorted (quicksort xs)) tests"

(* Export with tests *)
export_code quicksort test_sort in SML file "quicksort_test.sml"
```
