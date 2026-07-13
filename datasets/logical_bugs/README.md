# Logical Bugs Dataset

This dataset partition contains code samples that compile and execute successfully, but fail to achieve the intended algorithmic result.

## Supported Languages & Common Errors

* **Python:** Modifying sequences during iteration, default mutable argument state leaks, incorrect equality checks (`is` vs `==`), missing `return` statements resulting in `None`, and off-by-one `range()` boundaries.
* **C++:** Assigning inside conditionals (`=` vs `==`), floating-point exact equality, uninitialized variable usage (Undefined Behavior), variable shadowing, and missing null-terminators in C-strings.

## Purpose
Used to train models on deep semantic analysis. These bugs are the hardest for beginners to find because there are no error traces; the model must deduce the intended behavior versus the actual behavior.
