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

ensure_dir("../datasets/logical_bugs/cpp")
output_file = "../datasets/logical_bugs/cpp/common_logic_bugs.json"

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
        candidate = f"CP_LOGICAL_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

funcs = ["calculate", "processArray", "computeSum", "findMax", "analyzeData", "evaluate", "updateScore", "filterItems", "sortData", "mergeArrays"]
var_names = ["dataArr", "inputList", "values", "numbers", "records", "points", "scores", "dataset", "buffer", "elements"]
local_vars = ["total", "count", "average", "sumVal", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Assignment instead of Equality
        code = f"#include <iostream>\n\nvoid {func}(int {lvar}) {{\n    // Bug: Using = instead of == assigns the value 10 to {lvar}, which evaluates to true\n    if ({lvar} = 10) {{\n        std::cout << \"Value is 10\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(5);\n    return 0;\n}}"
        error = f"Logical Bug: Assignment operator used within condition always evaluates to true (non-zero)."
        opt_code = f"#include <iostream>\n\nvoid {func}(int {lvar}) {{\n    if ({lvar} == 10) {{\n        std::cout << \"Value is 10\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(5);\n    return 0;\n}}"
        technical = f"In C++, the assignment operator `=` returns the assigned value. When used in a conditional statement like `if(x = 10)`, `x` is assigned 10, and the expression evaluates to 10 (which is non-zero, hence boolean `true`). This executes the if-block unconditionally."
        beginner = f"You used a single `=` inside the `if` statement. Single `=` means 'make it equal to', so you accidentally changed the variable to 10. To ask 'is it equal to?', you must use double `==`."
        title = "Assignment in Conditional (`=` vs `==`)"
        tags = ["logical-bug", "assignment", "conditional", "equality"]
    
    elif variation == 1:
        # Floating Point Equality
        code = f"#include <iostream>\n\nvoid {func}(float a, float b) {{\n    float {lvar} = a + b;\n    // Bug: Direct equality comparison for floating point numbers\n    if ({lvar} == 0.3f) {{\n        std::cout << \"Match!\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(0.1f, 0.2f); // Often fails to print \"Match!\"\n    return 0;\n}}"
        error = f"Logical Bug: Exact equality comparison for floating-point values fails due to precision representation errors."
        opt_code = f"#include <iostream>\n#include <cmath>\n\nvoid {func}(float a, float b) {{\n    float {lvar} = a + b;\n    float epsilon = 0.00001f;\n    if (std::abs({lvar} - 0.3f) < epsilon) {{\n        std::cout << \"Match!\" << std::endl;\n    }}\n}}\n\nint main() {{\n    {func}(0.1f, 0.2f);\n    return 0;\n}}"
        technical = f"Floating-point numbers (float, double) are represented in binary fractions (IEEE 754). Many decimal fractions (like 0.1) cannot be perfectly represented, leading to tiny rounding errors. Thus, `0.1 + 0.2` is `0.30000001`, making `== 0.3` evaluate to false."
        beginner = f"Computers struggle to store decimals exactly. For the computer, 0.1 + 0.2 is actually 0.30000001, so it doesn't exactly equal 0.3. Never use `==` for decimals."
        title = "Floating-Point Exact Equality"
        tags = ["logical-bug", "floating-point", "equality", "precision"]
    
    elif variation == 2:
        # Uninitialized Variable
        code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar};\n    // Bug: Using an uninitialized local variable\n    for (int i = 0; i < 5; ++i) {{\n        {lvar} += i;\n    }}\n    return {lvar};\n}}\n\nint main() {{\n    std::cout << {func}() << std::endl;\n    return 0;\n}}"
        error = f"Logical Bug / UB: Local variable is used without initialization, containing garbage memory data."
        opt_code = f"#include <iostream>\n\nint {func}() {{\n    int {lvar} = 0; // Initialize to zero\n    for (int i = 0; i < 5; ++i) {{\n        {lvar} += i;\n    }}\n    return {lvar};\n}}\n\nint main() {{\n    std::cout << {func}() << std::endl;\n    return 0;\n}}"
        technical = f"In C++, local variables (automatic storage duration) are not default-initialized. If they are used before being assigned a value, they contain indeterminate 'garbage' values from whatever was previously at that memory address on the stack. Reading this value is Undefined Behavior."
        beginner = f"You started adding numbers to '{lvar}', but you never set '{lvar}' to 0 at the beginning. It started with whatever random garbage number the computer previously left in memory."
        title = "Uninitialized Variable"
        tags = ["logical-bug", "uninitialized", "undefined-behavior"]

    elif variation == 3:
        # Shadowing Member Variable
        code = f"#include <iostream>\n\nclass DataProcessor {{\n    int {lvar} = 100;\npublic:\n    void {func}(int {lvar}) {{\n        // Bug: The parameter shadows the member variable. The member remains unchanged.\n        {lvar} = {lvar} * 2;\n    }}\n    void print() {{ std::cout << {lvar} << std::endl; }}\n}};\n\nint main() {{\n    DataProcessor proc;\n    proc.{func}(50);\n    proc.print(); // Prints 100 instead of 100 * 2\n    return 0;\n}}"
        error = f"Logical Bug: A function parameter or local variable shares the same name as a class member, shadowing it and preventing modification."
        opt_code = f"#include <iostream>\n\nclass DataProcessor {{\n    int {lvar} = 100;\npublic:\n    void {func}(int newVal) {{\n        this->{lvar} = newVal * 2;\n    }}\n    void print() {{ std::cout << {lvar} << std::endl; }}\n}};\n\nint main() {{\n    DataProcessor proc;\n    proc.{func}(50);\n    proc.print();\n    return 0;\n}}"
        technical = f"When a local variable or parameter has the same identifier as a class member variable, the local identifier 'shadows' the member. Any reference to that identifier resolves to the local variable. To access the member, one must prefix it with `this->`."
        beginner = f"You named the input parameter exactly the same as the class variable. So when you wrote `{lvar} = ...`, the computer changed the input parameter, completely ignoring the class variable."
        title = "Variable Shadowing"
        tags = ["logical-bug", "shadowing", "scope", "class-member"]

    else:
        # Off-by-one in string null-terminator
        code = f"#include <iostream>\n\nvoid {func}() {{\n    char str[5];\n    // Bug: Filling all 5 slots leaves no room for the null-terminator '\\0'\n    for(int i=0; i<5; ++i) str[i] = 'A';\n    std::cout << str << std::endl; // Prints garbage after AAAAA\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        error = f"Logical Bug / UB: Missing null-terminator in C-style string causes functions like std::cout to read past the array bounds."
        opt_code = f"#include <iostream>\n\nvoid {func}() {{\n    char str[6]; // Allocate space for 5 characters + null terminator\n    for(int i=0; i<5; ++i) str[i] = 'A';\n    str[5] = '\\0'; // Explicitly add null terminator\n    std::cout << str << std::endl;\n}}\n\nint main() {{\n    {func}();\n    return 0;\n}}"
        technical = f"C-style strings rely on a null-terminator (`\\0`) to mark the end of the string. If a character array is completely filled with standard characters, functions that read it (like `std::cout` or `strlen`) will continue reading adjacent memory until they accidentally encounter a zero byte, causing garbage output or a segfault."
        beginner = f"You filled all 5 boxes with 'A', but strings in C++ always need a secret extra box at the end holding a zero `\\0` to tell the computer 'stop reading here'. Since it was missing, the computer kept reading whatever was next to it in memory."
        title = "Missing Null-Terminator"
        tags = ["logical-bug", "c-strings", "null-terminator", "out-of-bounds"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "logical_bug",
        "instruction": f"Fix the logical bug caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like expecting a specific behavior but overlooking a fundamental rule of how the system operates.",
            "solution": "Apply the correct operator, initialization, scoping (`this->`), or buffer sizing depending on the logical bug.",
            "prevention": "Enable aggressive compiler warnings (`-Wall -Wextra -Wshadow -Wuninitialized`) which detect most of these logical anti-patterns automatically.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated C++ Logical Bug Variations",
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
