# Common ACSL Annotation Patterns

Frequently used ACSL annotation patterns for typical programming scenarios.

## Array Operations

### Array Initialization

```c
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures \forall integer i; 0 <= i < n ==> array[i] == value;
  assigns array[0..n-1];
*/
void initialize_array(int *array, int n, int value) {
    /*@
      loop invariant 0 <= i <= n;
      loop invariant \forall integer k; 0 <= k < i ==> array[k] == value;
      loop assigns i, array[0..n-1];
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        array[i] = value;
    }
}
```

### Array Bounds Check

```c
/*@
  requires \valid_read(array + (0..length-1));
  requires 0 <= index < length;
  ensures \result == array[index];
  assigns \nothing;
*/
int safe_array_access(int *array, int length, int index) {
    return array[index];
}
```

### Array Sum

```c
/*@
  predicate sum_equals(int *a, integer n, integer total) =
    total == \sum(0, n-1, \lambda integer k; a[k]);
*/

/*@
  requires \valid_read(array + (0..n-1));
  requires n > 0;
  ensures sum_equals(array, n, \result);
  assigns \nothing;
*/
int array_sum(int *array, int n) {
    int sum = 0;

    /*@
      loop invariant 0 <= i <= n;
      loop invariant sum_equals(array, i, sum);
      loop assigns i, sum;
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        sum += array[i];
    }

    return sum;
}
```

### Array Maximum

```c
/*@
  requires \valid_read(array + (0..n-1));
  requires n > 0;
  ensures \result >= 0 && \result < n;
  ensures \forall integer i; 0 <= i < n ==> array[\result] >= array[i];
  assigns \nothing;
*/
int find_max_index(int *array, int n) {
    int max_idx = 0;

    /*@
      loop invariant 0 <= i <= n;
      loop invariant 0 <= max_idx < n;
      loop invariant \forall integer k; 0 <= k < i ==> array[max_idx] >= array[k];
      loop assigns i, max_idx;
      loop variant n - i;
    */
    for (int i = 1; i < n; i++) {
        if (array[i] > array[max_idx]) {
            max_idx = i;
        }
    }

    return max_idx;
}
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
void array_copy(int *dest, const int *src, int n) {
    /*@
      loop invariant 0 <= i <= n;
      loop invariant \forall integer k; 0 <= k < i ==> dest[k] == src[k];
      loop assigns i, dest[0..n-1];
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}
```

### Array Reversal

```c
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures \forall integer i; 0 <= i < n ==> array[i] == \old(array[n-1-i]);
  assigns array[0..n-1];
*/
void reverse_array(int *array, int n) {
    int left = 0;
    int right = n - 1;

    /*@
      loop invariant 0 <= left <= n/2;
      loop invariant n/2 <= right < n;
      loop invariant left + right == n - 1;
      loop invariant \forall integer i; 0 <= i < left ==>
                     array[i] == \at(array[n-1-i], Pre);
      loop invariant \forall integer i; right < i < n ==>
                     array[i] == \at(array[n-1-i], Pre);
      loop assigns left, right, array[0..n-1];
      loop variant right - left;
    */
    while (left < right) {
        int temp = array[left];
        array[left] = array[right];
        array[right] = temp;
        left++;
        right--;
    }
}
```

## Sorting

### Sorted Predicate

```c
/*@
  predicate sorted{L}(int *a, integer low, integer high) =
    \forall integer i, j; low <= i <= j < high ==> a[i] <= a[j];
*/

/*@
  predicate sorted_array{L}(int *a, integer n) =
    sorted(a, 0, n);
*/
```

### Bubble Sort

