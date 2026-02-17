# Optimization Patterns and Recommendations

This document provides language-specific optimization patterns based on common performance bottlenecks.

## Python Optimization Patterns

### 1. String Concatenation
**Problem:** Repeated string concatenation with `+` creates many intermediate objects.

**Bad:**
```python
result = ""
for item in items:
    result += str(item)  # O(n²) complexity
```

**Good:**
```python
result = "".join(str(item) for item in items)  # O(n) complexity
```

### 2. List Comprehensions vs Loops
**Problem:** Explicit loops are slower than comprehensions.

**Bad:**
```python
squares = []
for x in range(1000):
    squares.append(x * x)
```

**Good:**
```python
squares = [x * x for x in range(1000)]
```

### 3. Avoid Repeated Lookups
**Problem:** Dictionary/attribute lookups in loops are expensive.

**Bad:**
```python
for item in items:
    process(math.sqrt(item))  # Repeated module lookup
```

**Good:**
```python
sqrt = math.sqrt
for item in items:
    process(sqrt(item))
```

### 4. Use Built-in Functions
**Problem:** Python loops are slow; built-ins are implemented in C.

**Bad:**
```python
total = 0
for x in numbers:
    total += x
```

**Good:**
```python
total = sum(numbers)
```

### 5. Generator Expressions for Large Data
**Problem:** List comprehensions load everything into memory.

**Bad:**
```python
total = sum([x * x for x in range(10000000)])  # Uses lots of memory
```

**Good:**
```python
total = sum(x * x for x in range(10000000))  # Generator, constant memory
```

### 6. Use `__slots__` for Many Objects
**Problem:** Instance dictionaries consume memory.

**Bad:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

**Good:**
```python
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### 7. Cache Expensive Computations
**Problem:** Recomputing the same values repeatedly.

**Good:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Complex computation
    return result
```

## Java Optimization Patterns

### 1. StringBuilder for String Concatenation
**Problem:** String concatenation creates many temporary objects.

**Bad:**
```java
String result = "";
for (String item : items) {
    result += item;  // Creates new String each time
}
```

**Good:**
```java
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item);
}
String result = sb.toString();
```

### 2. Pre-size Collections
**Problem:** Dynamic resizing causes array copying.

**Bad:**
```java
List<String> list = new ArrayList<>();  // Default capacity 10
for (int i = 0; i < 10000; i++) {
    list.add("item" + i);  // Multiple resizes
}
```

**Good:**
```java
List<String> list = new ArrayList<>(10000);  // Pre-sized
for (int i = 0; i < 10000; i++) {
    list.add("item" + i);
}
```

### 3. Use Primitive Collections
**Problem:** Autoboxing creates wrapper objects.

**Bad:**
```java
List<Integer> numbers = new ArrayList<>();  // Boxes each int
```

**Good:**
```java
// Use libraries like fastutil or Eclipse Collections
IntArrayList numbers = new IntArrayList();
```

### 4. Avoid Reflection in Hot Paths
**Problem:** Reflection is 10-100x slower than direct calls.

**Bad:**
```java
for (Object obj : objects) {
    method.invoke(obj);  // Reflection in loop
}
```

**Good:**
```java
// Cache method handles or use direct calls
for (MyClass obj : objects) {
    obj.myMethod();
}
```

### 5. Use EnumMap/EnumSet
**Problem:** HashMap has overhead for enum keys.

**Bad:**
```java
Map<MyEnum, String> map = new HashMap<>();
```

**Good:**
```java
Map<MyEnum, String> map = new EnumMap<>(MyEnum.class);
```

### 6. Lazy Initialization
**Problem:** Initializing expensive objects that may not be used.

**Good:**
```java
private volatile ExpensiveObject instance;

public ExpensiveObject getInstance() {
    if (instance == null) {
        synchronized (this) {
            if (instance == null) {
                instance = new ExpensiveObject();
            }
        }
    }
    return instance;
}
```

### 7. Stream API Considerations
**Problem:** Streams have overhead for small collections.

