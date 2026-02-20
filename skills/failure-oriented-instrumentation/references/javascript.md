# JavaScript/TypeScript Instrumentation Patterns

## Console Logging

### Function Entry/Exit
```javascript
function targetFunction(arg1, arg2) {
    console.log(`ENTER targetFunction: arg1=${arg1}, arg2=${arg2}`);
    try {
        const result = process(arg1, arg2);
        console.log(`EXIT targetFunction: result=${result}`);
        return result;
    } catch (error) {
        console.error(`EXCEPTION in targetFunction:`, error);
        throw error;
    }
}
```

### Variable Tracking
```javascript
const x = computeValue();
console.log(`Variable x after compute: ${x}, type=${typeof x}`);

// Track object state
this.state = newState;
console.log(`State transition: ${oldState} -> ${this.state}`);
```

### Conditional Branch Tracking
```javascript
if (condition) {
    console.log(`Branch: condition=true, value=${condition}`);
    // true branch
} else {
    console.log(`Branch: condition=false, value=${condition}`);
    // false branch
}
```

### Loop Iteration Tracking
```javascript
items.forEach((item, index) => {
    console.log(`Loop iteration ${index}: item=${JSON.stringify(item)}`);
    // loop body
});
```

## Debug Module (Node.js)

```javascript
const debug = require('debug')('app:module');

function targetFunction(arg) {
    debug('ENTER targetFunction: arg=%o', arg);
    const result = process(arg);
    debug('EXIT targetFunction: result=%o', result);
    return result;
}
```

## Timing Information

```javascript
const start = performance.now();
const result = expensiveOperation();
const elapsed = performance.now() - start;
console.log(`Operation took ${elapsed.toFixed(3)}ms`);
```

## Wrapper Functions

```javascript
function instrumentFunction(fn, name) {
    return function(...args) {
        console.log(`CALL ${name}: args=${JSON.stringify(args)}`);
        try {
            const result = fn.apply(this, args);
            console.log(`RETURN ${name}: ${JSON.stringify(result)}`);
            return result;
        } catch (error) {
            console.error(`EXCEPTION ${name}:`, error);
            throw error;
        }
    };
}

const instrumentedFunc = instrumentFunction(originalFunc, 'originalFunc');
```

## Proxy-Based Instrumentation

```javascript
const handler = {
    get(target, prop) {
        console.log(`GET property: ${prop}`);
        return target[prop];
    },
    set(target, prop, value) {
        console.log(`SET property: ${prop} = ${value}`);
        target[prop] = value;
        return true;
    }
};

const instrumentedObj = new Proxy(originalObj, handler);
```

## Async Function Instrumentation

```javascript
async function instrumentedAsyncFunction(arg) {
    console.log(`ENTER async function: arg=${arg}`);
    try {
        const result = await asyncOperation(arg);
        console.log(`EXIT async function: result=${result}`);
        return result;
    } catch (error) {
        console.error(`EXCEPTION in async function:`, error);
        throw error;
    }
}
```

## Promise Chain Instrumentation

```javascript
fetchData()
    .then(data => {
        console.log('Step 1: data received', data);
        return processData(data);
    })
    .then(result => {
        console.log('Step 2: data processed', result);
        return saveResult(result);
    })
    .catch(error => {
        console.error('Error in promise chain:', error);
        throw error;
    });
```

## TypeScript Decorator (Experimental)

```typescript
function instrument(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        console.log(`CALL ${propertyKey}: args=${JSON.stringify(args)}`);
        try {
            const result = originalMethod.apply(this, args);
            console.log(`RETURN ${propertyKey}: ${JSON.stringify(result)}`);
            return result;
        } catch (error) {
            console.error(`EXCEPTION ${propertyKey}:`, error);
            throw error;
        }
    };

    return descriptor;
}

class MyClass {
    @instrument
    myMethod(x: number): number {
        return x * 2;
    }
}
```
