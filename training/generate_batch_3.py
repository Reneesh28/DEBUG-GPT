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

ensure_dir("../datasets/runtime_errors/python")
output_file = "../datasets/runtime_errors/python/type_error.json"

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
        candidate = f"PY_RUNTIME_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

# Source: Inspired by Python Official Documentation and typical beginner mistakes
var_names = ["user_input", "amount", "total", "count", "value", "score", "index", "price", "quantity", "age"]
funcs = ["add_values", "calculate", "process", "compute", "concat", "multiply", "format_output", "display", "print_result", "evaluate"]

# Variation 1: Concatenating string and integer
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"def {func}({vname}):\n    message = \"The value is: \" + {vname}\n    return message\n\n{func}(42)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}(42)\n  File \"main.py\", line 2, in {func}\n    message = \"The value is: \" + {vname}\nTypeError: can only concatenate str (not \"int\") to str"
    opt_code = f"def {func}({vname}):\n    message = f\"The value is: {{{vname}}}\"\n    return message\n\n{func}(42)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the TypeError caused by concatenating a string with an integer.",
        "input": {
            "title": "String and integer concatenation",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Python is a strongly typed language and does not implicitly coerce integers to strings during concatenation with the `+` operator.",
            "beginner": "You tried to glue together text and a number using the `+` sign. Python doesn't know if you want to do math or put the words side-by-side.",
            "analogy": "It's like trying to plug a USB cable into an electrical wall outlet. They are incompatible types of connections without an adapter.",
            "solution": "Convert the integer to a string using `str()`, or use formatted string literals (f-strings) which automatically handle the conversion.",
            "prevention": "Prefer using f-strings `f\"{variable}\"` for constructing strings that include variables, as they are safer and more readable.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common beginner mistakes",
            "language_version": "Python 3.x",
            "tags": ["type-error", "string-concatenation", "f-strings"]
        }
    }
    samples.append(sample)

# Variation 2: Calling a non-callable (e.g., an integer)
for i in range(25):
    vname = var_names[(i+2) % len(var_names)]
    func = funcs[(i+2) % len(funcs)]
    code = f"def {func}({vname}):\n    result = {vname}()\n    return result\n\n{func}(100)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}(100)\n  File \"main.py\", line 2, in {func}\n    result = {vname}()\nTypeError: 'int' object is not callable"
    opt_code = f"def {func}({vname}):\n    # Assuming the intent was just to use the value\n    result = {vname}\n    return result\n\n{func}(100)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the TypeError caused by attempting to call an integer as if it were a function.",
        "input": {
            "title": "Calling a non-callable object",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Parentheses `()` are the function call operator in Python. Placing them after an integer variable attempts to invoke the integer's `__call__` method, which does not exist.",
            "beginner": "You put parentheses `()` after a number variable. Python thought you were trying to run a function, but it's just a regular number.",
            "analogy": "It's like picking up a rock and trying to make a phone call with it. It's an object, but not one that can 'call'.",
            "solution": "Remove the parentheses if you just want to use the variable's value, or ensure you are actually calling a valid function.",
            "prevention": "Be careful with variable naming; avoid naming variables the same as built-in functions (like `list`, `str`, `sum`) which can lead to this error if you overwrite them.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["type-error", "callable", "functions"]
        }
    }
    samples.append(sample)

# Variation 3: Unsupported operand type(s) for math operations
for i in range(25):
    vname = var_names[(i+4) % len(var_names)]
    func = funcs[(i+4) % len(funcs)]
    code = f"def {func}({vname}, multiplier):\n    return {vname} / multiplier\n\n{func}(50, '2')"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}(50, '2')\n  File \"main.py\", line 2, in {func}\n    return {vname} / multiplier\nTypeError: unsupported operand type(s) for /: 'int' and 'str'"
    opt_code = f"def {func}({vname}, multiplier):\n    return {vname} / int(multiplier)\n\n{func}(50, '2')"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the TypeError caused by dividing a number by a string.",
        "input": {
            "title": "Mathematical operation on string",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The division operator `/` is not implemented between integer types and string types. The `__truediv__` method cannot process these mismatched operands.",
            "beginner": "You tried to divide a number by a word (or a number inside quotes). Math operations only work between actual numbers.",
            "analogy": "It's like trying to divide a pie by the word 'two' written on a piece of paper, instead of actually dividing it into 2 pieces.",
            "solution": "Convert the string to an integer or float using `int()` or `float()` before performing the mathematical operation.",
            "prevention": "When reading input from the user or a file, remember that it always comes in as a string. Parse it into numeric types immediately if it will be used in calculations.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Python Official Documentation",
            "language_version": "Python 3.x",
            "tags": ["type-error", "math", "type-conversion"]
        }
    }
    samples.append(sample)

# Variation 4: Iterating over a non-iterable (e.g., float)
for i in range(25):
    vname = var_names[(i+6) % len(var_names)]
    func = funcs[(i+6) % len(funcs)]
    code = f"def {func}({vname}):\n    for item in {vname}:\n        print(item)\n\n{func}(3.14)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}(3.14)\n  File \"main.py\", line 2, in {func}\n    for item in {vname}:\nTypeError: 'float' object is not iterable"
    opt_code = f"def {func}({vname}):\n    # If the goal is to handle single items or lists\n    iterable = {vname} if isinstance({vname}, (list, tuple)) else [{vname}]\n    for item in iterable:\n        print(item)\n\n{func}(3.14)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the TypeError caused by trying to loop through a non-iterable object.",
        "input": {
            "title": "Iterating over a float",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `for ... in ...` construct requires an iterable object (one that implements the `__iter__` method). Floats and integers do not implement this method.",
            "beginner": "You tried to loop through a single number as if it were a list of items. Python doesn't know how to step through a single decimal number.",
            "analogy": "It's like trying to flip through the pages of a single photograph. It's just one thing, not a sequence of things.",
            "solution": "Ensure the variable being iterated over is a list, tuple, string, or another iterable type. If it can be a single item, wrap it in a list.",
            "prevention": "Use type hinting (e.g., `def func(val: list):`) to make the expected type clear, and validate input types if the function can receive mixed types.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["type-error", "iteration", "iterable"]
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
