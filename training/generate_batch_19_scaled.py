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

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "filter_data", "run", "compute", "execute", "analyze"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]
local_vars = ["total", "count", "average", "sum_val", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # String and Int Concatenation
        code = f"def {func}({vname}, limit):\n    # Cannot implicitly concatenate string and int\n    print(\"Processing up to: \" + limit)\n    return {vname}[:limit]\n\n{func}([1, 2, 3], 5)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}([1, 2, 3], 5)\n  File \"main.py\", line 3, in {func}\n    print(\"Processing up to: \" + limit)\nTypeError: can only concatenate str (not \"int\") to str"
        opt_code = f"def {func}({vname}, limit):\n    print(\"Processing up to: \" + str(limit))\n    return {vname}[:limit]\n\n{func}([1, 2, 3], 5)"
        technical = f"Python is strongly typed and does not implicitly cast integers to strings during concatenation. The `+` operator requires both operands to be of the same type (`str + str` or `int + int`)."
        beginner = f"You tried to glue together a word and a number. Python doesn't know how to do that automatically. You have to turn the number into a string first using `str(limit)`."
        title = "String and Int Concatenation TypeError"
        tags = ["type-error", "concatenation", "strings", "types"]
    
    elif variation == 1:
        # Calling a Non-Callable
        code = f"def {func}({lvar}):\n    # Attempting to call an integer as a function\n    result = {lvar}()\n    return result\n\n{func}(10)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}(10)\n  File \"main.py\", line 3, in {func}\n    result = {lvar}()\nTypeError: 'int' object is not callable"
        opt_code = f"def {func}({lvar}):\n    result = {lvar}\n    return result\n\n{func}(10)"
        technical = f"The parentheses `()` invoke the `__call__` method on an object. Built-in primitives like `int`, `str`, and `list` do not implement `__call__`. Adding `()` to an integer variable raises a TypeError."
        beginner = f"You put parentheses `()` right after a variable holding a number, which tells Python to 'run' the number like it's a function. But numbers aren't functions, so Python throws an error."
        title = "Calling an Integer"
        tags = ["type-error", "non-callable", "functions"]
    
    elif variation == 2:
        # NoneType Arithmetic
        code = f"def fetch_data():\n    pass # Implicitly returns None\n\ndef {func}():\n    {lvar} = fetch_data()\n    return {lvar} + 10\n\n{func}()"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}()\n  File \"main.py\", line 5, in {func}\n    return {lvar} + 10\nTypeError: unsupported operand type(s) for +: 'NoneType' and 'int'"
        opt_code = f"def fetch_data():\n    return 0 # explicitly return a valid default\n\ndef {func}():\n    {lvar} = fetch_data()\n    if {lvar} is None:\n        {lvar} = 0\n    return {lvar} + 10\n\n{func}()"
        technical = f"A function without a `return` statement evaluates to `None` (type `NoneType`). Attempting mathematical operations (`+`) on `NoneType` results in a TypeError because the `__add__` operator is not defined for `NoneType` and `int`."
        beginner = f"The `fetch_data` function didn't return an answer, so you got `None` (nothing). You then tried to add 10 to `None`, which doesn't make mathematical sense."
        title = "Arithmetic on NoneType"
        tags = ["type-error", "none-type", "arithmetic", "return"]

    elif variation == 3:
        # Missing Positional Argument
        code = f"def {func}(a, b):\n    return a + b\n\n# Missing the second argument 'b'\n{lvar} = {func}(5)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {lvar} = {func}(5)\nTypeError: {func}() missing 1 required positional argument: 'b'"
        opt_code = f"def {func}(a, b):\n    return a + b\n\n{lvar} = {func}(5, 10)"
        technical = f"Python enforces strict arity matching for positional arguments. If a function signature dictates two parameters and no default arguments are provided, passing fewer than two arguments raises a TypeError."
        beginner = f"Your function expects two ingredients (`a` and `b`), but you only gave it one (`5`). Python refuses to run the function until you provide the second ingredient."
        title = "Missing Positional Argument"
        tags = ["type-error", "arguments", "functions"]

    else:
        # Iterating over a non-iterable (int)
        code = f"def {func}({lvar}):\n    total = 0\n    # Integers are not iterable\n    for i in {lvar}:\n        total += i\n    return total\n\n{func}(100)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}(100)\n  File \"main.py\", line 4, in {func}\n    for i in {lvar}:\nTypeError: 'int' object is not iterable"
        opt_code = f"def {func}({lvar}):\n    total = 0\n    for i in range({lvar}):\n        total += i\n    return total\n\n{func}(100)"
        technical = f"The `for...in` loop requires the target object to implement the `__iter__` or `__getitem__` methods (be an iterable). Primitives like `int` do not implement these methods, causing a TypeError."
        beginner = f"You tried to loop over a single number (`100`). You can loop over a list of items or text, but to loop a specific number of times, you need to use `range(100)`."
        title = "Iterating Over an Integer"
        tags = ["type-error", "iterable", "loops", "integers"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": f"Fix the TypeError caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like trying to plug a square peg into a round hole. The operation you want to perform is fundamentally incompatible with the shape of the data.",
            "solution": "Apply the correct type conversion (e.g., `str()`), check for `None`, supply missing arguments, or use `range()` for iteration.",
            "prevention": "Use Python Type Hints (`def func(a: int) -> int:`) and a type checker like MyPy to catch these incompatibilities before runtime.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated Python TypeError Variations",
            "language_version": "Python 3.x",
            "tags": tags
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
