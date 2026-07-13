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
output_file = "../datasets/compiler_errors/cpp/linker_and_syntax.json"

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
        # Undefined Reference (Linker Error)
        code = f"#include <iostream>\n\n// Declaration exists\nvoid {func}();\n\nint main() {{\n    // But implementation is missing\n    {func}();\n    return 0;\n}}"
        error = f"/usr/bin/ld: /tmp/ccXXXXXX.o: in function `main':\nmain.cpp:(.text+0x5): undefined reference to `{func}()'\ncollect2: error: ld returned 1 exit status"
        opt_code = f"#include <iostream>\n\n// Provide implementation\nvoid {func}() {{\n    std::cout << \"Executed\" << std::endl;\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"This is a Linker Error. The compiler successfully compiles `main.cpp` because `{func}()` is declared, but the linker cannot find the compiled binary code (definition) for `{func}()` to resolve the symbol during the final executable generation phase."
        beginner = f"You told the computer 'I promise a function called `{func}` exists', so it let you use it. But when it actually tried to build the final program, it couldn't find the instructions for that function anywhere."
        title = "Undefined Reference (Linker Error)"
        tags = ["compiler-error", "linker-error", "undefined-reference"]
    
    elif variation == 1:
        # Returning reference to local variable
        code = f"#include <iostream>\n\nint& {func}() {{\n    int {lvar} = 42;\n    // Returning reference to a stack-allocated local variable\n    return {lvar};\n}}\n\nint main() {{\n    int& ref = {func}();\n    return 0;\n}}"
        error = f"main.cpp: In function 'int& {func}()':\nmain.cpp:6:12: warning: reference to local variable '{lvar}' returned [-Wreturn-local-addr]"
        opt_code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 42;\n    // Return by value instead\n    return {lvar};\n}}\n\nint main() {{\n    int val = {func}();\n    return 0;\n}}"
        technical = f"Local variables are allocated on the stack frame of their enclosing function. When the function returns, its stack frame is destroyed. Returning a reference to a local variable means returning a pointer to destroyed memory, which leads to Undefined Behavior if accessed."
        beginner = f"You are trying to give someone a map to a house (a reference), but you immediately demolish the house (the function ends) before they can use the map. C++ warns you that the map points to garbage."
        title = "Returning Reference to Local Variable"
        tags = ["compiler-error", "warning", "references", "stack-memory"]
    
    elif variation == 2:
        # Missing typename in template dependent scope
        code = f"#include <iostream>\n#include <vector>\n\ntemplate <class T>\nvoid {func}(std::vector<T>& vec) {{\n    // Missing 'typename' before dependent scope\n    std::vector<T>::iterator it = vec.begin();\n}}\n\nint main() {{\n    std::vector<int> v;\n    {func}(v);\n    return 0;\n}}"
        error = f"main.cpp: In function 'void {func}(std::vector<T>&)':\nmain.cpp:6:5: error: need 'typename' before 'std::vector<T>::iterator' because 'std::vector<T>' is a dependent scope"
        opt_code = f"#include <iostream>\n#include <vector>\n\ntemplate <class T>\nvoid {func}(std::vector<T>& vec) {{\n    // Add 'typename'\n    typename std::vector<T>::iterator it = vec.begin();\n    // Or use 'auto it = vec.begin();' in C++11+\n}}\n\nint main() {{\n    std::vector<int> v;\n    {func}(v);\n    return 0;\n}}"
        technical = f"When using a nested type inside a template class (like `iterator` inside `std::vector<T>`), the compiler doesn't know if `iterator` is a type or a static member variable because `T` is unknown. The `typename` keyword explicitly tells the compiler it is a type."
        beginner = f"Because you used a generic Template, the compiler is confused. It asks: 'Is iterator a variable or a type?'. You have to put the word `typename` in front to clarify that it's a type."
        title = "Missing 'typename' in Dependent Scope"
        tags = ["compiler-error", "templates", "typename", "dependent-scope"]

    elif variation == 3:
        # Multiple Definitions (ODR Violation)
        code = f"// header.h\n#ifndef HEADER_H\n#define HEADER_H\n\n// Missing 'inline' causes multiple definition error if included in multiple .cpp files\nvoid {func}() {{\n    int x = 0;\n}}\n#endif"
        error = f"/usr/bin/ld: obj2.o: in function `{func}()':\nheader.h:6: multiple definition of `{func}()'; obj1.o:header.h:6: first defined here\ncollect2: error: ld returned 1 exit status"
        opt_code = f"// header.h\n#ifndef HEADER_H\n#define HEADER_H\n\n// Add 'inline' to allow multiple definitions across translation units\ninline void {func}() {{\n    int x = 0;\n}}\n#endif"
        technical = f"The One Definition Rule (ODR) states that a function or variable can only be defined once in the entire program. Including a non-inline function definition in a header file that is included by multiple `.cpp` files creates multiple copies of the function, causing the linker to fail."
        beginner = f"You wrote the full function instructions inside a header file. When two different C++ files loaded that header, the computer got two identical copies of the function and couldn't figure out which one to use."
        title = "Multiple Definition (ODR Violation)"
        tags = ["compiler-error", "linker-error", "odr", "inline"]

    else:
        # Missing main function
        code = f"#include <iostream>\n\nvoid {func}() {{\n    std::cout << \"Hello World\" << std::endl;\n}}\n\n// Missing int main() entry point"
        error = f"/usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/crt1.o: in function `_start':\n(.text+0x24): undefined reference to `main'\ncollect2: error: ld returned 1 exit status"
        opt_code = f"#include <iostream>\n\nvoid {func}() {{\n    std::cout << \"Hello World\" << std::endl;\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"Every executable C++ program requires a globally accessible `main` function as its entry point. If the linker builds an executable (not a shared library) and cannot find `main`, it will throw an undefined reference error via the C-runtime initialization code (`_start`)."
        beginner = f"You wrote some functions, but you forgot the `main()` function. The computer needs a `main()` function because that's the 'Start Here' sign telling it where the program begins."
        title = "Missing main() Function Entry Point"
        tags = ["compiler-error", "linker-error", "main-function"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "compiler_error",
        "instruction": f"Fix the C++ compiler/linker error caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like trying to assemble a piece of furniture, but the instruction manual keeps referencing a missing page (or references two different versions of the same page).",
            "solution": "Provide missing definitions, use `typename`, add `inline` guards, or fix return types.",
            "prevention": "Use header guards `#pragma once` properly, declare implementations in `.cpp` files rather than `.h` files, and pay attention to compiler warnings.",
            "optimized_code": opt_code,
            "complexity": {"before": "Fails to compile/link", "after": "Compiles successfully"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated C++ Linker/Compiler Error Variations",
            "language_version": "C++11/14",
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