```c
/*@
  requires \valid(array + (0..n-1));
  ensures sorted_array(array, n);
  ensures \forall integer i; 0 <= i < n ==>
          \exists integer j; 0 <= j < n && array[i] == \at(array[j], Pre);
  assigns array[0..n-1];
*/
void bubble_sort(int *array, int n) {
    /*@
      loop invariant 0 <= i <= n;
      loop invariant sorted(array, n-i, n);
      loop invariant \forall integer k; n-i <= k < n ==>
                     \forall integer m; 0 <= m < n-i ==> array[m] <= array[k];
      loop assigns i, array[0..n-1];
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        /*@
          loop invariant i <= j <= n;
          loop invariant \forall integer k; 0 <= k < j ==>
                         array[k] <= array[j] || k >= j;
          loop assigns j, array[0..n-1];
          loop variant n - j;
        */
        for (int j = i + 1; j < n; j++) {
            if (array[i] > array[j]) {
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
}
```

## Search Operations

### Linear Search

```c
/*@
  requires \valid_read(array + (0..n-1));
  ensures (\result == -1) <==>
          (\forall integer i; 0 <= i < n ==> array[i] != target);
  ensures (\result >= 0) ==>
          (0 <= \result < n && array[\result] == target);
  assigns \nothing;
*/
int linear_search(int *array, int n, int target) {
    /*@
      loop invariant 0 <= i <= n;
      loop invariant \forall integer k; 0 <= k < i ==> array[k] != target;
      loop assigns i;
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        if (array[i] == target) {
            return i;
        }
    }
    return -1;
}
```

### Binary Search

```c
/*@
  requires \valid_read(array + (0..n-1));
  requires sorted_array(array, n);
  ensures (\result == -1) <==>
          (\forall integer i; 0 <= i < n ==> array[i] != target);
  ensures (\result >= 0) ==>
          (0 <= \result < n && array[\result] == target);
  assigns \nothing;
*/
int binary_search(int *array, int n, int target) {
    int left = 0;
    int right = n - 1;

    /*@
      loop invariant 0 <= left <= right + 1 <= n;
      loop invariant \forall integer i; 0 <= i < left ==> array[i] < target;
      loop invariant \forall integer i; right < i < n ==> array[i] > target;
      loop assigns left, right;
      loop variant right - left;
    */
    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (array[mid] == target) {
            return mid;
        } else if (array[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
```

## Pointer Operations

### Pointer Swap

```c
/*@
  requires \valid(a) && \valid(b);
  requires \separated(a, b);
  ensures *a == \old(*b);
  ensures *b == \old(*a);
  assigns *a, *b;
*/
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

### Null Pointer Check

```c
/*@
  requires ptr == \null || \valid(ptr);
  ensures \result == (ptr != \null);
  assigns \nothing;
*/
int is_valid_pointer(int *ptr) {
    return ptr != NULL;
}
```

## String Operations

### String Length

```c
/*@
  requires \valid_read(str + (0..));
  requires \exists integer i; i >= 0 && str[i] == '\0';
  ensures \result >= 0;
  ensures str[\result] == '\0';
  ensures \forall integer i; 0 <= i < \result ==> str[i] != '\0';
  assigns \nothing;
*/
int string_length(const char *str) {
    int len = 0;

    /*@
      loop invariant len >= 0;
      loop invariant \forall integer i; 0 <= i < len ==> str[i] != '\0';
      loop assigns len;
      loop variant strlen(str) - len;
    */
    while (str[len] != '\0') {
        len++;
    }

    return len;
}
```

### String Copy

```c
/*@
  requires \valid(dest + (0..));
  requires \valid_read(src + (0..));
  requires \exists integer i; i >= 0 && src[i] == '\0';
  requires \separated(dest + (0..), src + (0..));
  ensures \forall integer i; i >= 0 && src[i] == '\0' ==>
          (dest[i] == '\0' && \forall integer j; 0 <= j < i ==> dest[j] == src[j]);
  assigns dest[0..];
*/
void string_copy(char *dest, const char *src) {
    int i = 0;

    /*@
      loop invariant i >= 0;
      loop invariant \forall integer k; 0 <= k < i ==> dest[k] == src[k];
      loop assigns i, dest[0..];
    */
    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}
