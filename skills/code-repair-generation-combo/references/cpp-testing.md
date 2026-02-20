# C++ Testing Patterns

## Google Test Framework

### Basic Test Structure

```cpp
#include <gtest/gtest.h>

TEST(TestSuiteName, TestName) {
    // Arrange
    int input = 5;

    // Act
    int result = functionUnderTest(input);

    // Assert
    EXPECT_EQ(expected, result);
}
```

### Common Assertions

```cpp
EXPECT_EQ(expected, actual);      // Non-fatal
ASSERT_EQ(expected, actual);      // Fatal (stops test)
EXPECT_NE(unexpected, actual);
EXPECT_TRUE(condition);
EXPECT_FALSE(condition);
EXPECT_LT(val1, val2);            // Less than
EXPECT_LE(val1, val2);            // Less or equal
EXPECT_GT(val1, val2);            // Greater than
EXPECT_GE(val1, val2);            // Greater or equal
EXPECT_STREQ(str1, str2);         // C-string equality
EXPECT_THROW(statement, exception_type);
EXPECT_NO_THROW(statement);
```

### Exception Testing

```cpp
TEST(TestSuiteName, TestException) {
    EXPECT_THROW({
        functionThatShouldThrow(invalidInput);
    }, std::invalid_argument);
}
```

### Parametrized Tests

```cpp
#include <gtest/gtest.h>

class FactorialTest : public ::testing::TestWithParam<std::pair<int, int>> {};

TEST_P(FactorialTest, ComputesFactorial) {
    auto [input, expected] = GetParam();
    EXPECT_EQ(expected, factorial(input));
}

INSTANTIATE_TEST_SUITE_P(
    FactorialTests,
    FactorialTest,
    ::testing::Values(
        std::make_pair(0, 1),
        std::make_pair(1, 1),
        std::make_pair(5, 120)
    )
);
```

### Test Fixtures

```cpp
class MyClassTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Initialize test fixtures
    }

    void TearDown() override {
        // Clean up
    }

    MyClass* obj;
};

TEST_F(MyClassTest, TestMethod) {
    EXPECT_TRUE(obj->method());
}
```

### Edge Cases to Test

- Null pointers
- Empty containers
- Boundary values (INT_MIN, INT_MAX, SIZE_MAX)
- Invalid inputs
- Memory leaks (use valgrind)
- Buffer overflows

### Test Organization

```cpp
TEST(TestSuiteName, NormalCase) { }
TEST(TestSuiteName, EdgeCase) { }
TEST(TestSuiteName, ErrorCase) { }
```

## Catch2 Framework (Alternative)

```cpp
#include <catch2/catch.hpp>

TEST_CASE("Description of test", "[tag]") {
    REQUIRE(condition);
    CHECK(condition);  // Non-fatal
}
```
