# Invariant Templates by Algorithm Type

## Sorting Algorithms

### Insertion Sort

**Loop Invariants**:
```
Outer loop (i from 1 to n):
  invariant 1 ≤ i ≤ n
  invariant sorted(arr[0..i-1])
  invariant multiset(arr) = multiset(old(arr))

Inner loop (j from i-1 down to 0):
  invariant -1 ≤ j < i
  invariant sorted(arr[0..j]) ∧ sorted(arr[j+2..i])
  invariant ∀k. j+2 ≤ k ≤ i ⟹ arr[k] > key
  invariant multiset(arr) = multiset(old(arr))
```

### Selection Sort

**Loop Invariants**:
```
Outer loop (i from 0 to n-1):
  invariant 0 ≤ i ≤ n
  invariant sorted(arr[0..i-1])
  invariant ∀k, l. 0 ≤ k < i ≤ l < n ⟹ arr[k] ≤ arr[l]
  invariant multiset(arr) = multiset(old(arr))

Inner loop (j from i+1 to n):
  invariant i < j ≤ n
  invariant min_idx = argmin(arr[i..j-1])
```

### Bubble Sort

**Loop Invariants**:
```
Outer loop (i from 0 to n-1):
  invariant 0 ≤ i ≤ n
  invariant sorted(arr[n-i..n-1])
  invariant ∀k, l. 0 ≤ k < n-i ≤ l < n ⟹ arr[k] ≤ arr[l]
  invariant multiset(arr) = multiset(old(arr))

Inner loop (j from 0 to n-i-1):
  invariant 0 ≤ j < n-i
  invariant ∀k. 0 ≤ k ≤ j ⟹ arr[k] ≤ arr[j]
```

### Merge Sort

**Merge Function Invariants**:
```
invariant 0 ≤ i ≤ len(left)
invariant 0 ≤ j ≤ len(right)
invariant len(result) = i + j
invariant sorted(result)
invariant ∀x ∈ result. x ∈ left ∨ x ∈ right
```

### Quick Sort

**Partition Invariants**:
```
invariant low - 1 ≤ i < j ≤ high
invariant ∀k. low ≤ k ≤ i ⟹ arr[k] ≤ pivot
invariant ∀k. i < k < j ⟹ arr[k] > pivot
invariant multiset(arr[low..high]) = multiset(old(arr[low..high]))
```

## Search Algorithms

### Linear Search

**Loop Invariants**:
```
invariant 0 ≤ i ≤ len(arr)
invariant ∀k. 0 ≤ k < i ⟹ arr[k] ≠ target
invariant found ⟹ arr[i] = target
```

### Binary Search

**Loop Invariants**:
```
invariant 0 ≤ low ≤ high + 1 ≤ len(arr)
invariant ∀k. 0 ≤ k < low ⟹ arr[k] < target
invariant ∀k. high < k < len(arr) ⟹ arr[k] > target
invariant sorted(arr)
```

### Binary Search (First Occurrence)

**Loop Invariants**:
```
invariant 0 ≤ low ≤ high + 1 ≤ len(arr)
invariant ∀k. 0 ≤ k < low ⟹ arr[k] < target
invariant ∀k. high < k < len(arr) ⟹ arr[k] ≥ target
invariant result = -1 ∨ arr[result] = target
```

## Array Manipulation

### Reverse Array

**Loop Invariants**:
```
invariant 0 ≤ left ≤ right < len(arr)
invariant ∀k. 0 ≤ k < left ⟹ arr[k] = old(arr[len(arr)-1-k])
invariant ∀k. right < k < len(arr) ⟹ arr[k] = old(arr[len(arr)-1-k])
invariant multiset(arr) = multiset(old(arr))
```

### Rotate Array

**Loop Invariants**:
```
invariant 0 ≤ i ≤ k
invariant ∀j. 0 ≤ j < i ⟹ arr[j] = old(arr[j+k])
invariant multiset(arr) = multiset(old(arr))
```

### Remove Duplicates (Sorted Array)

**Loop Invariants**:
```
invariant 0 ≤ i < j ≤ len(arr)
invariant ∀k, l. 0 ≤ k < l ≤ i ⟹ arr[k] < arr[l]
invariant ∀k. 0 ≤ k ≤ i ⟹ arr[k] ∈ arr[0..j-1]
```

