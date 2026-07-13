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

ensure_dir("../datasets/runtime_errors/cpp")
output_file = "../datasets/runtime_errors/cpp/common_runtime_errors.json"

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
        candidate = f"CP_RUNTIME_{i:06d}"
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
        # Dereferencing Null Pointer (Segmentation Fault)
        code = f"#include <iostream>\n\nvoid {func}(int* ptr) {{\n    // Dereferencing without checking for nullptr\n    std::cout << *ptr << std::endl;\n}}\n\nint main() {{\n    int* myPtr = nullptr;\n    {func}(myPtr);\n    return 0;\n}}"
        error = f"Segmentation fault (core dumped)"
        opt_code = f"#include <iostream>\n\nvoid {func}(int* ptr) {{\n    if (ptr != nullptr) {{\n        std::cout << *ptr << std::endl;\n    }} else {{\n        std::cerr << \"Error: Null pointer provided\" << std::endl;\n    }}\n}}\n\nint main() {{\n    int* myPtr = nullptr;\n    {func}(myPtr);\n    return 0;\n}}"
        technical = f"A segmentation fault occurs when a program attempts to access a memory location that it is not allowed to access. Dereferencing a `nullptr` attempts to read from memory address 0x0, which is protected by the operating system."
        beginner = f"You tried to look inside a box (pointer), but the box didn't exist (it was `nullptr`). The computer panicked and crashed."
        title = "Dereferencing Null Pointer"
        tags = ["runtime-error", "segmentation-fault", "pointers", "nullptr"]
    
    elif variation == 1:
        # std::out_of_range (vector::at)
        code = f"#include <iostream>\n#include <vector>\n\nvoid {func}() {{\n    std::vector<int> {vname} = {{1, 2, 3}};\n    int {lvar} = {vname}.at(5); // Out of bounds access\n    std::cout << {lvar} << std::endl;\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"terminate called after throwing an instance of 'std::out_of_range'\n  what():  vector::_M_range_check: __n (which is 5) >= this->size() (which is 3)\nAborted (core dumped)"
        opt_code = f"#include <iostream>\n#include <vector>\n\nvoid {func}() {{\n    std::vector<int> {vname} = {{1, 2, 3}};\n    try {{\n        int {lvar} = {vname}.at(5);\n        std::cout << {lvar} << std::endl;\n    }} catch (const std::out_of_range& e) {{\n        std::cerr << \"Index out of bounds\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"The `std::vector::at()` method performs bounds checking. If the requested index is greater than or equal to the vector's size, it throws a `std::out_of_range` exception, which terminates the program if unhandled."
        beginner = f"You asked for the 6th item in a list that only has 3 items. C++ caught the mistake and threw an exception to stop you from reading random memory."
        title = "std::out_of_range Exception"
        tags = ["runtime-error", "out-of-range", "vector", "exception"]
    
    elif variation == 2:
        # Division by Zero
        code = f"#include <iostream>\n\nint {func}(int a, int b) {{\n    int {lvar} = a / b;\n    return {lvar};\n}}\n\nint main() {{\n    std::cout << {func}(10, 0) << std::endl;\n    return 0;\n}}"
        error = f"Floating point exception (core dumped)"
        opt_code = f"#include <iostream>\n\nint {func}(int a, int b) {{\n    if (b == 0) {{\n        std::cerr << \"Division by zero error\" << std::endl;\n        return 0;\n    }}\n    int {lvar} = a / b;\n    return {lvar};\n}}\n\nint main() {{\n    std::cout << {func}(10, 0) << std::endl;\n    return 0;\n}}"
        technical = f"Attempting to perform integer division by zero raises a SIGFPE (Floating-Point Exception) signal in POSIX systems, which typically terminates the process immediately."
        beginner = f"You tried to divide a number by zero. Just like in math class, this is impossible, so the computer crashes."
        title = "Integer Division by Zero"
        tags = ["runtime-error", "division-by-zero", "sigfpe", "math"]

    elif variation == 3:
        # Stack Overflow (Infinite Recursion)
        code = f"#include <iostream>\n\nvoid {func}() {{\n    // Missing base case for recursion\n    {func}();\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"Segmentation fault (core dumped)"
        opt_code = f"#include <iostream>\n\nvoid {func}(int depth) {{\n    if (depth <= 0) return;\n    {func}(depth - 1);\n}}\n\nint main() {{\n    {func}(10);\n    return 0;\n}}"
        technical = f"When a function calls itself recursively without a reachable base case, it continuously adds new stack frames to the call stack. Eventually, the stack memory is exhausted, causing a stack overflow (usually manifesting as a segmentation fault)."
        beginner = f"You told a function to call itself forever without a stopping condition. Eventually, the computer ran out of memory to keep track of the calls, and crashed."
        title = "Stack Overflow (Infinite Recursion)"
        tags = ["runtime-error", "stack-overflow", "recursion", "segmentation-fault"]

    else:
        # std::bad_alloc (Huge memory allocation)
        code = f"#include <iostream>\n\nint main() {{\n    try {{\n        // Attempting to allocate an impossibly large array\n        long long* massiveArray = new long long[9999999999999999];\n        delete[] massiveArray;\n    }} catch (const std::exception& e) {{\n        std::cerr << e.what() << std::endl;\n    }}\n    return 0;\n}}"
        error = f"std::bad_alloc"
        opt_code = f"#include <iostream>\n#include <vector>\n\nint main() {{\n    try {{\n        // Allocate a reasonable amount of memory instead\n        std::vector<long long> reasonableArray(1000);\n    }} catch (const std::exception& e) {{\n        std::cerr << e.what() << std::endl;\n    }}\n    return 0;\n}}"
        technical = f"When the `new` operator fails to allocate the requested amount of contiguous heap memory (either because the system is out of memory or the requested size is absurd), it throws a `std::bad_alloc` exception."
        beginner = f"You asked the computer for way more memory than it actually has. It couldn't fulfill the request, so it threw an error."
        title = "std::bad_alloc Exception"
        tags = ["runtime-error", "bad-alloc", "memory-allocation", "exception"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "runtime_error",
        "instruction": f"Fix the C++ runtime error caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like a machine trying to process an impossible instruction and physically breaking in the attempt.",
            "solution": "Add appropriate boundary checks, base cases for recursion, or `try-catch` blocks to handle exceptions gracefully.",
            "prevention": "Always validate inputs, check pointers against `nullptr` before dereferencing, and use smart pointers / STL containers to manage memory safely.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1) to crash", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated C++ Runtime Error Variations",
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
