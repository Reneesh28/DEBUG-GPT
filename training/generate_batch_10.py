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

funcs = ["processData", "analyze", "evaluate", "computeMetrics", "summarize", "transform", "filterItems", "countElements", "aggregate", "calculateSum"]
var_names = ["dataset", "records", "inputs", "entries", "values", "points", "buffer", "matrix", "vectorList", "metrics"]

# Variation 1: Pass by Value vs Pass by Const Reference
for i in range(25):
    func = funcs[i % len(funcs)]
    vname = var_names[i % len(var_names)]
    code = f"#include <iostream>\n#include <vector>\n#include <string>\n\nvoid {func}(std::vector<std::string> {vname}) {{\n    for (size_t i = 0; i < {vname}.size(); ++i) {{\n        std::cout << {vname}[i] << \" \";\n    }}\n}}\n\nint main() {{\n    std::vector<std::string> my_data(10000, \"test\");\n    {func}(my_data);\n    return 0;\n}}"
    error = f"Performance Issue: Passing a large object like std::vector by value forces a full O(N) copy, wasting memory and CPU cycles."
    opt_code = f"#include <iostream>\n#include <vector>\n#include <string>\n\nvoid {func}(const std::vector<std::string>& {vname}) {{\n    for (size_t i = 0; i < {vname}.size(); ++i) {{\n        std::cout << {vname}[i] << \" \";\n    }}\n}}\n\nint main() {{\n    std::vector<std::string> my_data(10000, \"test\");\n    {func}(my_data);\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "optimization",
        "instruction": "Optimize the function signature to avoid expensive deep copies.",
        "input": {
            "title": "Pass by Value vs Const Reference",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Passing a non-trivial object like `std::vector` or `std::string` by value invokes the object's copy constructor, which dynamically allocates memory and copies every element in O(N) time. By using a `const` reference, we pass a pointer under the hood, making it O(1) time and avoiding the copy overhead while preserving read-only safety.",
            "beginner": "When you pass the list to the function, C++ makes a complete identical copy of it. If the list has 10,000 items, it copies all 10,000 items. Using a 'reference' just hands the function the address of the existing list.",
            "analogy": "It's like giving your friend a 1,000-page book to read. Passing by value means you photocopy every single page and give them the copies. Passing by reference means you just hand them your book.",
            "solution": "Change the function parameter from `std::vector<std::string> {vname}` to `const std::vector<std::string>& {vname}`.",
            "prevention": "As a rule of thumb, pass built-in types (int, float) by value, and complex objects (std::vector, std::string, custom classes) by `const &`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by C++ Best Practices",
            "language_version": "C++11",
            "tags": ["optimization", "pass-by-reference", "copy-constructor"]
        }
    }
    samples.append(sample)

# Variation 2: std::endl vs '\n'
for i in range(25):
    func = funcs[(i+2) % len(funcs)]
    code = f"#include <iostream>\n\nvoid {func}(int n) {{\n    for (int i = 0; i < n; ++i) {{\n        std::cout << \"Processing item \" << i << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(100000);\n    return 0;\n}}"
    error = f"Performance Issue: std::endl appends a newline AND explicitly flushes the output buffer, severely degrading I/O performance in a loop."
    opt_code = f"#include <iostream>\n\nvoid {func}(int n) {{\n    for (int i = 0; i < n; ++i) {{\n        std::cout << \"Processing item \" << i << '\\n';\n    }}\n}}\n\nint main() {{\n    {func}(100000);\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "optimization",
        "instruction": "Optimize the output loop by preventing unnecessary buffer flushes.",
        "input": {
            "title": "std::endl vs newline character",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "`std::endl` performs two actions: it writes a newline character to the stream and calls `std::flush`. Flushing the output buffer directly to the OS or console in every iteration of a large loop creates massive syscall overhead, making the loop extremely slow.",
            "beginner": "Using `std::endl` doesn't just go to the next line; it also forces the computer to immediately 'push' the text to the screen. Pushing it 100,000 times individually takes a long time compared to pushing it in big batches.",
            "analogy": "It's like delivering 100 letters to the post office by driving there and back for every single letter, instead of waiting until you have a whole stack and doing it in one trip.",
            "solution": "Use the newline character `'\\n'` instead of `std::endl` when writing output inside tight loops.",
            "prevention": "Only use `std::endl` when you specifically require the stream to be flushed immediately (e.g., ensuring a prompt is shown before waiting for input).",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N) with high I/O overhead", "after": "O(N) with buffered I/O"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by competitive programming practices",
            "language_version": "C++11",
            "tags": ["optimization", "iostream", "buffer-flush", "std::endl"]
        }
    }
    samples.append(sample)

