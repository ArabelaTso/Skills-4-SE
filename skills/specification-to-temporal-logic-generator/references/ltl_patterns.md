# LTL Pattern Library

## Basic Operators

- `G p` - Globally p (p holds at all future states)
- `F p` - Finally p (p holds at some future state)
- `X p` - Next p (p holds in the next state)
- `p U q` - p Until q (p holds until q becomes true)
- `p R q` - p Release q (q holds until p becomes true, or forever)

## Common Property Patterns

### Safety Properties (Something bad never happens)

**Invariant**: A property always holds
```
G(property)
Example: G(temperature < 100) - "Temperature never exceeds 100"
```

**Absence**: An event never occurs
```
G(!event)
Example: G(!collision) - "Collision never occurs"
```

**Bounded Response**: If p occurs, q must occur within k steps
```
G(p -> X^k q)
Example: G(request -> X X X response) - "Response within 3 steps"
```

### Liveness Properties (Something good eventually happens)

**Response**: If p occurs, q eventually follows
```
G(p -> F q)
Example: G(request -> F response) - "Every request gets a response"
```

**Persistence**: Once p becomes true, it stays true
```
F G p
Example: F G(stable) - "System eventually stabilizes"
```

**Recurrence**: p occurs infinitely often
```
G F p
Example: G F(heartbeat) - "Heartbeat occurs infinitely often"
```

### Fairness Properties

**Strong Fairness**: If p is true infinitely often, q occurs infinitely often
```
G F p -> G F q
Example: G F(enabled) -> G F(executed) - "If enabled infinitely often, executes infinitely often"
```

**Weak Fairness**: If p is continuously true, q eventually occurs
```
F G p -> F q
Example: F G(ready) -> F(start) - "If continuously ready, eventually starts"
```

### Precedence Properties

**p precedes q**: q cannot occur before p
```
(!q) U p
Example: (!access) U authenticated - "No access before authentication"
```

**p strictly precedes q**: p must occur before first q
```
(!q) U (p && !q)
Example: (!send) U (connect && !send) - "Must connect before sending"
```

### Real-Time Patterns (for timed systems)

**Bounded Eventually**: p occurs within time bound
```
G(trigger -> F[0,t] p)
Example: G(alarm -> F[0,5] response) - "Response within 5 time units"
```

**Stability**: p remains true for duration
```
G(p -> (p U[t,∞] q))
Example: G(active -> (active U[10,∞] idle)) - "Active for at least 10 units"
```

## Pattern Selection Guide

1. **"Always" / "Never"** → Use G (Globally)
2. **"Eventually" / "Sometime"** → Use F (Finally)
3. **"Immediately after"** → Use X (Next)
4. **"Until"** → Use U (Until)
5. **"Whenever X then Y"** → Use G(X -> F Y) or G(X -> X Y)
6. **"X leads to Y"** → Use G(X -> F Y)
7. **"X before Y"** → Use (!Y) U X

## Common Requirement Translations

| Requirement | LTL Formula |
|-------------|-------------|
| "The door is always closed when moving" | G(moving -> closed) |
| "Every request is eventually acknowledged" | G(request -> F ack) |
| "The system never deadlocks" | G(!deadlock) |
| "After reset, the system initializes" | G(reset -> X init) |
| "The alarm sounds until acknowledged" | G(alarm -> (alarm U ack)) |
| "The process runs infinitely often" | G F running |
| "Once started, runs until completion" | G(start -> (!stop U done)) |
