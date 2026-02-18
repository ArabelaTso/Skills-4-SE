# Tool-Specific Syntax Reference

## SPIN (Promela LTL)

### Syntax
```
[] p        - Always p (G p)
<> p        - Eventually p (F p)
X p         - Next p
p U q       - p Until q
p -> q      - Implication
p && q      - Conjunction
p || q      - Disjunction
!p          - Negation
```

### Examples
```promela
/* Safety: mutual exclusion */
[] !(process[0].critical && process[1].critical)

/* Liveness: every request gets response */
[] (request -> <> response)

/* Response: button press leads to action */
[] (button_press -> X action)

/* Fairness: if enabled infinitely often, executed infinitely often */
([] <> enabled) -> ([] <> executed)
```

### SPIN-Specific Features
- Use `_` prefix for SPIN built-in variables
- `_nr_pr` - number of processes
- `_pid` - process ID
- Atomic propositions must be boolean expressions

---

## NuSMV (CTL/LTL)

### CTL Syntax
```
AG p        - All paths, globally p
EG p        - Some path, globally p
AF p        - All paths, finally p
EF p        - Some path, finally p
AX p        - All paths, next p
EX p        - Some path, next p
A[p U q]    - All paths, p until q
E[p U q]    - Some path, p until q
```

### LTL Syntax
```
G p         - Globally p
F p         - Finally p
X p         - Next p
p U q       - p Until q
p -> q      - Implication
p & q       - Conjunction
p | q       - Disjunction
!p          - Negation
```

### Examples
```smv
-- CTL: System always terminates
SPEC AG(AF terminated)

-- CTL: Mutual exclusion
SPEC AG(!(state1 = critical & state2 = critical))

-- LTL: Every request gets response
LTLSPEC G(request -> F response)

-- CTL: Can reach error state
SPEC EF(error)

-- CTL: Deadlock freedom
SPEC AG(EX TRUE)
```

### NuSMV-Specific Features
- Use `SPEC` for CTL properties
- Use `LTLSPEC` for LTL properties
- Use `INVARSPEC` for invariants
- Boolean operators: `&`, `|`, `!`, `->`, `<->`
- Use `TRUE` and `FALSE` for constants

---

## TLA+ (Temporal Logic of Actions)

### Syntax
```
[]P         - Always P (box P)
<>P         - Eventually P (diamond P)
P ~> Q      - P leads to Q (P implies eventually Q)
[][A]_v     - Action A with stuttering on v
<<A>>_v     - Action A without stuttering on v
ENABLED A   - Action A is enabled
```

### Examples
```tla
\* Safety: Type invariant
TypeInvariant == x \in Nat /\ y \in Nat

\* Liveness: Eventually terminates
Termination == <>(pc = "Done")

\* Fairness: Weak fairness of action
WF_vars(Action)

\* Leads-to: Request leads to response
RequestResponse == [](request => <>response)

\* Invariant under action
[]([Action]_vars)
```

### TLA+-Specific Features
- Use `\*` for comments
- Primed variables (x') for next-state values
- `UNCHANGED vars` for stuttering
- Fairness: `WF_vars(A)` (weak), `SF_vars(A)` (strong)

---

## Uppaal (TCTL - Timed CTL)

### Syntax
```
A[] p           - Invariantly p (all paths, always)
E<> p           - Possibly p (some path, eventually)
A<> p           - Eventually p (all paths, eventually)
E[] p           - Potentially always p (some path, always)
p --> q         - p leads to q
p[<=t]          - p within time bound t
```

### Examples
```
/* Safety: No collision */
A[] !collision

/* Reachability: Can reach goal */
E<> goal

/* Response time: Request answered within 10 time units */
A[] (request imply A<> response[<=10])

/* Liveness: Eventually stable */
A<> stable

/* Deadlock freedom */
A[] not deadlock
```

### Uppaal-Specific Features
- Time bounds: `[<=t]`, `[>=t]`, `[==t]`
- Clock constraints in properties
- Use `imply` for implication
- Use `not` for negation
- Use `and`, `or` for boolean operators

---

## Maude (Linear Temporal Logic)

### Syntax
```
[] p        - Always p
<> p        - Eventually p
O p         - Next p (O for "next")
p U q       - p Until q
p R q       - p Release q
p -> q      - Implication
p /\ q      - Conjunction
p \/ q      - Disjunction
~ p         - Negation
```

### Examples
```maude
*** Safety property
[] (~ collision)

*** Liveness property
[] (request -> <> response)

*** Fairness
([] <> enabled) -> ([] <> executed)

*** Until property
(trying U critical)
```

### Maude-Specific Features
- Use `***` for comments
- Properties in `LTL` module
- Use `O` for next operator
- Atomic propositions are state predicates

---

## Conversion Guidelines

### LTL to CTL (when possible)
```
G p     →  AG p
F p     →  AF p (if must hold on all paths)
        →  EF p (if can hold on some path)
X p     →  AX p (if must hold on all paths)
        →  EX p (if can hold on some path)
p U q   →  A[p U q] (if must hold on all paths)
        →  E[p U q] (if can hold on some path)
```

### CTL to LTL (when possible)
```
AG p    →  G p
AF p    →  F p (loses "all paths" semantics)
EF p    →  F p (loses "some path" semantics)
AX p    →  X p (loses "all paths" semantics)
```

### Tool-Specific Conversions

**SPIN to NuSMV:**
```
[] p    →  G p (LTL) or AG p (CTL)
<> p    →  F p (LTL) or AF p (CTL)
X p     →  X p (LTL) or AX p (CTL)
```

**NuSMV to Uppaal:**
```
AG p    →  A[] p
AF p    →  A<> p
EF p    →  E<> p
EG p    →  E[] p
```

**TLA+ to SPIN:**
```
[]P     →  [] P
<>P     →  <> P
P ~> Q  →  [] (P -> <> Q)
```

## Syntax Validation Rules

### Common Errors
1. **Unbalanced operators**: Every path quantifier (A/E) must have temporal operator (G/F/X/U)
2. **Invalid nesting**: LTL doesn't allow nested path quantifiers
3. **Missing parentheses**: Use parentheses for complex formulas
4. **Wrong operator precedence**: ! > X > U,R > &&,|| > ->

### Well-Formedness Checks
- CTL: Every temporal operator must be preceded by path quantifier
- LTL: No path quantifiers allowed
- Atomic propositions must be boolean-valued
- Time bounds (if supported) must be non-negative
