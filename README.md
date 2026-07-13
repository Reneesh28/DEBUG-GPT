# Debug GPT Dataset

Welcome to the **Debug GPT Dataset**, a comprehensive, synthetic 20,000+ sample training dataset designed specifically to train, fine-tune, or provide RAG context for AI models specializing in code debugging, optimization, and educational explanations.

## Overview

The goal of this project is to create a high-quality, perfectly structured dataset that teaches Large Language Models (LLMs) how to act as senior engineers or tutors. Instead of just fixing code, the dataset provides a structured output containing technical breakdowns, beginner-friendly analogies, prevention strategies, and algorithmic complexity analysis (Big-O).

* **Total Samples:** 20,001
* **Languages Supported:** Python (11,100 samples), C++ (8,901 samples)
* **Format:** Strictly enforced JSON following JSON Schema validation.

## Dataset Categories

The dataset is partitioned into five main categories. Detailed descriptions and specific examples can be found in `datasets/metadata/categories.json`.

1. **[Runtime Errors](datasets/runtime_errors/README.md) (5,600 samples)**
   * Code that compiles/parses but crashes during execution.
   * *Python:* `NameError`, `TypeError`, `IndexError`, `KeyError`.
   * *C++:* Segmentation Faults, Division by Zero, `std::out_of_range`, Stack Overflow.

2. **[Compiler & Syntax Errors](datasets/compiler_errors/README.md) (4,000 samples)**
   * Code that fails the initial parsing or linking phase.
   * *Python:* Missing colons, unmatched parentheses, indentation errors.
   * *C++:* Missing semicolons, undeclared identifiers, ODR violations, undefined references.

3. **[Logical Bugs](datasets/logical_bugs/README.md) (4,000 samples)**
   * Functionally incorrect code that executes without crashing but yields wrong results.
   * *Python:* Mutating lists during iteration, default mutable arguments, incorrect boolean logic.
   * *C++:* Assignment in conditionals (`= vs ==`), uninitialized variables, variable shadowing.

4. **[Optimization Examples](datasets/optimization_examples/README.md) (3,201 samples)**
   * Code that is functionally correct but suffers from algorithmic or memory inefficiencies.
   * *Python:* O(N) list pops vs `deque`, massive list comprehensions vs generator expressions.
   * *C++:* Pass-by-value of large containers, missing `reserve()`, postfix vs prefix iterators.

5. **[Educational Explanations](datasets/educational_explanations/README.md) (3,200 samples)**
   * Deep-dive conceptual explanations of language paradigms rather than direct bug fixes.
   * *Python:* `__init__` vs `__new__`, Decorators, Context Managers, Generators (`yield`).
   * *C++:* RAII, Smart Pointers, Polymorphism (`virtual`), Value Categories (`lvalue`/`rvalue`).

## Dataset Structure

The structure of each sample is rigorously validated against `training/dataset_schema.json` prior to being written. A typical sample looks like this:

```json
{
    "id": "PY_RUNTIME_000001",
    "language": "python",
    "category": "runtime_error",
    "instruction": "Fix the NameError caused by the misspelled variable.",
    "input": {
        "title": "Misspelled Variable Name",
        "code": "def process(data):\n    count = 0\n    coun += 1\n    return count",
        "error_message": "NameError: name 'coun' is not defined"
    },
    "output": {
        "technical": "A NameError occurs when a variable name is referenced before it has been defined in the current or global scope.",
        "beginner": "You tried to use a variable called 'coun', but you haven't created it yet. It looks like a typo for 'count'.",
        "analogy": "It's like asking someone to fetch a book by a title they've never heard of.",
        "solution": "Ensure the variable is spelled correctly.",
        "prevention": "Use an IDE or linter to catch undefined variables before running.",
        "optimized_code": "def process(data):\n    count = 0\n    count += 1\n    return count",
        "complexity": {
            "before": "O(1)",
            "after": "O(1)"
        }
    },
    "metadata": {
        "difficulty": "easy",
        "source": "Generated NameError Variations",
        "language_version": "Python 3.x",
        "tags": ["name-error", "typo", "variables"]
    }
}
```

## Generation Pipeline

The generation pipeline is located in the `training/` directory. It uses automated, combinatorial Python scripts (`generate_batch_X.py`) that map permutations of variable names, functions, and contexts across known bug archetypes to rapidly produce hundreds of unique, non-duplicate samples.

To view the live statistics of the generated data, check out `datasets/metadata/dataset_statistics.json`.
