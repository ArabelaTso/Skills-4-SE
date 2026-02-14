# C/C++ Edge Cases and Testing Patterns

C and C++-specific edge cases, common pitfalls, and testing patterns focusing on memory safety, undefined behavior, and low-level concerns.

## Table of Contents

1. [Pointer and Memory Edge Cases](#pointer-and-memory-edge-cases)
2. [Integer Overflow and Undefined Behavior](#integer-overflow-and-undefined-behavior)
3. [Array and Buffer Edge Cases](#array-and-buffer-edge-cases)
4. [String Edge Cases](#string-edge-cases)
5. [Type Conversion Edge Cases](#type-conversion-edge-cases)
6. [Undefined Behavior](#undefined-behavior)
7. [C++ Specific Edge Cases](#c-specific-edge-cases)
8. [Testing Frameworks](#testing-frameworks)

## Pointer and Memory Edge Cases

### Null Pointer Dereference

```c
#include <assert.h>
#include <stdlib.h>
#include <string.h>

void test_null_pointer_edge_cases() {
    // Null pointer dereference (undefined behavior)
    int *ptr = NULL;

    // Dereferencing null is undefined behavior
    // *ptr = 42; // Segmentation fault or worse!

    // Safe null check
    if (ptr != NULL) {
        *ptr = 42;
    }

    // Null in function calls
    // strlen(NULL); // Undefined behavior (likely segfault)

    // Safe string handling
    const char *str = NULL;
    int len = (str != NULL) ? strlen(str) : 0;
    assert(len == 0);
}
```

### Dangling Pointers

```c
void test_dangling_pointer_edge_cases() {
    int *ptr = malloc(sizeof(int));
    *ptr = 42;

    free(ptr);
    // ptr is now dangling!

    // Using dangling pointer is undefined behavior
    // int value = *ptr; // Use after free!

    // Best practice: set to NULL after free
    ptr = NULL;

    // Now safe to check
    if (ptr != NULL) {
        int value = *ptr;
    }
}
```

### Memory Leaks

```c
void test_memory_leak_edge_cases() {
    // Leak: allocated but never freed
    int *leak = malloc(100 * sizeof(int));
    // ... no free()

    // Lost reference leak
    int *ptr = malloc(sizeof(int));
    ptr = malloc(sizeof(int)); // First allocation leaked!

    free(ptr);

    // Conditional leak
    int *conditional = malloc(sizeof(int));
    if (some_condition()) {
        free(conditional);
        conditional = NULL;
    }
    // Leaked if condition is false!

    // Always free on all paths
    if (conditional != NULL) {
        free(conditional);
    }
}
```

### Buffer Overflow

```c
void test_buffer_overflow_edge_cases() {
    char buffer[10];

    // Stack buffer overflow
    // strcpy(buffer, "This is longer than 10 chars"); // Overflow!

    // Safe copy with bounds check
    strncpy(buffer, "This is longer than 10 chars", sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0'; // Ensure null termination

    // Off-by-one error
    for (int i = 0; i <= 10; i++) { // Wrong! i should be < 10
        // buffer[i] = 'x'; // Buffer overflow when i == 10
    }

    // Correct
    for (int i = 0; i < 10; i++) {
        buffer[i] = 'x';
    }
}
```

## Integer Overflow and Undefined Behavior

### Signed Integer Overflow

```c
#include <limits.h>
#include <stdio.h>

void test_integer_overflow_edge_cases() {
    // Signed integer overflow is undefined behavior in C!
    int max = INT_MAX;

    // Undefined behavior
    // int overflow = max + 1; // UB!

    // Check before operation
    int a = INT_MAX;
    int b = 1;
    if (a > 0 && b > 0 && a > INT_MAX - b) {
        // Overflow would occur
        assert(1); // Detected
    } else {
        int sum = a + b;
    }

    // Unsigned overflow wraps around (defined behavior)
    unsigned int umax = UINT_MAX;
    unsigned int uwrap = umax + 1;
    assert(uwrap == 0); // Wraps to 0

    // Multiplication overflow check
    int x = 100000;
    int y = 100000;
    if (x != 0 && y != 0 && (INT_MAX / x) < y) {
        // Overflow would occur
        assert(1); // Detected
    }
}
```

### Integer Division Edge Cases

```c
void test_division_edge_cases() {
    // Division by zero is undefined behavior
    int x = 10;
    int y = 0;

    // Check before dividing
    if (y != 0) {
        int result = x / y;
    } else {
        // Handle divide by zero
    }

    // Integer division truncates toward zero
    assert(7 / 2 == 3);
    assert(-7 / 2 == -3);

    // Modulo with negative numbers
    assert(7 % 3 == 1);
    assert(-7 % 3 == -1);
    assert(7 % -3 == 1);

    // Special case: INT_MIN / -1 overflows!
    int min = INT_MIN;
    // int overflow = min / -1; // Undefined behavior!
}
```

## Array and Buffer Edge Cases

### Array Bounds

```c
void test_array_bounds_edge_cases() {
    int arr[5] = {1, 2, 3, 4, 5};

    // Valid access
    assert(arr[0] == 1);
    assert(arr[4] == 5);

    // Out of bounds (undefined behavior)
    // int oob = arr[5];  // Past end
    // int neg = arr[-1]; // Before start

    // Pointer arithmetic
    int *ptr = arr;
    assert(*ptr == 1);
    assert(*(ptr + 4) == 5);

    // Going past end
    // int bad = *(ptr + 5); // Undefined behavior
}
```

### Variable Length Arrays (C99)

```c
void test_vla_edge_cases(int n) {
    // VLA with zero or negative size
    if (n <= 0) {
        // Don't create VLA!
        return;
    }

    // Variable length array
    int vla[n];

    // Very large VLA can overflow stack
    // int huge_vla[1000000]; // Stack overflow!

    // Use heap for large allocations
    if (n > 1000) {
        int *heap_array = malloc(n * sizeof(int));
        if (heap_array == NULL) {
            // Allocation failed
            return;
        }
        // Use array...
        free(heap_array);
    } else {
        // Small arrays on stack are OK
        int stack_array[n];
    }
}
```

## String Edge Cases

### C String Operations

```c
#include <string.h>

void test_string_edge_cases() {
    // Empty string
    char empty[] = "";
    assert(strlen(empty) == 0);
    assert(empty[0] == '\0');

    // Null vs empty
    char *null_str = NULL;
    // strlen(null_str); // Undefined behavior!

    // Safe string length
    int safe_len = (null_str != NULL) ? strlen(null_str) : 0;
    assert(safe_len == 0);

    // String without null terminator
    char no_null[5] = {'H', 'e', 'l', 'l', 'o'};
    // strlen(no_null); // Undefined! Reads past end

    // Proper null-terminated string
    char proper[6] = "Hello";
    assert(strlen(proper) == 5);

    // strcpy buffer overflow
    char dest[5];
    // strcpy(dest, "Too long"); // Buffer overflow!

    // Safe copy
    strncpy(dest, "Too long", sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';
}
```

### String Comparison

```c
void test_string_comparison_edge_cases() {
    char *s1 = "hello";
    char *s2 = "hello";
    char s3[] = "hello";

    // Pointer comparison (wrong!)
    // May be true or false depending on string interning
    if (s1 == s2) {
        // May or may not execute
    }

    // Correct string comparison
    assert(strcmp(s1, s3) == 0);

    // Null in comparison
    char *null_str = NULL;
    // strcmp(null_str, "test"); // Undefined behavior!

    // Safe comparison
    int cmp = (null_str != NULL && strcmp(null_str, "test") == 0);
    assert(cmp == 0);

    // Case-insensitive comparison
    assert(strcasecmp("Hello", "HELLO") == 0); // POSIX only
}
```

## Type Conversion Edge Cases

### Implicit Conversions

```c
void test_type_conversion_edge_cases() {
    // Integer promotion
    char c = 127;
    char d = 1;
    // c + d is evaluated as int, not char
    int sum = c + d;
    assert(sum == 128); // Fine as int

    // But assigning back can overflow
    char result = c + d; // Overflow! Result is implementation-defined

    // Signed/unsigned conversion
    int signed_neg = -1;
    unsigned int unsigned_val = signed_neg; // Large positive number!
    assert(unsigned_val == UINT_MAX);

    // Comparison of signed and unsigned
    int s = -1;
    unsigned int u = 1;
    // if (s < u) { // Always false! -1 converted to large unsigned

    // Floating point to integer truncation
    double pi = 3.14159;
    int truncated = (int)pi;
    assert(truncated == 3);

    double large = 1e20;
    int overflow_int = (int)large; // Undefined behavior if doesn't fit!
}
```

## Undefined Behavior

### Common Undefined Behavior

```c
void test_undefined_behavior() {
    // 1. Null pointer dereference
    int *null_ptr = NULL;
    // *null_ptr = 42; // UB

    // 2. Out of bounds array access
    int arr[5];
    // arr[10] = 42; // UB

    // 3. Signed integer overflow
    int max = INT_MAX;
    // max + 1; // UB

    // 4. Divide by zero
    // int x = 10 / 0; // UB

    // 5. Use after free
    int *ptr = malloc(sizeof(int));
    free(ptr);
    // *ptr = 42; // UB

    // 6. Double free
    // free(ptr); // UB (already freed)

    // 7. Uninitialized variable
    int uninitialized;
    // int value = uninitialized; // UB (indeterminate value)

    // 8. Modifying string literal
    char *literal = "hello";
    // literal[0] = 'H'; // UB

    // 9. Overlapping memory in strcpy/memcpy
    char buffer[20] = "hello";
    // strcpy(buffer + 1, buffer); // UB (overlapping)
    // Use memmove for overlapping regions
    memmove(buffer + 1, buffer, strlen(buffer) + 1);

    // 10. Reading uninitialized memory
    int *heap = malloc(sizeof(int));
    // int val = *heap; // UB (not initialized)
    free(heap);
}
```

## C++ Specific Edge Cases

### Object Lifetime

```cpp
#include <memory>
#include <cassert>

void test_cpp_object_lifetime() {
    // Dangling reference
    int* ptr = nullptr;
    {
        int local = 42;
        ptr = &local;
    }
    // *ptr is now dangling! (UB)

    // Use after move
    std::string str = "hello";
    std::string moved = std::move(str);
    // str is now in valid but unspecified state
    // str.size(); // Safe but value is unspecified
    // str.clear(); // Safe
}
```

### Vector Edge Cases

```cpp
#include <vector>

void test_vector_edge_cases() {
    std::vector<int> vec;

    // Empty vector
    assert(vec.empty());
    assert(vec.size() == 0);

    // at() throws, operator[] doesn't
    try {
        vec.at(0); // Throws std::out_of_range
        assert(false);
    } catch (const std::out_of_range&) {
        assert(true);
    }

    // operator[] doesn't check bounds (UB)
    // int val = vec[0]; // Undefined behavior!

    // Iterator invalidation
    vec = {1, 2, 3, 4, 5};
    for (auto it = vec.begin(); it != vec.end(); ++it) {
        if (*it == 3) {
            vec.push_back(6); // Invalidates iterators! (UB)
            // *it; // Undefined behavior
            break;
        }
    }

    // Safe modification
    vec = {1, 2, 3, 4, 5};
    for (size_t i = 0; i < vec.size(); ++i) {
        if (vec[i] == 3) {
            vec.push_back(6); // Safe with index
        }
    }
}
```

### Smart Pointer Edge Cases

```cpp
void test_smart_pointer_edge_cases() {
    // Null unique_ptr
    std::unique_ptr<int> null_ptr;
    assert(null_ptr == nullptr);
    assert(!null_ptr);

    // Dereferencing null smart pointer (UB)
    // *null_ptr; // Undefined behavior!

    // Safe dereference
    if (null_ptr) {
        *null_ptr = 42;
    }

    // Double ownership (compile error)
    std::unique_ptr<int> ptr1(new int(42));
    // std::unique_ptr<int> ptr2 = ptr1; // Compile error (no copy)
    std::unique_ptr<int> ptr2 = std::move(ptr1);
    assert(ptr1 == nullptr); // Moved-from

    // Shared_ptr cycles (memory leak)
    struct Node {
        std::shared_ptr<Node> next;
    };
    auto n1 = std::make_shared<Node>();
    auto n2 = std::make_shared<Node>();
    n1->next = n2;
    n2->next = n1; // Circular reference! (leak)

    // Use weak_ptr to break cycles
}
```

## Testing Frameworks

### Google Test Patterns

```cpp
#include <gtest/gtest.h>

TEST(EdgeCaseTest, NullPointerHandling) {
    int* null_ptr = nullptr;
    EXPECT_EQ(null_ptr, nullptr);
    EXPECT_FALSE(null_ptr);

    // Test null handling
    EXPECT_THROW(process_pointer(null_ptr), std::invalid_argument);
}

TEST(EdgeCaseTest, IntegerOverflow) {
    EXPECT_EQ(INT_MAX, 2147483647);
    EXPECT_EQ(INT_MIN, -2147483648);

    // Check overflow detection
    EXPECT_TRUE(will_overflow(INT_MAX, 1));
    EXPECT_FALSE(will_overflow(100, 200));
}

TEST(EdgeCaseTest, ArrayBounds) {
    int arr[5] = {1, 2, 3, 4, 5};

    EXPECT_EQ(arr[0], 1);
    EXPECT_EQ(arr[4], 5);

    // Death test for out of bounds (ASAN/UBSAN will catch)
    #ifdef __has_feature
    #if __has_feature(address_sanitizer)
    EXPECT_DEATH(arr[10], "");
    #endif
    #endif
}

// Parameterized tests for edge cases
class IntegerBoundaryTest : public testing::TestWithParam<int> {};

TEST_P(IntegerBoundaryTest, HandlesAllValues) {
    int value = GetParam();
    EXPECT_NO_THROW(process_integer(value));
}

INSTANTIATE_TEST_SUITE_P(
    EdgeCases,
    IntegerBoundaryTest,
    testing::Values(
        INT_MIN,
        INT_MIN + 1,
        -1,
        0,
        1,
        INT_MAX - 1,
        INT_MAX
    )
);

// String edge cases
class StringEdgeCaseTest : public testing::TestWithParam<const char*> {};

TEST_P(StringEdgeCaseTest, HandlesEdgeCases) {
    const char* str = GetParam();
    if (str == nullptr) {
        EXPECT_THROW(process_string(str), std::invalid_argument);
    } else {
        EXPECT_NO_THROW(process_string(str));
    }
}

INSTANTIATE_TEST_SUITE_P(
    StringEdges,
    StringEdgeCaseTest,
    testing::Values(
        nullptr,
        "",
        "a",
        "very long string with many characters to test buffer handling",
        "\n\t\r",
        "unicode: 你好"
    )
);
```

### Testing with Sanitizers

```cpp
// Compile with sanitizers to catch edge cases:
// -fsanitize=address    (AddressSanitizer - memory errors)
// -fsanitize=undefined  (UndefinedBehaviorSanitizer - UB)
// -fsanitize=thread     (ThreadSanitizer - race conditions)

TEST(SanitizerTest, DetectsBufferOverflow) {
    char buffer[10];

    // ASAN will catch this
    // buffer[10] = 'x'; // Buffer overflow

    // Safe access
    buffer[9] = 'x';
    EXPECT_EQ(buffer[9], 'x');
}

TEST(SanitizerTest, DetectsUseAfterFree) {
    int* ptr = new int(42);
    delete ptr;

    // ASAN will catch this
    // *ptr = 10; // Use after free

    // Safe: don't use after delete
}

TEST(SanitizerTest, DetectsUndefinedBehavior) {
    int max = INT_MAX;

    // UBSAN will catch this
    // int overflow = max + 1; // Signed overflow (UB)

    // Safe: check before operation
    bool would_overflow = (max > INT_MAX - 1);
    EXPECT_TRUE(would_overflow);
}
```

### Valgrind Integration

```bash
# Run tests with Valgrind to detect memory issues
valgrind --leak-check=full --track-origins=yes ./my_tests

# Example Valgrind checks:
# - Memory leaks
# - Use of uninitialized values
# - Invalid memory access
# - Double free
# - Mismatched allocation/deallocation
```

### Helper Functions

```cpp
// Helper for safe string operations
inline size_t safe_strlen(const char* str) {
    return str ? strlen(str) : 0;
}

// Helper for overflow detection
inline bool add_would_overflow(int a, int b) {
    if (a > 0 && b > 0) {
        return a > INT_MAX - b;
    }
    if (a < 0 && b < 0) {
        return a < INT_MIN - b;
    }
    return false;
}

// Helper for safe array access
template<typename T, size_t N>
inline bool is_valid_index(const T (&arr)[N], size_t idx) {
    return idx < N;
}
```
