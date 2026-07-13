# Optimization & Performance Dataset

This dataset partition contains code samples that are functionally flawless but computationally or memory inefficient.

## Supported Languages & Common Issues

* **Python:** `list.pop(0)` overhead vs `collections.deque`, aggressive memory allocation in List Comprehensions vs Generator Expressions, tight-loop global variable accesses, string appending vs multiplication.
* **C++:** Passing large structures (`std::vector`) by value instead of `const reference`, I/O buffer flushing (`std::endl` vs `\n`), missing capacity pre-allocation (`reserve()`), postfix iterator (`it++`) temporary copies overhead.

## Purpose
Used to train models to act as senior code reviewers, identifying O(N^2) bottlenecks, unnecessary heap allocations, and caching opportunities without altering the business logic.
