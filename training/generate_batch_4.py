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
output_file = "../datasets/runtime_errors/python/attribute_error.json"

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

var_names = ["user", "data_processor", "handler", "manager", "controller", "service", "app", "parser", "generator", "loader"]
funcs = ["process", "run", "execute", "initialize", "start", "stop", "load", "save", "fetch", "update"]

# Variation 1: 'NoneType' object has no attribute
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"class {vname.capitalize()}:\n    def {func}(self):\n        pass\n\ndef get_{vname}():\n    return None\n\nobj = get_{vname}()\nobj.{func}()"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 8, in <module>\n    obj.{func}()\nAttributeError: 'NoneType' object has no attribute '{func}'"
    opt_code = f"class {vname.capitalize()}:\n    def {func}(self):\n        pass\n\ndef get_{vname}():\n    return None\n\nobj = get_{vname}()\nif obj is not None:\n    obj.{func}()"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the AttributeError caused by calling a method on a NoneType object.",
        "input": {
            "title": "NoneType AttributeError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `AttributeError` occurs because the variable `obj` is assigned the value `None`, which is of type `NoneType`. It does not have the expected methods or properties.",
            "beginner": "You tried to tell an object to do something, but the object was actually empty (`None`), so it didn't know how to do it.",
            "analogy": "It's like trying to turn the steering wheel of a car that isn't actually there.",
            "solution": "Check if the object is `None` before attempting to access its attributes or methods.",
            "prevention": "Always validate return values from functions that can potentially return `None`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["attribute-error", "nonetype", "objects"]
        }
    }
    samples.append(sample)

# Variation 2: Misspelled attribute name
for i in range(25):
    vname = var_names[(i+2) % len(var_names)]
    func = funcs[(i+2) % len(funcs)]
    misspelled = func + "s"
    code = f"class {vname.capitalize()}:\n    def {func}(self):\n        return True\n\nobj = {vname.capitalize()}()\nobj.{misspelled}()"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    obj.{misspelled}()\nAttributeError: '{vname.capitalize()}' object has no attribute '{misspelled}'"
    opt_code = f"class {vname.capitalize()}:\n    def {func}(self):\n        return True\n\nobj = {vname.capitalize()}()\nobj.{func}()"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the AttributeError caused by a misspelled method name.",
        "input": {
            "title": "Misspelled Method AttributeError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "An `AttributeError` is raised when an object instance does not possess the specific attribute or method name requested. In this case, the method name is misspelled.",
            "beginner": "You asked the object to perform an action using the wrong name or a typo.",
            "analogy": "It's like asking your dog to 'feetch' instead of 'fetch'. The dog doesn't understand the misspelled command.",
            "solution": "Correct the spelling of the method to match its definition in the class.",
            "prevention": "Use IDE autocomplete features to avoid typographical errors when accessing object properties and methods.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["attribute-error", "typo", "objects"]
        }
    }
    samples.append(sample)

# Variation 3: Attempting to append to a string instead of list
for i in range(25):
    vname = var_names[(i+4) % len(var_names)]
    code = f"def add_to_collection(item):\n    {vname}_collection = \"\"\n    {vname}_collection.append(item)\n    return {vname}_collection\n\nadd_to_collection('test')"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    add_to_collection('test')\n  File \"main.py\", line 3, in add_to_collection\n    {vname}_collection.append(item)\nAttributeError: 'str' object has no attribute 'append'"
    opt_code = f"def add_to_collection(item):\n    {vname}_collection = []\n    {vname}_collection.append(item)\n    return {vname}_collection\n\nadd_to_collection('test')"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the AttributeError caused by using a list method on a string.",
        "input": {
            "title": "String append AttributeError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Strings in Python are immutable and do not have an `append` method, which is specific to mutable sequences like lists.",
            "beginner": "You tried to use `.append()` on a piece of text (string). `.append()` is a tool only meant for lists.",
            "analogy": "It's like trying to pour water into a solid block of ice instead of a glass.",
            "solution": "Initialize the variable as an empty list `[]` instead of an empty string `\"\"`, or use string concatenation `+=` if a string was intended.",
            "prevention": "Ensure variables are initialized with the correct data types before invoking type-specific methods on them.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["attribute-error", "string", "list", "methods"]
        }
    }
    samples.append(sample)

# Variation 4: Module missing attribute
for i in range(25):
    code = f"import math\n\ndef get_pi():\n    return math.PI\n\nget_pi()"
    error = f"Traceback (most recent call last):\n  File \"main.py\", line 6, in <module>\n    get_pi()\n  File \"main.py\", line 4, in get_pi\n    return math.PI\nAttributeError: module 'math' has no attribute 'PI'"
    opt_code = f"import math\n\ndef get_pi():\n    return math.pi\n\nget_pi()"
    
    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": "Fix the AttributeError caused by incorrect module attribute casing.",
        "input": {
            "title": "Module AttributeError",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Python is case-sensitive. The `math` module contains the constant `pi`, not `PI`.",
            "beginner": "You asked the math toolkit for 'PI' (all caps), but it only knows 'pi' (lowercase).",
            "analogy": "It's like looking for 'JOHN' in a phonebook, but the person is listed as 'John'. Computers are extremely strict about capitalization.",
            "solution": "Use the correct case for the module attribute (`math.pi`).",
            "prevention": "Double-check official documentation or use an IDE with code completion when accessing module attributes.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by common Python runtime issues",
            "language_version": "Python 3.x",
            "tags": ["attribute-error", "module", "case-sensitivity"]
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
