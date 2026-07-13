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
output_file = "../datasets/runtime_errors/python/key_error.json"

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

# Source: Inspired by Stack Overflow discussions on KeyError
dict_names = ["user_data", "config", "settings", "records", "cache", "mapping", "attributes", "metadata", "options", "stats"]
funcs = ["get_value", "process_info", "update_record", "fetch_data", "retrieve", "calculate_stat", "read_config", "load_profile", "parse_data", "apply_settings"]

# Variation 1: Direct access of missing key
for i in range(25):
    dname = dict_names[i % len(dict_names)]
    func = funcs[i % len(funcs)]
    code = f"def {func}({dname}):\n    print({dname}['status'])\n\n{func}({{'id': 101, 'name': 'Alice'}})"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}({{'id': 101, 'name': 'Alice'}})\n  File \"main.py\", line 2, in {func}\n    print({dname}['status'])\nKeyError: 'status'"
    opt_code = f"def {func}({dname}):\n    print({dname}.get('status', 'Unknown'))\n\n{func}({{'id': 101, 'name': 'Alice'}})"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the KeyError caused by accessing a non-existent dictionary key.",
        "input": {
            "title": "Accessing missing dictionary key",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "A KeyError is raised when attempting to access a dictionary key that does not exist using bracket notation `dict[key]`.",
            "beginner": "You tried to look up a word in a dictionary, but that word isn't there.",
            "analogy": "It's like trying to open a locker with a specific number, but that locker number doesn't exist in the hallway.",
            "solution": "Use the `.get()` method to provide a default value if the key is missing, or check if the key exists using the `in` operator before accessing it.",
            "prevention": "Always use `.get(key, default)` when you are not absolutely certain a key exists in a dictionary.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["dictionary", "key-error", "missing-key"]
        }
    }
    samples.append(sample)

# Variation 2: Modifying dictionary during iteration
for i in range(25):
    dname = dict_names[(i+2) % len(dict_names)]
    func = funcs[(i+2) % len(funcs)]
    code = f"def {func}({dname}):\n    for key in {dname}:\n        if {dname}[key] == 0:\n            del {dname}[key]\n    return {dname}\n\n{func}({{'a': 1, 'b': 0, 'c': 3}})"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    {func}({{'a': 1, 'b': 0, 'c': 3}})\n  File \"main.py\", line 2, in {func}\n    for key in {dname}:\nRuntimeError: dictionary changed size during iteration"
    # Actually, Python raises RuntimeError here, not KeyError! 
    # Let's adjust this to a KeyError scenario: Popping a key that was already removed or trying to access it after removal.
    code = f"def {func}({dname}, keys_to_remove):\n    for key in keys_to_remove:\n        del {dname}[key]\n    return {dname}\n\n{func}({{'a': 1, 'b': 2}}, ['a', 'c'])"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    {func}({{'a': 1, 'b': 2}}, ['a', 'c'])\n  File \"main.py\", line 3, in {func}\n    del {dname}[key]\nKeyError: 'c'"
    opt_code = f"def {func}({dname}, keys_to_remove):\n    for key in keys_to_remove:\n        {dname}.pop(key, None)\n    return {dname}\n\n{func}({{'a': 1, 'b': 2}}, ['a', 'c'])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the KeyError caused by attempting to delete a dictionary key that doesn't exist.",
        "input": {
            "title": "Deleting missing dictionary key",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Using the `del` statement on a dictionary key raises a KeyError if the key is not present in the dictionary.",
            "beginner": "You tried to delete an item from the dictionary, but the item was already gone or never existed.",
            "analogy": "It's like trying to cross a name off a guest list, but the person wasn't on the list to begin with.",
            "solution": "Use the `.pop(key, None)` method, which removes the key if it exists but does nothing (returns None) if the key is missing.",
            "prevention": "Prefer using `.pop(key, default)` over `del dict[key]` when removing keys that might not exist.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Stack Overflow discussion",
            "language_version": "Python 3.x",
            "tags": ["dictionary", "key-error", "delete"]
        }
    }
    samples.append(sample)

