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

ensure_dir("../datasets/educational_explanations/cpp")
output_file = "../datasets/educational_explanations/cpp/concept_explanations.json"

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
        candidate = f"CP_EDUCATIONAL_{i:06d}"
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
        # lvalues vs rvalues
        code = f"#include <iostream>\n\nvoid {func}(int& lval_ref) {{\n    std::cout << \"lvalue ref\" << std::endl;\n}}\nvoid {func}(int&& rval_ref) {{\n    std::cout << \"rvalue ref\" << std::endl;\n}}\n\nint main() {{\n    int {lvar} = 5;\n    {func}({lvar}); // Calls lvalue overload\n    {func}(10); // Calls rvalue overload\n    return 0;\n}}"
        error = f"Educational: Understanding C++ value categories (lvalues and rvalues) and their references."
        opt_code = f"#include <iostream>\n\nvoid {func}(int& lval_ref) {{\n    std::cout << \"lvalue ref\" << std::endl;\n}}\nvoid {func}(int&& rval_ref) {{\n    std::cout << \"rvalue ref\" << std::endl;\n}}\n\nint main() {{\n    int {lvar} = 5;\n    {func}({lvar}); // Calls lvalue overload\n    {func}(10); // Calls rvalue overload\n    return 0;\n}}"
        technical = f"An `lvalue` refers to an object that occupies an identifiable location in memory (has a name and an address, like a variable). An `rvalue` is a temporary value that does not persist beyond the expression that uses it (like the literal 10). C++11 introduced `&&` (rvalue references) to allow functions to safely \"steal\" resources from temporary objects (move semantics)."
        beginner = f"An 'lvalue' is something you can point to and find in memory, like a named variable. An 'rvalue' is a temporary, fleeting value, like a number you just typed in. C++ lets you treat them differently to save time copying data."
        title = "Value Categories: lvalues vs rvalues"
        tags = ["educational", "lvalue", "rvalue", "move-semantics"]
    
    elif variation == 1:
        # Virtual Functions
        code = f"#include <iostream>\n\nclass Base {{\npublic:\n    virtual void {func}() {{ std::cout << \"Base\" << std::endl; }}\n}};\n\nclass Derived : public Base {{\npublic:\n    void {func}() override {{ std::cout << \"Derived\" << std::endl; }}\n}};\n\nint main() {{\n    Base* ptr = new Derived();\n    ptr->{func}(); // Prints \"Derived\"\n    delete ptr;\n    return 0;\n}}"
        error = f"Educational: Understanding `virtual` functions and dynamic dispatch (polymorphism)."
        opt_code = f"#include <iostream>\n\nclass Base {{\npublic:\n    virtual void {func}() {{ std::cout << \"Base\" << std::endl; }}\n    virtual ~Base() = default;\n}};\n\nclass Derived : public Base {{\npublic:\n    void {func}() override {{ std::cout << \"Derived\" << std::endl; }}\n}};\n\nint main() {{\n    Base* ptr = new Derived();\n    ptr->{func}();\n    delete ptr;\n    return 0;\n}}"
        technical = f"The `virtual` keyword tells the compiler to use late binding (dynamic dispatch) for a function. When a virtual function is called through a base class pointer, the program looks up the object's vtable (virtual table) at runtime to execute the most derived override of that function."
        beginner = f"Usually, a pointer of type 'Base' only knows how to do 'Base' things. The `virtual` keyword is like a sticky note that says 'Wait, check if I'm actually a more specific type (Derived) first, and use that version of the function instead.'"
        title = "Polymorphism: Virtual Functions"
        tags = ["educational", "virtual", "polymorphism", "oop"]
    
    elif variation == 2:
        # Smart Pointers
        code = f"#include <iostream>\n#include <memory>\n\nvoid {func}() {{\n    // Unique pointer enforces strict ownership\n    std::unique_ptr<int> ptr1 = std::make_unique<int>(100);\n    // std::unique_ptr<int> ptr2 = ptr1; // ERROR: Cannot copy\n    \n    // Shared pointer uses reference counting\n    std::shared_ptr<int> sptr1 = std::make_shared<int>(200);\n    std::shared_ptr<int> sptr2 = sptr1; // OK: Ref count is now 2\n}}"
        error = f"Educational: Understanding memory management with `std::unique_ptr` and `std::shared_ptr`."
        opt_code = f"#include <iostream>\n#include <memory>\n\nvoid {func}() {{\n    std::unique_ptr<int> ptr1 = std::make_unique<int>(100);\n    std::unique_ptr<int> ptr2 = std::move(ptr1); // OK: Ownership transferred\n    \n    std::shared_ptr<int> sptr1 = std::make_shared<int>(200);\n    std::shared_ptr<int> sptr2 = sptr1;\n}}"
        technical = f"`std::unique_ptr` implements exclusive ownership; a resource can only be owned by one unique_ptr at a time, preventing memory leaks via zero-overhead RAII. `std::shared_ptr` implements shared ownership via an atomic reference count; the memory is freed only when the last shared_ptr pointing to it is destroyed."
        beginner = f"`unique_ptr` is like a house key that cannot be copied—only one person can hold it, but they can hand it to someone else (move). `shared_ptr` is a key that can be copied, and a security guard tracks how many people have it. The house is locked up (deleted) only when everyone throws their key away."
        title = "Smart Pointers (unique_ptr vs shared_ptr)"
        tags = ["educational", "smart-pointers", "memory-management"]

    elif variation == 3:
        # RAII (Resource Acquisition Is Initialization)
        code = f"#include <iostream>\n#include <fstream>\n\nclass FileHandler {{\n    std::ofstream file;\npublic:\n    FileHandler(const std::string& name) : file(name) {{}}\n    ~FileHandler() {{\n        if (file.is_open()) file.close(); // Automatically closed when object goes out of scope\n    }}\n}};\n\nvoid {func}() {{\n    FileHandler fh(\"log.txt\");\n    // Do work. Even if an exception is thrown here, the destructor runs.\n}}"
        error = f"Educational: Understanding the RAII (Resource Acquisition Is Initialization) paradigm in C++."
        opt_code = f"#include <iostream>\n#include <fstream>\n\nclass FileHandler {{\n    std::ofstream file;\npublic:\n    FileHandler(const std::string& name) : file(name) {{}}\n    ~FileHandler() {{\n        if (file.is_open()) file.close();\n    }}\n}};\n\nvoid {func}() {{\n    FileHandler fh(\"log.txt\");\n}}"
        technical = f"RAII binds the lifecycle of a resource (memory, file handles, network sockets, mutexes) to the lifecycle of a stack-allocated object. When the object is created (Acquisition), it initializes the resource. When the object falls out of scope, C++ guarantees the destructor is called, safely releasing the resource even during stack-unwinding from an exception."
        beginner = f"RAII means that whenever you acquire a resource (like opening a file), you tie it to an object. When the program is done with that object, it automatically cleans up the resource. It's like a room that automatically turns off the lights when you leave."
        title = "RAII (Resource Acquisition Is Initialization)"
        tags = ["educational", "raii", "destructors", "resource-management"]

    else:
        # Templates
        code = f"#include <iostream>\n\n// Template function can accept any type T\ntemplate <typename T>\nT {func}(T a, T b) {{\n    return a + b;\n}}\n\nint main() {{\n    std::cout << {func}(5, 10) << std::endl; // Instantiates {func}<int>\n    std::cout << {func}(5.5, 2.2) << std::endl; // Instantiates {func}<double>\n    return 0;\n}}"
        error = f"Educational: Understanding C++ Templates and type deduction."
        opt_code = f"#include <iostream>\n\ntemplate <typename T>\nT {func}(T a, T b) {{\n    return a + b;\n}}\n\nint main() {{\n    std::cout << {func}(5, 10) << std::endl;\n    std::cout << {func}(5.5, 2.2) << std::endl;\n    return 0;\n}}"
        technical = f"Templates allow you to write generic, type-safe code. When you call a template function, the compiler performs Type Deduction to figure out what type `T` is, and then generates a specific version of that function (instantiation) for that type at compile-time."
        beginner = f"Templates are like cookie cutters. Instead of writing a separate addition function for integers, decimals, and fractions, you write one generic template. When you use it, the compiler stamps out the exact version you need."
        title = "Generic Programming with Templates"
        tags = ["educational", "templates", "generics", "type-deduction"]

    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "educational",
        "instruction": f"Explain the C++ concept: {title}.",
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
            "prevention": "Understanding these core language paradigms prevents anti-patterns and enables advanced C++ design.",
            "optimized_code": opt_code,
            "complexity": {"before": "N/A", "after": "N/A"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Generated C++ Educational Explanations",
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
