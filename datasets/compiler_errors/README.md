# Compiler & Syntax Errors Dataset

This dataset partition contains code samples that fail to compile or parse. These represent the earliest stage of debugging, often resolving typographical or strict syntactical rules.

## Supported Languages & Common Errors

* **Python:** `SyntaxError` (missing colons, unmatched parentheses, unterminated strings), `IndentationError` (mismatched whitespace levels).
* **C++:** Missing semicolons, undeclared identifiers, missing `#include` headers, `typename` requirements in templates, invalid type conversions, and linker errors (Undefined References, ODR violations).

## Purpose
Used to train models to act as highly-intelligent linters, pointing out exact lines where punctuation is missing, types conflict, or linkage fails, and offering beginner-friendly explanations.
