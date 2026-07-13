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

ensure_dir("../datasets/optimization_examples/python")
output_file = "../datasets/optimization_examples/python/common_optimizations.json"

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
        candidate = f"PY_OPTIMIZE_{i:06d}"
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
        # List pop(0) vs deque popleft()
        code = f"def {func}({vname}):\n    while len({vname}) > 0:\n        # Popping from the front of a list is O(N)\n        {lvar} = {vname}.pop(0)\n        print({lvar})\n\n{func}([1, 2, 3, 4, 5])"
        error = f"Performance Issue: Using `list.pop(0)` takes O(N) time because all subsequent elements must be shifted in memory. Doing this in a loop results in O(N^2) complexity."
        opt_code = f"from collections import deque\n\ndef {func}({vname}):\n    queue = deque({vname})\n    while len(queue) > 0:\n        {lvar} = queue.popleft() # O(1) time\n        print({lvar})\n\n{func}([1, 2, 3, 4, 5])"
        technical = f"Python lists are implemented as contiguous arrays. Removing the first element requires shifting all $N-1$ remaining elements one position to the left, which takes O(N) time. The `collections.deque` is implemented as a doubly-linked list, allowing O(1) removals from both ends."
        beginner = f"If you take the first person out of a line, everyone else in the line has to step forward. If the line has a million people, that takes a lot of effort. Use a 'deque' (double-ended queue) which handles this instantly."
        title = "O(N) List pop(0) vs O(1) Deque popleft()"
        tags = ["optimization", "list", "deque", "pop"]
    
    elif variation == 1:
        # Generator Expression vs List Comprehension in aggregation
        code = f"def {func}(n):\n    # Creates a massive list in memory just to sum it\n    return sum([x * x for x in range(n)])\n\n{func}(10000000)"
        error = f"Performance Issue: Using a list comprehension inside an aggregation function like `sum()` constructs the entire list in memory, potentially causing MemoryErrors and wasting RAM."
        opt_code = f"def {func}(n):\n    # Uses a generator expression (no brackets) to yield items one by one\n    return sum(x * x for x in range(n))\n\n{func}(10000000)"
        technical = f"A list comprehension `[...]` eagerly evaluates and stores all elements in memory simultaneously (O(N) space). A generator expression `(...)` lazily yields elements one at a time (O(1) space). When passing directly to an accumulator like `sum()`, generators are far more memory-efficient."
        beginner = f"You built a massive list of ten million numbers in the computer's memory just to add them together and throw the list away. If you remove the square brackets, Python will just generate and add the numbers one by one without storing them."
        title = "Generator vs List Comprehension for Aggregation"
        tags = ["optimization", "memory", "generator", "list-comprehension"]
    
    elif variation == 2:
        # Global variable access in tight loops
        code = f"GLOBAL_MULTIPLIER = 2.5\n\ndef {func}({vname}):\n    {lvar} = 0\n    for item in {vname}:\n        # Accessing the global scope inside a tight loop is slow in CPython\n        {lvar} += item * GLOBAL_MULTIPLIER\n    return {lvar}\n\n{func}([1, 2, 3])"
        error = f"Performance Issue: Looking up variables in the global scope requires a dictionary lookup (`LOAD_GLOBAL`), which is slower than local array-based lookups (`LOAD_FAST`) inside a tight loop."
        opt_code = f"GLOBAL_MULTIPLIER = 2.5\n\ndef {func}({vname}):\n    {lvar} = 0\n    local_multiplier = GLOBAL_MULTIPLIER # Cache locally\n    for item in {vname}:\n        {lvar} += item * local_multiplier\n    return {lvar}\n\n{func}([1, 2, 3])"
        technical = f"In CPython, local variables are accessed via extremely fast array offsets (`LOAD_FAST` bytecode). Global variables require dictionary lookups in the `globals()` dictionary (`LOAD_GLOBAL`), which incurs hashing overhead. In tight loops (millions of iterations), caching globals to local variables provides a measurable speedup."
        beginner = f"To read the global multiplier, the computer has to search through a big dictionary of names every single time the loop runs. By copying it into a local variable first, the computer can grab it instantly."
        title = "Global Variable Access in Tight Loops"
        tags = ["optimization", "globals", "local-variables", "cpython-internals"]

    elif variation == 3:
        # Recomputing loop invariants
        code = f"import math\n\ndef {func}({vname}, limit):\n    results = []\n    for item in {vname}:\n        # math.sqrt(limit) is recomputed on every iteration\n        if item < math.sqrt(limit):\n            results.append(item)\n    return results\n\n{func}([1, 2, 3, 4, 5], 100)"
        error = f"Performance Issue: An expensive calculation that does not change is repeatedly executed inside a loop."
        opt_code = f"import math\n\ndef {func}({vname}, limit):\n    results = []\n    threshold = math.sqrt(limit) # Calculate once outside the loop\n    for item in {vname}:\n        if item < threshold:\n            results.append(item)\n    return results\n\n{func}([1, 2, 3, 4, 5], 100)"
        technical = f"Loop-invariant code motion (hoisting) is an optimization technique. While some compiled languages do this automatically, Python's dynamic nature means `math.sqrt` is fully evaluated on every iteration. Moving static computations outside the loop saves significant CPU cycles."
        beginner = f"You are making the computer calculate the square root of 100 over and over again for every single item in the list. Calculate it once before the loop starts and save the answer."
        title = "Recomputing Loop Invariants"
        tags = ["optimization", "loop-invariants", "hoisting"]

    else:
        # String repeated concatenation using + vs * 
        code = f"def {func}(char, count):\n    {lvar} = \"\"\n    for _ in range(count):\n        {lvar} += char\n    return {lvar}\n\n{func}('-', 50)"
        error = f"Performance Issue: Building a string by repeatedly appending a single character in a loop is slow and non-pythonic compared to the string multiplication operator."
        opt_code = f"def {func}(char, count):\n    {lvar} = char * count # C-optimized memory allocation\n    return {lvar}\n\n{func}('-', 50)"
        technical = f"The string multiplication operator `str * int` is highly optimized in CPython. It allocates the exact required memory buffer once and rapidly fills it. A python-level loop incurs bytecode interpretation overhead and potential memory reallocations."
        beginner = f"Instead of looping 50 times to slowly build a string of dashes, you can just multiply the string by 50 in Python (`'-' * 50`). It's much faster and easier to read."
        title = "String Multiplication vs Loop Appending"
        tags = ["optimization", "string-multiplication", "pythonic"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "optimization",
        "instruction": f"Optimize the Python code to resolve the performance issue: {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like making 100 trips to the grocery store to buy 100 apples, instead of taking a big cart and buying them all in one trip.",
            "solution": "Refactor the logic to use the appropriate data structure, generator, or operator that minimizes algorithmic complexity or memory overhead.",
            "prevention": "Familiarize yourself with Python's Big-O time complexities for standard data structures (e.g., `list`, `set`, `deque`).",
            "optimized_code": opt_code,
            "complexity": {"before": "Higher time/space overhead", "after": "Optimal time/space complexity"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated Python Optimization Variations",
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
