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

ensure_dir("../datasets/compiler_errors/cpp")
output_file = "../datasets/compiler_errors/cpp/syntax_and_types.json"

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
        candidate = f"CP_COMPILER_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "filterData", "run", "compute", "execute", "analyze"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]
local_vars = ["total", "count", "average", "sumVal", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Missing Semicolon
        code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 10\n    std::cout << {lvar} << std::endl;\n    return 0;\n}}"
        error = f"main.cpp: In function 'int {func}()':\nmain.cpp:5:5: error: expected ',' or ';' before 'std'"
        opt_code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 10;\n    std::cout << {lvar} << std::endl;\n    return 0;\n}}"
        technical = f"C++ statements must be terminated with a semicolon. The compiler expects a semicolon after the assignment statement `int {lvar} = 10` but encounters `std::cout` on the next line."
        beginner = f"You forgot a semicolon `;` at the end of the line where you created '{lvar}'. C++ needs semicolons to know when a sentence ends."
        title = "Missing Semicolon"
        tags = ["compiler-error", "syntax", "missing-semicolon"]
    
    elif variation == 1:
        # Undeclared Identifier
        typo_lvar = lvar[:-1] + lvar[-1] * 2 if len(lvar) > 0 else "x"
        code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 10;\n    {typo_lvar} = 20;\n    return 0;\n}}"
        error = f"main.cpp: In function 'int {func}()':\nmain.cpp:5:5: error: '{typo_lvar}' was not declared in this scope"
        opt_code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 10;\n    {lvar} = 20;\n    return 0;\n}}"
        technical = f"The compiler encountered an identifier '{typo_lvar}' that has not been declared with a type in the current scope. C++ is statically typed and requires all variables to be declared before use."
        beginner = f"You tried to use a variable called '{typo_lvar}', but you never told C++ what '{typo_lvar}' is. It looks like a typo for '{lvar}'."
        title = "Undeclared Identifier"
        tags = ["compiler-error", "undeclared-identifier", "typo"]
    
    elif variation == 2:
        # Missing #include for standard library
        std_types = {"string": "std::string", "vector": "std::vector<int>", "map": "std::map<int, int>"}
        missing_inc = list(std_types.keys())[(i // 50) % len(std_types)]
        usage_type = std_types[missing_inc]
        code = f"#include <iostream>\n\nint {func}() {{\n    {usage_type} {vname};\n    return 0;\n}}"
        error = f"main.cpp: In function 'int {func}()':\nmain.cpp:4:5: error: '{usage_type}' was not declared in this scope"
        opt_code = f"#include <iostream>\n#include <{missing_inc}>\n\nint {func}() {{\n    {usage_type} {vname};\n    return 0;\n}}"
        technical = f"The identifier '{usage_type}' is part of the C++ standard library, which requires specific headers to be included. Without `#include <{missing_inc}>`, the compiler doesn't know what '{usage_type}' is."
        beginner = f"You are trying to use '{missing_inc}', but you forgot to tell C++ to load the '{missing_inc}' library at the top of your file."
        title = f"Missing #include for {missing_inc}"
        tags = ["compiler-error", "missing-include", "standard-library"]

    elif variation == 3:
        # Type Mismatch (Invalid Conversion)
        code = f"#include <iostream>\n#include <string>\n\nint {func}() {{\n    std::string text = \"100\";\n    int {lvar} = text;\n    return 0;\n}}"
        error = f"main.cpp: In function 'int {func}()':\nmain.cpp:6:18: error: cannot convert 'std::string' {{aka 'std::basic_string<char>'}} to 'int' in initialization"
        opt_code = f"#include <iostream>\n#include <string>\n\nint {func}() {{\n    std::string text = \"100\";\n    int {lvar} = std::stoi(text);\n    return 0;\n}}"
        technical = f"C++ is strongly typed and does not implicitly convert `std::string` objects to primitive integers. You must explicitly invoke a conversion function like `std::stoi()`."
        beginner = f"You tried to put text inside a box meant for numbers. C++ doesn't automatically turn text like \"100\" into a math number. You have to explicitly parse it."
        title = "Invalid Type Conversion"
        tags = ["compiler-error", "type-mismatch", "conversion"]

    else:
        # Missing Return Statement
        code = f"#include <iostream>\n\nint {func}(int {lvar}) {{\n    if ({lvar} > 0) {{\n        return 1;\n    }}\n    // Missing return for when {lvar} <= 0\n}}"
        error = f"main.cpp: In function 'int {func}(int)':\nmain.cpp:7:1: warning: control reaches end of non-void function [-Wreturn-type]"
        opt_code = f"#include <iostream>\n\nint {func}(int {lvar}) {{\n    if ({lvar} > 0) {{\n        return 1;\n    }}\n    return 0;\n}}"
        technical = f"The function '{func}' promises to return an `int`. If the condition `{lvar} > 0` evaluates to false, control flow reaches the end of the function without returning a value, which is undefined behavior in C++."
        beginner = f"Your function promised to give back a number, but if the condition isn't met, it doesn't give anything back. C++ warns you that you forgot to return something at the very end."
        title = "Missing Return Statement (Warning/Error)"
        tags = ["compiler-error", "missing-return", "control-flow"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "compiler_error",
        "instruction": f"Fix the C++ compiler error: {error.split(': error: ')[-1] if 'error: ' in error else 'control reaches end of non-void function'}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like writing a letter and stopping in the middle of a",
            "solution": "Apply the appropriate syntax fix, import, or type conversion as expected by the C++ language rules.",
            "prevention": "Use modern IDEs which flag syntax errors and missing includes in real-time as you type.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated C++ Compiler Error Variations",
            "language_version": "C++11",
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
