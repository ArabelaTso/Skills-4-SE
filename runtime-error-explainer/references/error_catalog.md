# Error Catalog - Python and Java

Comprehensive catalog of common runtime and compilation errors with detailed examples, root causes, and solutions.

## Table of Contents

**Python Errors:**
1. [AttributeError](#python-attributeerror)
2. [TypeError](#python-typeerror)
3. [ValueError](#python-valueerror)
4. [KeyError](#python-keyerror)
5. [IndexError](#python-indexerror)
6. [NameError](#python-nameerror)
7. [ImportError / ModuleNotFoundError](#python-importerror--modulenotfounderror)
8. [SyntaxError](#python-syntaxerror)
9. [IndentationError](#python-indentationerror)
10. [FileNotFoundError](#python-filenotfounderror)

**Java Errors:**
1. [NullPointerException](#java-nullpointerexception)
2. [ClassNotFoundException](#java-classnotfoundexception)
3. [NoClassDefFoundError](#java-noclassdeffounderror)
4. [ArrayIndexOutOfBoundsException](#java-arrayindexoutofboundsexception)
5. [IllegalArgumentException](#java-illegalargumentexception)
6. [NumberFormatException](#java-numberformatexception)
7. [Type Mismatch Compilation Error](#java-type-mismatch-compilation-error)
8. [Cannot Find Symbol](#java-cannot-find-symbol)
9. [Missing Semicolon](#java-missing-semicolon)
10. [Incompatible Types](#java-incompatible-types)

---

## Python Errors

### Python: AttributeError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 25, in <module>
    print(user.email.upper())
AttributeError: 'NoneType' object has no attribute 'email'
```

**Root Causes:**
1. Accessing attribute on `None`
2. Object doesn't have the attribute
3. Typo in attribute name
4. Accessing attribute before it's set

**Solutions:**

```python
# Cause 1: Accessing attribute on None
# Before
user = get_user(user_id)  # Returns None
print(user.email)  # AttributeError

# After - Option 1: Check for None
user = get_user(user_id)
if user is not None:
    print(user.email)

# After - Option 2: Use getattr with default
email = getattr(user, 'email', 'no-email@example.com')

# Cause 2: Object doesn't have attribute
# Before
class User:
    def __init__(self, name):
        self.name = name

user = User("Alice")
print(user.email)  # AttributeError: 'User' has no attribute 'email'

# After
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

# Cause 3: Typo
# Before
print(user.emial)  # Typo

# After
print(user.email)

# Cause 4: Attribute not yet set
# Before
class User:
    def __init__(self, name):
        self.name = name

    def send_welcome(self):
        print(f"Welcome {self.email}")  # email not set yet

# After
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### Python: TypeError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 15, in <module>
    result = "Age: " + 25
TypeError: can only concatenate str (not "int") to str
```

**Root Causes:**
1. Wrong type in operation (e.g., string + int)
2. Calling non-callable object
3. Wrong number of arguments to function
4. Unsupported operation for type

**Solutions:**

```python
# Cause 1: Wrong type in operation
# Before
age = 25
message = "Age: " + age  # TypeError

# After
age = 25
message = "Age: " + str(age)
# or
message = f"Age: {age}"

# Cause 2: Calling non-callable
# Before
x = 5
result = x()  # TypeError: 'int' object is not callable

# After
# x is not a function, don't call it
result = x

# Cause 3: Wrong number of arguments
# Before
def greet(name, age):
    return f"Hello {name}, {age}"

greet("Alice")  # TypeError: missing 1 required positional argument

# After
greet("Alice", 25)

# Cause 4: Unsupported operation
# Before
numbers = [1, 2, 3]
result = numbers / 2  # TypeError: unsupported operand type(s)

# After - divide each element
result = [n / 2 for n in numbers]
```

### Python: ValueError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 10, in <module>
    age = int("twenty-five")
ValueError: invalid literal for int() with base 10: 'twenty-five'
```

**Root Causes:**
1. Invalid conversion (e.g., int("abc"))
2. Invalid value for function (e.g., math.sqrt(-1))
3. Unpacking wrong number of values

**Solutions:**

```python
# Cause 1: Invalid conversion
# Before
user_input = "abc"
number = int(user_input)  # ValueError

# After - with try/except
try:
    number = int(user_input)
except ValueError:
    number = 0  # or handle error appropriately

# After - with validation
if user_input.isdigit():
    number = int(user_input)
else:
    print("Invalid input")

# Cause 2: Invalid value
# Before
import math
result = math.sqrt(-1)  # ValueError

# After
import math
if value >= 0:
    result = math.sqrt(value)
else:
    print("Cannot compute square root of negative number")

# Cause 3: Unpacking wrong number of values
# Before
x, y = [1, 2, 3]  # ValueError: too many values to unpack

# After
x, y, z = [1, 2, 3]
# or
x, y = [1, 2, 3][:2]  # Take only first 2
```

### Python: KeyError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 8, in <module>
    email = user_data['email']
KeyError: 'email'
```

**Root Causes:**
1. Key doesn't exist in dictionary
2. Typo in key name
3. Wrong data structure (expecting dict, got something else)

**Solutions:**

```python
# Cause 1: Key doesn't exist
# Before
user_data = {"name": "Alice", "age": 25}
email = user_data['email']  # KeyError

# After - Option 1: Use get() with default
email = user_data.get('email', 'no-email@example.com')

# After - Option 2: Check if key exists
if 'email' in user_data:
    email = user_data['email']
else:
    email = None

# After - Option 3: Try/except
try:
    email = user_data['email']
except KeyError:
    email = None

# Cause 2: Typo
# Before
email = user_data['emial']  # Typo

# After
email = user_data['email']
```

### Python: IndexError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 5, in <module>
    third_item = items[2]
IndexError: list index out of range
```

**Root Causes:**
1. Index exceeds list length
2. Accessing empty list
3. Off-by-one error

**Solutions:**

```python
# Cause 1: Index out of range
# Before
items = [1, 2]
third = items[2]  # IndexError

# After - Check length first
if len(items) > 2:
    third = items[2]
else:
    third = None

# After - Try/except
try:
    third = items[2]
except IndexError:
    third = None

# Cause 2: Empty list
# Before
items = []
first = items[0]  # IndexError

# After
if items:  # Check if list is not empty
    first = items[0]
else:
    first = None

# Cause 3: Off-by-one error
# Before
items = [1, 2, 3]
for i in range(len(items) + 1):
    print(items[i])  # IndexError on last iteration

# After
for i in range(len(items)):
    print(items[i])

# Better - iterate directly
for item in items:
    print(item)
```

### Python: NameError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 10, in <module>
    print(message)
NameError: name 'message' is not defined
```

**Root Causes:**
1. Variable not defined before use
2. Typo in variable name
3. Variable out of scope
4. Forgot to import module

**Solutions:**

```python
# Cause 1: Variable not defined
# Before
print(message)  # NameError

# After
message = "Hello"
print(message)

# Cause 2: Typo
# Before
message = "Hello"
print(mesage)  # Typo - NameError

# After
print(message)

# Cause 3: Variable out of scope
# Before
def create_message():
    msg = "Hello"

create_message()
print(msg)  # NameError - msg only exists inside function

# After
def create_message():
    msg = "Hello"
    return msg

msg = create_message()
print(msg)

# Cause 4: Forgot import
# Before
result = math.sqrt(16)  # NameError: name 'math' is not defined

# After
import math
result = math.sqrt(16)
```

### Python: ImportError / ModuleNotFoundError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

**Root Causes:**
1. Module not installed
2. Wrong module name
3. Wrong environment
4. Circular import

**Solutions:**

```bash
# Cause 1: Module not installed
# Before
import requests  # ModuleNotFoundError

# After - install module
pip install requests

# Cause 2: Wrong module name
# Before
import request  # ModuleNotFoundError

# After
import requests

# Cause 3: Wrong environment
# Check which Python is running
which python
# Activate correct virtual environment
source venv/bin/activate
pip install requests
```

```python
# Cause 4: Circular import
# File: a.py
from b import foo

def bar():
    return "bar"

# File: b.py
from a import bar  # Circular import!

def foo():
    return bar()

# After - Restructure code
# File: a.py
def bar():
    return "bar"

# File: b.py
from a import bar

def foo():
    return bar()

# File: main.py
import a
import b
```

### Python: SyntaxError

**Full Error Example:**
```
  File "app.py", line 5
    if x == 5
           ^
SyntaxError: invalid syntax
```

**Root Causes:**
1. Missing colon
2. Unmatched parentheses/brackets
3. Invalid operator
4. String quote mismatch

**Solutions:**

```python
# Cause 1: Missing colon
# Before
if x == 5
    print("Five")

# After
if x == 5:
    print("Five")

# Cause 2: Unmatched parentheses
# Before
result = calculate(a, b, (c + d)
print(result)

# After
result = calculate(a, b, (c + d))
print(result)

# Cause 3: Invalid operator
# Before
if x == 5 and y == 10 and  # Missing operand
    print("Match")

# After
if x == 5 and y == 10:
    print("Match")

# Cause 4: String quote mismatch
# Before
message = "Hello'  # Mismatched quotes

# After
message = "Hello"
# or
message = 'Hello'
```

### Python: IndentationError

**Full Error Example:**
```
  File "app.py", line 8
    return x + y
    ^
IndentationError: unexpected indent
```

**Root Causes:**
1. Mixing tabs and spaces
2. Inconsistent indentation
3. Unexpected indent level

**Solutions:**

```python
# Cause 1: Mixing tabs and spaces
# Before (using both tabs and spaces)
def calculate(x, y):
    result = x + y  # 4 spaces
\treturn result  # Tab - IndentationError

# After - use only spaces (recommended)
def calculate(x, y):
    result = x + y  # 4 spaces
    return result  # 4 spaces

# Cause 2: Inconsistent indentation
# Before
def greet(name):
    message = f"Hello {name}"  # 4 spaces
   return message  # 3 spaces - IndentationError

# After
def greet(name):
    message = f"Hello {name}"  # 4 spaces
    return message  # 4 spaces

# Cause 3: Unexpected indent
# Before
x = 5
    y = 10  # Unexpected indent

# After
x = 5
y = 10
```

### Python: FileNotFoundError

**Full Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    with open('data.txt', 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
```

**Root Causes:**
1. File doesn't exist at specified path
2. Wrong file path (relative vs absolute)
3. File moved or deleted
4. Permission issues

**Solutions:**

```python
# Cause 1: File doesn't exist
# Before
with open('data.txt', 'r') as f:
    content = f.read()

# After - check if file exists first
import os

if os.path.exists('data.txt'):
    with open('data.txt', 'r') as f:
        content = f.read()
else:
    print("File not found")

# After - try/except
try:
    with open('data.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("File not found, using defaults")
    content = ""

# Cause 2: Wrong file path
# Before (relative path from wrong location)
with open('data/input.txt', 'r') as f:
    content = f.read()

# After - use absolute path
import os
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'data', 'input.txt')
with open(file_path, 'r') as f:
    content = f.read()
```

---

## Java Errors

### Java: NullPointerException

(Already covered in SKILL.md - see complete example there)

### Java: ClassNotFoundException

(Already covered in SKILL.md - see complete example there)

### Java: NoClassDefFoundError

**Full Error Example:**
```
Exception in thread "main" java.lang.NoClassDefFoundError: com/example/Helper
    at com.example.Main.main(Main.java:5)
Caused by: java.lang.ClassNotFoundException: com.example.Helper
```

**Root Causes:**
1. Class was available at compile time but not runtime
2. JAR file missing from runtime classpath
3. Static initializer failed
4. Version mismatch between compile and runtime

**Solutions:**

```bash
# Cause 1: Runtime classpath issue
# Before
javac -cp lib/helper.jar Main.java  # Compiles fine
java Main  # NoClassDefFoundError

# After
java -cp .:lib/helper.jar Main

# Cause 2: Missing JAR at runtime
# Ensure all JARs in classpath
java -cp "lib/*:." Main
```

```java
# Cause 3: Static initializer failed
// Before
public class Helper {
    static {
        // If this throws exception, class won't load
        int x = 10 / 0;  // ArithmeticException
    }
}

// After - handle exceptions in static initializer
public class Helper {
    static {
        try {
            // Initialization code
        } catch (Exception e) {
            System.err.println("Failed to initialize: " + e);
        }
    }
}
```

### Java: ArrayIndexOutOfBoundsException

**Full Error Example:**
```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
    at Main.main(Main.java:8)
```

**Root Causes:**
1. Index >= array length
2. Negative index
3. Off-by-one error in loop

**Solutions:**

```java
// Cause 1: Index out of bounds
// Before
int[] numbers = {1, 2, 3};
int fourth = numbers[3];  // ArrayIndexOutOfBoundsException

// After - check bounds
if (index >= 0 && index < numbers.length) {
    int value = numbers[index];
} else {
    System.out.println("Index out of bounds");
}

// Cause 2: Negative index
// Before
int value = numbers[-1];  // ArrayIndexOutOfBoundsException

// After - validate index
if (index >= 0 && index < numbers.length) {
    int value = numbers[index];
}

// Cause 3: Off-by-one error
// Before
for (int i = 0; i <= numbers.length; i++) {
    System.out.println(numbers[i]);  // Exception on last iteration
}

// After
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}

// Better - enhanced for loop
for (int number : numbers) {
    System.out.println(number);
}
```

### Java: IllegalArgumentException

**Full Error Example:**
```
Exception in thread "main" java.lang.IllegalArgumentException: Age must be positive
    at User.<init>(User.java:8)
```

**Root Causes:**
1. Invalid argument passed to method
2. Argument violates method contract
3. Null when non-null expected (should use NullPointerException instead)

**Solutions:**

```java
// Cause 1: Invalid argument
// Before
public class User {
    private int age;

    public User(int age) {
        this.age = age;  // No validation
    }
}

new User(-5);  // Creates user with negative age

// After - validate arguments
public class User {
    private int age;

    public User(int age) {
        if (age < 0) {
            throw new IllegalArgumentException("Age must be non-negative");
        }
        this.age = age;
    }
}

// Calling code should handle
try {
    User user = new User(-5);
} catch (IllegalArgumentException e) {
    System.err.println("Invalid user data: " + e.getMessage());
}

// Cause 2: Argument violates contract
// Before
public void processItems(List<String> items) {
    // Method expects non-empty list
    String first = items.get(0);  // May fail
}

// After
public void processItems(List<String> items) {
    if (items == null || items.isEmpty()) {
        throw new IllegalArgumentException("Items list must not be empty");
    }
    String first = items.get(0);
}
```

### Java: NumberFormatException

**Full Error Example:**
```
Exception in thread "main" java.lang.NumberFormatException: For input string: "abc"
    at java.base/java.lang.Integer.parseInt(Integer.java:652)
```

**Root Causes:**
1. Invalid string for number parsing
2. Non-numeric characters in string
3. Number outside valid range

**Solutions:**

```java
// Cause 1: Invalid string
// Before
String input = "abc";
int number = Integer.parseInt(input);  // NumberFormatException

// After - with try/catch
try {
    int number = Integer.parseInt(input);
} catch (NumberFormatException e) {
    System.err.println("Invalid number format");
    int number = 0;  // Default value
}

// After - validate first
if (input.matches("\\d+")) {
    int number = Integer.parseInt(input);
} else {
    System.out.println("Not a valid number");
}

// Cause 2: Whitespace or special characters
// Before
String input = "  123  ";
int number = Integer.parseInt(input);  // NumberFormatException

// After - trim whitespace
int number = Integer.parseInt(input.trim());

// Cause 3: Number out of range
// Before
String input = "9999999999999";  // Too large for int
int number = Integer.parseInt(input);  // NumberFormatException

// After - use Long or handle exception
try {
    int number = Integer.parseInt(input);
} catch (NumberFormatException e) {
    System.err.println("Number too large or invalid format");
}
```

### Java: Type Mismatch Compilation Error

(Already covered in SKILL.md - see complete example there)

### Java: Cannot Find Symbol

**Full Error Example:**
```
Main.java:15: error: cannot find symbol
    String result = helper.process();
                          ^
  symbol:   method process()
  location: variable helper of type Helper
```

**Root Causes:**
1. Typo in method/variable name
2. Method doesn't exist on that type
3. Variable not declared
4. Missing import

**Solutions:**

```java
// Cause 1: Typo
// Before
String result = helper.proces();  // Typo

// After
String result = helper.process();

// Cause 2: Method doesn't exist
// Before
String result = helper.process();  // Helper has no process() method

// After - use correct method name
String result = helper.execute();

// Or add method to Helper class
public class Helper {
    public String process() {
        return "processed";
    }
}

// Cause 3: Variable not declared
// Before
result = "Hello";  // result not declared

// After
String result = "Hello";

// Cause 4: Missing import
// Before
List<String> items = new ArrayList<>();  // Cannot find symbol: List

// After
import java.util.List;
import java.util.ArrayList;

List<String> items = new ArrayList<>();
```

### Java: Missing Semicolon

**Full Error Example:**
```
Main.java:10: error: ';' expected
    int x = 5
            ^
```

**Root Causes:**
1. Forgot semicolon at end of statement
2. Missing semicolon in for loop

**Solutions:**

```java
// Cause 1: Missing semicolon
// Before
int x = 5
int y = 10

// After
int x = 5;
int y = 10;

// Cause 2: For loop
// Before
for (int i = 0 i < 10; i++) {
    System.out.println(i);
}

// After
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}
```

### Java: Incompatible Types

**Full Error Example:**
```
Main.java:8: error: incompatible types: possible lossy conversion from double to int
    int result = 3.14;
                 ^
```

**Root Causes:**
1. Assigning larger type to smaller type
2. Type mismatch in assignment
3. Generic type mismatch

**Solutions:**

```java
// Cause 1: Lossy conversion
// Before
int result = 3.14;  // double to int

// After - explicit cast (loses decimal)
int result = (int) 3.14;  // result = 3

// Or use correct type
double result = 3.14;

// Cause 2: Type mismatch
// Before
String text = 123;  // int to String

// After
String text = String.valueOf(123);
// or
String text = Integer.toString(123);

// Cause 3: Generic type mismatch
// Before
List<String> strings = new ArrayList<Integer>();  // Incompatible types

// After
List<String> strings = new ArrayList<String>();
// or use diamond operator
List<String> strings = new ArrayList<>();
```

---

## Prevention Strategies

**Python:**
1. Use type hints: `def process(user: Optional[User]) -> str:`
2. Enable linters: `pylint`, `flake8`
3. Use formatters: `black`, `autopep8`
4. Write defensive code with null checks
5. Use virtual environments to isolate dependencies

**Java:**
1. Use Optional for nullable values
2. Enable IDE warnings for potential null issues
3. Use annotations: `@Nullable`, `@NonNull`
4. Follow Java naming conventions
5. Use build tools (Maven/Gradle) to manage dependencies
6. Write unit tests to catch errors early
