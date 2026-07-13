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
output_file = "../datasets/runtime_errors/python/name_error.json"

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

funcs = ["calculate", "process", "update", "evaluate", "aggregate", "filter_data", "run", "compute", "execute", "analyze"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]
local_vars = ["total", "count", "average", "sum_val", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Typo in variable name
        typo_lvar = lvar[:-1] + lvar[-1] * 2 if len(lvar) > 0 else "x"
        code = f"def {func}({vname}):\n    {lvar} = 0\n    for item in {vname}:\n        {typo_lvar} += item\n    return {lvar}\n\n{func}([1, 2, 3])"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 7, in <module>\n    {func}([1, 2, 3])\n  File \"main.py\", line 4, in {func}\n    {typo_lvar} += item\nNameError: name '{typo_lvar}' is not defined"
        opt_code = f"def {func}({vname}):\n    {lvar} = 0\n    for item in {vname}:\n        {lvar} += item\n    return {lvar}\n\n{func}([1, 2, 3])"
        technical = f"A NameError occurs when Python encounters a variable name ({typo_lvar}) that has not been defined in the current or global scope. This is usually caused by a typo."
        beginner = f"You tried to use a variable called '{typo_lvar}', but you haven't created it yet. It looks like a typo for '{lvar}'."
        title = "Misspelled Variable Name"
        tags = ["name-error", "typo", "variables"]
    
    elif variation == 1:
        # Missing import
        modules = ["math", "os", "sys", "json", "random"]
        mod = modules[(i // 50) % len(modules)]
        attrs = {"math": "pi", "os": "name", "sys": "version", "json": "loads", "random": "randint"}
        attr = attrs[mod]
        code = f"def {func}():\n    return {mod}.{attr}\n\n{func}()"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}()\n  File \"main.py\", line 2, in {func}\n    return {mod}.{attr}\nNameError: name '{mod}' is not defined"
        opt_code = f"import {mod}\n\ndef {func}():\n    return {mod}.{attr}\n\n{func}()"
        technical = f"The module '{mod}' is referenced before it has been imported. Python requires modules to be explicitly imported into the current namespace before they can be used."
        beginner = f"You are trying to use '{mod}', but you forgot to import it at the top of your file."
        title = "Missing Import Statement"
        tags = ["name-error", "import", "modules"]
    
    elif variation == 2:
        # Out of scope variable (defined in conditional that wasn't executed)
        code = f"def {func}(condition):\n    if condition:\n        {lvar} = 10\n    print({lvar})\n\n{func}(False)"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    {func}(False)\n  File \"main.py\", line 4, in {func}\n    print({lvar})\nNameError: name '{lvar}' is not defined"
        opt_code = f"def {func}(condition):\n    {lvar} = 0\n    if condition:\n        {lvar} = 10\n    print({lvar})\n\n{func}(False)"
        technical = f"The variable '{lvar}' is conditionally defined. Because the condition was False, the assignment never executed, and the variable does not exist when referenced."
        beginner = f"You only created '{lvar}' if the condition was true. But when it was false, Python skipped creating it, and then got confused when you tried to print it."
        title = "Conditionally Defined Variable"
        tags = ["name-error", "scope", "conditional"]

    elif variation == 3:
        # Calling function before definition (in script scope)
        code = f"result = helper_func()\n\ndef helper_func():\n    return 42"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    result = helper_func()\nNameError: name 'helper_func' is not defined"
        opt_code = f"def helper_func():\n    return 42\n\nresult = helper_func()"
        technical = f"Python executes scripts top-to-bottom. The function 'helper_func' is called before the interpreter has reached its 'def' statement, so it doesn't exist in the namespace yet."
        beginner = f"You tried to use a function before you taught Python what that function does. Move the function definition to the top."
        title = "Calling Function Before Definition"
        tags = ["name-error", "functions", "execution-order"]

    else:
        # Typo in standard function
        std_funcs = ["print", "len", "range", "type", "str"]
        std_f = std_funcs[(i // 100) % len(std_funcs)]
        typo_f = std_f + std_f[-1]
        code = f"def {func}({vname}):\n    {typo_f}({vname})\n\n{func}([1, 2, 3])"
        error = f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {func}([1, 2, 3])\n  File \"main.py\", line 2, in {func}\n    {typo_f}({vname})\nNameError: name '{typo_f}' is not defined"
        opt_code = f"def {func}({vname}):\n    {std_f}({vname})\n\n{func}([1, 2, 3])"
        technical = f"Built-in functions like '{std_f}' must be spelled correctly. '{typo_f}' is interpreted as an undefined variable or function."
        beginner = f"You made a typo. It looks like you meant to write '{std_f}', but you wrote '{typo_f}'."
        title = "Built-in Function Typo"
        tags = ["name-error", "built-in", "typo"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "runtime_error",
        "instruction": f"Fix the NameError caused by the undefined reference to '{typo_lvar if variation==0 else (mod if variation==1 else (lvar if variation==2 else ('helper_func' if variation==3 else typo_f)))}'.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like asking someone to fetch a book by a title they've never heard of. They don't know what you're talking about.",
            "solution": "Ensure the variable or function is defined or imported before it is used, and check for spelling mistakes.",
            "prevention": "Use an IDE or linter (like Flake8 or PyLint) to catch undefined variables before running the code.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated NameError Variations",
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