### Partition (Even/Odd)

**Loop Invariants**:
```
invariant 0 ≤ i ≤ j ≤ len(arr)
invariant ∀k. 0 ≤ k < i ⟹ even(arr[k])
invariant ∀k. i ≤ k < j ⟹ odd(arr[k])
invariant multiset(arr) = multiset(old(arr))
```

## String Algorithms

### String Reversal

**Loop Invariants**:
```
invariant 0 ≤ left ≤ right < len(s)
invariant ∀k. 0 ≤ k < left ⟹ s[k] = old(s[len(s)-1-k])
invariant ∀k. right < k < len(s) ⟹ s[k] = old(s[len(s)-1-k])
```

### Palindrome Check

**Loop Invariants**:
```
invariant 0 ≤ left ≤ right < len(s)
invariant ∀k. 0 ≤ k < left ⟹ s[k] = s[len(s)-1-k]
invariant is_palindrome ⟹ (∀k. 0 ≤ k < left ⟹ s[k] = s[len(s)-1-k])
```

### String Pattern Matching (KMP)

**Loop Invariants**:
```
invariant 0 ≤ i ≤ len(text)
invariant 0 ≤ j ≤ len(pattern)
invariant j = length of longest proper prefix of pattern[0..j-1] that is also suffix
invariant ∀k. 0 ≤ k < i-j ⟹ pattern not found starting at k
```

## Graph Algorithms

### Depth-First Search

**Loop Invariants**:
```
invariant ∀v ∈ visited. reachable(start, v)
invariant ∀v ∈ stack. v ∈ visited
invariant ∀v. reachable(start, v) ∧ discovered(v) ⟹ v ∈ visited
```

### Breadth-First Search

**Loop Invariants**:
```
invariant ∀v ∈ visited. reachable(start, v)
invariant ∀v ∈ queue. v ∈ visited
invariant ∀v ∈ queue. distance(start, v) ∈ {d, d+1}
invariant ∀v. distance(start, v) < d ⟹ v ∈ visited
```

### Dijkstra's Algorithm

**Loop Invariants**:
```
invariant ∀v ∈ visited. dist[v] = shortest_path_length(start, v)
invariant ∀v ∉ visited. dist[v] = shortest_path_length_via_visited(start, v)
invariant ∀v. dist[v] ≥ 0
```

### Bellman-Ford

**Loop Invariants**:
```
Outer loop (i from 1 to n-1):
  invariant 1 ≤ i ≤ n
  invariant ∀v. dist[v] ≤ shortest_path_length_with_at_most_i_edges(start, v)

Inner loop (for each edge):
  invariant dist[u] + weight(u, v) ≥ dist[v] for processed edges
```

## Dynamic Programming

### Longest Common Subsequence

**Loop Invariants**:
```
Outer loop (i from 0 to m):
  invariant 0 ≤ i ≤ m
  invariant ∀r, c. 0 ≤ r < i ∧ 0 ≤ c ≤ n ⟹
    dp[r][c] = LCS_length(s1[0..r-1], s2[0..c-1])

Inner loop (j from 0 to n):
  invariant 0 ≤ j ≤ n
  invariant ∀c. 0 ≤ c < j ⟹
    dp[i][c] = LCS_length(s1[0..i-1], s2[0..c-1])
```

### Knapsack Problem

**Loop Invariants**:
```
Outer loop (i from 0 to n):
  invariant 0 ≤ i ≤ n
  invariant ∀r, w. 0 ≤ r < i ∧ 0 ≤ w ≤ W ⟹
    dp[r][w] = max_value(items[0..r-1], capacity=w)

Inner loop (w from 0 to W):
  invariant 0 ≤ w ≤ W
  invariant ∀c. 0 ≤ c < w ⟹
    dp[i][c] = max_value(items[0..i-1], capacity=c)
```

### Edit Distance

**Loop Invariants**:
```
invariant 0 ≤ i ≤ len(s1)
invariant 0 ≤ j ≤ len(s2)
invariant ∀r, c. 0 ≤ r ≤ i ∧ 0 ≤ c ≤ j ⟹
  dp[r][c] = edit_distance(s1[0..r-1], s2[0..c-1])
```

