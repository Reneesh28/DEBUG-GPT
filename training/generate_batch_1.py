import json
import os
import jsonschema
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

schema_path = "dataset_schema.json"
with open(schema_path, "r") as f:
    schema = json.load(f)

ensure_dir("../datasets/runtime_errors/python")
output_file = "../datasets/runtime_errors/python/index_error.json"

if os.path.exists(output_file):
    with open(output_file, "r") as f:
        data = json.load(f)
else:
    data = []

import glob

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

# Source: Inspired by Stack Overflow discussions on IndexError
var_names = ["items", "data", "records", "users", "values", "numbers", "elements", "scores", "results", "points"]
funcs = ["process", "analyze", "calculate", "evaluate", "compute", "update", "transform", "filter", "aggregate", "sort"]

# Variation 1: Off-by-one error in while loop (access)
for i in range(25):
    var = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    val1 = random.randint(3, 10)
    code = f"def {func}({var}):\n    i = 0\n    while i <= len({var}):\n        print({var}[i])\n        i += 1\n\n{func}([1, 2, 3])"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}([1, 2, 3])\n  File \"main.py\", line 4, in {func}\n    print({var}[i])\nIndexError: list index out of range"
    opt_code = f"def {func}({var}):\n    for item in {var}:\n        print(item)\n\n{func}([1, 2, 3])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the IndexError caused by an off-by-one boundary condition in the loop.",
        "input": {
            "title": "Off-by-one loop boundary",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The loop condition `i <= len(var)` allows the index to reach the length of the list. Since Python uses 0-based indexing, the maximum valid index is `len(var) - 1`. Accessing `var[len(var)]` raises an IndexError.",
            "beginner": "You are trying to access an item at a position that doesn't exist. If a list has 3 items, they are at positions 0, 1, and 2. Trying to access position 3 causes an error.",
            "analogy": "Imagine a 3-story building with floors labeled 0, 1, and 2. If you try to take the elevator to floor 3, it breaks because that floor doesn't exist.",
            "solution": "Change the loop condition to `i < len(var)` or use a `for` loop to iterate directly over the elements.",
            "prevention": "Prefer iterating directly over elements using `for item in lst:` rather than using a while loop with an index counter.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["index-error", "loop", "off-by-one"]
        }
    }
    samples.append(sample)

# Variation 2: Assignment to empty list (assignment)
for i in range(25):
    var = var_names[(i+2) % len(var_names)]
    func = funcs[(i+2) % len(funcs)]
    code = f"def {func}_items(n):\n    {var} = []\n    for i in range(n):\n        {var}[i] = i * 2\n    return {var}\n\n{func}_items(5)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}_items(5)\n  File \"main.py\", line 4, in {func}_items\n    {var}[i] = i * 2\nIndexError: list assignment index out of range"
    opt_code = f"def {func}_items(n):\n    {var} = []\n    for i in range(n):\n        {var}.append(i * 2)\n    return {var}\n\n{func}_items(5)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the IndexError caused by assigning a value to an index in an empty list.",
        "input": {
            "title": "Assignment to empty list",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Attempting to assign a value to an index that does not yet exist in the list raises an IndexError. Lists in Python do not automatically resize upon assignment to out-of-bounds indices.",
            "beginner": "You are trying to put a value into a specific slot in a list, but that list is currently empty so the slot doesn't exist yet.",
            "analogy": "It's like trying to place a book on the 5th shelf of a bookcase that hasn't been built yet.",
            "solution": "Use the `.append()` method to add new items to the end of the list, or initialize the list with a predetermined size (e.g., `[0] * n`).",
            "prevention": "Use `.append()` or list comprehensions when dynamically building a list from scratch.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["index-error", "assignment", "list-building"]
        }
    }
    samples.append(sample)

# Variation 3: Accessing an empty list
for i in range(25):
    var = var_names[(i+4) % len(var_names)]
    func = funcs[(i+4) % len(funcs)]
    code = f"def get_first_{var}(data_list):\n    # Filter some items\n    filtered = [x for x in data_list if x > 10]\n    return filtered[0]\n\nget_first_{var}([1, 2, 3])"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    get_first_{var}([1, 2, 3])\n  File \"main.py\", line 4, in get_first_{var}\n    return filtered[0]\nIndexError: list index out of range"
    opt_code = f"def get_first_{var}(data_list):\n    # Filter some items\n    filtered = [x for x in data_list if x > 10]\n    return filtered[0] if filtered else None\n\nget_first_{var}([1, 2, 3])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the IndexError caused by accessing the first element of a potentially empty list.",
        "input": {
            "title": "Accessing element of empty list",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The list comprehension may return an empty list if no elements satisfy the condition. Accessing index `0` of an empty list raises an IndexError since no elements exist.",
            "beginner": "The filtering step removed all the items, leaving an empty list. When you tried to get the 'first' item from this empty list, Python gave an error.",
            "analogy": "It's like reaching into an empty cookie jar and expecting to grab the first cookie.",
            "solution": "Check if the list is empty before accessing its elements. You can use a conditional expression like `lst[0] if lst else None`.",
            "prevention": "Always verify that a list contains elements before accessing specific indices, especially after filtering operations.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["index-error", "empty-list", "filtering"]
        }
    }
    samples.append(sample)

# Variation 4: Modifying list while iterating
for i in range(25):
    var = var_names[(i+6) % len(var_names)]
    func = funcs[(i+6) % len(funcs)]
    code = f"def remove_evens({var}):\n    for i in range(len({var})):\n        if {var}[i] % 2 == 0:\n            {var}.pop(i)\n    return {var}\n\nremove_evens([1, 2, 3, 4, 5])"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    remove_evens([1, 2, 3, 4, 5])\n  File \"main.py\", line 3, in remove_evens\n    if {var}[i] % 2 == 0:\nIndexError: list index out of range"
    opt_code = f"def remove_evens({var}):\n    return [x for x in {var} if x % 2 != 0]\n\nremove_evens([1, 2, 3, 4, 5])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the IndexError caused by modifying a list while iterating through it with indices.",
        "input": {
            "title": "Modifying list while iterating",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Removing elements from a list shifts the indices of subsequent elements. The loop bound `len(var)` is evaluated once at the start, so accessing `var[i]` eventually exceeds the new, smaller bounds of the list.",
            "beginner": "When you delete an item from the list, the list shrinks, but your loop keeps trying to reach the original length, eventually looking past the end of the new list.",
            "analogy": "Imagine a line of 5 people. If the 2nd person leaves, the line shrinks to 4. If you then call out for the 5th person, no one is there.",
            "solution": "Iterate backwards, create a copy of the list to iterate over, or better yet, use a list comprehension to create a new filtered list.",
            "prevention": "Never modify the structure (add/remove elements) of a list while iterating over it using indices or directly.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N^2)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["index-error", "iteration", "list-modification"]
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
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully generated and validated {len(samples)} samples. Total in file: {len(data)}")
else:
    print(f"Failed to validate {invalid_count} samples. Output not saved.")
