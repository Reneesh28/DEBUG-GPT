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
output_file = "../datasets/runtime_errors/python/index_and_key_errors.json"

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
        # IndexError: list index out of range (len)
        code = f"def {func}({vname}):\n    # Lists are 0-indexed, so len(list) is 1 past the end\n    last_item = {vname}[len({vname})]\n    return last_item\n\n{func}([10, 20, 30])"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}([10, 20, 30])\n  File \"main.py\", line 3, in {func}\n    last_item = {vname}[len({vname})]\nIndexError: list index out of range"
        opt_code = f"def {func}({vname}):\n    if not {vname}:\n        return None\n    last_item = {vname}[-1] # Or {vname}[len({vname}) - 1]\n    return last_item\n\n{func}([10, 20, 30])"
        technical = f"Python sequences are 0-indexed. A list with 3 elements has valid indices 0, 1, and 2. Attempting to access `list[len(list)]` looks for index 3, which is out of bounds."
        beginner = f"Since Python starts counting from 0, the last item in a 3-item list is at position 2, not 3. Trying to grab position 3 asks for something that isn't there."
        title = "List Index Out of Range (Off-by-One)"
        tags = ["runtime-error", "index-error", "list", "off-by-one"]
    
    elif variation == 1:
        # KeyError: Dictionary lookup
        code = f"def {func}(user_dict, search_key):\n    # Accessing a missing key using bracket notation\n    value = user_dict[search_key]\n    return value\n\n{func}({{'name': 'Alice', 'age': 30}}, 'email')"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}({{'name': 'Alice', 'age': 30}}, 'email')\n  File \"main.py\", line 3, in {func}\n    value = user_dict[search_key]\nKeyError: 'email'"
        opt_code = f"def {func}(user_dict, search_key):\n    # Use .get() to safely handle missing keys\n    value = user_dict.get(search_key, 'Not Found')\n    return value\n\n{func}({{'name': 'Alice', 'age': 30}}, 'email')"
        technical = f"Using bracket notation (`dict[key]`) to access a dictionary directly throws a `KeyError` if the key does not exist in the hash map. To avoid this, use `dict.get(key, default)` or check `if key in dict:` first."
        beginner = f"You asked the dictionary for the definition of 'email', but 'email' isn't in this dictionary. Python panicked and threw a KeyError. Use `.get()` to safely ask for something that might not be there."
        title = "Missing Dictionary Key"
        tags = ["runtime-error", "key-error", "dictionary"]
    
    elif variation == 2:
        # KeyError: Set removal
        code = f"def {func}(my_set, item_to_remove):\n    # .remove() throws an error if the item is missing\n    my_set.remove(item_to_remove)\n    return my_set\n\n{func}({{1, 2, 3}}, 99)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}({{1, 2, 3}}, 99)\n  File \"main.py\", line 3, in {func}\n    my_set.remove(item_to_remove)\nKeyError: 99"
        opt_code = f"def {func}(my_set, item_to_remove):\n    # .discard() removes the item if present, but does nothing if missing\n    my_set.discard(item_to_remove)\n    return my_set\n\n{func}({{1, 2, 3}}, 99)"
        technical = f"The `set.remove(elem)` method requires that the element exists in the set; otherwise, it raises a `KeyError`. If you want to remove an element only if it exists without throwing an error, use `set.discard(elem)`."
        beginner = f"You told Python to aggressively remove the number 99 from the set. Since 99 wasn't there, Python threw an error. Use `.discard()` if you just want to say 'remove 99 if you happen to see it'."
        title = "Set KeyError on Removal"
        tags = ["runtime-error", "key-error", "set", "remove"]

    elif variation == 3:
        # IndexError: String indexing
        code = f"def {func}(text):\n    for i in range(10):\n        # Assumes the string is at least 10 characters long\n        print(text[i])\n\n{func}(\"Hi\")"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}(\"Hi\")\n  File \"main.py\", line 4, in {func}\n    print(text[i])\nIndexError: string index out of range"
        opt_code = f"def {func}(text):\n    for i in range(min(10, len(text))):\n        print(text[i])\n    # Or simply: for char in text[:10]: print(char)\n\n{func}(\"Hi\")"
        technical = f"Like lists, strings are sequences accessed by index. Attempting to access an index beyond the length of the string (`len(string) - 1`) raises an `IndexError`."
        beginner = f"You told the loop to print the first 10 letters of the word, but the word 'Hi' only has 2 letters. When the loop asked for the 3rd letter, it crashed."
        title = "String Index Out of Range"
        tags = ["runtime-error", "index-error", "string"]

    else:
        # IndexError: Empty list pop
        code = f"def {func}({vname}):\n    while True:\n        # Attempting to pop from an empty list\n        item = {vname}.pop()\n        if item == 'STOP':\n            break\n\n{func}(['A', 'B', 'C'])"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}(['A', 'B', 'C'])\n  File \"main.py\", line 4, in {func}\n    item = {vname}.pop()\nIndexError: pop from empty list"
        opt_code = f"def {func}({vname}):\n    while {vname}:\n        item = {vname}.pop()\n        if item == 'STOP':\n            break\n\n{func}(['A', 'B', 'C'])"
        technical = f"The `list.pop()` method removes and returns the last element of the list. If the list is completely empty, it has no elements to remove, and it raises an `IndexError`. Always check if the list is non-empty before calling `pop()` in a loop."
        beginner = f"The loop kept taking items out of the box one by one. Once the box was completely empty, it reached in to grab another item and failed, causing a crash."
        title = "Popping from Empty List"
        tags = ["runtime-error", "index-error", "list", "pop"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": f"Fix the Python runtime error caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like reaching into a bag of 5 apples, grabbing them one by one, and then blindly reaching in for a 6th apple.",
            "solution": "Apply bounds checking, use safe access methods (`.get()`, `.discard()`), or verify sequence lengths before indexing.",
            "prevention": "Avoid hardcoded iteration limits (`range(10)`). Prefer iterating over the sequence directly (`for item in seq:`).",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1) to crash", "after": "O(1) access"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated Python Index/Key Error Variations",
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