```

## Mathematical Operations

### Integer Division (Safe)

```c
/*@
  requires divisor != 0;
  ensures divisor * \result <= dividend < divisor * (\result + 1);
  assigns \nothing;
*/
int safe_divide(int dividend, int divisor) {
    return dividend / divisor;
}
```

### GCD (Greatest Common Divisor)

```c
/*@
  requires a > 0 && b > 0;
  ensures \result > 0;
  ensures a % \result == 0 && b % \result == 0;
  ensures \forall integer d; d > \result ==> !(a % d == 0 && b % d == 0);
  assigns \nothing;
  decreases a + b;
*/
int gcd(int a, int b) {
    /*@
      loop invariant a > 0 && b > 0;
      loop assigns a, b;
      loop variant a + b;
    */
    while (a != b) {
        if (a > b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }
    return a;
}
```

### Factorial

```c
/*@
  requires n >= 0;
  ensures \result >= 1;
  assigns \nothing;
  decreases n;
*/
int factorial(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

## Memory Safety

### Safe Memory Access

```c
/*@
  requires \valid(buffer + (0..size-1));
  requires 0 <= offset < size;
  ensures \result == buffer[offset];
  assigns \nothing;
*/
int safe_read(char *buffer, int size, int offset) {
    //@ assert 0 <= offset < size;
    //@ assert \valid(buffer + offset);
    return buffer[offset];
}
```

### Buffer Bounds Check

```c
/*@
  requires \valid(buffer + (0..buffer_size-1));
  requires data_size >= 0;
  ensures \result <==> (data_size <= buffer_size);
  assigns \nothing;
*/
int can_fit_in_buffer(char *buffer, int buffer_size, int data_size) {
    return data_size <= buffer_size;
}
```

## Overflow Prevention

### Safe Addition

```c
/*@
  requires INT_MIN <= (integer)a + (integer)b <= INT_MAX;
  ensures \result == a + b;
  assigns \nothing;
*/
int safe_add(int a, int b) {
    return a + b;
}
```

### Safe Multiplication

```c
/*@
  requires INT_MIN <= (integer)a * (integer)b <= INT_MAX;
  ensures \result == a * b;
  assigns \nothing;
*/
int safe_multiply(int a, int b) {
    return a * b;
}
```

## Struct Operations

### Struct Initialization

```c
struct point {
    int x;
    int y;
};

/*@
  requires \valid(p);
  ensures p->x == x_val;
  ensures p->y == y_val;
  assigns p->x, p->y;
*/
void init_point(struct point *p, int x_val, int y_val) {
    p->x = x_val;
    p->y = y_val;
}
```

### Struct Copy

```c
/*@
  requires \valid(dest) && \valid_read(src);
  requires \separated(dest, src);
  ensures dest->x == \old(src->x);
  ensures dest->y == \old(src->y);
  assigns dest->x, dest->y;
*/
void copy_point(struct point *dest, const struct point *src) {
    dest->x = src->x;
    dest->y = src->y;
}
```

## Common Predicates

### Range Checking

```c
/*@
  predicate in_range(integer val, integer low, integer high) =
    low <= val <= high;
*/
```

### Array Permutation

```c
/*@
  predicate is_permutation{L1,L2}(int *a, int *b, integer n) =
    \forall integer i; 0 <= i < n ==>
      \exists integer j; 0 <= j < n && \at(a[i], L1) == \at(b[j], L2);
*/
```

### All Elements Equal

```c
/*@
  predicate all_equal(int *a, integer n, integer val) =
    \forall integer i; 0 <= i < n ==> a[i] == val;
*/
```

### Array Contains

```c
/*@
  predicate contains(int *a, integer n, integer val) =
    \exists integer i; 0 <= i < n && a[i] == val;
*/
```
