# Language Idiom Mappings

This reference provides common idiom mappings between popular programming languages to guide translation decisions.

## Python ↔ JavaScript

### Iteration
- Python: `for item in items:` → JS: `for (const item of items) {}`
- Python: `for i, item in enumerate(items):` → JS: `items.forEach((item, i) => {})`
- Python: `[x*2 for x in items]` → JS: `items.map(x => x*2)`

### Dictionary/Object Operations
- Python: `dict.get(key, default)` → JS: `dict[key] ?? default`
- Python: `dict.keys()`, `dict.values()`, `dict.items()` → JS: `Object.keys()`, `Object.values()`, `Object.entries()`

### String Operations
- Python: `str.split()`, `str.join()` → JS: `str.split()`, `arr.join()`
- Python: `f"{var}"` → JS: `` `${var}` ``

### Error Handling
- Python: `try/except/finally` → JS: `try/catch/finally`
- Python: `raise Exception()` → JS: `throw new Error()`

## Java ↔ C#

### Collections
- Java: `ArrayList<T>` → C#: `List<T>`
- Java: `HashMap<K,V>` → C#: `Dictionary<K,V>`
- Java: `stream().map().collect()` → C#: `.Select().ToList()`

### Properties
- Java: `getX()/setX()` → C#: `public X { get; set; }`

### Null Handling
- Java: `Optional<T>` → C#: `T?` (nullable reference types)

## Python ↔ Go

### Error Handling
- Python: `try/except` → Go: `if err != nil { return err }`
- Python: `raise` → Go: `return errors.New()`

### Collections
- Python: `list` → Go: `[]T` (slice)
- Python: `dict` → Go: `map[K]V`
- Python: list comprehension → Go: explicit loop

### Concurrency
- Python: `threading.Thread` → Go: `go func()`
- Python: `queue.Queue` → Go: `chan T`

## Ruby ↔ Python

### Blocks/Lambdas
- Ruby: `items.each { |x| }` → Python: `for x in items:`
- Ruby: `items.map { |x| x*2 }` → Python: `[x*2 for x in items]`

### String Interpolation
- Ruby: `"#{var}"` → Python: `f"{var}"`

### Symbols
- Ruby: `:symbol` → Python: `"symbol"` (string literal)

## TypeScript ↔ Python

### Type Annotations
- TS: `function foo(x: number): string` → Python: `def foo(x: int) -> str:`
- TS: `interface` → Python: `class` with `@dataclass` or `TypedDict`
- TS: `type` → Python: `TypeAlias`

### Async/Await
- Both languages use similar `async`/`await` syntax
- TS: `Promise<T>` → Python: `Awaitable[T]` or `Coroutine`
