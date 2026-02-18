# CTL Pattern Library

## Basic Operators

### Path Quantifiers
- `A` - For all paths (universal quantification)
- `E` - There exists a path (existential quantification)

### Temporal Operators
- `X p` - Next p (p holds in the next state)
- `F p` - Finally p (p holds at some future state)
- `G p` - Globally p (p holds at all future states)
- `p U q` - p Until q (p holds until q becomes true)

## CTL Formula Structure

CTL formulas always pair path quantifiers with temporal operators:
- `AX`, `EX` - Next
- `AF`, `EF` - Finally
- `AG`, `EG` - Globally
- `AU`, `EU` - Until

## Common Property Patterns

### Safety Properties

**Invariant**: Property holds in all reachable states
```
AG(property)
Example: AG(temperature < 100) - "Temperature never exceeds 100 in any execution"
```

**Absence**: Event never occurs on any path
```
AG(!event)
Example: AG(!collision) - "No collision on any execution path"
```

**Mutual Exclusion**: Two processes never in critical section simultaneously
```
AG(!(process1_critical && process2_critical))
```

### Liveness Properties

**Inevitable**: Property eventually holds on all paths
```
AF(property)
Example: AF(terminated) - "All executions eventually terminate"
```

**Possible Eventually**: Property can eventually hold on some path
```
EF(property)
Example: EF(goal_state) - "Goal state is reachable"
```

**Persistence**: Once true, stays true on all paths
```
AG(p -> AG p)
Example: AG(committed -> AG committed) - "Once committed, always committed"
```

### Reachability Properties

**State is reachable**: There exists a path to the state
```
EF(state)
Example: EF(error) - "Error state is reachable"
```

**State is inevitable**: All paths lead to the state
```
AF(state)
Example: AF(done) - "All executions reach done state"
```

**State is unreachable**: No path leads to the state
```
AG(!state)
Example: AG(!deadlock) - "Deadlock is unreachable"
```

### Response Properties

**Universal Response**: On all paths, p leads to q
```
AG(p -> AF q)
Example: AG(request -> AF response) - "Every request eventually gets response on all paths"
```

**Existential Response**: On some path, p leads to q
```
AG(p -> EF q)
Example: AG(try -> EF success) - "Every try can lead to success on some path"
```

**Immediate Response**: On all paths, p immediately leads to q
```
AG(p -> AX q)
Example: AG(button_press -> AX action) - "Button press immediately triggers action"
```

### Fairness Properties

**Strong Fairness**: If enabled infinitely often, executed infinitely often
```
AG(AF enabled -> AF executed)
```

**Weak Fairness**: If continuously enabled, eventually executed
```
AG(EG enabled -> AF executed)
```

### Possibility Properties

**Potential Deadlock**: There exists a path to a deadlock state
```
EF(AG(enabled = false))
```

**Potential Livelock**: There exists an infinite path without progress
```
EG(!progress)
```

**Reversibility**: From any state, can return to initial state
```
AG(EF init)
```

## CTL vs LTL Distinctions

### CTL Can Express (but LTL cannot):
- **Inevitable reachability**: `AF p` - All paths eventually reach p
- **Potential reachability**: `EF p` - Some path reaches p
- **Deadlock freedom**: `AG(EX true)` - Always possible to take a step

### LTL Can Express (but CTL cannot):
- **Fairness**: `GF p` - p occurs infinitely often
- **Stability**: `FG p` - p eventually holds forever

### Both Can Express:
- **Safety**: `AG p` (CTL) ≡ `G p` (LTL)
- **Response**: `AG(p -> AF q)` (CTL) ≡ `G(p -> F q)` (LTL)

## Pattern Selection Guide

1. **"In all executions"** → Use A (universal)
2. **"There exists an execution"** → Use E (existential)
3. **"Always possible to"** → Use AG(EF ...)
4. **"Inevitable"** → Use AF
5. **"Can reach"** → Use EF
6. **"Never on any path"** → Use AG(!)
7. **"On all paths, eventually"** → Use AF

## Common Requirement Translations

| Requirement | CTL Formula |
|-------------|-------------|
| "System can reach error state" | EF(error) |
| "System always terminates" | AF(terminated) |
| "Deadlock is impossible" | AG(EX true) |
| "From any state, can return to init" | AG(EF init) |
| "Request always gets response" | AG(request -> AF response) |
| "Critical section is mutually exclusive" | AG(!(cs1 && cs2)) |
| "System can stabilize" | EF(AG stable) |
| "Every enabled action can execute" | AG(enabled -> EF executed) |

## CTL* Extensions

CTL* combines CTL and LTL, allowing arbitrary nesting:
- `A(GF p)` - On all paths, p occurs infinitely often
- `E(FG p)` - On some path, p eventually holds forever
- `AG(EF(p U q))` - Complex nested properties
