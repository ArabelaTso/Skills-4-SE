# Language-Specific Reduction Techniques

## Python

### Test Structure

Python tests typically have:
- Imports
- Test setup (fixtures, data)
- Test execution
- Assertions
- Cleanup

### Reduction Strategy

**Preserve:**
- Required imports (used by remaining code)
- Test function signature
- At least one assertion

**Remove:**
- Unused imports
- Unnecessary setup
- Extra assertions
- Docstrings and comments

### Example

```python
# Original (20 lines)
import unittest
import sys
import os
from mymodule import MyClass, helper_function

class TestMyClass(unittest.TestCase):
    def setUp(self):
        self.obj = MyClass()
        self.data = [1, 2, 3, 4, 5]

    def test_process(self):
        """Test the process method"""
        # Setup test data
        input_data = self.data

        # Execute
        result = self.obj.process(input_data)

        # Verify
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(x > 0 for x in result))

# Reduced (6 lines)
from mymodule import MyClass

class TestMyClass:
    def test_process(self):
        result = MyClass().process([1, 2, 3, 4, 5])
        self.assertTrue(all(x > 0 for x in result))
```

### Python-Specific Tools

**AST-based reduction:**
```python
import ast

def remove_node(tree, node_to_remove):
    """Remove a node from AST"""
    class NodeRemover(ast.NodeTransformer):
        def visit(self, node):
            if node is node_to_remove:
                return None
            return self.generic_visit(node)

    return NodeRemover().visit(tree)
```

## JavaScript/TypeScript

### Test Structure

JavaScript tests typically have:
- Imports/requires
- Test suite (describe blocks)
- Test cases (it/test blocks)
- Assertions (expect/assert)
- Mocks and spies

### Reduction Strategy

**Preserve:**
- Test framework imports (jest, mocha, etc.)
- Test function structure
- Core assertions

**Remove:**
- Unnecessary describe blocks
- Extra test cases
- Mock setup if not needed
- Console logs

### Example

```javascript
// Original (25 lines)
const { expect } = require('chai');
const sinon = require('sinon');
const MyClass = require('./MyClass');
const helper = require('./helper');

describe('MyClass', () => {
    let instance;
    let stub;

    beforeEach(() => {
        instance = new MyClass();
        stub = sinon.stub(helper, 'getData').returns([1, 2, 3]);
    });

    afterEach(() => {
        stub.restore();
    });

    it('should process data correctly', () => {
        const result = instance.process();
        expect(result).to.be.an('array');
        expect(result).to.have.lengthOf(3);
        expect(result[0]).to.be.greaterThan(0);
    });
});

// Reduced (5 lines)
const { expect } = require('chai');
const MyClass = require('./MyClass');

it('should process data correctly', () => {
    expect(new MyClass().process()[0]).to.be.greaterThan(0);
});
```

## Java

### Test Structure

Java tests typically have:
- Imports
- Test class
- Setup/teardown methods (@Before, @After)
- Test methods (@Test)
- Assertions

### Reduction Strategy

**Preserve:**
- Test framework imports (JUnit, TestNG)
- Test class structure
- @Test annotation
- Core assertions

**Remove:**
- Unnecessary @Before/@After
- Extra test methods
- Verbose assertions
- Comments

### Example

```java
// Original (30 lines)
import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

public class MyClassTest {
    private MyClass instance;
    private TestData data;

    @Before
    public void setUp() {
        instance = new MyClass();
        data = new TestData();
        data.initialize();
    }

    @After
    public void tearDown() {
        instance.cleanup();
        data.cleanup();
    }

    @Test
    public void testProcess() {
        List<Integer> input = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> result = instance.process(input);

        assertNotNull(result);
        assertEquals(5, result.size());
        assertTrue(result.get(0) > 0);
    }
}

// Reduced (8 lines)
import org.junit.Test;
import static org.junit.Assert.*;

public class MyClassTest {
    @Test
    public void testProcess() {
        assertTrue(new MyClass().process(Arrays.asList(1, 2, 3)).get(0) > 0);
    }
}
```

## C/C++

### Test Structure

