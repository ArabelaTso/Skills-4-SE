# ACSL Syntax Reference

This reference covers the complete ACSL (ANSI/ISO C Specification Language) syntax for formal verification.

## Table of Contents

1. [Function Contracts](#function-contracts)
2. [Loop Annotations](#loop-annotations)
3. [Assertions and Assumptions](#assertions-and-assumptions)
4. [Predicates and Logic Functions](#predicates-and-logic-functions)
5. [Axiomatic Definitions](#axiomatic-definitions)
6. [Built-in Predicates](#built-in-predicates)
7. [Memory Model](#memory-model)
8. [Behaviors](#behaviors)
9. [Type Invariants](#type-invariants)
10. [Ghost Code](#ghost-code)

## Function Contracts

### Basic Contract Structure

```c
/*@
  requires precondition1;
  requires precondition2;
  ensures postcondition1;
  ensures postcondition2;
  assigns modified_locations;
*/
```

### Requires Clause (Preconditions)

Specifies what must be true when the function is called:

```c
/*@ requires x > 0; */
/*@ requires \valid(ptr); */
/*@ requires \valid(array + (0..n-1)); */
/*@ requires n >= 0 && n < MAX_SIZE; */
```

### Ensures Clause (Postconditions)

Specifies what will be true when the function returns:

```c
/*@ ensures \result >= 0; */
/*@ ensures *ptr == \old(*ptr) + 1; */
/*@ ensures \forall integer i; 0 <= i < n ==> array[i] >= 0; */
```

### Assigns Clause

Specifies which memory locations may be modified:

```c
/*@ assigns \nothing; */               // No modifications
/*@ assigns *ptr; */                   // Single location
/*@ assigns array[0..n-1]; */          // Array range
/*@ assigns ptr->field; */             // Structure field
/*@ assigns *ptr1, *ptr2, global_var; */ // Multiple locations
```

## Loop Annotations

### Loop Invariant

Property that holds before and after each iteration:

```c
/*@
  loop invariant 0 <= i <= n;
  loop invariant \forall integer k; 0 <= k < i ==> array[k] >= 0;
*/
```

### Loop Variant

Decreasing measure for termination:

```c
/*@ loop variant n - i; */              // Simple variant
/*@ loop variant max_value - current; */ // General expression
```

### Loop Assigns

Memory modified within the loop:

```c
/*@ loop assigns i, sum; */
/*@ loop assigns array[0..n-1]; */
```

### Complete Loop Example

```c
/*@
  loop invariant 0 <= i <= n;
  loop invariant \forall integer k; 0 <= k < i ==> array[k] == \old(array[k]) * 2;
  loop assigns i, array[0..n-1];
  loop variant n - i;
*/
for (i = 0; i < n; i++) {
    array[i] *= 2;
}
```

## Assertions and Assumptions

### Assertions

Runtime checks (must be proven):

```c
//@ assert x >= 0;
//@ assert \valid(ptr);
//@ assert 0 <= index && index < length;
```

### Assumptions

Assumed to be true (not proven):

```c
//@ assume divisor != 0;
//@ assume \valid(ptr);
```

### Check

Similar to assert but may not be proven:

```c
//@ check x > 0;
```

## Predicates and Logic Functions

### Predicate Definition

```c
/*@
  predicate sorted{L}(int *a, integer n) =
    \forall integer i, j; 0 <= i <= j < n ==> a[i] <= a[j];
*/

/*@
  predicate valid_range{L}(int *a, integer low, integer high) =
    \valid(a + (low..high)) && low <= high;
*/
```

### Logic Function Definition

```c
/*@
  logic integer max(integer a, integer b) =
    (a >= b) ? a : b;
*/

/*@
  logic integer array_sum{L}(int *a, integer n) =
    (n <= 0) ? 0 : array_sum(a, n-1) + a[n-1];
*/
```

### Using Labels

Access values at different program points:

```c
/*@
  ensures array[0] == \at(array[n-1], Pre);
*/
void reverse_first_last(int *array, int n) {
    int temp = array[0];
    array[0] = array[n-1];
    array[n-1] = temp;
}
```

## Axiomatic Definitions

Define abstract mathematical concepts:

```c
/*@
  axiomatic ArraySum {
    logic integer sum{L}(int *a, integer low, integer high);

    axiom sum_empty{L}:
      \forall int *a, integer i; sum(a, i, i) == 0;

    axiom sum_range{L}:
      \forall int *a, integer low, high;
        low < high ==> sum(a, low, high) == sum(a, low, high-1) + a[high-1];
  }
*/
```

## Built-in Predicates

### Memory Validity

```c
\valid(ptr)                    // Pointer is valid for read/write
\valid_read(ptr)               // Pointer is valid for read
\valid(ptr + (low..high))      // Range is valid
\valid_function(fptr)          // Function pointer is valid
```

### Pointer Relations

```c
\separated(ptr1, ptr2)         // Pointers don't alias
\base_addr(ptr)                // Base address of allocation
\block_length(ptr)             // Size of allocated block
\offset(ptr)                   // Offset from base address
```

### Initialization

```c
\initialized(ptr)              // Memory is initialized
\initialized(ptr + (0..n-1))   // Range is initialized
```

### Allocation

```c
\allocable(ptr)                // Can be allocated
\freeable(ptr)                 // Can be freed
\fresh(ptr, n)                 // Newly allocated memory
```

## Memory Model

### Old Values

```c
\old(expr)                     // Value at function entry
\at(expr, Label)               // Value at specific label
```

### Result Value

```c
\result                        // Function return value
```

### Pointer Arithmetic

```c
ptr + n                        // Pointer offset
\base_addr(ptr)                // Base of allocation
\offset(ptr)                   // Offset in bytes
\block_length(ptr)             // Allocation size
```

### Sets and Ranges

```c
ptr + (low..high)              // Pointer range
\union(set1, set2)             // Set union
\inter(set1, set2)             // Set intersection
\nothing                       // Empty set
```

## Behaviors

### Multiple Behaviors

```c
/*@
  behavior positive:
    assumes x > 0;
    ensures \result == x;

  behavior negative:
    assumes x < 0;
    ensures \result == -x;

  behavior zero:
    assumes x == 0;
    ensures \result == 0;

  complete behaviors;
  disjoint behaviors;
*/
int absolute_value(int x);
```

### Complete and Disjoint

```c
complete behaviors;             // All cases covered
disjoint behaviors;             // Cases are mutually exclusive
```

## Type Invariants

Define invariants for struct types:

```c
struct counter {
    int value;
    int max;
};

/*@
  type invariant valid_counter(struct counter c) =
    0 <= c.value <= c.max;
*/
```

## Ghost Code

Code visible only to verification:

```c
/*@ ghost int verification_counter = 0; */

//@ ghost verification_counter++;

/*@
  ghost
    int max_value = array[0];
    for (int i = 1; i < n; i++) {
        if (array[i] > max_value) max_value = array[i];
    }
*/
```

## Quantifiers

### Universal Quantifier

```c
\forall type var; condition ==> property
\forall integer i; 0 <= i < n ==> array[i] >= 0
```

### Existential Quantifier

```c
\exists type var; condition && property
\exists integer i; 0 <= i < n && array[i] == target
```

## Common Patterns

### Array Initialization

```c
/*@
  requires \valid(array + (0..n-1));
  ensures \forall integer i; 0 <= i < n ==> array[i] == value;
  assigns array[0..n-1];
*/
```

### Array Copy

```c
/*@
  requires \valid(dest + (0..n-1));
  requires \valid_read(src + (0..n-1));
  requires \separated(dest + (0..n-1), src + (0..n-1));
  ensures \forall integer i; 0 <= i < n ==> dest[i] == \old(src[i]);
  assigns dest[0..n-1];
*/
```

### Sorted Array

```c
/*@
  predicate sorted(int *a, integer n) =
    \forall integer i, j; 0 <= i <= j < n ==> a[i] <= a[j];
*/
```

### Array Search

```c
/*@
  requires \valid_read(array + (0..n-1));
  ensures (\result == -1) <==>
          (\forall integer i; 0 <= i < n ==> array[i] != target);
  ensures (\result != -1) ==>
          (0 <= \result < n && array[\result] == target);
  assigns \nothing;
*/
int search(int *array, int n, int target);
```

## Integer Types

ACSL distinguishes between C integer types and mathematical integers:

- `int`, `unsigned`, `char`, etc. - C types (bounded)
- `integer` - Mathematical integers (unbounded)
- `\max(type)` - Maximum value of a type
- `\min(type)` - Minimum value of a type

```c
/*@ requires INT_MIN <= a + b <= INT_MAX; */  // Overflow check
/*@ ensures \result == (integer)a + (integer)b; */  // Mathematical addition
```

## Real Numbers

```c
/*@ logic real distance(real x, real y) = \sqrt((x*x) + (y*y)); */
```

## Bitwise Operations

```c
\at(x, Pre) & 0xFF               // Bitwise AND
\at(x, Pre) | mask               // Bitwise OR
\at(x, Pre) ^ mask               // Bitwise XOR
~\at(x, Pre)                     // Bitwise NOT
```

## Terminates Clause

Specify that function terminates:

```c
/*@
  terminates \true;
*/
```

## Decreases Clause

For recursive functions:

```c
/*@
  decreases n;
*/
int factorial(int n);
```
