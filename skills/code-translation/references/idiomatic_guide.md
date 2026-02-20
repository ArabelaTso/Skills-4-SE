# Idiomatic Translation Guide

## What is Idiomatic Translation?

Idiomatic translation adapts code to follow the conventions, patterns, and best practices of the target language, rather than performing a literal line-by-line conversion. The goal is code that feels "native" to the target language.

## Core Principles

### 1. Follow Language Conventions

**Python: Use snake_case**
```python
# Good (idiomatic Python)
def calculate_total_price(item_list):
    return sum(item.price for item in item_list)

# Bad (translated from Java)
def calculateTotalPrice(itemList):
    totalPrice = 0
    for item in itemList:
        totalPrice += item.price
    return totalPrice
```

**JavaScript: Use camelCase**
```javascript
// Good (idiomatic JavaScript)
function calculateTotalPrice(itemList) {
    return itemList.reduce((sum, item) => sum + item.price, 0);
}

// Bad (translated from Python)
function calculate_total_price(item_list) {
    let total_price = 0;
    for (const item of item_list) {
        total_price += item.price;
    }
    return total_price;
}
```

### 2. Use Language-Specific Features

**Python: List Comprehensions**
```python
# Idiomatic
squares = [x**2 for x in range(10) if x % 2 == 0]

# Not idiomatic (Java-style)
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)
```

**JavaScript: Array Methods**
```javascript
// Idiomatic
const squares = numbers
    .filter(x => x % 2 === 0)
    .map(x => x ** 2);

// Not idiomatic (C-style)
const squares = [];
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        squares.push(numbers[i] ** 2);
    }
}
```

**Go: Error Handling**
```go
// Idiomatic
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read file: %w", err)
    }
    return data, nil
}

// Not idiomatic (exception-style)
func readFile(path string) []byte {
    data, err := os.ReadFile(path)
    if err != nil {
        panic(err) // Don't panic for expected errors
    }
    return data
}
```

**Rust: Pattern Matching**
```rust
// Idiomatic
fn process_result(result: Result<i32, String>) -> i32 {
    match result {
        Ok(value) => value * 2,
        Err(e) => {
            eprintln!("Error: {}", e);
            0
        }
    }
}

// Not idiomatic (if-else style)
fn process_result(result: Result<i32, String>) -> i32 {
    if result.is_ok() {
        result.unwrap() * 2
    } else {
        eprintln!("Error: {}", result.unwrap_err());
        0
    }
}
```

### 3. Adapt Data Structures

**Python: Use Built-in Types Effectively**
```python
# Idiomatic: Use dict for counting
from collections import Counter
word_counts = Counter(words)

# Not idiomatic: Manual counting
word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
```

**JavaScript: Use Appropriate Collections**
```javascript
// Idiomatic: Use Set for uniqueness
const uniqueItems = new Set(items);

// Not idiomatic: Manual deduplication
const uniqueItems = [];
for (const item of items) {
    if (!uniqueItems.includes(item)) {
        uniqueItems.push(item);
    }
}
```

### 4. Leverage Standard Library

**Python: Use pathlib**
```python
# Idiomatic
from pathlib import Path

config_path = Path.home() / ".config" / "app" / "config.json"
if config_path.exists():
    data = config_path.read_text()

# Not idiomatic
import os
config_path = os.path.join(
    os.path.expanduser("~"), ".config", "app", "config.json"
)
if os.path.exists(config_path):
    with open(config_path) as f:
        data = f.read()
```

**JavaScript: Use Modern APIs**
```javascript
// Idiomatic: fetch API
const data = await fetch(url).then(res => res.json());

// Not idiomatic: XMLHttpRequest
const xhr = new XMLHttpRequest();
xhr.open('GET', url);
xhr.onload = () => {
    const data = JSON.parse(xhr.responseText);
};
xhr.send();
```

## Language-Specific Idioms

### Python Idioms

**Context Managers**
```python
# Idiomatic
with open('file.txt') as f:
    content = f.read()

# Not idiomatic
f = open('file.txt')
try:
    content = f.read()
finally:
    f.close()
```

**Enumerate Instead of Range(len())**
```python
# Idiomatic
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Not idiomatic
for i in range(len(items)):
    print(f"{i}: {items[i]}")
```

**Multiple Assignment**
```python
# Idiomatic
x, y = y, x  # Swap

# Not idiomatic
temp = x
x = y
y = temp
```

**Duck Typing**
```python
# Idiomatic: Ask for forgiveness
try:
    value = obj.method()
except AttributeError:
    value = default_value

# Not idiomatic: Look before you leap
if hasattr(obj, 'method'):
    value = obj.method()
else:
    value = default_value
```

### JavaScript Idioms

**Destructuring**
```javascript
// Idiomatic
const { name, age } = user;
const [first, second, ...rest] = array;

// Not idiomatic
const name = user.name;
const age = user.age;
const first = array[0];
const second = array[1];
```

