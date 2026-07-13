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

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Assigning result of list.append() to a variable
        code = f"def {func}({vname}, new_item):\n    # list.append() modifies in-place and returns None\n    updated_{vname} = {vname}.append(new_item)\n    return updated_{vname}\n\nprint({func}([1, 2], 3)) # Prints None"
        error = f"Logical Bug: A function intended to return an updated list returns `None` instead because it returns the result of `list.append()`."
        opt_code = f"def {func}({vname}, new_item):\n    {vname}.append(new_item)\n    return {vname}\n\nprint({func}([1, 2], 3))"
        technical = f"In Python, methods that mutate objects in-place (like `list.append()`, `list.sort()`, `dict.update()`) generally return `None` to explicitly signal that they mutate the object rather than returning a new one."
        beginner = f"When you use `.append()`, it adds the item to the list but gives back `None`. By saving the answer of `.append()` into a variable, you accidentally threw away your list and just kept `None`."
        title = "Assigning result of .append()"
        tags = ["logical-bug", "list", "append", "none"]
    
    elif variation == 1:
        # Off-by-one in range (missing last element)
        code = f"def {func}({vname}):\n    # Trying to iterate up to the length of the list, but range(1, len) misses the 0th index and stops before len\n    for i in range(1, len({vname})):\n        print({vname}[i])\n\n{func}(['A', 'B', 'C']) # Skips 'A'"
        error = f"Logical Bug: Incorrect bounds in `range()` cause the loop to skip elements."
        opt_code = f"def {func}({vname}):\n    for i in range(len({vname})):\n        print({vname}[i])\n\n{func}(['A', 'B', 'C'])"
        technical = f"The `range(start, stop)` function generates a sequence from `start` (inclusive) to `stop` (exclusive). By using `range(1, len())`, the loop completely skips the 0th index (the first element) of the list."
        beginner = f"Python lists start at index 0. Because you told the range to start at 1, the loop completely skips the very first item in the list."
        title = "Off-By-One Range Error"
        tags = ["logical-bug", "off-by-one", "range", "loops"]
    
    elif variation == 2:
        # Missing Return Statement
        code = f"def {func}(a, b):\n    {lvar} = a + b\n    # Missing return statement\n\nresult = {func}(5, 10)\n# result is None"
        error = f"Logical Bug: A function performs a calculation but fails to return the result, causing downstream code to receive `None`."
        opt_code = f"def {func}(a, b):\n    {lvar} = a + b\n    return {lvar}\n\nresult = {func}(5, 10)"
        technical = f"If a Python function execution reaches the end of its code block without encountering a `return` statement, it implicitly returns `None`. Any variable capturing the function's output will be assigned `None`."
        beginner = f"Your function does the math perfectly, but it never gives the answer back to the rest of the program. So when you ask for the result, you get `None` (nothing)."
        title = "Missing Return Statement"
        tags = ["logical-bug", "missing-return", "none"]

    elif variation == 3:
        # Dictionary iteration modifying size
        code = f"def {func}(my_dict):\n    for key in my_dict.keys():\n        if my_dict[key] == 0:\n            del my_dict[key] # RuntimeError in Python 3, logical bug in some contexts\n    return my_dict"
        error = f"Logical Bug / RuntimeError: dictionary changed size during iteration"
        opt_code = f"def {func}(my_dict):\n    keys_to_delete = [k for k, v in my_dict.items() if v == 0]\n    for key in keys_to_delete:\n        del my_dict[key]\n    return my_dict"
        technical = f"In Python 3, `.keys()`, `.values()`, and `.items()` return dictionary views. Iterating over a view while adding or deleting items from the underlying dictionary raises a RuntimeError or leads to skipped elements."
        beginner = f"You can't delete items from a dictionary while you are in the middle of looping through it. The loop loses its place."
        title = "Modifying Dictionary During Iteration"
        tags = ["logical-bug", "dictionary", "iteration", "mutation"]

    else:
        # Using `is` for string/value comparison
        code = f"def {func}(user_input):\n    # `is` checks memory identity, not value equality\n    if user_input is \"STOP\":\n        return True\n    return False\n\n# {func}(\"ST\" + \"OP\") might return False"
        error = f"Logical Bug: Using `is` instead of `==` for string comparison can lead to unpredictable results due to string interning."
        opt_code = f"def {func}(user_input):\n    if user_input == \"STOP\":\n        return True\n    return False"
        technical = f"The `is` operator checks if two references point to the same object in memory. While Python caches (interns) some small strings, dynamically constructed strings are often separate objects, making `a is b` evaluate to False even if their values are identical."
        beginner = f"You asked Python 'Are these the exact same physical string in memory?' instead of 'Do these strings say the same thing?'. Use `==` to check if they have the same text."
        title = "String Comparison using `is`"
        tags = ["logical-bug", "string-comparison", "identity-operator"]

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
            "solution": "Apply the correct syntax, loop bounds, return logic, or operator depending on the logical bug.",
            "prevention": "Write unit tests to verify function outputs, and use static analysis tools like PyLint to catch anti-patterns.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N) or O(1)", "after": "O(N) or O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated Python Logical Bug Variations",
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
