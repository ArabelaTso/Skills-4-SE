# Pseudocode to Java Mapping Patterns

## Common Control Structures

### If-Else Statements

**Pseudocode:**
```
IF condition THEN
    statements
ELSE
    statements
END IF
```

**Java:**
```java
if (condition) {
    // statements
} else {
    // statements
}
```

### For Loops

**Pseudocode:**
```
FOR i FROM 1 TO n DO
    statements
END FOR
```

**Java:**
```java
for (int i = 1; i <= n; i++) {
    // statements
}
```

**Pseudocode (for-each):**
```
FOR EACH item IN collection DO
    statements
END FOR
```

**Java:**
```java
for (ItemType item : collection) {
    // statements
}
```

### While Loops

**Pseudocode:**
```
WHILE condition DO
    statements
END WHILE
```

**Java:**
```java
while (condition) {
    // statements
}
```

### Do-While Loops

**Pseudocode:**
```
REPEAT
    statements
UNTIL condition
```

**Java:**
```java
do {
    // statements
} while (!condition);
```

## Data Structures Mapping

### Arrays

**Pseudocode:**
```
DECLARE array[n] OF INTEGER
array[i] ← value
```

**Java:**
```java
int[] array = new int[n];
array[i] = value;
```

### Lists

**Pseudocode:**
```
DECLARE list AS LIST OF INTEGER
APPEND value TO list
item ← list[i]
```

**Java:**
```java
List<Integer> list = new ArrayList<>();
list.add(value);
int item = list.get(i);
```

### Sets

**Pseudocode:**
```
DECLARE set AS SET OF INTEGER
ADD value TO set
IF value IN set THEN
```

**Java:**
```java
Set<Integer> set = new HashSet<>();
set.add(value);
if (set.contains(value)) {
```

### Maps/Dictionaries

**Pseudocode:**
```
DECLARE map AS MAP FROM STRING TO INTEGER
map[key] ← value
value ← map[key]
```

**Java:**
```java
Map<String, Integer> map = new HashMap<>();
map.put(key, value);
int value = map.get(key);
```

### Stacks

**Pseudocode:**
```
DECLARE stack AS STACK OF INTEGER
PUSH value ONTO stack
value ← POP FROM stack
```

**Java:**
```java
Stack<Integer> stack = new Stack<>();
stack.push(value);
int value = stack.pop();
```

### Queues

**Pseudocode:**
```
DECLARE queue AS QUEUE OF INTEGER
ENQUEUE value TO queue
value ← DEQUEUE FROM queue
```

**Java:**
```java
Queue<Integer> queue = new LinkedList<>();
queue.offer(value);
int value = queue.poll();
```

## Functions/Procedures

**Pseudocode:**
```
FUNCTION functionName(param1, param2) RETURNS INTEGER
    statements
    RETURN result
END FUNCTION
```

**Java:**
```java
public int functionName(Type1 param1, Type2 param2) {
    // statements
    return result;
}
```

**Pseudocode (procedure):**
```
PROCEDURE procedureName(param1, param2)
    statements
END PROCEDURE
```

**Java:**
```java
public void procedureName(Type1 param1, Type2 param2) {
    // statements
}
```

## Common Operations

### String Operations

| Pseudocode | Java |
|------------|------|
| `length ← LENGTH(string)` | `int length = string.length();` |
| `substring ← SUBSTRING(string, start, end)` | `String substring = string.substring(start, end);` |
| `result ← CONCATENATE(str1, str2)` | `String result = str1 + str2;` |
| `IF string CONTAINS substring` | `if (string.contains(substring))` |

### Math Operations

| Pseudocode | Java |
|------------|------|
| `result ← POWER(base, exponent)` | `double result = Math.pow(base, exponent);` |
| `result ← SQRT(value)` | `double result = Math.sqrt(value);` |
| `result ← ABS(value)` | `int result = Math.abs(value);` |
| `result ← MAX(a, b)` | `int result = Math.max(a, b);` |
| `result ← MIN(a, b)` | `int result = Math.min(a, b);` |

### Array/List Operations

| Pseudocode | Java |
|------------|------|
| `length ← LENGTH(array)` | `int length = array.length;` (arrays)<br>`int length = list.size();` (lists) |
| `SORT(array)` | `Arrays.sort(array);` (arrays)<br>`Collections.sort(list);` (lists) |
| `REVERSE(array)` | `Collections.reverse(Arrays.asList(array));` |

## Type Conversions

| Pseudocode | Java |
|------------|------|
| `INTEGER(string)` | `Integer.parseInt(string)` |
| `STRING(integer)` | `String.valueOf(integer)` or `Integer.toString(integer)` |
| `FLOAT(string)` | `Float.parseFloat(string)` |
| `CHAR(string, index)` | `string.charAt(index)` |

## Input/Output

**Pseudocode:**
```
OUTPUT "message"
INPUT variable
```

**Java:**
```java
System.out.println("message");
Scanner scanner = new Scanner(System.in);
int variable = scanner.nextInt();
```

## Exception Handling

**Pseudocode:**
```
TRY
    statements
CATCH exception
    handle exception
END TRY
```

**Java:**
```java
try {
    // statements
} catch (ExceptionType exception) {
    // handle exception
}
```

## Common Algorithms Patterns

### Binary Search

**Pseudocode:**
```
FUNCTION binarySearch(array, target)
    left ← 0
    right ← LENGTH(array) - 1
    WHILE left ≤ right DO
        mid ← (left + right) / 2
        IF array[mid] = target THEN
            RETURN mid
        ELSE IF array[mid] < target THEN
            left ← mid + 1
        ELSE
            right ← mid - 1
        END IF
    END WHILE
    RETURN -1
END FUNCTION
```

**Java:**
```java
public int binarySearch(int[] array, int target) {
    int left = 0;
    int right = array.length - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (array[mid] == target) {
            return mid;
        } else if (array[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```

### Swap Elements

**Pseudocode:**
```
SWAP(array[i], array[j])
```

**Java:**
```java
int temp = array[i];
array[i] = array[j];
array[j] = temp;
```

## Best Practices

1. **Variable Naming**: Convert UPPERCASE pseudocode variables to camelCase in Java
2. **Type Inference**: Determine appropriate Java types based on pseudocode context
3. **Null Safety**: Add null checks where appropriate
4. **Imports**: Include necessary import statements (java.util.*, etc.)
5. **Main Method**: Wrap code in a proper main method for executability
6. **Comments**: Preserve pseudocode as comments for clarity