**Bad (for small n):**
```java
list.stream().filter(x -> x > 0).count();  // Overhead for small lists
```

**Good (for small n):**
```java
int count = 0;
for (int x : list) {
    if (x > 0) count++;
}
```

## C/C++ Optimization Patterns

### 1. Reserve Vector Capacity
**Problem:** Dynamic resizing causes reallocations.

**Bad:**
```cpp
std::vector<int> vec;
for (int i = 0; i < 10000; i++) {
    vec.push_back(i);  // Multiple reallocations
}
```

**Good:**
```cpp
std::vector<int> vec;
vec.reserve(10000);  // Single allocation
for (int i = 0; i < 10000; i++) {
    vec.push_back(i);
}
```

### 2. Pass by const Reference
**Problem:** Passing large objects by value causes copying.

**Bad:**
```cpp
void process(std::string str) {  // Copies string
    // ...
}
```

**Good:**
```cpp
void process(const std::string& str) {  // No copy
    // ...
}
```

### 3. Use Move Semantics
**Problem:** Unnecessary copies when transferring ownership.

**Bad:**
```cpp
std::vector<int> create() {
    std::vector<int> result;
    // fill result
    return result;  // May copy (pre-C++11)
}
```

**Good:**
```cpp
std::vector<int> create() {
    std::vector<int> result;
    // fill result
    return std::move(result);  // Move, no copy
}
```

### 4. Inline Small Functions
**Problem:** Function call overhead for tiny functions.

**Good:**
```cpp
inline int square(int x) {
    return x * x;
}
```

### 5. Use emplace Instead of push
**Problem:** push_back constructs temporary then copies.

**Bad:**
```cpp
vec.push_back(MyClass(a, b, c));  // Construct temp, then copy
```

**Good:**
```cpp
vec.emplace_back(a, b, c);  // Construct in-place
```

### 6. Avoid Virtual Functions in Hot Paths
**Problem:** Virtual dispatch prevents inlining.

**Consider:** Use templates or CRTP for compile-time polymorphism.

### 7. Memory Alignment
**Problem:** Unaligned access is slower.

**Good:**
```cpp
alignas(64) struct CacheLine {
    int data[16];
};
```

### 8. Loop Optimizations
**Problem:** Inefficient loop patterns.

**Bad:**
```cpp
for (int i = 0; i < vec.size(); i++) {  // size() called each iteration
    process(vec[i]);
}
```

**Good:**
```cpp
const size_t n = vec.size();
for (size_t i = 0; i < n; i++) {
    process(vec[i]);
}
```

## Cross-Language Patterns

### 1. Algorithm Complexity
Always choose the right algorithm first:
- O(n²) → O(n log n): Use better sorting/searching
- O(n) → O(1): Use hash tables instead of linear search
- O(2ⁿ) → O(n): Use dynamic programming

### 2. Data Structure Selection
- **Frequent lookups:** Hash table/map
- **Ordered iteration:** Tree-based map
- **Stack operations:** Vector/ArrayList
- **Queue operations:** Deque/LinkedList
- **Many small objects:** Object pooling

### 3. I/O Optimization
- Buffer reads/writes
- Use binary formats over text
- Batch operations
- Async I/O for concurrent operations

### 4. Memory Access Patterns
- Sequential access is faster than random
- Cache-friendly data structures
- Avoid pointer chasing
- Structure of Arrays (SoA) vs Array of Structures (AoS)

### 5. Parallelization
- Identify independent operations
- Use thread pools, avoid creating threads
- Consider data parallelism
- Watch for false sharing

## Optimization Workflow

1. **Profile first:** Don't guess, measure
2. **Focus on hotspots:** 80/20 rule applies
3. **One change at a time:** Measure impact
4. **Consider readability:** Don't over-optimize
5. **Test correctness:** Ensure optimizations don't break functionality
6. **Document tradeoffs:** Explain non-obvious optimizations

## When NOT to Optimize

- Premature optimization is the root of all evil
- Code that runs once or rarely
- Code that's already fast enough
- When it hurts readability significantly
- When it makes maintenance difficult
