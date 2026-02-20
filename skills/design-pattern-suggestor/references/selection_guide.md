# Pattern Selection Guide

Decision trees and criteria for choosing the right design pattern.

## Quick Selection by Problem Type

### Problem: Creating Objects

**Single instance needed globally?**
→ **Singleton**

**Creation logic complex or multi-step?**
→ **Builder**

**Need different object types based on input?**
→ **Factory Method** or **Abstract Factory**

**Object creation expensive, need copies?**
→ **Prototype**

---

### Problem: Object Structure

**Need to add behavior without modifying class?**
→ **Decorator**

**Incompatible interfaces need to work together?**
→ **Adapter**

**Simplify complex subsystem interface?**
→ **Facade**

**Control access to object?**
→ **Proxy**

**Treat individual and composite objects uniformly?**
→ **Composite**

---

### Problem: Object Behavior

**Behavior changes based on state?**
→ **State**

**Need interchangeable algorithms?**
→ **Strategy**

**One object change affects many others?**
→ **Observer**

**Encapsulate requests as objects?**
→ **Command**

**Algorithm steps vary but structure is fixed?**
→ **Template Method**

**Multiple handlers for same request?**
→ **Chain of Responsibility**

---

## Detailed Decision Trees

### When Adding Functionality

```
Need to add functionality?
├─ To single object at runtime?
│  └─ Decorator
├─ Via subclass override?
│  └─ Template Method
└─ By selecting algorithm?
   └─ Strategy
```

### When Managing Dependencies

```
Managing dependencies?
├─ Hide complexity?
│  └─ Facade
├─ Make compatible?
│  └─ Adapter
├─ Control access?
│  └─ Proxy
└─ Decouple creation?
   └─ Factory/Abstract Factory
```

### When Handling State

```
State-dependent behavior?
├─ Behavior changes frequently?
│  └─ State
├─ One state affects many objects?
│  └─ Observer
└─ Need undo/redo?
   └─ Command
```

---

## Selection Criteria Matrix

| Pattern | Flexibility | Complexity | When to Use |
|---------|-------------|------------|-------------|
| **Singleton** | Low | Low | Single instance needed |
| **Factory** | Medium | Low-Medium | Object type varies |
| **Builder** | High | Medium | Complex construction |
| **Adapter** | Medium | Low | Interface incompatibility |
| **Decorator** | High | Medium | Add responsibilities dynamically |
| **Facade** | Low | Low | Simplify subsystem |
| **Proxy** | Medium | Medium | Control access |
| **Strategy** | High | Low-Medium | Interchangeable algorithms |
| **Observer** | High | Medium | Event notification |
| **Command** | High | Medium | Encapsulate requests |
| **State** | High | Medium-High | State-dependent behavior |
| **Template Method** | Medium | Low | Fixed algorithm structure |

---

## Common Scenarios

### Scenario: E-commerce Checkout

**Requirements:**
- Multiple payment methods (credit card, PayPal, crypto)
- Different shipping options
- Tax calculation varies by region
- Order state tracking

**Suggested Patterns:**
- **Strategy**: Payment methods, shipping calculators
- **State**: Order lifecycle (pending → paid → shipped → delivered)
- **Factory**: Create appropriate tax calculator by region
- **Observer**: Notify customer of status changes

---

### Scenario: Document Editor

**Requirements:**
- Support multiple file formats (PDF, DOCX, TXT)
- Undo/redo functionality
- Plugin system for features
- Real-time collaboration

**Suggested Patterns:**
- **Factory**: Create appropriate document type
- **Command**: Undo/redo operations
- **Decorator**: Add features via plugins
- **Observer**: Notify collaborators of changes
- **Composite**: Document structure (sections, paragraphs, text)

---

### Scenario: API Gateway

**Requirements:**
- Route requests to microservices
- Authentication and authorization
- Rate limiting
- Caching
- Logging

**Suggested Patterns:**
- **Facade**: Unified API interface
- **Proxy**: Access control and caching
- **Chain of Responsibility**: Middleware (auth → rate limit → logging)
- **Decorator**: Add cross-cutting concerns
- **Strategy**: Different routing strategies

---

### Scenario: Game Development

**Requirements:**
- Character AI with different behaviors
- Multiple weapon types
- Game state management
- UI event handling

**Suggested Patterns:**
- **State**: Game states (menu, playing, paused, game over)
- **Strategy**: AI behaviors, weapon types
- **Factory**: Create enemies, items
- **Observer**: UI updates on game events
- **Command**: Input handling, action replay

---

## Pattern Combinations

Patterns often work together:

### Repository + Factory
```
Repository uses Factory to create domain objects from data
```

### Strategy + Factory
```
Factory creates appropriate Strategy based on context
```

### Decorator + Composite
```
Decorators wrap Composite components to add functionality
```

### Observer + Mediator
```
Mediator manages communication between Observers
```

### Command + Memento
```
Commands create Mementos for undo functionality
```

---

## Red Flags: When NOT to Use Patterns

### Don't use Singleton when:
- Testing requires multiple instances
- State needs to vary
- Parallel execution needed

### Don't use Factory when:
- Only one product type
- Creation is trivial
- Direct instantiation is clearer

### Don't use Observer when:
- Few observers that rarely change
- Direct calls are simpler
- Performance critical (observer overhead)

### Don't use Strategy when:
- Only one algorithm
- Algorithm rarely changes
- Simple if/else is clearer

### Don't use Decorator when:
- Composition is excessive
- Static composition sufficient
- Class hierarchy more appropriate

---

## SOLID Principles Mapping

Patterns support SOLID principles:

**Single Responsibility:**
- Strategy (one algorithm per class)
- Command (one action per class)
- State (one state per class)

**Open/Closed:**
- Decorator (extend without modifying)
- Strategy (new algorithms without changing context)
- Factory (new products without changing factory interface)

**Liskov Substitution:**
- All patterns using interfaces/abstract classes
- Strategy, State, Command are exemplars

**Interface Segregation:**
- Facade (simplified interface)
- Adapter (tailored interface)

**Dependency Inversion:**
- Factory (depend on abstractions)
- Dependency Injection
- Repository (abstract data access)

---

## Performance Considerations

### Low Overhead:
- Singleton, Factory Method, Template Method

### Medium Overhead:
- Strategy, Adapter, Facade, State

### Higher Overhead:
- Decorator (multiple object wrapping)
- Observer (notification overhead)
- Chain of Responsibility (traversal cost)

**Optimization Tips:**
- Cache created objects (Factory)
- Lazy initialization (Proxy, Singleton)
- Event batching (Observer)
- Short circuits in chains (Chain of Responsibility)

---

## Language-Specific Considerations

### Python
- Use decorators (@ syntax) for Decorator pattern
- Metaclasses for Singleton
- First-class functions for Strategy
- Duck typing simplifies many patterns

### Java
- Interfaces and abstract classes common
- Generics for type-safe factories
- Streams API complements patterns
- Spring framework uses many patterns

### JavaScript/TypeScript
- Closures for encapsulation
- Prototypal inheritance
- Promises for async patterns
- React uses Observer (state management)

### Go
- Interfaces (implicit implementation)
- No classes (use structs + methods)
- Channels for concurrency patterns
- Composition over inheritance
