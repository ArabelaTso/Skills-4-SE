# Design Pattern Catalog

Comprehensive reference of common software design patterns organized by category.

## Table of Contents

1. [Creational Patterns](#creational-patterns)
2. [Structural Patterns](#structural-patterns)
3. [Behavioral Patterns](#behavioral-patterns)
4. [Architectural Patterns](#architectural-patterns)
5. [Concurrency Patterns](#concurrency-patterns)

---

## Creational Patterns

Patterns for object creation mechanisms.

### Singleton

**Intent:** Ensure a class has only one instance with global access point.

**Use When:**
- Exactly one instance needed (e.g., configuration, logger, cache)
- Controlled access to shared resource
- Lazy initialization required

**Structure:**
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Examples:** Database connection pool, application settings, logging service

---

### Factory Method

**Intent:** Define interface for creating objects, let subclasses decide which class to instantiate.

**Use When:**
- Class can't anticipate object types to create
- Subclasses specify objects to create
- Delegating creation to helper subclasses

**Structure:**
```python
class Creator:
    def factory_method(self):
        raise NotImplementedError

    def operation(self):
        product = self.factory_method()
        return product.do_something()

class ConcreteCreatorA(Creator):
    def factory_method(self):
        return ConcreteProductA()
```

**Examples:** Document creator (PDF, Word, HTML), UI widget factory, notification sender

---

### Abstract Factory

**Intent:** Provide interface for creating families of related objects without specifying concrete classes.

**Use When:**
- System should be independent of how products are created
- Need families of related products
- Want to enforce product compatibility

**Examples:** UI themes (dark/light mode), database drivers, cloud provider SDKs

---

### Builder

**Intent:** Separate construction of complex object from its representation.

**Use When:**
- Object creation involves many steps
- Same construction process creates different representations
- Need readable construction code

**Structure:**
```python
class QueryBuilder:
    def __init__(self):
        self.query = {}

    def select(self, fields):
        self.query['select'] = fields
        return self

    def where(self, condition):
        self.query['where'] = condition
        return self

    def build(self):
        return Query(self.query)
```

**Examples:** SQL query builder, HTTP request builder, test data builder, form validator

---

### Prototype

**Intent:** Create new objects by cloning existing prototype.

**Use When:**
- Object creation is expensive
- Need copies with slight variations
- Avoid subclass explosion

**Examples:** Game character templates, document templates, configuration presets

---

## Structural Patterns

Patterns for composing classes and objects into larger structures.

### Adapter

**Intent:** Convert interface of class into another interface clients expect.

**Use When:**
- Want to use existing class with incompatible interface
- Need to create reusable class that cooperates with unforeseen classes
- Need to use several existing subclasses but impractical to adapt by subclassing

**Structure:**
```python
class Target:
    def request(self):
        pass

class Adaptee:
    def specific_request(self):
        return "Specific behavior"

class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()
```

**Examples:** Legacy code integration, third-party library wrapper, API version compatibility

---

### Decorator

**Intent:** Attach additional responsibilities to object dynamically.

**Use When:**
- Add responsibilities to individual objects without affecting others
- Responsibilities should be withdrawable
- Extension by subclassing is impractical

**Structure:**
```python
class Component:
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "Base"

class Decorator(Component):
    def __init__(self, component):
        self._component = component

    def operation(self):
        return f"Decorated({self._component.operation()})"
```

**Examples:** Stream I/O (buffered, compressed, encrypted), UI components (scrollable, bordered), middleware pipeline

---

### Facade

**Intent:** Provide unified interface to set of interfaces in subsystem.

**Use When:**
- Simple interface needed for complex subsystem
- Many dependencies between clients and implementation classes
- Want to layer subsystems

**Examples:** API client wrapper, payment gateway interface, email service facade

---

### Proxy

**Intent:** Provide surrogate or placeholder for another object to control access.

**Use When:**
- Need lazy initialization (virtual proxy)
- Access control needed (protection proxy)
- Remote object access (remote proxy)
- Logging/caching needed (smart proxy)

**Examples:** Image lazy loading, access control wrapper, caching layer, RPC stub

---

### Composite

**Intent:** Compose objects into tree structures to represent part-whole hierarchies.

**Use When:**
- Represent part-whole hierarchies
- Ignore difference between composition and individual objects
- Need uniform treatment of objects

**Examples:** File system (files/directories), UI component trees, organization hierarchies

---

## Behavioral Patterns

Patterns for algorithms and assignment of responsibilities between objects.

### Strategy

**Intent:** Define family of algorithms, encapsulate each one, make them interchangeable.

**Use When:**
- Many related classes differ only in behavior
- Need different variants of algorithm
- Algorithm uses data clients shouldn't know
- Class defines many behaviors as conditional statements

**Structure:**
```python
class Strategy:
    def execute(self, data):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return f"Strategy A: {data}"

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def do_business_logic(self, data):
        return self.strategy.execute(data)
```

**Examples:** Sorting algorithms, payment methods, compression algorithms, validation rules

---

### Observer

**Intent:** Define one-to-many dependency so when one object changes, dependents are notified.

**Use When:**
- Change to one object requires changing others (unknown number)
- Object should notify others without assumptions about who they are
- Event-driven system needed

**Examples:** Event listeners, pub/sub systems, model-view updates, reactive programming

---

### Command

**Intent:** Encapsulate request as object, allowing parameterization and queuing.

**Use When:**
- Parameterize objects by action
- Queue, log, or support undo of requests
- Support transactions

**Examples:** Button actions, undo/redo, task queue, database transactions

---

### Template Method

**Intent:** Define skeleton of algorithm, deferring some steps to subclasses.

**Use When:**
- Implement invariant parts once, let subclasses vary
- Control subclass extensions
- Factor common behavior into single place

**Examples:** Data processing pipeline, test frameworks, rendering pipeline

---

### State

**Intent:** Allow object to alter behavior when internal state changes.

**Use When:**
- Object behavior depends on state
- Operations have large conditional statements on state
- State-specific behavior should be in separate classes

**Examples:** TCP connection states, order lifecycle, authentication states, game states

---

### Chain of Responsibility

**Intent:** Avoid coupling sender to receiver by giving multiple objects chance to handle request.

**Use When:**
- More than one object may handle request
- Set of handlers should be specified dynamically
- Request should be handled without specifying receiver explicitly

**Examples:** Event bubbling, middleware chain, approval workflows, exception handling

---

## Architectural Patterns

High-level patterns for overall system structure.

### Model-View-Controller (MVC)

**Intent:** Separate data (Model), presentation (View), and user interaction (Controller).

**Use When:**
- Need to support multiple views of same data
- Want to change UI without changing business logic
- Building interactive applications

**Examples:** Web applications, desktop GUIs, mobile apps

---

### Model-View-ViewModel (MVVM)

**Intent:** Separate UI (View) from business logic (ViewModel) and data (Model).

**Use When:**
- Building data-driven UIs
- Need two-way data binding
- Want testable UI logic

**Examples:** Angular, Vue.js, WPF applications

---

### Repository

**Intent:** Mediate between domain and data mapping layers using collection-like interface.

**Use When:**
- Abstracting data access
- Centralizing data access logic
- Testing with mock data

**Examples:** Database abstraction, API client wrapper, data access layer

---

### Service Layer

**Intent:** Define application's boundary with layer of services.

**Use When:**
- Multiple clients need same operations
- Business logic should be separated from presentation
- Need transactional control

**Examples:** Business logic facade, API services, application services

---

### Dependency Injection

**Intent:** Invert control of dependencies by injecting them rather than creating.

**Use When:**
- Decouple object creation from usage
- Enable testing with mocks
- Configure dependencies externally

**Examples:** Framework injection (Spring, NestJS), constructor injection, service containers

---

## Concurrency Patterns

Patterns for multi-threaded and asynchronous programming.

### Producer-Consumer

**Intent:** Decouple production and consumption of data via queue.

**Use When:**
- Production and consumption rates differ
- Need buffering between stages
- Want to parallelize work

**Examples:** Task queue, message broker, data pipeline

---

### Thread Pool

**Intent:** Maintain pool of worker threads to execute tasks.

**Use When:**
- Creating threads is expensive
- Number of tasks >> optimal thread count
- Want to limit resource usage

**Examples:** Web server request handling, background job processing

---

### Future/Promise

**Intent:** Represent result of asynchronous operation.

**Use When:**
- Non-blocking operations needed
- Composing async operations
- Error handling in async code

**Examples:** JavaScript Promises, Python asyncio, Java CompletableFuture

---

### Actor Model

**Intent:** Encapsulate state and behavior in actors that communicate via messages.

**Use When:**
- Building concurrent systems
- Need fault tolerance
- Scale across machines

**Examples:** Akka, Erlang, message-passing systems

---

## Anti-Patterns to Avoid

### God Object
**Problem:** One class does too much
**Solution:** Split into cohesive classes with single responsibilities

### Spaghetti Code
**Problem:** Tangled, unstructured code flow
**Solution:** Apply proper patterns, refactor into modules

### Golden Hammer
**Problem:** Using same pattern for every problem
**Solution:** Choose patterns based on actual needs

### Premature Optimization
**Problem:** Optimizing before understanding performance needs
**Solution:** Profile first, optimize bottlenecks only