C/C++ tests typically have:
- Includes
- Test fixtures (if using framework)
- Test functions
- Assertions (assert, EXPECT, etc.)

### Reduction Strategy

**Preserve:**
- Required includes
- Test framework macros
- Core assertions

**Remove:**
- Unnecessary includes
- Setup/teardown if not needed
- Extra assertions
- Debug prints

### Example

```cpp
// Original (25 lines)
#include <gtest/gtest.h>
#include <vector>
#include <iostream>
#include "MyClass.h"
#include "TestHelper.h"

class MyClassTest : public ::testing::Test {
protected:
    void SetUp() override {
        instance = new MyClass();
        data = {1, 2, 3, 4, 5};
    }

    void TearDown() override {
        delete instance;
    }

    MyClass* instance;
    std::vector<int> data;
};

TEST_F(MyClassTest, ProcessTest) {
    auto result = instance->process(data);
    EXPECT_FALSE(result.empty());
    EXPECT_EQ(result.size(), 5);
    EXPECT_GT(result[0], 0);
}

// Reduced (7 lines)
#include <gtest/gtest.h>
#include "MyClass.h"

TEST(MyClassTest, ProcessTest) {
    MyClass instance;
    EXPECT_GT(instance.process({1, 2, 3})[0], 0);
}
```

## Input Files

### Text Files

**Strategy:**
- Remove lines one at a time
- Try removing blocks of lines
- Preserve file format structure

**Example:**
```
# Original (100 lines of data)
header: value
config: setting
data: line1
data: line2
...
data: line100

# Reduced (5 lines)
header: value
data: line42
data: line43
```

### JSON

**Strategy:**
- Remove object properties
- Remove array elements
- Preserve JSON structure

**Example:**
```json
// Original
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 35}
  ],
  "settings": {
    "timeout": 5000,
    "retries": 3,
    "debug": true
  }
}

// Reduced
{
  "users": [
    {"id": 2, "name": "Bob"}
  ]
}
```

### XML

**Strategy:**
- Remove elements
- Remove attributes
- Preserve XML structure and namespaces

**Example:**
```xml
<!-- Original -->
<root xmlns="http://example.com">
  <config>
    <setting name="timeout">5000</setting>
    <setting name="retries">3</setting>
  </config>
  <data>
    <item id="1" value="foo"/>
    <item id="2" value="bar"/>
    <item id="3" value="baz"/>
  </data>
</root>

<!-- Reduced -->
<root xmlns="http://example.com">
  <data>
    <item id="2" value="bar"/>
  </data>
</root>
```

## Framework-Specific Considerations

### pytest (Python)

**Preserve:**
- Fixture dependencies
- Parametrize decorators (if needed)
- Markers

**Example:**
```python
# Original
@pytest.fixture
def setup_data():
    return [1, 2, 3, 4, 5]

@pytest.mark.slow
@pytest.mark.parametrize("input,expected", [
    ([1, 2], 2),
    ([3, 4], 4),
])
def test_process(setup_data, input, expected):
    result = process(input)
    assert len(result) == expected

# Reduced
def test_process():
    assert len(process([1, 2])) == 2
```

### Jest (JavaScript)

**Preserve:**
- Mock setup if needed
- Async/await structure

**Example:**
```javascript
// Original
jest.mock('./api');

describe('fetchData', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('should fetch data', async () => {
        const mockData = { id: 1, name: 'test' };
        api.getData.mockResolvedValue(mockData);

        const result = await fetchData();

        expect(result).toEqual(mockData);
        expect(api.getData).toHaveBeenCalledTimes(1);
    });
});

// Reduced
jest.mock('./api');

it('should fetch data', async () => {
    api.getData.mockResolvedValue({ id: 1 });
    expect(await fetchData()).toEqual({ id: 1 });
});
```

### JUnit (Java)

**Preserve:**
- @Test annotation
- Exception expectations

**Example:**
```java
// Original
@Test(expected = IllegalArgumentException.class)
public void testInvalidInput() {
    MyClass instance = new MyClass();
    instance.configure(new Config());
    instance.process(null);
}

// Reduced
@Test(expected = IllegalArgumentException.class)
public void testInvalidInput() {
    new MyClass().process(null);
}
```
