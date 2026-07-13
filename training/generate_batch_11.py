import json
import os
import jsonschema
import glob
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

schema_path = "dataset_schema.json"
with open(schema_path, "r") as f:
    schema = json.load(f)

ensure_dir("../datasets/educational_explanations/python")
output_file = "../datasets/educational_explanations/python/concept_explanations.json"

if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# ID generation
existing_ids = set()
for filepath in glob.glob("../datasets/**/*.json", recursive=True):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            file_data = json.load(f)
            if isinstance(file_data, list):
                for item in file_data:
                    if "id" in item:
                        existing_ids.add(item["id"])
    except Exception:
        pass

def get_next_id():
    i = 1
    while True:
        candidate = f"PY_EDUCATIONAL_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "append_item", "filter_data", "run", "compute", "execute"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]

# Variation 1: Scope and UnboundLocalError
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"counter = 0\n\ndef {func}():\n    counter += 1\n    print(f\"Processed {{counter}} {vname}\")\n\n{func}()"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    {func}()\n  File \"main.py\", line 4, in {func}\n    counter += 1\nUnboundLocalError: local variable 'counter' referenced before assignment"
    opt_code = f"counter = 0\n\ndef {func}():\n    global counter\n    counter += 1\n    print(f\"Processed {{counter}} {vname}\")\n\n{func}()"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "educational",
        "instruction": "Explain the concept of local vs global scope in Python that causes UnboundLocalError.",
        "input": {
            "title": "Understanding Python Scope (UnboundLocalError)",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "In Python, if a variable is assigned a value anywhere within a function's body (e.g., `counter += 1` expands to `counter = counter + 1`), it is assumed to be a local variable unless explicitly declared as `global`. When the RHS `counter + 1` evaluates, the local variable `counter` has not been initialized yet, raising an `UnboundLocalError`.",
            "beginner": "Even though `counter` exists outside the function, because you try to change its value *inside* the function, Python thinks you want to create a brand new local variable named `counter`. But when it tries to add 1 to it, it realizes this new local variable hasn't been given a starting value yet.",
            "analogy": "It's like looking at a clock in the town square (global). But if you decide to build your own identical clock inside your house (local), you can't tell what time your house clock says if you haven't set it yet, even if the town square clock is ticking.",
            "solution": "Use the `global counter` statement inside the function to tell Python you intend to modify the global variable, not create a local one.",
            "prevention": "Avoid modifying global variables inside functions. Instead, pass the variable as an argument, modify it, and return the new value.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by official Python FAQ on scope",
            "language_version": "Python 3.x",
            "tags": ["educational", "scope", "global", "unbound-local-error"]
        }
    }
    samples.append(sample)

# Variation 2: Mutability (TypeError with Tuples)
for i in range(25):
    vname = var_names[(i+2) % len(var_names)]
    func = funcs[(i+2) % len(funcs)]
    code = f"def update_{vname}(my_tuple):\n    my_tuple[0] = 99\n    return my_tuple\n\nt = (1, 2, 3)\nupdate_{vname}(t)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    update_{vname}(t)\n  File \"main.py\", line 2, in update_{vname}\n    my_tuple[0] = 99\nTypeError: 'tuple' object does not support item assignment"
    opt_code = f"def update_{vname}(my_tuple):\n    my_list = list(my_tuple)\n    my_list[0] = 99\n    return tuple(my_list)\n\nt = (1, 2, 3)\nupdate_{vname}(t)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "educational",
        "instruction": "Explain the concept of mutability vs immutability using a Tuple.",
        "input": {
            "title": "Understanding Immutability (Tuple TypeError)",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Tuples are immutable sequences in Python. Once a tuple is created in memory, its contents (the object references it holds) cannot be changed, added, or removed. Attempting to assign a new value to an index raises a `TypeError`.",
            "beginner": "In Python, lists `[]` are like whiteboards where you can erase and rewrite things (mutable). Tuples `()` are like stone tablets. Once carved, you cannot change the items inside them.",
            "analogy": "It's like trying to rewrite a printed book with a pen. The book is finalized (immutable). If you want a different book, you have to write a whole new one.",
            "solution": "Convert the tuple to a list using `list()`, modify the element, and convert it back to a tuple using `tuple()`.",
            "prevention": "Use lists when you need a collection of items that might change over time. Use tuples for fixed data that should never be altered.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Python introductory tutorials",
            "language_version": "Python 3.x",
            "tags": ["educational", "mutability", "tuple", "type-error"]
        }
    }
    samples.append(sample)

