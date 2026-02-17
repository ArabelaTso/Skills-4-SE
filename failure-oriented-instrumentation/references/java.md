# Java Instrumentation Patterns

## Logging with SLF4J/Logback

### Function Entry/Exit
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyClass {
    private static final Logger logger = LoggerFactory.getLogger(MyClass.class);

    public Result targetMethod(String arg1, int arg2) {
        logger.debug("ENTER targetMethod: arg1={}, arg2={}", arg1, arg2);
        try {
            Result result = process(arg1, arg2);
            logger.debug("EXIT targetMethod: result={}", result);
            return result;
        } catch (Exception e) {
            logger.error("EXCEPTION in targetMethod", e);
            throw e;
        }
    }
}
```

### Variable Tracking
```java
int x = computeValue();
logger.debug("Variable x after compute: {}, type={}", x, x.getClass().getName());

// Track state changes
State oldState = this.state;
this.state = newState;
logger.debug("State transition: {} -> {}", oldState, this.state);
```

### Conditional Branch Tracking
```java
if (condition) {
    logger.debug("Branch: condition=true, value={}", condition);
    // true branch
} else {
    logger.debug("Branch: condition=false, value={}", condition);
    // false branch
}
```

### Loop Iteration Tracking
```java
for (int i = 0; i < items.size(); i++) {
    Item item = items.get(i);
    logger.debug("Loop iteration {}: item={}", i, item);
    // loop body
}
```

## Timing Information

```java
long start = System.nanoTime();
Result result = expensiveOperation();
long elapsed = System.nanoTime() - start;
logger.debug("Operation took {}ms", elapsed / 1_000_000.0);
```

## Try-With-Resources for Scoped Instrumentation

```java
class InstrumentedSection implements AutoCloseable {
    private final String name;
    private final long start;

    public InstrumentedSection(String name) {
        this.name = name;
        this.start = System.nanoTime();
        logger.debug("ENTER section: {}", name);
    }

    @Override
    public void close() {
        long elapsed = System.nanoTime() - start;
        logger.debug("EXIT section: {} ({}ms)", name, elapsed / 1_000_000.0);
    }
}

// Usage
try (InstrumentedSection section = new InstrumentedSection("data_processing")) {
    processData();
}
```

## Assertions

```java
public Result processData(Data data) {
    assert data != null : "Data should not be null";
    assert !data.isEmpty() : "Data should not be empty, size=" + data.size();

    Result result = transform(data);

    assert result != null : "Result should not be null";
    assert result instanceof List : "Result should be List, got " + result.getClass();
    return result;
}
```

## Aspect-Oriented Programming (AspectJ)

```java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;

@Aspect
public class InstrumentationAspect {
    private static final Logger logger = LoggerFactory.getLogger(InstrumentationAspect.class);

    @Around("execution(* com.example.service.*.*(..))")
    public Object instrumentMethod(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();

        logger.debug("CALL {}: args={}", methodName, Arrays.toString(args));
        try {
            Object result = joinPoint.proceed();
            logger.debug("RETURN {}: {}", methodName, result);
            return result;
        } catch (Exception e) {
            logger.error("EXCEPTION {}: {}", methodName, e.getMessage(), e);
            throw e;
        }
    }
}
```

## Method Wrapper Pattern

```java
public class InstrumentedWrapper {
    private final OriginalClass delegate;
    private static final Logger logger = LoggerFactory.getLogger(InstrumentedWrapper.class);

    public InstrumentedWrapper(OriginalClass delegate) {
        this.delegate = delegate;
    }

    public Result method(String arg) {
        logger.debug("CALL method: arg={}", arg);
        try {
            Result result = delegate.method(arg);
            logger.debug("RETURN method: result={}", result);
            return result;
        } catch (Exception e) {
            logger.error("EXCEPTION method", e);
            throw e;
        }
    }
}
```

## Stack Trace Capture

```java
// Capture current stack trace
StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
logger.debug("Current stack trace:");
for (StackTraceElement element : stackTrace) {
    logger.debug("  at {}", element);
}
```

## Thread Information

```java
Thread currentThread = Thread.currentThread();
logger.debug("Thread: name={}, id={}, state={}",
    currentThread.getName(),
    currentThread.getId(),
    currentThread.getState());
```