**Spread Operator**
```javascript
// Idiomatic
const combined = [...arr1, ...arr2];
const clone = { ...original };

// Not idiomatic
const combined = arr1.concat(arr2);
const clone = Object.assign({}, original);
```

**Optional Chaining**
```javascript
// Idiomatic
const city = user?.address?.city;

// Not idiomatic
const city = user && user.address && user.address.city;
```

**Promises and Async/Await**
```javascript
// Idiomatic
async function fetchUserData(id) {
    try {
        const user = await fetch(`/api/users/${id}`).then(r => r.json());
        return user;
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Not idiomatic
function fetchUserData(id, callback) {
    fetch(`/api/users/${id}`)
        .then(r => r.json())
        .then(user => callback(null, user))
        .catch(error => callback(error, null));
}
```

### Go Idioms

**Early Returns**
```go
// Idiomatic
func processData(data []byte) error {
    if len(data) == 0 {
        return errors.New("empty data")
    }

    if !isValid(data) {
        return errors.New("invalid data")
    }

    // Process data
    return nil
}

// Not idiomatic
func processData(data []byte) error {
    if len(data) > 0 {
        if isValid(data) {
            // Process data
            return nil
        } else {
            return errors.New("invalid data")
        }
    }
    return errors.New("empty data")
}
```

**Accept Interfaces, Return Structs**
```go
// Idiomatic
type Reader interface {
    Read(p []byte) (n int, err error)
}

func processData(r Reader) (*Result, error) {
    // Implementation
}

// Not idiomatic
func processData(f *os.File) (*Result, error) {
    // Too specific
}
```

**Use Goroutines and Channels**
```go
// Idiomatic
func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

// Not idiomatic: Using mutex for everything
var mu sync.Mutex
var results []int

for item := range input {
    go func(item int) {
        result := process(item)
        mu.Lock()
        results = append(results, result)
        mu.Unlock()
    }(item)
}
```

### Rust Idioms

**Iterator Chains**
```rust
// Idiomatic
let sum: i32 = numbers
    .iter()
    .filter(|&&x| x > 0)
    .map(|&x| x * 2)
    .sum();

// Not idiomatic
let mut sum = 0;
for &x in &numbers {
    if x > 0 {
        sum += x * 2;
    }
}
```

**Pattern Matching**
```rust
// Idiomatic
match value {
    Some(x) if x > 0 => println!("Positive: {}", x),
    Some(x) => println!("Non-positive: {}", x),
    None => println!("No value"),
}

// Not idiomatic
if value.is_some() {
    let x = value.unwrap();
    if x > 0 {
        println!("Positive: {}", x);
    } else {
        println!("Non-positive: {}", x);
    }
} else {
    println!("No value");
}
```

**Ownership and Borrowing**
```rust
// Idiomatic
fn process_and_return(mut data: Vec<i32>) -> Vec<i32> {
    data.push(42);
    data
}

// Not idiomatic (unnecessary clone)
fn process_and_return(data: Vec<i32>) -> Vec<i32> {
    let mut new_data = data.clone();
    new_data.push(42);
    new_data
}
```

## Anti-Patterns to Avoid

### Don't Translate Comments Literally
```python
# Bad: Literal translation from Java
# This method calculates the total
# @param items - the list of items
# @return the total price
def calculate_total(items):
    pass

# Good: Python docstring
def calculate_total(items):
    """Calculate total price from list of items.

    Args:
        items: List of item objects with price attribute

    Returns:
        Total price as float
    """
    pass
```

### Don't Preserve Foreign Patterns
```javascript
// Bad: Preserving Java getter/setter pattern
class User {
    constructor(name) {
        this._name = name;
    }

    getName() {
        return this._name;
    }

    setName(name) {
        this._name = name;
    }
}

// Good: Use JavaScript property access
class User {
    constructor(name) {
        this.name = name;
    }
}
```

### Don't Ignore Language Safety Features
```rust
// Bad: Using unwrap everywhere (translated from Python)
fn get_user(id: i32) -> User {
    database.find_user(id).unwrap()
}

// Good: Proper error handling
fn get_user(id: i32) -> Result<User, DatabaseError> {
    database.find_user(id)
}
```

## Idiomatic Translation Checklist

- [ ] Follow naming conventions (snake_case, camelCase, PascalCase)
- [ ] Use language-specific features (list comprehensions, array methods, etc.)
- [ ] Leverage standard library idiomatically
- [ ] Adapt data structures to target language norms
- [ ] Apply appropriate error handling patterns
- [ ] Use modern language features (not legacy patterns)
- [ ] Follow community style guides
- [ ] Adapt comments and documentation format
- [ ] Consider performance implications of idioms
- [ ] Test that translated code behaves identically
