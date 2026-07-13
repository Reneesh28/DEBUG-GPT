# Runtime Errors Dataset

This dataset partition contains code samples that crash during execution. These are errors that bypass the compiler/parser but violate runtime constraints of the language or OS.

## Supported Languages & Common Errors

* **Python:** `NameError`, `TypeError`, `IndexError`, `KeyError`, `AttributeError`, `ValueError`, `ZeroDivisionError`.
* **C++:** Segmentation Faults (dereferencing `nullptr`), `std::out_of_range` bounds checks, `std::bad_alloc` memory exhaustion, infinite recursion (Stack Overflow).

## Purpose
Used to train models to identify dynamic typing conflicts, missing variable definitions, out-of-bounds memory accesses, and improper exception handling.
