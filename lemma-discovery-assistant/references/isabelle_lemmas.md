# Isabelle/HOL Lemma Discovery

Comprehensive guide for discovering and using lemmas in Isabelle/HOL.

## Automatic Lemma Discovery

### Sledgehammer

Sledgehammer is Isabelle's most powerful automatic proof tool that searches for relevant lemmas.

**Basic usage:**
```isabelle
lemma "P"
  by sledgehammer
```

**With timeout:**
```isabelle
lemma "P"
  by (sledgehammer [timeout = 60])
```

**Selecting provers:**
```isabelle
lemma "P"
  by (sledgehammer [provers = e spass z3])
```

**Example:**
```isabelle
lemma "length (xs @ ys) = length xs + length ys"
  by sledgehammer
(* Sledgehammer finds: by (simp add: length_append) *)
```

### Try and Try0

Quick proof search tactics.

**try:** Attempts various proof methods
```isabelle
lemma "sorted []"
  by try
```

**try0:** Faster version, tries only basic tactics
```isabelle
lemma "x + 0 = x"
  by try0
```

## Finding Existing Lemmas

### Find Theorems

Search for lemmas by pattern or name.

**By pattern:**
```isabelle
find_theorems "length (_ @ _)"
(* Finds: length_append, length_append_singleton, etc. *)
```

**By name:**
```isabelle
find_theorems name: "append"
(* Finds all lemmas with "append" in name *)
```

**With constraints:**
```isabelle
find_theorems "length ?xs = ?n" "?xs @ ?ys"
(* Finds lemmas matching both patterns *)
```

**Excluding patterns:**
```isabelle
find_theorems "_ + _" -"_ * _"
(* Finds addition lemmas, excluding multiplication *)
```

### Print Theorems

List all available theorems.

```isabelle
print_theorems
(* Lists all theorems in current context *)
```

## Common Lemma Patterns

### List Lemmas

**Append properties:**
```isabelle
lemma append_Nil: "xs @ [] = xs"
lemma append_Nil2: "[] @ xs = xs"
lemma append_assoc: "(xs @ ys) @ zs = xs @ (ys @ zs)"
lemma length_append: "length (xs @ ys) = length xs + length ys"
```

**Map properties:**
```isabelle
lemma map_append: "map f (xs @ ys) = map f xs @ map f ys"
lemma map_map: "map f (map g xs) = map (f ∘ g) xs"
lemma map_ident: "map id xs = xs"
lemma length_map: "length (map f xs) = length xs"
```

**Filter properties:**
```isabelle
lemma filter_append: "filter P (xs @ ys) = filter P xs @ filter P ys"
lemma filter_filter: "filter P (filter Q xs) = filter (λx. P x ∧ Q x) xs"
lemma length_filter_le: "length (filter P xs) ≤ length xs"
```

**Reverse properties:**
```isabelle
lemma rev_append: "rev (xs @ ys) = rev ys @ rev xs"
lemma rev_rev_ident: "rev (rev xs) = xs"
lemma length_rev: "length (rev xs) = length xs"
```

### Arithmetic Lemmas

**Addition:**
```isabelle
lemma add_0: "0 + n = n"
lemma add_0_right: "n + 0 = n"
lemma add_commute: "m + n = n + m"
lemma add_assoc: "(m + n) + p = m + (n + p)"
lemma add_left_cancel: "k + m = k + n ⟹ m = n"
```

**Multiplication:**
```isabelle
lemma mult_0: "0 * n = 0"
lemma mult_1: "1 * n = n"
lemma mult_commute: "m * n = n * m"
lemma mult_assoc: "(m * n) * p = m * (n * p)"
lemma mult_distrib: "(m + n) * p = m * p + n * p"
```

**Ordering:**
```isabelle
lemma le_refl: "n ≤ n"
lemma le_trans: "⟦ i ≤ j; j ≤ k ⟧ ⟹ i ≤ k"
lemma le_antisym: "⟦ m ≤ n; n ≤ m ⟧ ⟹ m = n"
lemma add_le_mono: "⟦ i ≤ j; k ≤ l ⟧ ⟹ i + k ≤ j + l"
```

