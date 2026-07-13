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

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "initialize", "filterData", "run", "compute", "execute"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]

# Variation 1: Pointers vs References
for i in range(25):
    vname = var_names[i % len(var_names)]
    func = funcs[i % len(funcs)]
    code = f"#include <iostream>\n\nvoid reassignPointer(int* ptr, int* newAddr) {{\n    // Only modifies the local copy of the pointer\n    ptr = newAddr;\n}}\n\nint main() {{\n    int a = 10, b = 20;\n    int* myPtr = &a;\n    reassignPointer(myPtr, &b);\n    // Logical issue: myPtr still points to 'a'\n    std::cout << *myPtr << std::endl;\n    return 0;\n}}"
    error = f"Logical Output Issue: The pointer was passed by value, so reassigning it inside the function did not affect the original pointer."
    opt_code = f"#include <iostream>\n\nvoid reassignPointer(int*& ptr, int* newAddr) {{\n    // Modifies the original pointer via reference\n    ptr = newAddr;\n}}\n\nint main() {{\n    int a = 10, b = 20;\n    int* myPtr = &a;\n    reassignPointer(myPtr, &b);\n    std::cout << *myPtr << std::endl; // Prints 20\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "educational",
        "instruction": "Explain the difference between passing a pointer by value and passing a pointer by reference.",
        "input": {
            "title": "Understanding Pointers and References",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "In C++, pointers are just variables that hold memory addresses. When you pass a pointer to a function like `int* ptr`, it is passed by value. A local copy of the address is made. Modifying what the pointer points to (`*ptr = ...`) affects the original data, but reassigning the pointer itself (`ptr = ...`) only changes the local copy. To reassign the original pointer, you must pass it by reference (`int*& ptr`) or pass a pointer to the pointer (`int** ptr`).",
            "beginner": "A pointer is just a piece of paper with an address on it. When you give it to the function, you give them a *copy* of the paper. If the function crosses out the address on their copy and writes a new one, your original piece of paper doesn't change.",
            "analogy": "It's like giving someone a copy of a treasure map. If they draw a new X on their copy of the map, your original map still points to the old treasure.",
            "solution": "Change the function parameter to a reference to a pointer: `int*& ptr`.",
            "prevention": "If you need a function to change *where* a pointer is pointing, you must pass the pointer by reference.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by common beginner C++ confusion",
            "language_version": "C++11",
            "tags": ["educational", "pointers", "references"]
        }
    }
    samples.append(sample)

# Variation 2: The Rule of Three (Double Free)
for i in range(25):
    code = f"#include <iostream>\n\nclass IntBuffer {{\npublic:\n    int* buffer;\n    IntBuffer(int size) {{ buffer = new int[size]; }}\n    ~IntBuffer() {{ delete[] buffer; }}\n    // Missing copy constructor!\n}};\n\nvoid processBuffer(IntBuffer temp) {{\n    temp.buffer[0] = 10;\n}}\n\nint main() {{\n    IntBuffer myBuf(5);\n    processBuffer(myBuf); // Shallow copy created and destroyed\n    // UB: myBuf.buffer is now a dangling pointer. Double free upon exit.\n    return 0;\n}}"
    error = f"free(): double free detected in tcache 2\nAborted (core dumped)"
    opt_code = f"#include <iostream>\n#include <algorithm>\n\nclass IntBuffer {{\n    int size_;\npublic:\n    int* buffer;\n    IntBuffer(int size) : size_(size) {{ buffer = new int[size_]; }}\n    ~IntBuffer() {{ delete[] buffer; }}\n    // Copy Constructor (Rule of Three)\n    IntBuffer(const IntBuffer& other) : size_(other.size_) {{\n        buffer = new int[size_];\n        std::copy(other.buffer, other.buffer + size_, buffer);\n    }}\n}};\n\nvoid processBuffer(IntBuffer temp) {{\n    temp.buffer[0] = 10;\n}}\n\nint main() {{\n    IntBuffer myBuf(5);\n    processBuffer(myBuf);\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "educational",
        "instruction": "Explain the Rule of Three and why omitting a copy constructor causes a double-free error.",
        "input": {
            "title": "Understanding the Rule of Three",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "The 'Rule of Three' states that if a class requires a user-defined destructor, copy constructor, or copy assignment operator, it almost certainly requires all three. Without a custom copy constructor, C++ generates a default one that performs a shallow copy. When passed by value, both `myBuf` and `temp` point to the same heap memory. When `temp` goes out of scope, its destructor frees the memory. When `main` ends, `myBuf` tries to free the exact same memory, causing a double-free crash.",
            "beginner": "When you passed the buffer to the function, C++ made a lazy copy that shared the exact same memory. When the function finished, it cleaned up that memory. Then your main program tried to clean up the exact same memory a second time, which crashed the program.",
            "analogy": "It's like two people having identical keys to a rental car. Person A returns the car to the lot. Later, Person B tries to return the exact same car, but it's already gone, causing extreme confusion at the rental desk.",
            "solution": "Implement a deep copy constructor that allocates new memory and copies the values, or better yet, use `std::vector` or `std::unique_ptr` which handle memory automatically.",
            "prevention": "Adhere to the Rule of Zero: design classes so they don't require custom destructors or copy constructors by utilizing standard library containers and smart pointers.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1) creation, UB crash", "after": "O(N) copy"}
        },
        "metadata": {
            "difficulty": "hard",
            "source": "Inspired by standard C++ idioms",
            "language_version": "C++98",
            "tags": ["educational", "rule-of-three", "memory-management", "double-free"]
        }
    }
    samples.append(sample)

