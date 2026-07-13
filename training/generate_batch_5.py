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
output_file = "../datasets/runtime_errors/python/value_error.json"

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

var_names = ["user_input", "age_str", "count_value", "price_tag", "quantity_input", "score_str", "amount_val", "index_str", "limit_input", "data_point"]
funcs = ["parse_integer", "convert_to_number", "get_count", "process_age", "calculate_total", "validate_input", "extract_value", "read_score", "format_data", "convert_price"]

# Variation 1: Invalid int() conversion with letters
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"def {func}({vname}):\n    numeric_value = int({vname})\n    return numeric_value * 2\n\n{func}('10abc')"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}('10abc')\n  File \"main.py\", line 2, in {func}\n    numeric_value = int({vname})\nValueError: invalid literal for int() with base 10: '10abc'"
    opt_code = f"def {func}({vname}):\n    try:\n        numeric_value = int({vname})\n        return numeric_value * 2\n    except ValueError:\n        return 0\n\n{func}('10abc')"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the ValueError caused by attempting to convert a non-numeric string to an integer.",
        "input": {
            "title": "Invalid literal for int()",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `int()` function expects a string containing only digits (and optionally a leading sign). Passing a string with alphabetical characters raises a ValueError because it cannot be parsed as a base-10 integer.",
            "beginner": "You tried to convert text into a whole number, but the text had letters in it. The computer doesn't know what number '10abc' is.",
            "analogy": "It's like trying to translate a sentence from Spanish to English, but some of the words are just random scribbles.",
            "solution": "Wrap the conversion in a `try...except ValueError` block to handle invalid inputs gracefully, or validate the string with `.isdigit()` before converting.",
            "prevention": "Always sanitize and validate user input before attempting type conversions.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["value-error", "type-conversion", "string-parsing"]
        }
    }
    samples.append(sample)

# Variation 2: Unpacking too many/few values
for i in range(25):
    code = f"def process_coordinates(coord_string):\n    x, y, z = coord_string.split(',')\n    return int(x) + int(y) + int(z)\n\nprocess_coordinates('10,20')"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    process_coordinates('10,20')\n  File \"main.py\", line 2, in process_coordinates\n    x, y, z = coord_string.split(',')\nValueError: not enough values to unpack (expected 3, got 2)"
    opt_code = f"def process_coordinates(coord_string):\n    parts = coord_string.split(',')\n    if len(parts) == 3:\n        return int(parts[0]) + int(parts[1]) + int(parts[2])\n    return 0\n\nprocess_coordinates('10,20')"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the ValueError caused by unpacking an incorrect number of elements.",
        "input": {
            "title": "Not enough values to unpack",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "When unpacking an iterable into multiple variables, the number of elements in the iterable must exactly match the number of variables on the left side of the assignment.",
            "beginner": "You tried to put the split pieces of text into 3 separate boxes (x, y, and z), but the text only split into 2 pieces.",
            "analogy": "It's like buying a 3-piece suit but only receiving the jacket and pants; there's nothing to assign to the 'vest' variable.",
            "solution": "Check the length of the list before unpacking, or assign the result to a single list variable and access it by index.",
            "prevention": "Avoid hardcoded unpacking if the length of the resulting iterable is dynamic or based on untrusted input.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["value-error", "unpacking", "lists"]
        }
    }
    samples.append(sample)

# Variation 3: Passing negative number to math.sqrt
for i in range(25):
    code = f"import math\n\ndef calculate_hypotenuse(a, b):\n    c_squared = (a**2) - (b**2) # Logical mistake leading to negative\n    return math.sqrt(c_squared)\n\ncalculate_hypotenuse(3, 5)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    calculate_hypotenuse(3, 5)\n  File \"main.py\", line 4, in calculate_hypotenuse\n    return math.sqrt(c_squared)\nValueError: math domain error"
    opt_code = f"import math\n\ndef calculate_hypotenuse(a, b):\n    c_squared = (a**2) + (b**2)\n    return math.sqrt(c_squared)\n\ncalculate_hypotenuse(3, 5)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the ValueError (math domain error) caused by passing a negative number to a square root function.",
        "input": {
            "title": "Math domain error",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `math.sqrt()` function expects a non-negative number. Passing a negative number falls outside the mathematical domain of real numbers, raising a ValueError.",
            "beginner": "You tried to find the square root of a negative number, which isn't possible with standard numbers.",
            "analogy": "It's like trying to find a real physical box that has a negative volume.",
            "solution": "Ensure the logic producing the number is correct (e.g., adding instead of subtracting), or use `cmath.sqrt()` if you intentionally want to work with complex/imaginary numbers.",
            "prevention": "Use `abs()` or validate that variables are `>= 0` before passing them to domain-restricted math functions.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by standard library documentation",
            "language_version": "Python 3.x",
            "tags": ["value-error", "math", "domain-error"]
        }
    }
    samples.append(sample)

# Variation 4: .remove() on item not in list
for i in range(25):
    code = f"def filter_list(items, to_remove):\n    items.remove(to_remove)\n    return items\n\nfilter_list([1, 2, 3], 5)"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    filter_list([1, 2, 3], 5)\n  File \"main.py\", line 2, in filter_list\n    items.remove(to_remove)\nValueError: list.remove(x): x not in list"
    opt_code = f"def filter_list(items, to_remove):\n    if to_remove in items:\n        items.remove(to_remove)\n    return items\n\nfilter_list([1, 2, 3], 5)"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the ValueError caused by trying to remove an item that is not in the list.",
        "input": {
            "title": "list.remove(x): x not in list",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `list.remove(value)` method searches for the first occurrence of the specified value and removes it. If the value is not present in the list, it raises a ValueError.",
            "beginner": "You asked Python to take the number 5 out of a list, but the list didn't have a 5 in it.",
            "analogy": "It's like asking someone to take the pepperonis off a cheese pizza.",
            "solution": "Check if the item exists in the list using the `in` operator before trying to remove it, or wrap the remove call in a `try...except` block.",
            "prevention": "Always verify existence with `if item in lst:` before calling `.remove(item)`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python list errors",
            "language_version": "Python 3.x",
            "tags": ["value-error", "list", "remove"]
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