### Set Lemmas

**Basic operations:**
```isabelle
lemma Un_empty: "A ∪ {} = A"
lemma Un_commute: "A ∪ B = B ∪ A"
lemma Un_assoc: "(A ∪ B) ∪ C = A ∪ (B ∪ C)"
lemma Int_empty: "A ∩  = {}"
lemma Int_commute: "A ∩ B = B ∩ A"
```

**Membership:**
```isabelle
lemma mem_Un: "x ∈ A ∪ B ⟷ x ∈ A ∨ x ∈ B"
lemma mem_Int: "x ∈ A ∩ B ⟷ x ∈ A ∧ x ∈ B"
lemma mem_Diff: "x ∈ A - B ⟷ x ∈ A ∧ x ∉ B"
```

## Induction Lemmas

### Strengthening Induction Hypotheses

**Problem:** Induction hypothesis too weak.

**Pattern:** Generalize the statement.

**Example:**
```isabelle
(* Too specific *)
lemma "sum_upto n = n * (n + 1) div 2"
  (* Fails: need to generalize *)

(* Generalized with accumulator *)
lemma sum_upto_acc: "sum_upto_acc n acc = acc + n * (n + 1) div 2"
proof (induction n arbitrary: acc)
  case 0
  then show ?case by simp
next
  case (Suc n)
  then show ?case by simp
qed
```

### Mutual Induction

**Pattern:** Prove multiple properties simultaneously.

**Example:**
```isabelle
lemma even_odd:
  "even n ⟷ ¬ odd n"
  "odd n ⟷ ¬ even n"
proof (induction n)
  case 0
  then show "even 0 ⟷ ¬ odd 0" by simp
  then show "odd 0 ⟷ ¬ even 0" by simp
next
  case (Suc n)
  then show "even (Suc n) ⟷ ¬ odd (Suc n)" by simp
  then show "odd (Suc n) ⟷ ¬ even (Suc n)" by simp
qed
```

### Rule Induction

**Pattern:** Induction on inductively defined predicates.

**Example:**
```isabelle
inductive even :: "nat ⇒ bool" where
  even_0: "even 0" |
  even_SS: "even n ⟹ even (Suc (Suc n))"

lemma even_double: "even n ⟹ ∃k. n = 2 * k"
proof (induction rule: even.induct)
  case even_0
  then show ?case by (rule exI[of _ 0]) simp
next
  case (even_SS n)
  then obtain k where "n = 2 * k" by blast
  then show ?case by (rule exI[of _ "Suc k"]) simp
qed
```

## Simplification Lemmas

### Adding to Simpset

**Declare as simp rule:**
```isabelle
declare my_lemma [simp]
```

**Conditional simp rule:**
```isabelle
lemma my_cond_simp [simp]: "P ⟹ f x = g x"
```

**Remove from simpset:**
```isabelle
declare my_lemma [simp del]
```

### Rewrite Lemmas

**Pattern:** Equations for simplification.

**Example:**
```isabelle
lemma comp_apply [simp]: "(f ∘ g) x = f (g x)"
  by (simp add: comp_def)

lemma id_apply [simp]: "id x = x"
  by (simp add: id_def)

lemma const_apply [simp]: "const c x = c"
  by (simp add: const_def)
```

## Case Analysis Lemmas

### Split Rules

**Pattern:** Case split for conditional expressions.

**Example:**
```isabelle
lemma if_split: "P (if c then x else y) = ((c ⟶ P x) ∧ (¬c ⟶ P y))"
  by auto

lemma case_split: "P (case xs of [] ⇒ a | _ ⇒ b) =
  ((xs = [] ⟶ P a) ∧ (xs ≠ [] ⟶ P b))"
  by (cases xs) auto
```

### Exhaustiveness Lemmas

**Pattern:** Cover all cases of a datatype.

