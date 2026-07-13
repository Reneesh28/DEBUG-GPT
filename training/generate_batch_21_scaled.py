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

ensure_dir("../datasets/optimization_examples/cpp")
output_file = "../datasets/optimization_examples/cpp/common_optimizations.json"

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
        candidate = f"CP_OPTIMIZE_{i:06d}"
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
        # Pass by Value instead of Const Reference
        code = f"#include <iostream>\n#include <vector>\n\n// Performance issue: passing a large vector by value\nvoid {func}(std::vector<int> {vname}) {{\n    int {lvar} = 0;\n    for(int i : {vname}) {lvar} += i;\n    std::cout << {lvar} << '\\n';\n}}\n\nint main() {{\n    std::vector<int> largeArray(1000000, 1);\n    {func}(largeArray);\n    return 0;\n}}"
        error = f"Performance Issue: Passing large objects (like `std::vector` or `std::string`) by value triggers an expensive O(N) deep copy of the entire data structure."
        opt_code = f"#include <iostream>\n#include <vector>\n\n// Optimized: pass by const reference to avoid copying\nvoid {func}(const std::vector<int>& {vname}) {{\n    int {lvar} = 0;\n    for(int i : {vname}) {lvar} += i;\n    std::cout << {lvar} << '\\n';\n}}\n\nint main() {{\n    std::vector<int> largeArray(1000000, 1);\n    {func}(largeArray);\n    return 0;\n}}"
        technical = f"In C++, passing an argument by value invokes the object's copy constructor. For large containers like `std::vector`, this means allocating new heap memory and copying every element (O(N) time and space). Passing by `const reference` (`const T&`) passes a memory address instead, which is O(1) time and guarantees the function won't modify the original data."
        beginner = f"Instead of handing the function a map to the data (`const reference`), you accidentally forced the computer to draw a complete replica of a million-item list just so the function could look at it."
        title = "Pass by Value vs Const Reference"
        tags = ["optimization", "pass-by-value", "pass-by-reference", "copy-constructor"]
    
    elif variation == 1:
        # std::endl vs '\n'
        code = f"#include <iostream>\n\nvoid {func}() {{\n    for (int i = 0; i < 100000; ++i) {{\n        // std::endl forces a flush of the output buffer on every iteration\n        std::cout << i << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"Performance Issue: Using `std::endl` in a tight loop forces the underlying output stream to flush its buffer to the OS on every iteration, leading to massive I/O overhead."
        opt_code = f"#include <iostream>\n\nvoid {func}() {{\n    for (int i = 0; i < 100000; ++i) {{\n        // '\\n' just appends a newline without flushing\n        std::cout << i << '\\n';\n    }}\n    std::cout << std::flush;\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"`std::endl` does two things: it outputs a newline character (`\\n`) and explicitly calls `std::flush` on the stream. I/O operations are very slow. By flushing the buffer on every iteration, the program spends most of its time waiting for the OS. Using `\\n` allows the stream to buffer data and flush it efficiently in large blocks."
        beginner = f"You are telling the computer to 'print this number and immediately send it to the screen' 100,000 times. It's much faster to say 'add this to the print queue' (`\\n`) and let the computer send the whole queue when it's ready."
        title = "std::endl vs \\n (I/O Flushing)"
        tags = ["optimization", "io-overhead", "std-endl", "flushing"]
    
    elif variation == 2:
        # std::vector reallocation (missing reserve)
        code = f"#include <iostream>\n#include <vector>\n\nvoid {func}(int count) {{\n    std::vector<int> {vname};\n    // The vector will constantly reallocate and copy elements as it grows\n    for (int i = 0; i < count; ++i) {{\n        {vname}.push_back(i);\n    }}\n}}\n\nint main() {{\n    {func}(1000000);\n    return 0;\n}}"
        error = f"Performance Issue: Dynamically growing a `std::vector` inside a loop without pre-allocating capacity causes multiple costly memory reallocations and element copies."
        opt_code = f"#include <iostream>\n#include <vector>\n\nvoid {func}(int count) {{\n    std::vector<int> {vname};\n    {vname}.reserve(count); // Pre-allocate memory once\n    for (int i = 0; i < count; ++i) {{\n        {vname}.push_back(i);\n    }}\n}}\n\nint main() {{\n    {func}(1000000);\n    return 0;\n}}"
        technical = f"When `std::vector::push_back` exceeds the current capacity, the vector must allocate a larger block of memory (usually double the size), copy all existing elements to the new block, and delete the old block. If the final size is known in advance, calling `reserve(N)` allocates the memory exactly once."
        beginner = f"The list keeps outgrowing its box. Every time it gets too full, it has to buy a bigger box and move everything over. By telling it how big the final box needs to be from the start, you save a lot of moving time."
        title = "Missing std::vector::reserve"
        tags = ["optimization", "std-vector", "reserve", "memory-allocation"]

    elif variation == 3:
        # Postfix vs Prefix Iterators
        code = f"#include <iostream>\n#include <vector>\n\nvoid {func}() {{\n    std::vector<int> {vname}(1000000, 1);\n    // Using postfix increment i++ creates a temporary copy of the iterator\n    for (std::vector<int>::iterator it = {vname}.begin(); it != {vname}.end(); it++) {{\n        *it = *it * 2;\n    }}\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"Performance Issue: Using the postfix increment operator (`it++`) on complex iterator objects requires creating and destroying a temporary copy on every loop iteration."
        opt_code = f"#include <iostream>\n#include <vector>\n\nvoid {func}() {{\n    std::vector<int> {vname}(1000000, 1);\n    // Using prefix increment ++i avoids the temporary copy\n    for (std::vector<int>::iterator it = {vname}.begin(); it != {vname}.end(); ++it) {{\n        *it = *it * 2;\n    }}\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"For non-primitive types like STL iterators, `it++` (postfix) returns a copy of the original state before incrementing. This involves a constructor and destructor call. `++it` (prefix) increments the object in-place and returns a reference to itself, avoiding the overhead of temporary object creation."
        beginner = f"Writing `it++` forces the computer to make a backup copy of 'it', add 1 to 'it', and then instantly throw away the backup copy. `++it` just adds 1 directly without wasting time making backups."
        title = "Postfix vs Prefix Iterators"
        tags = ["optimization", "iterators", "postfix", "prefix"]

    else:
        # String repeated concatenation
        code = f"#include <iostream>\n#include <string>\n\nvoid {func}() {{\n    std::string {lvar} = \"\";\n    // String reallocates multiple times as it grows\n    for(int i=0; i<10000; ++i) {{\n        {lvar} += \"A\";\n    }}\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"Performance Issue: Concatenating to a `std::string` inside a tight loop causes it to repeatedly reallocate memory and copy its contents."
        opt_code = f"#include <iostream>\n#include <string>\n\nvoid {func}() {{\n    std::string {lvar} = \"\";\n    {lvar}.reserve(10000); // Pre-allocate the memory\n    for(int i=0; i<10000; ++i) {{\n        {lvar} += \"A\";\n    }}\n    // Or alternatively: std::string {lvar}(10000, 'A');\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"Similar to `std::vector`, `std::string` manages dynamic memory. Repeated `+=` operations can trigger O(N) capacity reallocations and O(N) character copies per reallocation, leading to O(N^2) overall behavior. Using `reserve()` or constructing with a specified length eliminates this."
        beginner = f"Building a huge string one letter at a time forces C++ to keep asking the system for slightly bigger chunks of memory. If you know you need 10,000 letters, ask for a 10,000-letter chunk of memory upfront."
        title = "String Reallocation in Loop"
        tags = ["optimization", "std-string", "reserve", "concatenation"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "optimization",
        "instruction": f"Optimize the C++ code to resolve the performance issue: {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like paying for shipping on every single item of a 100-item order, instead of putting them all in one box and shipping them together.",
            "solution": "Refactor to use pass-by-reference, prefix iterators (`++it`), buffered output (`\\n`), or pre-allocate memory using `reserve()`.",
            "prevention": "Enable performance-oriented compiler warnings (like `-Wsuggest-attribute=pure` or clang-tidy performance checks) which can catch inefficient loops and copies automatically.",
            "optimized_code": opt_code,
            "complexity": {"before": "High memory/CPU overhead", "after": "Optimal O(1) or O(N) operations"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated C++ Optimization Variations",
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
