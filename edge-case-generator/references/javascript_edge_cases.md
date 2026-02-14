# JavaScript/TypeScript Edge Cases and Testing Patterns

JavaScript and TypeScript-specific edge cases, common pitfalls, and testing patterns using Jest, Mocha, and other frameworks.

## Table of Contents

1. [Type Coercion and Truthiness](#type-coercion-and-truthiness)
2. [Undefined vs Null](#undefined-vs-null)
3. [Array Edge Cases](#array-edge-cases)
4. [Object Edge Cases](#object-edge-cases)
5. [String Edge Cases](#string-edge-cases)
6. [Number Edge Cases](#number-edge-cases)
7. [Async/Promise Edge Cases](#asyncpromise-edge-cases)
8. [this Binding](#this-binding)
9. [TypeScript-Specific](#typescript-specific)
10. [Testing Frameworks](#testing-frameworks)

## Type Coercion and Truthiness

### Falsy Values

```javascript
describe('falsy values', () => {
  test('all falsy values', () => {
    const falsyValues = [false, 0, -0, 0n, '', null, undefined, NaN];

    falsyValues.forEach(value => {
      expect(Boolean(value)).toBe(false);
      expect(!!value).toBe(false);
    });
  });

  test('everything else is truthy', () => {
    expect(!![]).toBe(true);      // Empty array is truthy!
    expect(!!{}).toBe(true);      // Empty object is truthy!
    expect(!!'0').toBe(true);     // String "0" is truthy!
    expect(!!'false').toBe(true); // String "false" is truthy!
  });
});
```

### Type Coercion Edge Cases

```javascript
describe('type coercion edge cases', () => {
  test('equality operators', () => {
    // == vs ===
    expect(0 == false).toBe(true);   // Coercion!
    expect(0 === false).toBe(false); // Strict equality

    expect('' == false).toBe(true);
    expect('' === false).toBe(false);

    expect(null == undefined).toBe(true);   // Special case
    expect(null === undefined).toBe(false);

    // Unexpected coercions
    expect([] == false).toBe(true);   // [] coerces to ''
    expect([1] == 1).toBe(true);      // [1] coerces to '1'
    expect(['1'] == 1).toBe(true);    // ['1'] coerces to '1'
  });

  test('addition coercion', () => {
    // Number + String = String (concatenation)
    expect(1 + '2').toBe('12');
    expect('1' + 2).toBe('12');

    // Number + Number = Number
    expect(1 + 2).toBe(3);

    // Array coercion
    expect([1, 2] + [3, 4]).toBe('1,23,4');
    expect([] + []).toBe('');
    expect([] + {}).toBe('[object Object]');
  });

  test('subtraction coercion', () => {
    // Subtraction always tries to convert to numbers
    expect('5' - 2).toBe(3);
    expect('5' - '2').toBe(3);
    expect('five' - 2).toBeNaN();
  });
});
```

## Undefined vs Null

### Edge Cases

```javascript
describe('undefined vs null edge cases', () => {
  test('undefined is default for missing things', () => {
    let uninitializedVar;
    expect(uninitializedVar).toBeUndefined();

    const obj = {};
    expect(obj.missingProperty).toBeUndefined();

    function noReturn() {}
    expect(noReturn()).toBeUndefined();

    function missingParam(param) {
      return param;
    }
    expect(missingParam()).toBeUndefined();
  });

  test('null must be explicitly assigned', () => {
    const explicitNull = null;
    expect(explicitNull).toBeNull();
    expect(explicitNull == undefined).toBe(true);   // Loose equality
    expect(explicitNull === undefined).toBe(false); // Strict equality
  });

  test('typeof edge cases', () => {
    expect(typeof undefined).toBe('undefined');
    expect(typeof null).toBe('object');  // Famous JavaScript bug!
  });

  test('checking for null or undefined', () => {
    function isNullish(value) {
      return value == null; // Checks both null and undefined
    }

    expect(isNullish(null)).toBe(true);
    expect(isNullish(undefined)).toBe(true);
    expect(isNullish(0)).toBe(false);
    expect(isNullish('')).toBe(false);
  });
});
```

## Array Edge Cases

### Array Methods

```javascript
describe('array edge cases', () => {
  test('empty array edge cases', () => {
    const arr = [];

    expect(arr.length).toBe(0);
    expect(arr[0]).toBeUndefined();
    expect(arr[-1]).toBeUndefined(); // Negative indexing doesn't work
    expect(arr.pop()).toBeUndefined();
    expect(arr.shift()).toBeUndefined();
  });

  test('sparse arrays', () => {
    const sparse = new Array(3);  // [empty × 3]

    expect(sparse.length).toBe(3);
    expect(sparse[0]).toBeUndefined();
    expect(0 in sparse).toBe(false); // No actual element!

    // forEach skips empty slots
    let count = 0;
    sparse.forEach(() => count++);
    expect(count).toBe(0);

    // map also skips empty slots
    const mapped = sparse.map(x => x * 2);
    expect(mapped.length).toBe(3);
    expect(mapped[0]).toBeUndefined();
  });

  test('array-like objects', () => {
    const arrayLike = { 0: 'a', 1: 'b', length: 2 };

    // Can't use array methods directly
    expect(() => arrayLike.map(x => x)).toThrow();

    // Convert to real array
    const realArray = Array.from(arrayLike);
    expect(realArray).toEqual(['a', 'b']);

    // Or use call
    const result = Array.prototype.map.call(arrayLike, x => x.toUpperCase());
    expect(result).toEqual(['A', 'B']);
  });

  test('mutating methods edge cases', () => {
    // splice with no elements to remove
    const arr = [1, 2, 3];
    arr.splice(1, 0, 'a', 'b');
    expect(arr).toEqual([1, 'a', 'b', 2, 3]);

    // sort mutates in place and returns same array
    const original = [3, 1, 2];
    const sorted = original.sort();
    expect(sorted).toBe(original); // Same reference!
    expect(original).toEqual([1, 2, 3]);

    // Default sort is lexicographic!
    expect([10, 2, 1].sort()).toEqual([1, 10, 2]); // "10" < "2"
    expect([10, 2, 1].sort((a, b) => a - b)).toEqual([1, 2, 10]);
  });

  test('reduce edge cases', () => {
    // Empty array without initial value
    expect(() => [].reduce((acc, x) => acc + x)).toThrow();

    // Empty array with initial value
    expect([].reduce((acc, x) => acc + x, 0)).toBe(0);

    // Single element without initial value
    expect([5].reduce((acc, x) => acc + x)).toBe(5);
  });
});
```

## Object Edge Cases

### Property Access

```javascript
describe('object edge cases', () => {
  test('property access edge cases', () => {
    const obj = { key: 'value' };

    // Undefined properties
    expect(obj.missing).toBeUndefined();
    expect(obj['missing']).toBeUndefined();

    // Nested undefined access throws
    expect(() => obj.missing.nested).toThrow();

    // Optional chaining (safe)
    expect(obj.missing?.nested).toBeUndefined();
  });

  test('object keys edge cases', () => {
    const obj = {
      '1': 'number key',
      1: 'numeric key',      // Same as '1'
      true: 'boolean key',
      [Symbol('sym')]: 'symbol key'
    };

    expect(obj['1']).toBe('numeric key');
    expect(obj[1]).toBe('numeric key');
    expect(Object.keys(obj)).toEqual(['1', 'true']); // Symbols excluded!
  });

  test('prototype edge cases', () => {
    const obj = Object.create({ inherited: 'value' });
    obj.own = 'own value';

    // hasOwnProperty vs in
    expect('own' in obj).toBe(true);
    expect('inherited' in obj).toBe(true);
    expect(obj.hasOwnProperty('own')).toBe(true);
    expect(obj.hasOwnProperty('inherited')).toBe(false);

    // Object.keys only returns own properties
    expect(Object.keys(obj)).toEqual(['own']);
  });

  test('object comparison edge cases', () => {
    // Objects are compared by reference
    expect({} === {}).toBe(false);
    expect({ a: 1 } == { a: 1 }).toBe(false);

    const obj1 = { a: 1 };
    const obj2 = obj1;
    expect(obj1 === obj2).toBe(true);

    // Deep equality requires special comparison
    expect(JSON.stringify({ a: 1 }) === JSON.stringify({ a: 1 })).toBe(true);
  });
});
```

## String Edge Cases

### String Operations

```javascript
describe('string edge cases', () => {
  test('empty string edge cases', () => {
    expect(''.length).toBe(0);
    expect(''[0]).toBeUndefined();
    expect(''.charAt(0)).toBe('');
    expect(''.split('')).toEqual([]);
  });

  test('unicode edge cases', () => {
    // Emoji can have surprising length
    expect('😀'.length).toBe(2);  // Surrogate pair!
    expect('👨‍👩‍👧‍👦'.length).toBe(11); // Family emoji
    expect([...'😀'].length).toBe(1);  // Spread operator handles it correctly

    // String indexing doesn't work well with emoji
    expect('😀'[0]).not.toBe('😀');
    expect([...'😀'][0]).toBe('😀');
  });

  test('template literal edge cases', () => {
    // Null and undefined in template literals
    expect(`value: ${null}`).toBe('value: null');
    expect(`value: ${undefined}`).toBe('value: undefined');

    // Object in template literal
    expect(`value: ${{a: 1}}`).toBe('value: [object Object]');

    // Nested template literals
    expect(`outer ${`inner`}`).toBe('outer inner');
  });

  test('string comparison edge cases', () => {
    // Case sensitivity
    expect('Hello' === 'hello').toBe(false);
    expect('Hello'.toLowerCase() === 'hello').toBe(false);

    // Whitespace
    expect('hello' === ' hello').toBe(false);
    expect('hello'.trim() === 'hello').toBe(true);

    // Number strings
    expect('10' < '2').toBe(true);   // Lexicographic!
    expect(Number('10') < Number('2')).toBe(false);
  });
});
```

## Number Edge Cases

### Special Number Values

```javascript
describe('number edge cases', () => {
  test('NaN edge cases', () => {
    // NaN is the only value not equal to itself
    expect(NaN === NaN).toBe(false);
    expect(NaN == NaN).toBe(false);
    expect(Number.isNaN(NaN)).toBe(true);

    // Operations that produce NaN
    expect(Number.isNaN(0 / 0)).toBe(true);
    expect(Number.isNaN(parseInt('abc'))).toBe(true);
    expect(Number.isNaN(Math.sqrt(-1))).toBe(true);

    // Type coercion with NaN
    expect(NaN + 1).toBeNaN();
    expect(NaN * 0).toBeNaN();
  });

  test('Infinity edge cases', () => {
    expect(1 / 0).toBe(Infinity);
    expect(-1 / 0).toBe(-Infinity);
    expect(Infinity + 1).toBe(Infinity);
    expect(Infinity * 2).toBe(Infinity);
    expect(Infinity / Infinity).toBeNaN();
    expect(Infinity - Infinity).toBeNaN();
  });

  test('integer limits', () => {
    // JavaScript uses 64-bit floats for all numbers
    expect(Number.MAX_SAFE_INTEGER).toBe(9007199254740991);
    expect(Number.MIN_SAFE_INTEGER).toBe(-9007199254740991);

    // Beyond safe integer range
    expect(Number.MAX_SAFE_INTEGER + 1).toBe(Number.MAX_SAFE_INTEGER + 2); // Precision loss!

    // BigInt for large integers
    expect(BigInt(Number.MAX_SAFE_INTEGER) + 1n).not.toBe(BigInt(Number.MAX_SAFE_INTEGER) + 2n);
  });

  test('floating point precision', () => {
    expect(0.1 + 0.2).not.toBe(0.3); // Classic!
    expect(Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON).toBe(true);

    // Comparison with epsilon
    function areCloseEnough(a, b, epsilon = 0.00001) {
      return Math.abs(a - b) < epsilon;
    }
    expect(areCloseEnough(0.1 + 0.2, 0.3)).toBe(true);
  });

  test('parseInt/parseFloat edge cases', () => {
    // Radix matters!
    expect(parseInt('10')).toBe(10);
    expect(parseInt('10', 8)).toBe(8);
    expect(parseInt('10', 16)).toBe(16);

    // Parsing stops at first invalid character
    expect(parseInt('123abc')).toBe(123);
    expect(parseInt('abc123')).toBeNaN();

    // parseFloat doesn't take radix
    expect(parseFloat('3.14')).toBe(3.14);
    expect(parseFloat('3.14more')).toBe(3.14);
  });
});
```

## Async/Promise Edge Cases

### Promise Edge Cases

```javascript
describe('async/promise edge cases', () => {
  test('unhandled promise rejection', async () => {
    const promise = Promise.reject(new Error('test error'));

    // Must handle rejection to avoid unhandled rejection warning
    await expect(promise).rejects.toThrow('test error');
  });

  test('promise constructor executor runs synchronously', () => {
    let executed = false;

    new Promise(resolve => {
      executed = true;
      resolve();
    });

    // Executor runs immediately, before promise is returned
    expect(executed).toBe(true);
  });

  test('promise resolution is always async', async () => {
    let resolved = false;

    Promise.resolve().then(() => {
      resolved = true;
    });

    // Still false immediately after
    expect(resolved).toBe(false);

    // Wait for next tick
    await new Promise(resolve => setImmediate(resolve));
    expect(resolved).toBe(true);
  });

  test('async function always returns promise', async () => {
    async function returns42() {
      return 42;
    }

    const result = returns42();
    expect(result).toBeInstanceOf(Promise);
    expect(await result).toBe(42);
  });

  test('Promise.all edge cases', async () => {
    // Empty array resolves immediately
    await expect(Promise.all([])).resolves.toEqual([]);

    // Rejects on first rejection
    const mixed = [
      Promise.resolve(1),
      Promise.reject(new Error('fail')),
      Promise.resolve(3)
    ];
    await expect(Promise.all(mixed)).rejects.toThrow('fail');

    // Non-promise values are wrapped
    await expect(Promise.all([1, 2, 3])).resolves.toEqual([1, 2, 3]);
  });

  test('race condition edge cases', async () => {
    // Empty race never settles!
    const emptyRace = Promise.race([]);
    const timeout = new Promise(resolve => setTimeout(() => resolve('timeout'), 100));
    expect(await Promise.race([emptyRace, timeout])).toBe('timeout');
  });
});
```

## this Binding

### this Context Edge Cases

```javascript
describe('this binding edge cases', () => {
  test('lost this context', () => {
    const obj = {
      value: 42,
      getValue() {
        return this.value;
      }
    };

    expect(obj.getValue()).toBe(42);

    const extracted = obj.getValue;
    expect(extracted()).toBeUndefined(); // Lost context!

    // Fix with bind
    const bound = obj.getValue.bind(obj);
    expect(bound()).toBe(42);
  });

  test('arrow function this binding', () => {
    const obj = {
      value: 42,
      getValueArrow: () => this.value,
      getValueRegular() {
        return (() => this.value)(); // Arrow inherits this
      }
    };

    expect(obj.getValueArrow()).toBeUndefined(); // Arrow doesn't bind this
    expect(obj.getValueRegular()).toBe(42);      // Inherits from regular function
  });

  test('callback this binding', (done) => {
    const obj = {
      value: 42,
      delayedGetValue() {
        setTimeout(function() {
          expect(this.value).toBeUndefined(); // Lost context
          done();
        }, 10);
      }
    };

    obj.delayedGetValue();
  });
});
```

## TypeScript-Specific

### Type Edge Cases

```typescript
describe('TypeScript type edge cases', () => {
  test('null vs undefined in TypeScript', () => {
    // In strict mode, null and undefined are different
    const maybeString: string | null = null;
    const maybeUndefined: string | undefined = undefined;

    // Can't assign null to undefined and vice versa
    // @ts-expect-error
    const wrong1: string | null = undefined;
    // @ts-expect-error
    const wrong2: string | undefined = null;
  });

  test('type narrowing edge cases', () => {
    function process(value: string | number | null) {
      // Type guard
      if (typeof value === 'string') {
        expect(value.toUpperCase()).toBeTruthy();
      } else if (typeof value === 'number') {
        expect(value.toFixed(2)).toBeTruthy();
      } else {
        // value is null here
        expect(value).toBeNull();
      }
    }

    process('hello');
    process(42);
    process(null);
  });

  test('any vs unknown', () => {
    let anyValue: any = 42;
    let unknownValue: unknown = 42;

    // any allows anything
    expect(anyValue.nonExistentMethod).toBeUndefined();

    // unknown requires type checking
    // @ts-expect-error
    unknownValue.toFixed(2);

    // Must narrow type first
    if (typeof unknownValue === 'number') {
      expect(unknownValue.toFixed(2)).toBe('42.00');
    }
  });
});
```

## Testing Frameworks

### Jest Patterns

```javascript
describe('Jest testing patterns', () => {
  // Test edge cases with parameterized tests
  test.each([
    [null, 'null'],
    [undefined, 'undefined'],
    [0, 'zero'],
    ['', 'empty string'],
    [[], 'empty array'],
    [{}, 'empty object'],
  ])('handles %s (%s)', (input, description) => {
    expect(handleInput(input)).toBeDefined();
  });

  // Async edge cases
  test('handles async rejection', async () => {
    await expect(asyncFunction()).rejects.toThrow('error');
  });

  test('timeout for slow operations', async () => {
    await expect(slowOperation()).resolves.toBe('result');
  }, 10000); // 10 second timeout

  // Mock edge cases
  test('mocks handle edge cases', () => {
    const mockFn = jest.fn()
      .mockReturnValueOnce(1)
      .mockReturnValueOnce(2)
      .mockReturnValue(3);

    expect(mockFn()).toBe(1);
    expect(mockFn()).toBe(2);
    expect(mockFn()).toBe(3);
    expect(mockFn()).toBe(3); // Continues returning 3
  });
});
```

### Testing Edge Cases Checklist

```javascript
// Comprehensive edge case test template
describe('function edge cases', () => {
  test('null input', () => {
    expect(() => func(null)).toThrow();
  });

  test('undefined input', () => {
    expect(() => func(undefined)).toThrow();
  });

  test('empty input', () => {
    expect(func('')).toEqual(expectedEmptyResult);
  });

  test('single item', () => {
    expect(func([1])).toEqual(expectedSingleResult);
  });

  test('large input', () => {
    const largeInput = new Array(100000).fill(1);
    expect(() => func(largeInput)).not.toThrow();
  });

  test('invalid type', () => {
    expect(() => func(123)).toThrow(TypeError);
  });

  test('concurrent calls', async () => {
    const promises = Array(100).fill(null).map(() => asyncFunc());
    const results = await Promise.all(promises);
    expect(results).toHaveLength(100);
  });
});
```