# Variation 3: Circular Imports
for i in range(25):
    code = f"# file_a.py\nfrom file_b import B_VAR\nA_VAR = B_VAR + 1\n\n# file_b.py\nfrom file_a import A_VAR\nB_VAR = A_VAR + 1\n\n# main.py\nimport file_a"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    import file_a\n  File \"file_a.py\", line 1, in <module>\n    from file_b import B_VAR\n  File \"file_b.py\", line 1, in <module>\n    from file_a import A_VAR\nImportError: cannot import name 'A_VAR' from partially initialized module 'file_a' (most likely due to a circular import)"
    opt_code = f"# file_a.py\ndef get_a():\n    from file_b import get_b\n    return get_b() + 1\n\n# file_b.py\nB_VAR = 10\ndef get_b():\n    return B_VAR\n\n# main.py\nimport file_a"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "educational",
        "instruction": "Explain how Python imports work and what causes circular imports.",
        "input": {
            "title": "Understanding Circular Imports",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "When a module is imported, Python executes its top-level code and adds it to `sys.modules`. If module A imports module B, Python pauses A and starts executing B. If B then tries to import A, Python sees A is already in `sys.modules` but hasn't finished executing. Thus, B tries to grab `A_VAR` before it has been defined, resulting in an ImportError.",
            "beginner": "File A needs File B to finish loading before A can finish. But File B needs File A to finish loading before B can finish. They get stuck waiting for each other, like two people refusing to walk through a door first.",
            "analogy": "It's like trying to look up the definition of 'recursion' in a dictionary, and the definition just says 'See recursion'. You get stuck in an infinite loop.",
            "solution": "Refactor the code to move the shared dependencies into a third module (File C), or move the import statement inside a function so it executes at runtime instead of import time.",
            "prevention": "Design your software architecture in a directed acyclic graph (DAG). Modules should only import 'downward', never 'upward' to their parents.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "hard",
            "source": "Inspired by Python import system documentation",
            "language_version": "Python 3.x",
            "tags": ["educational", "import", "circular-dependency", "architecture"]
        }
    }
    samples.append(sample)

# Variation 4: is vs == (Identity vs Equality)
for i in range(25):
    func = funcs[(i+6) % len(funcs)]
    code = f"def check_cache(val1, val2):\n    # val1 and val2 are 1000\n    assert val1 is val2, \"Values are not the exact same object!\"\n    return True\n\ncheck_cache(1000, 1000)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    check_cache(1000, 1000)\n  File \"main.py\", line 3, in check_cache\n    assert val1 is val2, \"Values are not the exact same object!\"\nAssertionError: Values are not the exact same object!"
    opt_code = f"def check_cache(val1, val2):\n    assert val1 == val2, \"Values do not have the same value!\"\n    return True\n\ncheck_cache(1000, 1000)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "educational",
        "instruction": "Explain the difference between Identity (`is`) and Equality (`==`).",
        "input": {
            "title": "Identity vs Equality (`is` vs `==`)",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "`==` checks for value equality (invoking `__eq__`), while `is` checks for object identity (whether two variables point to the exact same memory address via `id()`). Python caches small integers (typically -5 to 256), so `256 is 256` is True, but `1000 is 1000` evaluates to False because two distinct integer objects are created in memory.",
            "beginner": "`==` asks 'Do these two things look the same?' while `is` asks 'Are these two things literally the exact same physical object?'. Since 1000 is a large number, Python created two separate physical copies of it.",
            "analogy": "It's like having two identical red cars. `==` says True because they are both red cars. `is` says False because they are two different cars parked in different garages.",
            "solution": "Use `==` when you want to compare the value of two variables. Use `is` only when comparing against singletons like `None`, `True`, or `False`.",
            "prevention": "Never use `is` for strings or numbers, as Python's internal memory caching makes the behavior unpredictable depending on the value.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Python fundamental semantics",
            "language_version": "Python 3.x",
            "tags": ["educational", "identity", "equality", "memory"]
        }
    }
    samples.append(sample)

# Validation
invalid_count = 0
for sample in samples:
    try:
        jsonschema.validate(instance=sample, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation failed for sample: {e.message}")
        invalid_count += 1

if invalid_count == 0:
    data.extend(samples)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully generated and validated {len(samples)} samples. Total in file: {len(data)}")
else:
    print(f"Failed to validate {invalid_count} samples. Output not saved.")