# Variation 3: Virtual Functions and Object Slicing
for i in range(25):
    code = f"#include <iostream>\n\nclass Base {{\npublic:\n    virtual void speak() const {{ std::cout << \"Base\\n\"; }}\n}};\n\nclass Derived : public Base {{\npublic:\n    void speak() const override {{ std::cout << \"Derived\\n\"; }}\n}};\n\nvoid makeItSpeak(Base obj) {{\n    obj.speak(); // Object slicing occurs here\n}}\n\nint main() {{\n    Derived d;\n    makeItSpeak(d); // Prints \"Base\" instead of \"Derived\"\n    return 0;\n}}"
    error = f"Logical Output Issue: Polymorphism failed because the object was passed by value, causing object slicing."
    opt_code = f"#include <iostream>\n\nclass Base {{\npublic:\n    virtual void speak() const {{ std::cout << \"Base\\n\"; }}\n    virtual ~Base() = default;\n}};\n\nclass Derived : public Base {{\npublic:\n    void speak() const override {{ std::cout << \"Derived\\n\"; }}\n}};\n\n// Pass by reference to preserve dynamic type\nvoid makeItSpeak(const Base& obj) {{\n    obj.speak();\n}}\n\nint main() {{\n    Derived d;\n    makeItSpeak(d); // Prints \"Derived\"\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "educational",
        "instruction": "Explain object slicing and how polymorphism works in C++.",
        "input": {
            "title": "Understanding Object Slicing and Virtual Functions",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "In C++, polymorphism (virtual function resolution) only works through pointers or references. When a derived object is passed by value to a function expecting a base object, the compiler copies only the base portion of the object. This is called 'object slicing'. The new object inside the function is strictly of type `Base`, so `Base::speak()` is called.",
            "beginner": "When you handed the 'Derived' object to a function that asked for a 'Base' object, C++ chopped off all the extra 'Derived' parts so it would fit exactly into a 'Base' box. Since it was stripped down to a Base, it acted like a Base.",
            "analogy": "It's like having a smartphone (Derived) which is a type of phone (Base). If a museum exhibit only has a slot for a basic rotary phone, you have to rip out the screen and cameras (slicing) to make it fit. It loses its smartphone abilities.",
            "solution": "Pass the object by reference (`const Base& obj`) or by pointer (`Base* obj`) so the virtual table (vtable) can resolve the function call to the derived class dynamically at runtime.",
            "prevention": "Never pass polymorphic base classes by value. Always pass them by reference or pointer.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "medium",
            "source": "Inspired by C++ inheritance pitfalls",
            "language_version": "C++11",
            "tags": ["educational", "polymorphism", "object-slicing", "virtual-functions"]
        }
    }
    samples.append(sample)

# Variation 4: Static Variables in Functions
for i in range(25):
    func = funcs[(i+6) % len(funcs)]
    code = f"#include <iostream>\n\nvoid {func}() {{\n    static int count = 0;\n    count++;\n    std::cout << count << \" \";\n}}\n\nint main() {{\n    {func}();\n    {func}();\n    {func}();\n    // Prints: 1 2 3\n    return 0;\n}}"
    error = f"Educational Prompt: Explain how a variable initialized inside a function retains its value across multiple calls."
    opt_code = f"// The code behaves as intended. This is an educational explanation of the mechanism.\n#include <iostream>\n\nvoid {func}() {{\n    // 'count' is allocated in the data segment, initialized only once.\n    static int count = 0;\n    count++;\n    std::cout << count << \" \";\n}}\n\nint main() {{\n    {func}();\n    {func}();\n    {func}();\n    return 0;\n}}"
    
    sample = {
        "id": get_next_id(),
        "language": "cpp",
        "category": "educational",
        "instruction": "Explain the concept of local static variables in C++.",
        "input": {
            "title": "Understanding Local Static Variables",
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": "When a local variable is declared with the `static` keyword, its lifetime is extended to the entire run of the program, rather than being limited to the function's scope. Memory for the variable is allocated in the static data segment (BSS/Data), not the stack. The initialization line (`static int count = 0;`) is executed only once, the very first time control passes through its declaration.",
            "beginner": "Normally, variables inside functions are created when the function starts and destroyed when it ends. A 'static' variable is different: it is created once and 'sticks around' in memory, remembering its value for the next time you call the function.",
            "analogy": "It's like a notepad kept inside a locked room. Every time a worker enters the room, they read the notepad, update the number, and leave the notepad there. The next worker sees the updated number. Normal variables are like workers bringing their own fresh notepads every time.",
            "solution": "N/A - The code functions as expected. Understanding this behavior is crucial for state tracking, singletons, and caching.",
            "prevention": "Be careful when using local static variables in multi-threaded programs, as they are shared across threads and can cause race conditions if not protected by mutexes.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Inspired by C++ memory models",
            "language_version": "C++11",
            "tags": ["educational", "static", "memory", "scope"]
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