## Linked List Algorithms

### Reverse Linked List

**Loop Invariants**:
```
invariant prev = reverse(processed_nodes)
invariant curr = remaining_nodes
invariant original_list = processed_nodes + remaining_nodes
```

### Detect Cycle (Floyd's Algorithm)

**Loop Invariants**:
```
invariant slow moves 1 step per iteration
invariant fast moves 2 steps per iteration
invariant has_cycle ⟹ eventually slow = fast
invariant ¬has_cycle ⟹ fast reaches end
```

### Merge Two Sorted Lists

**Loop Invariants**:
```
invariant result = merge(processed(list1), processed(list2))
invariant sorted(result)
invariant list1 = remaining nodes from original list1
invariant list2 = remaining nodes from original list2
```

## Tree Algorithms

### Binary Search Tree Insertion

**Invariants**:
```
invariant BST_property(tree)
invariant ∀v ∈ tree. v ∈ old(tree) ∨ v = new_value
invariant size(tree) = size(old(tree)) + 1
```

### Tree Traversal (Inorder)

**Loop Invariants**:
```
invariant ∀v ∈ visited. v processed in inorder
invariant ∀v ∈ stack. v or its descendants not yet processed
invariant result = inorder(visited_nodes)
```

### Tree Height Calculation

**Recursive Invariant**:
```
ensures result = max(height(left), height(right)) + 1
ensures result ≥ 0
ensures result = 0 ⟺ node is leaf
```

## Mathematical Algorithms

### GCD (Euclidean Algorithm)

**Loop Invariants**:
```
invariant gcd(a, b) = gcd(original_a, original_b)
invariant a ≥ 0 ∧ b ≥ 0
invariant b < old(b) (decreasing)
```

### Power (Exponentiation by Squaring)

**Loop Invariants**:
```
invariant result * base^exp = original_base^original_exp
invariant exp ≥ 0
invariant exp decreases
```

### Factorial

**Loop Invariants**:
```
invariant 0 ≤ i ≤ n
invariant result = i!
```

### Fibonacci

**Loop Invariants**:
```
invariant 0 ≤ i ≤ n
invariant a = fib(i)
invariant b = fib(i+1)
```

## Matrix Algorithms

### Matrix Multiplication

**Loop Invariants**:
```
Outer loop (i from 0 to m):
  invariant 0 ≤ i ≤ m
  invariant ∀r, c. 0 ≤ r < i ∧ 0 ≤ c < p ⟹
    result[r][c] = Σ(A[r][k] * B[k][c] for k in 0..n-1)

Middle loop (j from 0 to p):
  invariant 0 ≤ j ≤ p
  invariant ∀c. 0 ≤ c < j ⟹
    result[i][c] = Σ(A[i][k] * B[k][c] for k in 0..n-1)

Inner loop (k from 0 to n):
  invariant 0 ≤ k ≤ n
  invariant result[i][j] = Σ(A[i][l] * B[l][j] for l in 0..k-1)
```

### Matrix Transpose

**Loop Invariants**:
```
invariant 0 ≤ i ≤ m
invariant 0 ≤ j ≤ n
invariant ∀r, c. 0 ≤ r < i ∧ 0 ≤ c < n ⟹ result[c][r] = matrix[r][c]
invariant ∀c. 0 ≤ c < j ⟹ result[c][i] = matrix[i][c]
```

## Bit Manipulation

### Count Set Bits

**Loop Invariants**:
```
invariant count = number of 1 bits in (original_n & ((1 << processed_bits) - 1))
invariant n = original_n >> processed_bits
invariant n ≥ 0
```

### Reverse Bits

**Loop Invariants**:
```
invariant 0 ≤ i ≤ 32
invariant result contains reversed bits of original_n[0..i-1]
invariant n = original_n >> i
```

## General Template Structure

For any algorithm, invariants typically include:

1. **Bounds**: Loop counter ranges
2. **Progress**: What has been accomplished
3. **Preservation**: What remains unchanged
4. **Correctness**: Partial correctness property
5. **Termination**: Decreasing measure

**Template**:
```
invariant bounds(loop_variables)
invariant progress_property(processed_data)
invariant preservation_property(data)
invariant partial_correctness(result_so_far)
invariant termination_measure decreases
```
