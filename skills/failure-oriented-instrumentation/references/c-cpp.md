# C/C++ Instrumentation Patterns

## Printf/Fprintf Debugging

### Function Entry/Exit
```c
#include <stdio.h>

int target_function(int arg1, const char* arg2) {
    fprintf(stderr, "ENTER target_function: arg1=%d, arg2=%s\n", arg1, arg2);

    int result = process(arg1, arg2);

    fprintf(stderr, "EXIT target_function: result=%d\n", result);
    return result;
}
```

### Variable Tracking
```c
int x = compute_value();
fprintf(stderr, "Variable x after compute: %d\n", x);

// Track pointer values
void* ptr = allocate_memory();
fprintf(stderr, "Allocated pointer: %p\n", ptr);
```

### Conditional Branch Tracking
```c
if (condition) {
    fprintf(stderr, "Branch: condition=true, value=%d\n", condition);
    // true branch
} else {
    fprintf(stderr, "Branch: condition=false, value=%d\n", condition);
    // false branch
}
```

### Loop Iteration Tracking
```c
for (int i = 0; i < count; i++) {
    fprintf(stderr, "Loop iteration %d: item=%d\n", i, items[i]);
    // loop body
}
```

## Macro-Based Instrumentation

```c
#ifdef DEBUG
#define LOG_DEBUG(fmt, ...) \
    fprintf(stderr, "[DEBUG] %s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#else
#define LOG_DEBUG(fmt, ...) ((void)0)
#endif

#define LOG_ENTER(func) \
    fprintf(stderr, "ENTER %s at %s:%d\n", func, __FILE__, __LINE__)

#define LOG_EXIT(func) \
    fprintf(stderr, "EXIT %s at %s:%d\n", func, __FILE__, __LINE__)

// Usage
void my_function(int x) {
    LOG_ENTER("my_function");
    LOG_DEBUG("x=%d", x);
    // function body
    LOG_EXIT("my_function");
}
```

## Assertions

```c
#include <assert.h>

void process_data(int* data, size_t size) {
    assert(data != NULL && "Data pointer should not be NULL");
    assert(size > 0 && "Size should be positive");

    // process data

    assert(result != NULL && "Result should not be NULL");
}
```

## Timing Information

```c
#include <time.h>

clock_t start = clock();
expensive_operation();
clock_t end = clock();
double elapsed = ((double)(end - start)) / CLOCKS_PER_SEC;
fprintf(stderr, "Operation took %.3f seconds\n", elapsed);
```

## C++ Logging

### iostream-based
```cpp
#include <iostream>
#include <chrono>

void target_function(int arg1, const std::string& arg2) {
    std::cerr << "ENTER target_function: arg1=" << arg1
              << ", arg2=" << arg2 << std::endl;

    try {
        int result = process(arg1, arg2);
        std::cerr << "EXIT target_function: result=" << result << std::endl;
        return result;
    } catch (const std::exception& e) {
        std::cerr << "EXCEPTION in target_function: " << e.what() << std::endl;
        throw;
    }
}
```

### RAII-based Scoped Instrumentation
```cpp
class ScopedInstrumentation {
    std::string name;
    std::chrono::time_point<std::chrono::high_resolution_clock> start;

public:
    ScopedInstrumentation(const std::string& n) : name(n) {
        start = std::chrono::high_resolution_clock::now();
        std::cerr << "ENTER section: " << name << std::endl;
    }

    ~ScopedInstrumentation() {
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cerr << "EXIT section: " << name
                  << " (" << duration.count() << "ms)" << std::endl;
    }
};

// Usage
void process_data() {
    ScopedInstrumentation instr("data_processing");
    // code to instrument
}
```

## Function Wrapper Pattern

```cpp
template<typename Func, typename... Args>
auto instrument_call(const char* name, Func&& func, Args&&... args) {
    std::cerr << "CALL " << name << std::endl;
    try {
        auto result = func(std::forward<Args>(args)...);
        std::cerr << "RETURN " << name << std::endl;
        return result;
    } catch (...) {
        std::cerr << "EXCEPTION " << name << std::endl;
        throw;
    }
}

// Usage
auto result = instrument_call("my_function", my_function, arg1, arg2);
```

## Memory Tracking

```c
void* instrumented_malloc(size_t size, const char* file, int line) {
    void* ptr = malloc(size);
    fprintf(stderr, "MALLOC: %zu bytes at %p (%s:%d)\n", size, ptr, file, line);
    return ptr;
}

void instrumented_free(void* ptr, const char* file, int line) {
    fprintf(stderr, "FREE: %p (%s:%d)\n", ptr, file, line);
    free(ptr);
}

#define MALLOC(size) instrumented_malloc(size, __FILE__, __LINE__)
#define FREE(ptr) instrumented_free(ptr, __FILE__, __LINE__)
```

## GDB Scripting for Dynamic Instrumentation

```gdb
# Set breakpoint and print variables
break target_function
commands
    silent
    printf "ENTER target_function: arg1=%d\n", arg1
    continue
end

# Watchpoint for variable changes
watch my_variable
commands
    silent
    printf "Variable changed: old=%d, new=%d\n", $old_value, my_variable
    continue
end
```