# Variation 3: Postfix vs Prefix Iterators
for i in range(25):
    vname = var_names[(i+4) % len(var_names)]
    code = f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vname}(100000, 1);\n    int sum = 0;\n    // Using postfix operator it++ creates a temporary copy of the iterator\n    for (std::vector<int>::iterator it = {vname}.begin(); it != {vname}.end(); it++) {{\n        sum += *it;\n    }}\n    std::cout << sum << \"\\n\";\n    return 0;\n}}"
    error = f"Performance Issue: Using the postfix increment operator (it++) on iterators or complex objects incurs the overhead of creating a temporary copy."
    opt_code = f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vname}(100000, 1);\n    int sum = 0;\n    for (std::vector<int>::iterator it = {vname}.begin(); it != {vname}.end(); ++it) {{\n        sum += *it;\n    }}\n    std::cout << sum << \"\\n\";\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "optimization",
        "instruction": "Optimize the loop iterator incrementation.",
        "input": {
            "title": "Postfix vs Prefix Iterator Increment",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The postfix increment operator `it++` requires the object to store a copy of its old state, increment the internal state, and return the old copy. For complex objects like iterators, this temporary copy creation adds overhead inside loops. Prefix `++it` increments and returns the reference directly without creating temporaries.",
            "beginner": "When you write `it++`, the computer has to make a backup copy of the old 'it' before increasing it. When you write `++it`, it just increases it directly, which is slightly faster.",
            "analogy": "It's like taking a photo of a whiteboard, erasing it, writing the new number, and handing someone the photo, versus just erasing the board and writing the new number directly.",
            "solution": "Change the postfix increment `it++` to a prefix increment `++it` in the loop signature.",
            "prevention": "Form a habit of using prefix `++i` and `++it` everywhere in C++, unless you specifically rely on the old value returned by the postfix operator.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N) with temporary copy overhead", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ Core Guidelines",
            "language_version": "C++98",
            "tags": ["optimization", "iterators", "prefix-postfix"]
        }
    }
    samples.append(sample)

# Variation 4: String concatenation creating temporaries (s = s + "a")
for i in range(25):
    func = funcs[(i+6) % len(funcs)]
    code = f"#include <iostream>\n#include <string>\n\nstd::string {func}(int n) {{\n    std::string result = \"\";\n    for (int i = 0; i < n; ++i) {{\n        // s = s + str forces the creation of a temporary string and a deep copy\n        result = result + \"a\";\n    }}\n    return result;\n}}\n\nint main() {{\n    std::cout << {func}(50000).size() << \"\\n\";\n    return 0;\n}}"
    error = f"Performance Issue: Using `str = str + append` creates a new temporary string object, copies both operands into it, and then replaces the original. This is O(N^2)."
    opt_code = f"#include <iostream>\n#include <string>\n\nstd::string {func}(int n) {{\n    std::string result = \"\";\n    // result.reserve(n); // Optional: further optimizes by preallocating memory\n    for (int i = 0; i < n; ++i) {{\n        result += \"a\"; // Appends directly to the existing string buffer\n    }}\n    return result;\n}}\n\nint main() {{\n    std::cout << {func}(50000).size() << \"\\n\";\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "optimization",
        "instruction": "Optimize string concatenation inside the loop to avoid quadratic complexity.",
        "input": {
            "title": "String `s = s + str` vs `s += str`",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The expression `result = result + \"a\"` invokes `operator+` which returns a completely new, dynamically allocated string containing the combined content, and then the assignment operator replaces `result`. This O(N) allocation happens in every loop iteration, leading to O(N^2) complexity. Using `+=` invokes `operator+=` which modifies the existing string buffer in-place, achieving O(1) amortized time per operation.",
            "beginner": "Using `+` to add to a string creates a completely new string from scratch every single time. If you do this thousands of times, the computer spends all its time repeatedly copying text. `+=` modifies the string you already have.",
            "analogy": "It's like buying a brand new notebook, copying everything from your old notebook into it, writing one new word, and throwing the old notebook away—every time you want to write a word.",
            "solution": "Use the `+=` operator or the `.append()` method to append to the string. For maximum performance, also use `.reserve()` to preallocate memory before the loop.",
            "prevention": "Always use `+=` when mutating a string inside a loop in C++.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N^2)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ string performance pitfalls",
            "language_version": "C++11",
            "tags": ["optimization", "string-concatenation", "memory-allocation"]
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
