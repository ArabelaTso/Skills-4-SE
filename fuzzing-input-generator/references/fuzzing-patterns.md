# Fuzzing Input Patterns

## String Fuzzing Patterns

### Edge Case Strings

```python
# Empty and whitespace
""                          # Empty string
" "                         # Single space
"   "                       # Multiple spaces
"\t"                        # Tab
"\n"                        # Newline
"\r\n"                      # Windows newline
"\x00"                      # Null byte

# Length edge cases
"a"                         # Single character
"a" * 1000                  # Long string
"a" * 1000000               # Very long string
"a" * 2**20                 # Megabyte string

# Special characters
"!@#$%^&*()_+-={}[]|:;<>?,./~`"
"'"                         # Single quote
"\""                        # Double quote
"\\"                        # Backslash
"<script>"                  # HTML tag
"../../etc/passwd"          # Path traversal
```

### Unicode and Encoding

```python
# Unicode edge cases
"🔥"                        # Emoji
"你好"                      # Chinese characters
"مرحبا"                     # Arabic (RTL)
"\u0000"                    # Null character
"\uffff"                    # Max BMP character
"𝕳𝖊𝖑𝖑𝖔"                    # Mathematical alphanumeric
"Ẓ̸̧̙̥͔̮̞̏͒a̷̢̧͖̮̹̋l̴̰̈́g̷̢̱̈́ǫ̶̣̼̈́͜"           # Combining characters

# Different encodings
bytes([0xFF, 0xFE])         # Invalid UTF-8
"\ud800"                    # Surrogate pair (invalid)
```

### Format Strings

```python
# Format string attacks
"%s%s%s%s"
"%x%x%x%x"
"{0}{1}{2}"
"${var}"
"{{7*7}}"                   # Template injection
```

### SQL/Command Injection

```python
# SQL injection patterns
"' OR '1'='1"
"'; DROP TABLE users--"
"1' UNION SELECT * FROM users--"

# Command injection
"; ls -la"
"| cat /etc/passwd"
"`whoami`"
"$(cat /etc/passwd)"
```

## Number Fuzzing Patterns

### Integer Edge Cases

```python
# Boundary values
0
1
-1
2**31 - 1                   # Max 32-bit int
-2**31                      # Min 32-bit int
2**63 - 1                   # Max 64-bit int
-2**63                      # Min 64-bit int
2**64                       # Overflow

# Special cases
-0
+0
```

### Float Edge Cases

```python
# Special floats
0.0
-0.0
float('inf')                # Positive infinity
float('-inf')               # Negative infinity
float('nan')                # Not a number

# Precision edge cases
0.1 + 0.2                   # Floating point precision
1e308                       # Near max float
1e-308                      # Near min positive float
1.7976931348623157e+308     # Max float
2.2250738585072014e-308     # Min positive float

# Denormalized numbers
5e-324                      # Smallest positive float
```

## Structured Data Patterns

### JSON Edge Cases

```python
# Empty structures
{}
[]
{"key": null}

# Deep nesting
{"a": {"b": {"c": {"d": "e"}}}}  # Nested objects
[[[[[]]]]]                        # Nested arrays

# Large structures
{f"key{i}": i for i in range(10000)}  # Many keys

# Type confusion
{"number": "123"}            # String that looks like number
{"bool": "true"}             # String that looks like bool
{"null": "null"}             # String that looks like null

# Special keys
{"": "empty key"}
{"key with spaces": "value"}
{"key.with.dots": "value"}
{"key/with/slashes": "value"}
```

### XML Edge Cases

```python
# Malformed XML
"<tag>"                      # Unclosed tag
"<tag></tag2>"               # Mismatched tags
"<tag attribute>"            # Invalid attribute

# XXE (XML External Entity)
'<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'

# Billion laughs attack
'<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ENTITY lol2 "&lol;&lol;">]><lolz>&lol2;</lolz>'
```

### Lists/Arrays Edge Cases

```python
# Empty and size
[]                           # Empty
[None]                       # Single None
[1]                          # Single element
[1] * 10000                  # Large list

# Mixed types
[1, "string", None, True, {"key": "value"}]