# Variation 3: Iterating over keys but expecting items
for i in range(25):
    dname = dict_names[(i+4) % len(dict_names)]
    func = funcs[(i+4) % len(funcs)]
    code = f"def print_{dname}({dname}):\n    for key, value in {dname}:\n        print(value)\n\nprint_{dname}({{'x': 10, 'y': 20}})"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    print_{dname}({{'x': 10, 'y': 20}})\n  File \"main.py\", line 2, in print_{dname}\n    for key, value in {dname}:\nValueError: not enough values to unpack (expected 2, got 1)"
    # Wait, this is a ValueError. Let's make it a KeyError.
    code = f"def get_nested_{dname}({dname}, key1, key2):\n    return {dname}[key1][key2]\n\nget_nested_{dname}({{'groupA': {{}}}}, 'groupA', 'settings')"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    get_nested_{dname}({{'groupA': {{}}}}, 'groupA', 'settings')\n  File \"main.py\", line 2, in get_nested_{dname}\n    return {dname}[key1][key2]\nKeyError: 'settings'"
    opt_code = f"def get_nested_{dname}({dname}, key1, key2):\n    return {dname}.get(key1, {{}}).get(key2)\n\nget_nested_{dname}({{'groupA': {{}}}}, 'groupA', 'settings')"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the KeyError caused by accessing a missing key in a nested dictionary.",
        "input": {
            "title": "Nested dictionary KeyError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Chaining bracket notation `dict[key1][key2]` will raise a KeyError on whichever level the key is missing. If `key1` exists but its value doesn't contain `key2`, it fails on the second access.",
            "beginner": "You tried to look inside a folder, and then inside another folder, but the second folder wasn't there.",
            "analogy": "It's like opening a Russian doll expecting another one inside, but finding it empty.",
            "solution": "Chain `.get()` methods, providing an empty dictionary as the default for intermediate steps: `dict.get(key1, {}).get(key2)`.",
            "prevention": "Be cautious with deeply nested dictionaries. Consider using `collections.defaultdict` or chaining `.get()` with safe defaults.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Python Official Documentation",
            "language_version": "Python 3.x",
            "tags": ["dictionary", "key-error", "nested-dictionary"]
        }
    }
    samples.append(sample)

# Variation 4: KeyError in string formatting mapping
for i in range(25):
    dname = dict_names[(i+6) % len(dict_names)]
    func = funcs[(i+6) % len(funcs)]
    code = f"def format_message({dname}):\n    message = \"User {{name}} has {{points}} points.\".format(**{dname})\n    return message\n\nformat_message({{'name': 'Bob'}})"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    format_message({{'name': 'Bob'}})\n  File \"main.py\", line 2, in format_message\n    message = \"User {{name}} has {{points}} points.\".format(**{dname})\nKeyError: 'points'"
    opt_code = f"def format_message({dname}):\n    message = \"User {{name}} has {{points}} points.\".format(name={dname}.get('name', 'Unknown'), points={dname}.get('points', 0))\n    return message\n\nformat_message({{'name': 'Bob'}})"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the KeyError during dictionary unpacking in string formatting.",
        "input": {
            "title": "String formatting KeyError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "When unpacking a dictionary into `.format(**dict)`, all named placeholders in the string must have corresponding keys in the dictionary. Missing keys cause a KeyError.",
            "beginner": "The text template required certain pieces of information (like 'points'), but the dictionary provided didn't have them.",
            "analogy": "It's like a fill-in-the-blanks form asking for your middle name, but you didn't provide one, so the system gets confused.",
            "solution": "Pass arguments explicitly using `.get()` to provide fallback values, or ensure the dictionary is fully populated before formatting.",
            "prevention": "When using `**kwargs` unpacking for string formatting, always validate that the dictionary contains all required keys.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by Python Official Documentation",
            "language_version": "Python 3.x",
            "tags": ["dictionary", "key-error", "string-formatting"]
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
