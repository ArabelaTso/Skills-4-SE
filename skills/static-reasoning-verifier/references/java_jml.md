# JML (Java Modeling Language) Contracts

## Overview

JML is a behavioral interface specification language for Java that allows formal specification of contracts for Java programs.

## Basic Syntax

### Preconditions (@requires)

```java
public class MathUtils {
    /*@ requires x >= 0;
      @ ensures \result >= 0;
      @ ensures \result * \result <= x;
      @ ensures (x - \result * \result) < (2 * \result + 1);
      @*/
    public static int sqrt(int x) {
        // Implementation
    }
}
```

### Postconditions (@ensures)

```java
/*@ ensures \result == a + b;
  @*/
public int add(int a, int b) {
    return a + b;
}
```

### Exceptional Postconditions (@signals)

```java
/*@ requires divisor != 0;
  @ ensures \result == dividend / divisor;
  @ signals (ArithmeticException e) divisor == 0;
  @*/
public int divide(int dividend, int divisor) throws ArithmeticException {
    if (divisor == 0) {
        throw new ArithmeticException("Division by zero");
    }
    return dividend / divisor;
}
```

## Class-Level Contracts

### Invariants

```java
public class BankAccount {
    private double balance;

    /*@ invariant balance >= 0;
      @*/

    /*@ requires initialBalance >= 0;
      @ ensures balance == initialBalance;
      @*/
    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    /*@ requires amount > 0;
      @ requires amount <= balance;
      @ ensures balance == \old(balance) - amount;
      @*/
    public void withdraw(double amount) {
        balance -= amount;
    }

    /*@ requires amount > 0;
      @ ensures balance == \old(balance) + amount;
      @*/
    public void deposit(double amount) {
        balance += amount;
    }
}
```

## Advanced JML Features

### Old Values

```java
/*@ ensures balance == \old(balance) + amount;
  @*/
public void deposit(double amount) {
    balance += amount;
}
```

### Quantifiers

```java
/*@ requires arr != null;
  @ requires (\forall int i; 0 <= i && i < arr.length; arr[i] > 0);
  @ ensures \result >= 0;
  @*/
public int sumPositive(int[] arr) {
    int sum = 0;
    for (int val : arr) {
        sum += val;
    }
    return sum;
}
```

### Pure Methods

Methods without side effects:

```java
/*@ pure @*/
public int getBalance() {
    return balance;
}
```

### Assignable Clause

Specifies what fields can be modified:

```java
/*@ requires amount > 0;
  @ assignable balance;
  @ ensures balance == \old(balance) + amount;
  @*/
public void deposit(double amount) {
    balance += amount;
}
```

## Common Patterns

### Non-null Parameters

```java
/*@ requires obj != null;
  @ ensures \result != null;
  @*/
public String process(@NonNull Object obj) {
    return obj.toString();
}
```

### Array Bounds

```java
/*@ requires arr != null;
  @ requires 0 <= index && index < arr.length;
  @ ensures \result == arr[index];
  @*/
public int getElement(int[] arr, int index) {
    return arr[index];
}
```

### Result Constraints

```java
/*@ ensures \result >= 0;
  @ ensures \result < array.length;
  @*/
public int findMax(int[] array) {
    int maxIndex = 0;
    for (int i = 1; i < array.length; i++) {
        if (array[i] > array[maxIndex]) {
            maxIndex = i;
        }
    }
    return maxIndex;
}
```

## Null Safety with JML

### Nullable and NonNull Annotations

```java
import org.jmlspecs.annotation.*;

public class UserService {
    /*@ requires userId > 0;
      @ ensures \result != null ==> \result.getId() == userId;
      @*/
    public @Nullable User findUser(int userId) {
        // May return null if not found
    }

    /*@ requires user != null;
      @ ensures \result != null;
      @*/
    public @NonNull String formatUser(@NonNull User user) {
        return user.getName() + " (" + user.getEmail() + ")";
    }
}
```

## Tools for JML Verification

### OpenJML

Static checker for JML specifications:

```bash
# Check JML specifications
openjml -check MyClass.java

# Runtime assertion checking
openjml -rac MyClass.java
```

### ESC/Java2

Extended Static Checker for Java:

```bash
escjava2 -warn Null MyClass.java
```

## Best Practices

### 1. Specify Complete Contracts

```java
/*@ requires x > 0;           // What must be true before
  @ ensures \result > 0;      // What will be true after
  @ signals (IllegalArgumentException e) x <= 0;  // Exception behavior
  @ assignable this.value;     // What can change
  @*/
public int compute(int x) {
    if (x <= 0) throw new IllegalArgumentException();
    this.value = x * 2;
    return this.value;
}
```

### 2. Use Pure for Queries

```java
/*@ pure @*/
public int getSize() {
    return size;
}

/*@ requires index >= 0 && index < getSize();
  @ ensures \result == elements[index];
  @ pure
  @*/
public Object get(int index) {
    return elements[index];
}
```

### 3. Document Loop Invariants

```java
/*@ requires arr != null;
  @ ensures (\forall int i; 0 <= i && i < arr.length; \result >= arr[i]);
  @*/
public int findMax(int[] arr) {
    int max = arr[0];

    /*@ loop_invariant 1 <= i && i <= arr.length;
      @ loop_invariant (\forall int j; 0 <= j && j < i; max >= arr[j]);
      @ decreases arr.length - i;
      @*/
    for (int i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}
```

### 4. Specify Frame Conditions

```java
/*@ assignable balance, lastModified;
  @ ensures balance == \old(balance) + amount;
  @ ensures lastModified > \old(lastModified);
  @*/
public void deposit(double amount, long timestamp) {
    balance += amount;
    lastModified = timestamp;
}
```

## Contract Inheritance

```java
public abstract class Shape {
    /*@ requires width > 0 && height > 0;
      @ ensures \result > 0;
      @ pure
      @*/
    public abstract double area(double width, double height);
}

public class Rectangle extends Shape {
    /*@ also
      @ requires width > 0 && height > 0;
      @ ensures \result == width * height;
      @ pure
      @*/
    @Override
    public double area(double width, double height) {
        return width * height;
    }
}
```

## Common JML Keywords

- `\result` - Return value of method
- `\old(expr)` - Value of expression before method execution
- `\forall` - Universal quantifier (for all)
- `\exists` - Existential quantifier (there exists)
- `\sum` - Summation
- `pure` - Method has no side effects
- `assignable` - What fields can be modified
- `signals` - Exception specifications
- `also` - Extends inherited specification

## Verification Example

```java
public class Stack<T> {
    private T[] elements;
    private int size;

    /*@ invariant 0 <= size && size <= elements.length;
      @ invariant (\forall int i; 0 <= i && i < size; elements[i] != null);
      @*/

    /*@ requires capacity > 0;
      @ ensures size == 0;
      @ ensures elements.length == capacity;
      @*/
    public Stack(int capacity) {
        elements = (T[]) new Object[capacity];
        size = 0;
    }

    /*@ requires !isFull();
      @ requires item != null;
      @ ensures size == \old(size) + 1;
      @ ensures elements[size - 1] == item;
      @ assignable elements[size], size;
      @*/
    public void push(T item) {
        elements[size++] = item;
    }

    /*@ requires !isEmpty();
      @ ensures size == \old(size) - 1;
      @ ensures \result == \old(elements[size - 1]);
      @ assignable size;
      @*/
    public T pop() {
        return elements[--size];
    }

    /*@ pure @*/
    public boolean isEmpty() {
        return size == 0;
    }

    /*@ pure @*/
    public boolean isFull() {
        return size == elements.length;
    }
}
```
