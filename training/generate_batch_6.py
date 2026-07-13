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
output_file = "../datasets/runtime_errors/cpp/invalid_argument.json"

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

var_names = ["inputStr", "userAge", "priceTag", "amountInput", "countVal", "scoreData", "indexStr", "limitInput", "dataPoint", "offsetStr"]
funcs = ["parseInput", "convertString", "processData", "extractNumber", "readCount", "loadAge", "fetchPrice", "computeLimit", "validateScore", "getNumber"]

# Variation 1: std::stoi with non-numeric string
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    int num = std::stoi({vname});\n    std::cout << num * 2 << std::endl;\n}}\n\nint main() {{\n    {func}(\"abc10\");\n    return 0;\n}}"
    error = f"terminate called after throwing an instance of 'std::invalid_argument'\n  what():  stoi\nAborted (core dumped)"
    opt_code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    try {{\n        int num = std::stoi({vname});\n        std::cout << num * 2 << std::endl;\n    }} catch (const std::invalid_argument& e) {{\n        std::cerr << \"Invalid input: not a number\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(\"abc10\");\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "runtime_error",
        "instruction": "Fix the std::invalid_argument runtime exception caused by parsing a non-numeric string.",
        "input": {
            "title": "std::stoi invalid_argument",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `std::stoi` function throws a `std::invalid_argument` exception if no conversion could be performed because the string does not start with a valid numeric character.",
            "beginner": "You tried to convert text into a number, but the text started with letters. The computer doesn't know how to turn 'abc' into a math number.",
            "analogy": "It's like putting a plastic toy apple into a juicer and expecting apple juice.",
            "solution": "Wrap the conversion in a `try-catch` block to handle `std::invalid_argument` and `std::out_of_range` exceptions gracefully.",
            "prevention": "Validate user input using string matching or regular expressions before attempting to parse it into an integer.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ reference documentation",
            "language_version": "C++11",
            "tags": ["std::stoi", "exception", "parsing"]
        }
    }
    samples.append(sample)

# Variation 2: std::stod with empty string
for i in range(25):
    vname = var_names[(i+2) % len(var_names)]
    func = funcs[(i+2) % len(funcs)]
    code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    double val = std::stod({vname});\n    std::cout << val << std::endl;\n}}\n\nint main() {{\n    {func}(\"\");\n    return 0;\n}}"
    error = f"terminate called after throwing an instance of 'std::invalid_argument'\n  what():  stod\nAborted (core dumped)"
    opt_code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    if ({vname}.empty()) {{\n        std::cerr << \"Error: empty string provided\" << std::endl;\n        return;\n    }}\n    try {{\n        double val = std::stod({vname});\n        std::cout << val << std::endl;\n    }} catch (const std::exception& e) {{\n        std::cerr << \"Parsing error\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(\"\");\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "runtime_error",
        "instruction": "Fix the std::invalid_argument exception caused by passing an empty string to std::stod.",
        "input": {
            "title": "std::stod empty string",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Passing an empty string to `std::stod` (or `std::stoi`, `std::stof`) results in a `std::invalid_argument` exception because there are no characters to process.",
            "beginner": "You asked the computer to read a number from an empty piece of text. It panicked because there was nothing to read.",
            "analogy": "It's like asking a translator to translate a blank sheet of paper.",
            "solution": "Check if the string is `.empty()` before passing it to parsing functions, and use `try-catch` blocks.",
            "prevention": "Ensure variables representing input are always initialized properly and check for empty input from users or files.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ standard library behavior",
            "language_version": "C++11",
            "tags": ["std::stod", "empty-string", "exception"]
        }
    }
    samples.append(sample)

# Variation 3: Passing nullptr to a function expecting std::string
for i in range(25):
    vname = var_names[(i+4) % len(var_names)]
    func = funcs[(i+4) % len(funcs)]
    code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    std::cout << {vname} << std::endl;\n}}\n\nint main() {{\n    const char* c_str = nullptr;\n    {func}(c_str);\n    return 0;\n}}"
    error = f"terminate called after throwing an instance of 'std::logic_error'\n  what():  basic_string::_M_construct null not valid\nAborted (core dumped)"
    opt_code = f"#include <iostream>\n#include <string>\n\nvoid {func}(const std::string& {vname}) {{\n    std::cout << {vname} << std::endl;\n}}\n\nint main() {{\n    const char* c_str = nullptr;\n    if (c_str != nullptr) {{\n        {func}(c_str);\n    }} else {{\n        {func}(\"default_string\");\n    }}\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "runtime_error",
        "instruction": "Fix the std::logic_error exception caused by implicitly constructing a std::string from a null pointer.",
        "input": {
            "title": "Constructing std::string from nullptr",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "Constructing a `std::string` from a `nullptr` violates the preconditions of the string constructor, resulting in a `std::logic_error`.",
            "beginner": "You tried to create text from a pointer that points to absolutely nothing. C++ doesn't allow creating a string out of nothing.",
            "analogy": "It's like trying to build a house, but instead of giving the builder a blueprint, you give them empty air.",
            "solution": "Check if the C-style string pointer is `nullptr` before passing it to a function that expects a `std::string`.",
            "prevention": "Be extremely careful when interfacing C++ code with older C APIs that might return `nullptr`.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by common C++ logic errors",
            "language_version": "C++11",
            "tags": ["std::string", "nullptr", "logic-error"]
        }
    }
    samples.append(sample)

# Variation 4: Invalid argument to bitset
for i in range(25):
    code = f"#include <iostream>\n#include <bitset>\n#include <string>\n\nint main() {{\n    std::string bits = \"10102010\";\n    std::bitset<8> b(bits);\n    std::cout << b << std::endl;\n    return 0;\n}}"
    error = f"terminate called after throwing an instance of 'std::invalid_argument'\n  what():  bitset::_M_copy_from_ptr\nAborted (core dumped)"
    opt_code = f"#include <iostream>\n#include <bitset>\n#include <string>\n\nint main() {{\n    std::string bits = \"10102010\";\n    try {{\n        std::bitset<8> b(bits);\n        std::cout << b << std::endl;\n    }} catch (const std::invalid_argument& e) {{\n        std::cerr << \"String contains non-binary characters\" << std::endl;\n    }}\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "runtime_error",
        "instruction": "Fix the std::invalid_argument exception caused by passing non-binary characters to std::bitset.",
        "input": {
            "title": "std::bitset invalid_argument",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The `std::bitset` string constructor throws `std::invalid_argument` if any character in the provided string is not '0' or '1'.",
            "beginner": "You gave a piece of text to a system that only understands '0's and '1's, but your text had a '2' in it.",
            "analogy": "It's like giving a multiple-choice answer sheet (A, B, C, D) but bubbling in 'E'.",
            "solution": "Wrap the `std::bitset` initialization in a `try-catch` block, or validate the string first to ensure it only contains '0' and '1'.",
            "prevention": "When dealing with strict binary conversions, sanitize the input beforehand.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(N)", "after": "O(N)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ standard library behavior",
            "language_version": "C++11",
            "tags": ["std::bitset", "exception", "invalid-argument"]
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
