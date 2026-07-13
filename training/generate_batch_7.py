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

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "append_item", "filter_data", "run", "compute", "execute"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "list_obj", "collection"]

# Variation 1: Mutable Default Argument
for i in range(25):
    func = funcs[i % len(funcs)]
    vname = var_names[i % len(var_names)]
    code = f"def {func}(item, {vname}=[]):\n    {vname}.append(item)\n    return {vname}\n\n# Call 1\nr1 = {func}(1)\n# Call 2\nr2 = {func}(2)\n# r2 is [1, 2] instead of [2]"
    error = f"Logical Bug: State is persisted across multiple calls because `{vname}` uses a mutable default argument."
    opt_code = f"def {func}(item, {vname}=None):\n    if {vname} is None:\n        {vname} = []\n    {vname}.append(item)\n    return {vname}\n\n# Call 1\nr1 = {func}(1) # [1]\n# Call 2\nr2 = {func}(2) # [2]"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "logical_bug",
        "instruction": "Fix the logical bug caused by using a mutable default argument.",
        "input": {
            "title": "Mutable Default Argument",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Default arguments are evaluated only once at function definition time. When a mutable object like a list is used, the same object is shared across all function calls that omit that argument, leading to unintended state accumulation.",
            "beginner": "You used an empty list `[]` as a default. Python creates this list once when the program starts. So every time you call the function without providing a new list, it keeps adding to that exact same initial list.",
            "analogy": "It's like having a shared shopping cart at the front of the store instead of taking a new one. Everyone who doesn't bring their own cart ends up adding their groceries to the same shared cart.",
            "solution": "Use `None` as the default argument, and initialize the mutable object inside the function body using an `if` statement.",
            "prevention": "Never use mutable objects (like lists, dictionaries, or sets) as default function arguments. Always use `None`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by common Python gotchas",
            "language_version": "Python 3.x",
            "tags": ["logical-bug", "mutable-default", "functions"]
        }
    }
    samples.append(sample)

# Variation 2: Late Binding Closures (Loop Variable Leak)
for i in range(25):
    code = f"def create_multipliers():\n    multipliers = []\n    for i in range(5):\n        multipliers.append(lambda x: x * i)\n    return multipliers\n\nfuncs = create_multipliers()\n# funcs[0](2) returns 8 instead of 0\n# funcs[1](2) returns 8 instead of 2"
    error = f"Logical Bug: All lambda functions return the same result because they bind to the final value of the loop variable `i`."
    opt_code = f"def create_multipliers():\n    multipliers = []\n    for i in range(5):\n        multipliers.append(lambda x, i=i: x * i)\n    return multipliers\n\nfuncs = create_multipliers()\n# funcs[0](2) now returns 0"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "logical_bug",
        "instruction": "Fix the logical bug related to late binding closures in loops.",
        "input": {
            "title": "Late Binding Closures",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Python closures exhibit late binding. Variables used in a closure (like a lambda inside a loop) are looked up at the time the inner function is called, not when it is defined. Therefore, all lambdas reference the final state of the loop variable `i`.",
            "beginner": "The functions you created in the loop don't remember the value of `i` right then; they look at `i` later when they actually run. By that time, the loop has finished and `i` is stuck at its last value.",
            "analogy": "It's like telling 5 people 'take a picture of whatever is on my TV right now' but handing them cameras with delayed timers. By the time the cameras click, the TV is showing the final scene for all of them.",
            "solution": "Bind the loop variable locally by passing it as a default argument to the lambda: `lambda x, i=i: x * i`.",
            "prevention": "When creating closures inside loops, capture loop variables immediately by setting them as default keyword arguments.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "hard",
            "source": "Inspired by common Python gotchas",
            "language_version": "Python 3.x",
            "tags": ["logical-bug", "closures", "lambda", "late-binding"]
        }
    }
    samples.append(sample)

# Variation 3: Incorrect range exclusion in checking overlap
for i in range(25):
    code = f"def is_overlapping(start1, end1, start2, end2):\n    # Bug: misses the case where one encompasses the other perfectly or overlaps partially but starts before\n    return (start1 >= start2 and start1 <= end2) or (end1 >= start2 and end1 <= end2)\n\n# is_overlapping(1, 10, 2, 5) returns False, which is incorrect"
    error = f"Logical Bug: Incorrect boolean logic fails to detect all types of overlapping ranges."
    opt_code = f"def is_overlapping(start1, end1, start2, end2):\n    # Ranges overlap if the first starts before the second ends AND the first ends after the second starts\n    return start1 <= end2 and end1 >= start2"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "logical_bug",
        "instruction": "Fix the logical bug in the overlapping interval detection logic.",
        "input": {
            "title": "Interval Overlap Logic",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The original boolean logic only checks if the endpoints of interval 1 fall within interval 2. It fails to detect when interval 1 completely engulfs interval 2 (e.g., start1 < start2 and end1 > end2).",
            "beginner": "Your code asks 'does the start or end of the first line fall inside the second line?'. But it forgets to check if the first line is so big that it completely swallows the second line without its ends touching the inside.",
            "analogy": "It's like checking if a car is in the garage by seeing if the front bumper or rear bumper is directly under the garage roof. If a giant truck is parked there, both bumpers might be outside, but the truck is definitely inside.",
            "solution": "Simplify the logic by checking the opposite of non-overlapping: two intervals overlap if `start1 <= end2` AND `end1 >= start2`.",
            "prevention": "For interval overlap problems, it is usually simpler to define the conditions for *not* overlapping and invert them, or use the standard overlap formula.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by LeetCode / competitive programming",
            "language_version": "Python 3.x",
            "tags": ["logical-bug", "boolean-logic", "intervals"]
        }
    }
    samples.append(sample)

# Variation 4: Floating Point Precision Equality
for i in range(25):
    code = f"def check_price(price):\n    tax = 0.1\n    total = price + tax\n    if total == 0.3:\n        return True\n    return False\n\n# check_price(0.2) returns False due to float precision (0.2 + 0.1 = 0.30000000000000004)"
    error = f"Logical Bug: Direct equality comparison `==` fails for floating-point numbers due to representation precision."
    opt_code = f"import math\n\ndef check_price(price):\n    tax = 0.1\n    total = price + tax\n    if math.isclose(total, 0.3):\n        return True\n    return False"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "logical_bug",
        "instruction": "Fix the logical bug where floating-point numbers are incorrectly compared for exact equality.",
        "input": {
            "title": "Floating Point Equality",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Floating-point numbers are represented in base-2 fractions, meaning some base-10 decimals cannot be represented perfectly. This introduces tiny precision errors, making exact equality `==` comparisons highly prone to failure.",
            "beginner": "Computers struggle to store decimals exactly. For the computer, 0.2 + 0.1 is actually 0.30000000000000004, so it doesn't exactly equal 0.3.",
            "analogy": "It's like trying to measure exactly 1/3 of a cup of water using a measuring cup that only has 1/4 markings. You'll get very close, but never precisely there.",
            "solution": "Use `math.isclose()` to compare floating-point numbers, or check if the absolute difference between them is smaller than a tiny tolerance (epsilon).",
            "prevention": "Never use `==` or `!=` to compare floating-point values. If exact precision is required (like in finance), use the `decimal` module.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by standard numerical computing issues",
            "language_version": "Python 3.x",
            "tags": ["logical-bug", "floats", "precision"]
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
