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

ensure_dir("../datasets/educational_explanations/python")
output_file = "../datasets/educational_explanations/python/concept_explanations.json"

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
        candidate = f"PY_EDUCATIONAL_{i:06d}"
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
        # yield vs return
        code = f"def generate_{vname}():\n    for i in range(3):\n        # yield pauses the function and returns a value\n        yield i\n\nfor val in generate_{vname}():\n    print(val)"
        error = f"Educational: Understanding the difference between `yield` and `return` in Python functions."
        opt_code = f"def generate_{vname}():\n    for i in range(3):\n        yield i\n\nfor val in generate_{vname}():\n    print(val)"
        technical = f"While `return` terminates a function entirely and passes back a single value (or tuple), `yield` turns a function into a Generator. When `yield` is called, the function's state is paused and saved. The next time the generator is iterated over, it resumes execution immediately after the `yield` statement."
        beginner = f"Think of `return` as saying 'I am completely finished, here is the final result.' Think of `yield` as saying 'Here is one piece of the puzzle, I will pause here until you ask me for the next piece.'"
        title = "Generators: yield vs return"
        tags = ["educational", "generators", "yield", "return"]
    
    elif variation == 1:
        # *args and **kwargs
        code = f"def {func}(*args, **kwargs):\n    for arg in args:\n        print(\"Positional:\", arg)\n    for key, value in kwargs.items():\n        print(f\"Keyword: {{key}}={{value}}\")\n\n{func}(1, 2, 3, name=\"Alice\", age=30)"
        error = f"Educational: Understanding how to accept a variable number of positional and keyword arguments using `*args` and `**kwargs`."
        opt_code = f"def {func}(*args, **kwargs):\n    for arg in args:\n        print(\"Positional:\", arg)\n    for key, value in kwargs.items():\n        print(f\"Keyword: {{key}}={{value}}\")\n\n{func}(1, 2, 3, name=\"Alice\", age=30)"
        technical = f"The `*` unpacking operator allows a function to accept an arbitrary number of positional arguments as a tuple (`args`). The `**` operator allows accepting an arbitrary number of keyword arguments as a dictionary (`kwargs`). This enables highly flexible function signatures."
        beginner = f"`*args` is just a way to say 'give me any number of normal ingredients, and I'll put them in a list'. `**kwargs` means 'give me any number of named ingredients (like sugar=2), and I'll put them in a dictionary'."
        title = "Variable Arguments: *args and **kwargs"
        tags = ["educational", "args", "kwargs", "functions"]
    
    elif variation == 2:
        # Decorators
        code = f"def my_decorator(func):\n    def wrapper():\n        print(\"Before the function runs\")\n        func()\n        print(\"After the function runs\")\n    return wrapper\n\n@my_decorator\ndef {func}():\n    print(\"Inside the function\")\n\n{func}()"
        error = f"Educational: Understanding how Decorators wrap functions to extend their behavior."
        opt_code = f"def my_decorator(func):\n    def wrapper():\n        print(\"Before the function runs\")\n        func()\n        print(\"After the function runs\")\n    return wrapper\n\n@my_decorator\ndef {func}():\n    print(\"Inside the function\")\n\n{func}()"
        technical = f"A decorator is a function that takes another function as an argument, extends its behavior without explicitly modifying it, and returns a new function (the wrapper). The `@decorator_name` syntax is syntactic sugar for `{func} = my_decorator({func})`."
        beginner = f"A decorator is like wrapping a present. The original function is the gift inside, and the decorator adds the wrapping paper and a bow around it before and after you open it."
        title = "Function Decorators"
        tags = ["educational", "decorators", "wrappers"]

    elif variation == 3:
        # Context Managers (with statement)
        code = f"def {func}():\n    # The 'with' statement handles setup and teardown automatically\n    with open('data.txt', 'w') as file:\n        file.write(\"Hello\")\n    # file is automatically closed here"
        error = f"Educational: Understanding the `with` statement and Context Managers."
        opt_code = f"def {func}():\n    with open('data.txt', 'w') as file:\n        file.write(\"Hello\")"
        technical = f"The `with` statement simplifies exception handling by encapsulating common preparation and cleanup tasks in so-called context managers. The object evaluated must implement `__enter__()` (setup) and `__exit__()` (teardown, like closing a file or releasing a lock)."
        beginner = f"Using `with` is like borrowing a library book. You don't have to remember to return it when you're done; Python automatically handles the 'returning' (closing the file) for you as soon as you finish the indented block."
        title = "Context Managers (The 'with' statement)"
        tags = ["educational", "context-managers", "with-statement", "files"]

    else:
        # __init__ vs __new__
        code = f"class {func.capitalize()}Obj:\n    def __new__(cls, *args, **kwargs):\n        # __new__ actually creates and returns the memory instance\n        instance = super().__new__(cls)\n        return instance\n\n    def __init__(self):\n        # __init__ just initializes the already-created instance\n        self.{lvar} = 0"
        error = f"Educational: Understanding the object instantiation lifecycle (`__new__` vs `__init__`)."
        opt_code = f"class {func.capitalize()}Obj:\n    def __new__(cls, *args, **kwargs):\n        instance = super().__new__(cls)\n        return instance\n\n    def __init__(self):\n        self.{lvar} = 0"
        technical = f"`__new__` is a static class method called first to allocate memory and construct a new instance of the class. It returns that instance. `__init__` is an instance method called immediately after to initialize the newly created object's state. It returns None."
        beginner = f"`__new__` is the construction worker that builds the physical house. `__init__` is the interior designer that moves the furniture in after the house is built."
        title = "Object Creation: __new__ vs __init__"
        tags = ["educational", "oop", "instantiation", "dunder-methods"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "educational",
        "instruction": f"Explain the Python concept: {title}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "Analogies help ground abstract programming concepts in real-world logic.",
            "solution": "N/A - This is an educational explanation, not a bug fix.",
            "prevention": "Understanding these core language paradigms prevents anti-patterns and enables advanced Pythonic design.",
            "optimized_code": opt_code,
            "complexity": {"before": "N/A", "after": "N/A"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated Python Educational Explanations",
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