**Example:**
```isabelle
lemma list_cases: "xs = [] ∨ (∃y ys. xs = y # ys)"
  by (cases xs) auto

lemma nat_cases: "n = 0 ∨ (∃m. n = Suc m)"
  by (cases n) auto
```

## Proof Automation

### Auto and Simp

**auto:** Applies classical reasoning and simplification
```isabelle
lemma "P ∧ Q ⟹ Q ∧ P"
  by auto
```

**simp:** Applies simplification rules
```isabelle
lemma "xs @ [] = xs"
  by simp
```

**simp with additional rules:**
```isabelle
lemma "..."
  by (simp add: my_lemma1 my_lemma2)
```

### Blast and Force

**blast:** Fast classical reasoner
```isabelle
lemma "⟦ P ⟶ Q; Q ⟶ R; P ⟧ ⟹ R"
  by blast
```

**force:** Combines auto and blast
```isabelle
lemma "..."
  by force
```

### Clarify and Safe

**clarify:** Performs safe steps without splitting
```isabelle
lemma "..."
  by clarify
```

**safe:** Performs all safe steps
```isabelle
lemma "..."
  by safe
```

## Specialized Lemmas

### Monotonicity Lemmas

**Pattern:** Preserve ordering.

**Example:**
```isabelle
lemma map_mono: "⟦ ∀x ∈ set xs. f x ≤ g x ⟧ ⟹
  map f xs ≤ map g xs"
  by (induction xs) auto

lemma filter_mono: "⟦ ∀x. P x ⟶ Q x ⟧ ⟹
  set (filter P xs) ⊆ set (filter Q xs)"
  by auto
```

### Injectivity Lemmas

**Pattern:** Function is injective.

**Example:**
```isabelle
lemma Suc_inject: "Suc m = Suc n ⟹ m = n"
  by simp

lemma Cons_inject: "x # xs = y # ys ⟹ x = y ∧ xs = ys"
  by simp
```

### Distinctness Lemmas

**Pattern:** Constructors are distinct.

**Example:**
```isabelle
lemma Nil_not_Cons: "[] ≠ x # xs"
  by simp

lemma Zero_not_Suc: "0 ≠ Suc n"
  by simp
```

## Lemma Discovery Workflow

### Step 1: Try Automatic Tools

```isabelle
lemma "goal"
  by sledgehammer
  (* or *)
  by try
  (* or *)
  by auto
```

### Step 2: Search for Relevant Lemmas

```isabelle
find_theorems "pattern"
```

### Step 3: Manual Proof with Lemmas

```isabelle
lemma "goal"
proof -
  have "intermediate" by (simp add: lemma1)
  then show ?thesis by (simp add: lemma2)
qed
```

### Step 4: Identify Missing Lemmas

If proof fails, identify what's missing and propose new lemma.

## Example: Complete Discovery

**Goal:**
```isabelle
lemma "length (filter P (map f xs)) ≤ length xs"
```

**Attempt 1:**
```isabelle
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  (* Stuck: need lemma about length of filter *)
  then show ?case sorry
qed
```

**Search for lemmas:**
```isabelle
find_theorems "length (filter _ _)"
(* Finds: length_filter_le *)
```

**Attempt 2:**
```isabelle
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  (* Still stuck: need lemma about filter and map *)
  then show ?case sorry
qed
```

**Propose new lemma:**
```isabelle
lemma filter_map: "filter P (map f xs) = map f (filter (P ∘ f) xs)"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  then show ?case by (auto simp: comp_def)
qed
```

**Final proof:**
```isabelle
lemma "length (filter P (map f xs)) ≤ length xs"
proof -
  have "length (filter P (map f xs)) = length (map f (filter (P ∘ f) xs))"
    by (simp add: filter_map)
  also have "... = length (filter (P ∘ f) xs)"
    by (simp add: length_map)
  also have "... ≤ length xs"
    by (rule length_filter_le)
  finally show ?thesis .
qed
```
