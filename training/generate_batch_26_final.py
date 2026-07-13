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

ensure_dir("../datasets/logical_bugs/python")
output_file = "../datasets/logical_bugs/python/common_logic_bugs.json"

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
        candidate = f"PY_LOGICAL_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "filter_data", "run", "compute", "execute", "analyze"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]
local_vars = ["total", "count", "average", "sum_val", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(800):
    variation = i % 4
    func = funcs[(i // 4) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Modifying a list while iterating
        code = f"def {func}({vname}):\n    # Removing items during iteration causes the loop to skip the next item\n    for item in {vname}:\n        if item % 2 == 0:\n            {vname}.remove(item)\n    return {vname}\n\nprint({func}([1, 2, 2, 3])) # Fails to remove the second '2'"
        error = f"Logical Bug: Modifying a sequence while iterating over it leads to skipped elements."
        opt_code = f"def {func}({vname}):\n    # Iterate over a copy of the list\n    for item in {vname}[:]:\n        if item % 2 == 0:\n            {vname}.remove(item)\n    return {vname}\n    # Or better: return [x for x in {vname} if x % 2 != 0]"
        technical = f"When iterating over a list, Python maintains an internal index. If an item is removed, all subsequent items shift left. On the next iteration, the internal index increments, meaning it skips over the element that shifted into the current position."
        beginner = f"If you pull a book off a bookshelf while someone is counting them from left to right, the books slide over and they will accidentally skip counting the next book. Always make a copy of the list if you want to remove things while looping."
        title = "Modifying List During Iteration"
        tags = ["logical-bug", "list-mutation", "iteration", "skipping"]
    
    elif variation == 1:
        # Default Mutable Arguments
        code = f"def {func}(new_item, {vname}=[]):\n    # The default list is instantiated ONCE when the function is defined\n    {vname}.append(new_item)\n    return {vname}\n\nprint({func}(1)) # [1]\nprint({func}(2)) # [1, 2] instead of [2]"
        error = f"Logical Bug: Default mutable arguments retain state across multiple function calls."
        opt_code = f"def {func}(new_item, {vname}=None):\n    if {vname} is None:\n        {vname} = []\n    {vname}.append(new_item)\n    return {vname}\n\nprint({func}(1))\nprint({func}(2))"
        technical = f"In Python, default arguments are evaluated exactly once at function definition time, not each time the function is called. If the default is a mutable object like a list or dictionary, all calls to the function that omit that argument will share the same instance of the object."
        beginner = f"You gave the function an empty box `[]` as a default. But Python only creates that box once. Every time you call the function without providing a box, it reuses the exact same box, keeping all the old items."
        title = "Default Mutable Argument"
        tags = ["logical-bug", "default-arguments", "mutability", "state-leak"]
    
    elif variation == 2:
        # `is` vs `==` for integers outside cached range
        code = f"def {func}(a, b):\n    # 'is' checks memory identity. This works for small ints but fails for large ones\n    if a is b:\n        return True\n    return False\n\nprint({func}(1000, 10**3)) # Returns False"
        error = f"Logical Bug: Using `is` for value equality on integers is unsafe outside the cached range [-5, 256]."
        opt_code = f"def {func}(a, b):\n    # '==' checks value equality\n    if a == b:\n        return True\n    return False\n\nprint({func}(1000, 10**3)) # Returns True"
        technical = f"CPython caches small integers from -5 to 256. Therefore, `100 is 100` is True because they point to the exact same cached object in memory. However, `1000 is 1000` evaluates to False if they are computed separately, because they are distinct objects in memory. You must use `==` for value equality."
        beginner = f"You asked Python 'Are these numbers the exact same physical object in memory?' (`is`), but you should have asked 'Do these numbers have the same value?' (`==`). For large numbers, Python creates separate objects even if their values match."
        title = "Integer Comparison with `is`"
        tags = ["logical-bug", "integer-caching", "identity-operator", "equality"]

    else:
        # Incorrect boolean logic (De Morgan's Laws)
        code = f"def {func}(a, b):\n    # Intention: run if neither A nor B is true\n    # Bug: 'not a or not b' runs if AT LEAST one is false\n    if not a or not b:\n        return \"Failed\"\n    return \"Passed\"\n\n# {func}(False, True) returns 'Failed', which is correct.\n# But {func}(True, False) also returns 'Failed'."
        error = f"Logical Bug: Incorrect boolean logic implementation violating De Morgan's laws."
        opt_code = f"def {func}(a, b):\n    # Correct implementation of NOR\n    if not (a or b): # equivalent to 'not a and not b'\n        return \"Failed\"\n    return \"Passed\""
        technical = f"According to De Morgan's Laws, `not A and not B` is logically equivalent to `not (A or B)`. Conversely, `not A or not B` is equivalent to `not (A and B)`. Mixing these up leads to logical branches executing under the wrong conditions."
        beginner = f"Your logic is backwards. You wanted 'If A is false AND B is false', but you wrote 'If A is false OR B is false'. If you use 'OR', the code triggers if just one of them fails."
        title = "Incorrect Boolean Logic (De Morgan's)"
        tags = ["logical-bug", "boolean-logic", "de-morgans-laws", "conditionals"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "logical_bug",
        "instruction": f"Fix the logical bug caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like expecting a specific behavior but overlooking a fundamental rule of how the system operates.",
            "solution": "Apply the correct operator, initialization, or iteration pattern depending on the logical bug.",
            "prevention": "Enable aggressive static analysis tools (like PyLint or SonarQube) which detect mutable default arguments and unsafe `is` comparisons automatically.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N) or O(1)", "after": "O(N) or O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated Python Logical Bug Variations (Finale)",
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
