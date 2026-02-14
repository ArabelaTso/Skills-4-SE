# Language-Specific Translation Patterns

## Python → JavaScript/TypeScript

### Data Structures

**Lists → Arrays**
```python
# Python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
numbers.extend([7, 8])
first = numbers[0]
```

```javascript
// JavaScript
const numbers = [1, 2, 3, 4, 5];
numbers.push(6);
numbers.push(...[7, 8]);
const first = numbers[0];
```

**Dictionaries → Objects/Maps**
```python
# Python
user = {"name": "Alice", "age": 30}
user["email"] = "alice@example.com"
name = user.get("name", "Unknown")
```

```javascript
// JavaScript
const user = { name: "Alice", age: 30 };
user.email = "alice@example.com";
const name = user.name || "Unknown";
```

**Sets**
```python
# Python
unique_items = {1, 2, 3}
unique_items.add(4)
```

```javascript
// JavaScript
const uniqueItems = new Set([1, 2, 3]);
uniqueItems.add(4);
```

### Control Flow

**List Comprehensions → Array Methods**
```python
# Python
squares = [x**2 for x in range(10)]
evens = [x for x in numbers if x % 2 == 0]
```

```javascript
// JavaScript
const squares = Array.from({ length: 10 }, (_, x) => x ** 2);
const evens = numbers.filter(x => x % 2 === 0);
```

**Exception Handling**
```python
# Python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Error: {e}")
finally:
    cleanup()
```

```javascript
// JavaScript
try {
    const result = riskyOperation();
} catch (e) {
    if (e instanceof ValueError) {
        console.log(`Error: ${e}`);
    } else {
        throw e;
    }
} finally {
    cleanup();
}
```

### Functions

**Default Arguments**
```python
# Python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"
```

```javascript
// JavaScript
function greet(name, greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
```

**Async/Await**
```python
# Python
async def fetch_data(url):
    response = await make_request(url)
    return response.json()
```

```javascript
// JavaScript
async function fetchData(url) {
    const response = await makeRequest(url);
    return response.json();
}
```

## JavaScript → Python

### Callbacks → Async/Await
```javascript
// JavaScript
getData(url, (error, data) => {
    if (error) {
        console.error(error);
    } else {
        processData(data);
    }
});
```

```python
# Python
try:
    data = await get_data(url)
    process_data(data)
except Exception as e:
    print(f"Error: {e}")
```

### Promises → Asyncio
```javascript
// JavaScript
Promise.all([fetch1(), fetch2(), fetch3()])
    .then(results => processResults(results))
    .catch(error => handleError(error));
```

```python
# Python
import asyncio

results = await asyncio.gather(fetch1(), fetch2(), fetch3())
process_results(results)
```

## Java → Python

### Classes and Objects
```java
// Java
public class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

```python
# Python
class User:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
```

### Generics → Type Hints
```java
// Java
List<String> names = new ArrayList<>();
Map<String, Integer> scores = new HashMap<>();
```

```python
# Python
from typing import List, Dict

names: List[str] = []
scores: Dict[str, int] = {}
```

### Streams → List Comprehensions
```java
// Java
List<Integer> squares = numbers.stream()
    .map(x -> x * x)
    .filter(x -> x > 10)
    .collect(Collectors.toList());
```

```python
# Python
squares = [x * x for x in numbers if x * x > 10]
```

## Python → Go

### Error Handling
```python
# Python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(e)
```

```go
// Go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}

result, err := divide(10, 0)
if err != nil {
    fmt.Println(err)
}
```

### Context Managers → Defer
```python
# Python
with open("file.txt", "r") as f:
    content = f.read()
```

```go
// Go
f, err := os.Open("file.txt")
if err != nil {
    return err
}
defer f.Close()

content, err := io.ReadAll(f)
```

### Concurrency
```python
# Python
import asyncio

async def worker(task_id):
    await asyncio.sleep(1)
    return f"Task {task_id} complete"

tasks = [worker(i) for i in range(5)]
results = await asyncio.gather(*tasks)
```

```go
// Go
func worker(taskID int) string {
    time.Sleep(1 * time.Second)
    return fmt.Sprintf("Task %d complete", taskID)
}

var wg sync.WaitGroup
results := make([]string, 5)

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        results[id] = worker(id)
    }(i)
}
wg.Wait()
```

## C++ → Rust

### Memory Management
```cpp
// C++
std::vector<int> numbers;
numbers.push_back(1);
numbers.push_back(2);

int* ptr = new int(42);
// ... use ptr ...
delete ptr;
```

```rust
// Rust
let mut numbers: Vec<i32> = Vec::new();
numbers.push(1);
numbers.push(2);

let value = Box::new(42);
// Automatically dropped when out of scope
```

### Ownership and Borrowing
```cpp
// C++
void process(std::vector<int>& data) {
    // Modifies data
}

std::vector<int> nums = {1, 2, 3};
process(nums);
```

```rust
// Rust
fn process(data: &mut Vec<i32>) {
    // Modifies data
}

let mut nums = vec![1, 2, 3];
process(&mut nums);
```

### Option/Result Types
```cpp
// C++
std::optional<int> find_value(const std::string& key) {
    if (/* found */) {
        return value;
    }
    return std::nullopt;
}
```

```rust
// Rust
fn find_value(key: &str) -> Option<i32> {
    if /* found */ {
        Some(value)
    } else {
        None
    }
}
```

## TypeScript → Go

### Interfaces
```typescript
// TypeScript
interface User {
    name: string;
    age: number;
    greet(): string;
}

class Person implements User {
    constructor(public name: string, public age: number) {}

    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
}
```

```go
// Go
type User interface {
    GetName() string
    GetAge() int
    Greet() string
}

type Person struct {
    Name string
    Age  int
}

func (p *Person) GetName() string {
    return p.Name
}

func (p *Person) GetAge() int {
    return p.Age
}

func (p *Person) Greet() string {
    return fmt.Sprintf("Hello, I'm %s", p.Name)
}
```

### Generics
```typescript
// TypeScript
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}
```

```go
// Go
func first[T any](arr []T) *T {
    if len(arr) == 0 {
        return nil
    }
    return &arr[0]
}
```

## Common Patterns Across Languages

### Null/None/Nil Handling

**Python**
```python
value = data.get("key")
if value is not None:
    process(value)
```

**JavaScript**
```javascript
const value = data.key;
if (value != null) {
    process(value);
}
```

**Go**
```go
value, exists := data["key"]
if exists {
    process(value)
}
```

**Rust**
```rust
if let Some(value) = data.get("key") {
    process(value);
}
```

### Iteration

**Python**
```python
for item in collection:
    process(item)

for i, item in enumerate(collection):
    process(i, item)
```

**JavaScript**
```javascript
for (const item of collection) {
    process(item);
}

collection.forEach((item, i) => {
    process(i, item);
});
```

**Go**
```go
for _, item := range collection {
    process(item)
}

for i, item := range collection {
    process(i, item)
}
```

**Rust**
```rust
for item in &collection {
    process(item);
}

for (i, item) in collection.iter().enumerate() {
    process(i, item);
}
```

### String Formatting

**Python**
```python
message = f"Hello, {name}! You are {age} years old."
```

**JavaScript**
```javascript
const message = `Hello, ${name}! You are ${age} years old.`;
```

**Go**
```go
message := fmt.Sprintf("Hello, %s! You are %d years old.", name, age)
```

**Rust**
```rust
let message = format!("Hello, {}! You are {} years old.", name, age);
```