# Nested
[[[[]]]]
[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
```

## Boolean and None Patterns

```python
# Boolean edge cases
True
False
None
0                            # Falsy
1                            # Truthy
""                           # Falsy
[]                           # Falsy
{}                           # Falsy

# Boolean-like strings
"true"
"false"
"True"
"False"
"TRUE"
"FALSE"
"null"
"None"
```

## Date/Time Patterns

```python
# Edge case dates
"1970-01-01"                 # Unix epoch
"2038-01-19"                 # Year 2038 problem
"1900-01-01"                 # Old date
"9999-12-31"                 # Far future
"0000-00-00"                 # Invalid date
"2024-02-30"                 # Invalid date (Feb 30)
"13:70:90"                   # Invalid time

# Timezone edge cases
"2024-01-01T00:00:00Z"
"2024-01-01T00:00:00+14:00"  # Max timezone
"2024-01-01T00:00:00-12:00"  # Min timezone
```

## File Path Patterns

```python
# Path traversal
"../../etc/passwd"
"..\\..\\windows\\system32"
"/etc/passwd"
"C:\\Windows\\System32"

# Special paths
"."
".."
"/"
"\\"
"~"
"~/."
"/dev/null"
"CON"                        # Windows reserved
"NUL"                        # Windows reserved

# Long paths
"a/" * 1000 + "file.txt"     # Very deep path
"a" * 300 + ".txt"           # Very long filename
```

## Common Fuzzing Strategies

### Mutation-Based Fuzzing

Start with valid input and apply mutations:
- Bit flips
- Byte flips
- Delete bytes
- Insert bytes
- Swap bytes
- Change to boundary values

### Generation-Based Fuzzing

Generate inputs from scratch based on:
- Grammar/format specification
- Type definitions
- API schemas
- Regular expressions

### Coverage-Guided Fuzzing

Use code coverage feedback to:
- Prioritize inputs that reach new code
- Mutate inputs that increase coverage
- Track which paths have been explored

### Property-Based Fuzzing

Generate random inputs and check:
- Invariants (properties that should always hold)
- Idempotence (f(f(x)) == f(x))
- Commutativity (f(x, y) == f(y, x))
- Round-trip (decode(encode(x)) == x)

## Language-Specific Patterns

### Python

```python
# Type errors
int("not a number")
list("string")
dict([1, 2, 3])

# Index errors
[][0]
[1, 2, 3][100]
[1, 2, 3][-100]

# Division errors
1 / 0
1 // 0
1 % 0
```

### JavaScript

```python
# Type coercion edge cases
undefined
null
NaN
Infinity
-Infinity
""
0
[]
{}

# Prototype pollution
'{"__proto__": {"polluted": "true"}}'
```

### Java

```python
# Null pointer
null

# Integer overflow
Integer.MAX_VALUE + 1
Integer.MIN_VALUE - 1

# Array index
-1
Integer.MAX_VALUE
```

## Security Fuzzing Patterns

### XSS (Cross-Site Scripting)

```python
"<script>alert(1)</script>"
"<img src=x onerror=alert(1)>"
"javascript:alert(1)"
"<svg/onload=alert(1)>"
"';alert(1)//'"
```

### Path Traversal

```python
"../../../etc/passwd"
"..\\..\\..\\windows\\system32\\config\\sam"
"%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
"....//....//....//etc/passwd"
```

### LDAP Injection

```python
"*"
"*)(&"
"*)(uid=*))(|(uid=*"
"admin)(&(password=*)"
```

### NoSQL Injection

```python
'{"$gt": ""}'
'{"$ne": null}'
'{"$regex": ".*"}'
```

## Byte-Level Fuzzing

```python
# Invalid UTF-8 sequences
b'\xFF\xFF\xFF\xFF'
b'\x80\x80\x80\x80'
b'\xC0\x80'                  # Overlong encoding

# Binary edge cases
b'\x00' * 1000               # Null bytes
b'\xFF' * 1000               # Max bytes
bytes(range(256))            # All byte values

# Magic numbers (file signatures)
b'PK\x03\x04'                # ZIP
b'\x89PNG\r\n\x1a\n'         # PNG
b'%PDF'                      # PDF
```
