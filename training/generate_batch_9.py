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

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "build_string", "filter_data", "run", "compute", "execute"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]

# Variation 1: String Concatenation in a Loop
for i in range(25):
    func = funcs[i % len(funcs)]
    vname = var_names[i % len(var_names)]
    code = f"def {func}({vname}):\n    result = \"\"\n    for word in {vname}:\n        result += word + \" \"\n    return result\n\n{func}([\"hello\", \"world\"])"
    error = f"Performance Issue: Using `+=` in a loop to build strings results in O(N^2) time complexity because strings are immutable."
    opt_code = f"def {func}({vname}):\n    return \" \".join({vname}) + \" \"\n\n{func}([\"hello\", \"world\"])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "optimization",
        "instruction": "Optimize the string concatenation inside the loop to run in linear time.",
        "input": {
            "title": "String Concatenation inside a loop",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "In Python, strings are immutable. Using `+=` inside a loop creates a new string object at each iteration and copies the contents of the old string. This leads to quadratic O(N^2) time complexity.",
            "beginner": "Every time you add a word to the sentence using `+=`, the computer has to rewrite the entire sentence from scratch. If you have a thousand words, it rewrites it a thousand times, which is very slow.",
            "analogy": "It's like writing a book by typing the first word on page 1. Then to add the second word, you get a new piece of paper, copy the first word, and add the second. Then a new piece of paper to copy the first two and add the third.",
            "solution": "Store all the string fragments in a list and use the `\"\".join(list)` method to concatenate them all at once at the end.",
            "prevention": "Always use `.join()` when combining a large or unknown number of strings in Python.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N^2)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Python Performance Anti-patterns",
            "language_version": "Python 3.x",
            "tags": ["optimization", "string-concatenation", "join"]
        }
    }
    samples.append(sample)

# Variation 2: Checking membership in a List instead of a Set
for i in range(25):
    func = funcs[(i+2) % len(funcs)]
    vname = var_names[(i+2) % len(var_names)]
    code = f"def check_{func}({vname}, targets):\n    found = []\n    for item in {vname}:\n        if item in targets:  # targets is a list\n            found.append(item)\n    return found\n\ncheck_{func}([1, 2, 3], [2, 4, 6])"
    error = f"Performance Issue: The `in` operator on a list takes O(N) time. Doing this in a loop results in O(N*M) time complexity."
    opt_code = f"def check_{func}({vname}, targets):\n    targets_set = set(targets)\n    found = [item for item in {vname} if item in targets_set]\n    return found\n\ncheck_{func}([1, 2, 3], [2, 4, 6])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "optimization",
        "instruction": "Optimize the membership checking operation to run in O(1) time.",
        "input": {
            "title": "O(N) List Membership check",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Checking membership `item in collection` takes O(N) time for a list because it requires a linear scan. Converting the collection to a `set` first allows for O(1) average-time complexity lookups using hash tables.",
            "beginner": "To check if a number is in a list, the computer looks at every single item one by one. If you use a 'set' instead, the computer uses a clever filing system to instantly know if the number is there.",
            "analogy": "It's like looking for a word in a book by reading every single page from start to finish (List), versus just looking it up in the alphabetical index at the back of the book (Set).",
            "solution": "Convert the `targets` list into a `set` before the loop, so that the `in` operation becomes extremely fast.",
            "prevention": "Whenever you need to check if items exist in a collection repeatedly (e.g., inside a loop), use a `set` or a `dict`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N * M)", "after": "O(N + M)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by LeetCode / competitive programming",
            "language_version": "Python 3.x",
            "tags": ["optimization", "set", "membership-check", "hash-table"]
        }
    }
    samples.append(sample)

# Variation 3: List Comprehension vs For Loop with Append
for i in range(25):
    func = funcs[(i+4) % len(funcs)]
    vname = var_names[(i+4) % len(var_names)]
    code = f"def transform_{func}({vname}):\n    squared = []\n    for x in {vname}:\n        squared.append(x * x)\n    return squared\n\ntransform_{func}([1, 2, 3, 4, 5])"
    error = f"Performance Issue: Using a standard for loop with `.append()` incurs unnecessary method call overhead in Python."
    opt_code = f"def transform_{func}({vname}):\n    return [x * x for x in {vname}]\n\ntransform_{func}([1, 2, 3, 4, 5])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "optimization",
        "instruction": "Optimize the loop by removing the `.append()` overhead using a list comprehension.",
        "input": {
            "title": "For loop with append vs List Comprehension",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "List comprehensions are evaluated in C at the core CPython level. A standard `for` loop with `.append()` must execute a function call dynamically for every element, adding significant bytecode interpretation overhead.",
            "beginner": "Instead of setting up an empty list and slowly adding items to it one by one using a loop, you can tell Python to build the whole list in one quick, optimized sentence.",
            "analogy": "It's like building a brick wall by walking to the pile, picking up one brick, walking back, and placing it, versus hiring a machine that lays all the bricks in a single pass.",
            "solution": "Replace the `for` loop and `.append()` with a list comprehension: `[x * x for x in iterable]`.",
            "prevention": "Whenever you are transforming or filtering a list into a new list, a list comprehension (or map/filter) is usually the fastest and most pythonic approach.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N) with high overhead", "after": "O(N) with low overhead"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by Pythonic idioms",
            "language_version": "Python 3.x",
            "tags": ["optimization", "list-comprehension", "overhead"]
        }
    }
    samples.append(sample)

# Variation 4: Multiple Count operations instead of Counter
for i in range(25):
    vname = var_names[(i+6) % len(var_names)]
    code = f"def get_frequencies({vname}):\n    freq = {{}}\n    for item in set({vname}):\n        freq[item] = {vname}.count(item)\n    return freq\n\nget_frequencies(['a', 'b', 'a', 'c', 'b', 'a'])"
    error = f"Performance Issue: The `.count()` method scans the entire list for every unique item, resulting in O(N^2) complexity for worst-case (all unique items)."
    opt_code = f"from collections import Counter\n\ndef get_frequencies({vname}):\n    return dict(Counter({vname}))\n\nget_frequencies(['a', 'b', 'a', 'c', 'b', 'a'])"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "optimization",
        "instruction": "Optimize the frequency counting to single-pass linear time.",
        "input": {
            "title": "O(N^2) List Count",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Calling `list.count()` inside a loop that iterates over the unique elements means the entire list is traversed $K$ times (where $K$ is the number of unique elements). This makes the time complexity O(N*K), which degrades to O(N^2) if all elements are unique.",
            "beginner": "To count how many times each word appears, your code looks at a word, then reads the entire book from start to finish to count it. Then it looks at the next word, and reads the entire book again.",
            "analogy": "It's like trying to count how many apples, bananas, and oranges you have by dumping the basket out, counting the apples, putting everything back, dumping it out again to count bananas, etc.",
            "solution": "Use `collections.Counter`, which traverses the list exactly once (O(N) time), tallying up all elements into a dictionary automatically.",
            "prevention": "Avoid using `list.count()` inside a loop. If you need frequencies of elements, `collections.Counter` is highly optimized in C and runs in single-pass O(N).",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N^2)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by standard library capabilities",
            "language_version": "Python 3.x",
            "tags": ["optimization", "collections.Counter", "frequency-counting"]
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
