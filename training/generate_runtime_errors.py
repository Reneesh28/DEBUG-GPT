import json
import os
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir("datasets/runtime_errors/cpp")
ensure_dir("datasets/runtime_errors/python")

var_types = ["int", "float", "double", "char", "long"]
var_names = ["count", "total", "index", "sum", "average", "result", "value", "temp", "max_val", "min_val", "counter", "limit", "threshold", "score", "age", "size", "length", "width", "height", "depth"]
func_names = ["calculate", "process", "compute", "execute", "run", "start", "initialize", "update", "render", "display", "fetch", "load", "save", "delete", "create", "read", "write", "parse", "validate", "verify"]
classes = ["Manager", "Handler", "Processor", "Controller", "Service", "Repository", "Factory", "Builder", "Observer", "Strategy"]

def get_unique_name(pool, i):
    return f"{pool[i % len(pool)]}_{i}"

def generate_cpp_samples():
    cpp_files = {
        "segmentation_fault.json": [],
        "division_by_zero.json": [],
        "out_of_bounds.json": [],
        "stack_overflow.json": [],
        "memory_leak.json": [],
        "use_after_free.json": [],
        "uninitialized_variable.json": [],
        "logic_error_exception.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"CP_RUNTIME_{total_id:06d}"

    # 1. Segmentation Fault (62)
    for i in range(62):
        ptr = get_unique_name(var_names, i)
        cpp_files["segmentation_fault.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the segmentation fault caused by dereferencing a null pointer.",
            "input": {
                "title": "Null Pointer Dereference",
                "code": f"#include <iostream>\n\nint main() {{\n    int* {ptr} = nullptr;\n    std::cout << *{ptr} << std::endl;\n    return 0;\n}}\n",
                "error_message": "Segmentation fault (core dumped)"
            },
            "output": {
                "technical": f"A segmentation fault occurs because the pointer `{ptr}` is initialized to `nullptr` and then dereferenced. The program attempts to access a memory address it does not have permission to read.",
                "beginner": f"You are trying to read a value from a pointer (`{ptr}`) that doesn't point to anything (it's null).",
                "analogy": "It's like trying to open a door that doesn't exist. You end up walking into a wall.",
                "solution": f"Ensure `{ptr}` points to valid memory before dereferencing it, for example, by allocating memory with `new int` or pointing it to an existing variable.",
                "prevention": "Always initialize pointers and check if they are null before dereferencing them.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int val = 10;\n    int* {ptr} = &val;\n    std::cout << *{ptr} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["pointers", "segmentation-fault", "memory"]}
        })

    # 2. Division by Zero (62)
    for i in range(62):
        denom = get_unique_name(var_names, i)
        cpp_files["division_by_zero.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the division by zero error.",
            "input": {
                "title": "Integer Division by Zero",
                "code": f"#include <iostream>\n\nint main() {{\n    int total = 100;\n    int {denom} = 0;\n    int result = total / {denom};\n    std::cout << result << std::endl;\n    return 0;\n}}\n",
                "error_message": "Floating point exception (core dumped)"
            },
            "output": {
                "technical": f"The program performs integer division where the denominator `{denom}` is zero. This causes a hardware exception (SIGFPE) on most platforms.",
                "beginner": "You are trying to divide a number by zero, which is mathematically undefined and crashes the program.",
                "analogy": "It's like trying to share a pizza among zero people. It doesn't make sense and breaks reality.",
                "solution": f"Check if `{denom}` is zero before performing the division.",
                "prevention": "Always validate user input or logic that dictates the denominator before dividing.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int total = 100;\n    int {denom} = 0;\n    if ({denom} != 0) {{\n        int result = total / {denom};\n        std::cout << result << std::endl;\n    }} else {{\n        std::cout << \"Cannot divide by zero.\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["math", "division-by-zero", "exception"]}
        })

    # 3. Out of Bounds (62)
    for i in range(62):
        arr = get_unique_name(var_names, i)
        cpp_files["out_of_bounds.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the array index out of bounds error.",
            "input": {
                "title": "Vector Out of Bounds",
                "code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {arr} = {{1, 2, 3}};\n    std::cout << {arr}.at(5) << std::endl;\n    return 0;\n}}\n",
                "error_message": "terminate called after throwing an instance of 'std::out_of_range'\n  what():  vector::_M_range_check: __n (which is 5) >= this->size() (which is 3)\nAborted (core dumped)"
            },
            "output": {
                "technical": f"The `at()` method performs bounds checking and throws `std::out_of_range` because the index 5 is greater than or equal to the vector's size (3).",
                "beginner": "You are trying to access the 6th item in a list that only has 3 items.",
                "analogy": "It's like trying to open the 5th drawer in a cabinet that only has 3 drawers.",
                "solution": "Ensure the index used to access the vector is less than its size.",
                "prevention": "Use bounds-checking methods like `at()` or ensure your loop bounds are strictly less than `size()`.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {arr} = {{1, 2, 3}};\n    if ({arr}.size() > 5) {{\n        std::cout << {arr}.at(5) << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["vector", "out-of-bounds", "exception"]}
        })

    # 4. Stack Overflow (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        cpp_files["stack_overflow.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the infinite recursion causing a stack overflow.",
            "input": {
                "title": "Infinite Recursion",
                "code": f"#include <iostream>\n\nvoid {fn}() {{\n    {fn}();\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "error_message": "Segmentation fault (core dumped) // Due to stack exhaustion"
            },
            "output": {
                "technical": f"The function `{fn}` calls itself infinitely without a base case. This exhausts the call stack, resulting in a stack overflow and a segmentation fault.",
                "beginner": "Your function keeps calling itself forever, and the computer runs out of memory to keep track of it.",
                "analogy": "It's like two mirrors facing each other, creating an endless tunnel of reflections. Eventually, it has to stop.",
                "solution": "Add a base case to stop the recursion.",
                "prevention": "Always define a termination condition (base case) for recursive functions.",
                "optimized_code": f"#include <iostream>\n\nvoid {fn}(int limit) {{\n    if (limit <= 0) return;\n    {fn}(limit - 1);\n}}\n\nint main() {{\n    {fn}(5);\n    return 0;\n}}\n",
                "complexity": {"before": "O(infinity)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["recursion", "stack-overflow"]}
        })

    # 5. Memory Leak (63)
    for i in range(63):
        ptr = get_unique_name(var_names, i)
        cpp_files["memory_leak.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the memory leak by deallocating memory.",
            "input": {
                "title": "Memory Leak",
                "code": f"#include <iostream>\n\nvoid run() {{\n    int* {ptr} = new int[100];\n}}\n\nint main() {{\n    run();\n    return 0;\n}}\n",
                "error_message": "Memory Leak (Detected by tools like Valgrind or AddressSanitizer, no immediate crash)"
            },
            "output": {
                "technical": f"Memory is allocated on the heap using `new int[100]` for `{ptr}`, but it is never freed using `delete[]`. This causes a memory leak.",
                "beginner": "You borrowed memory from the computer but never gave it back. If you do this enough, the computer runs out of memory.",
                "analogy": "It's like borrowing books from a library and never returning them. Eventually, the library runs out of books.",
                "solution": f"Use `delete[] {ptr};` before the function ends, or better, use smart pointers.",
                "prevention": "Prefer using `std::vector` or `std::unique_ptr` over raw pointers to automate memory management.",
                "optimized_code": f"#include <iostream>\n#include <memory>\n\nvoid run() {{\n    std::unique_ptr<int[]> {ptr}(new int[100]);\n}}\n\nint main() {{\n    run();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["memory-leak", "pointers"]}
        })

    # 6. Use After Free (63)
    for i in range(63):
        ptr = get_unique_name(var_names, i)
        cpp_files["use_after_free.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the use-after-free vulnerability.",
            "input": {
                "title": "Use After Free",
                "code": f"#include <iostream>\n\nint main() {{\n    int* {ptr} = new int(42);\n    delete {ptr};\n    std::cout << *{ptr} << std::endl;\n    return 0;\n}}\n",
                "error_message": "Undefined behavior / Heap-use-after-free (Detected by AddressSanitizer)"
            },
            "output": {
                "technical": f"The pointer `{ptr}` is dereferenced after the memory it points to has been deallocated with `delete`. This is undefined behavior and often leads to crashes or security vulnerabilities.",
                "beginner": "You are trying to read a value from memory that you already told the computer it could recycle.",
                "analogy": "It's like returning the keys to a rental car, but then trying to get back into the car later.",
                "solution": f"Do not access `{ptr}` after deleting it. Setting it to `nullptr` can help prevent accidental use.",
                "prevention": "Set pointers to `nullptr` immediately after deletion, or use smart pointers.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int* {ptr} = new int(42);\n    std::cout << *{ptr} << std::endl;\n    delete {ptr};\n    {ptr} = nullptr;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "hard", "source": "synthetic", "language_version": "C++17", "tags": ["memory", "use-after-free"]}
        })

    # 7. Uninitialized Variable (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["uninitialized_variable.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Fix the uninitialized variable usage.",
            "input": {
                "title": "Uninitialized Local Variable",
                "code": f"#include <iostream>\n\nint main() {{\n    int {vn};\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": "Garbage value printed / Undefined behavior"
            },
            "output": {
                "technical": f"The local variable `{vn}` is declared but not initialized. Reading from an uninitialized local variable is undefined behavior in C++ and usually results in a garbage value.",
                "beginner": "You created a variable but didn't give it a starting value, so it just holds whatever random data was left over in memory.",
                "analogy": "It's like picking up a random piece of scratch paper and assuming it's blank, but someone else wrote a random number on it earlier.",
                "solution": "Initialize the variable when you declare it.",
                "prevention": "Always initialize variables upon declaration.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 0;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["uninitialized", "undefined-behavior"]}
        })

    # 8. Logic Error Exception (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["logic_error_exception.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "runtime_error",
            "instruction": "Handle the exception thrown by std::stoi.",
            "input": {
                "title": "Uncaught Exception",
                "code": f"#include <iostream>\n#include <string>\n\nint main() {{\n    std::string text = \"abc\";\n    int {vn} = std::stoi(text);\n    return 0;\n}}\n",
                "error_message": "terminate called after throwing an instance of 'std::invalid_argument'\n  what():  stoi\nAborted (core dumped)"
            },
            "output": {
                "technical": "The `std::stoi` function throws a `std::invalid_argument` exception because the string 'abc' cannot be converted to an integer. The exception is uncaught, causing the program to terminate.",
                "beginner": "You tried to convert the word 'abc' into a number, which doesn't make sense, so the program panicked and crashed.",
                "analogy": "It's like asking someone to translate 'apple' into a number. They don't know how, so they just stop working.",
                "solution": "Use a `try-catch` block to handle the exception gracefully.",
                "prevention": "Wrap functions that can throw exceptions in `try-catch` blocks.",
                "optimized_code": f"#include <iostream>\n#include <string>\n#include <stdexcept>\n\nint main() {{\n    std::string text = \"abc\";\n    try {{\n        int {vn} = std::stoi(text);\n    }} catch (const std::invalid_argument& e) {{\n        std::cout << \"Invalid argument: \" << e.what() << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["exception", "conversion"]}
        })

    for filename, content in cpp_files.items():
        with open(f"datasets/runtime_errors/cpp/{filename}", "w") as f:
            json.dump(content, f, indent=2)

def generate_python_samples():
    py_files = {
        "index_error.json": [],
        "key_error.json": [],
        "type_error.json": [],
        "value_error.json": [],
        "zero_division_error.json": [],
        "attribute_error.json": [],
        "name_error.json": [],
        "recursion_error.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"PY_RUNTIME_{total_id:06d}"

    # 1. IndexError (62)
    for i in range(62):
        arr = get_unique_name(var_names, i)
        py_files["index_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the IndexError caused by accessing a non-existent list element.",
            "input": {
                "title": "IndexError",
                "code": f"{arr} = [1, 2, 3]\nprint({arr}[5])\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 2, in <module>\n    print({arr}[5])\nIndexError: list index out of range"
            },
            "output": {
                "technical": "An `IndexError` is raised because you are attempting to access index 5 in a list that only has elements up to index 2.",
                "beginner": "You asked for the 6th item in a list that only contains 3 items.",
                "analogy": "It's like asking for the 10th page in a 5-page book.",
                "solution": "Check the length of the list before accessing the index, or use a valid index.",
                "prevention": "Ensure index values are always strictly less than `len(list)`.",
                "optimized_code": f"{arr} = [1, 2, 3]\nif len({arr}) > 5:\n    print({arr}[5])\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["list", "index-error"]}
        })

    # 2. KeyError (62)
    for i in range(62):
        dct = get_unique_name(var_names, i)
        py_files["key_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the KeyError from accessing a missing dictionary key.",
            "input": {
                "title": "KeyError",
                "code": f"{dct} = {{'a': 1, 'b': 2}}\nprint({dct}['c'])\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 2, in <module>\n    print({dct}['c'])\nKeyError: 'c'"
            },
            "output": {
                "technical": "A `KeyError` is raised when trying to access a dictionary key ('c') that does not exist in the dictionary.",
                "beginner": "You looked for a label ('c') in the dictionary, but it hasn't been added yet.",
                "analogy": "It's like trying to call a friend named 'Alice' using your phone contacts, but she isn't saved in your phone.",
                "solution": "Use the `.get()` method which returns `None` (or a default value) instead of crashing, or check if the key exists using `in`.",
                "prevention": "Use `.get()` when you aren't absolutely sure a key exists.",
                "optimized_code": f"{dct} = {{'a': 1, 'b': 2}}\nprint({dct}.get('c', 'Not found'))\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["dict", "key-error"]}
        })

    # 3. TypeError (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["type_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the TypeError caused by adding incompatible types.",
            "input": {
                "title": "TypeError",
                "code": f"{vn} = 10 + \"20\"\nprint({vn})\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    {vn} = 10 + \"20\"\nTypeError: unsupported operand type(s) for +: 'int' and 'str'"
            },
            "output": {
                "technical": "A `TypeError` occurs because Python does not implicitly convert strings to integers for addition.",
                "beginner": "You tried to add a number and a word together. Python doesn't know if you want to do math (10 + 20) or glue words together ('1020').",
                "analogy": "It's like trying to multiply apples by oranges. They are different things.",
                "solution": "Convert the string to an integer using `int()` before adding.",
                "prevention": "Ensure variables are of the correct type before performing operations on them.",
                "optimized_code": f"{vn} = 10 + int(\"20\")\nprint({vn})\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["types", "type-error"]}
        })

    # 4. ValueError (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["value_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the ValueError during conversion.",
            "input": {
                "title": "ValueError",
                "code": f"{vn} = int(\"hello\")\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    {vn} = int(\"hello\")\nValueError: invalid literal for int() with base 10: 'hello'"
            },
            "output": {
                "technical": "A `ValueError` is raised because the string 'hello' does not contain a valid base-10 integer representation, so `int()` fails.",
                "beginner": "You tried to turn the word 'hello' into a number, which doesn't make sense.",
                "analogy": "It's like asking a calculator to solve 'banana' plus 5.",
                "solution": "Ensure the string contains only digits before calling `int()`, or handle the error using try-except.",
                "prevention": "Validate user input or string data before converting to integers.",
                "optimized_code": f"try:\n    {vn} = int(\"hello\")\nexcept ValueError:\n    {vn} = 0\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["conversion", "value-error"]}
        })

    # 5. ZeroDivisionError (63)
    for i in range(63):
        denom = get_unique_name(var_names, i)
        py_files["zero_division_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the ZeroDivisionError.",
            "input": {
                "title": "ZeroDivisionError",
                "code": f"{denom} = 0\nresult = 100 / {denom}\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 2, in <module>\n    result = 100 / {denom}\nZeroDivisionError: division by zero"
            },
            "output": {
                "technical": "A `ZeroDivisionError` is raised when the second argument of a division or modulo operation is zero.",
                "beginner": "You tried to divide by zero, which is impossible.",
                "analogy": "If you have 100 pieces of candy and divide them among 0 people, how many does each person get? It breaks reality.",
                "solution": "Check if the denominator is zero before dividing, or use try-except.",
                "prevention": "Always guard division operations if the denominator comes from an untrusted or variable source.",
                "optimized_code": f"{denom} = 0\nresult = 100 / {denom} if {denom} != 0 else 0\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["math", "zero-division"]}
        })

    # 6. AttributeError (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["attribute_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the AttributeError on a NoneType object.",
            "input": {
                "title": "AttributeError",
                "code": f"{vn} = None\n{vn}.append(5)\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 2, in <module>\n    {vn}.append(5)\nAttributeError: 'NoneType' object has no attribute 'append'"
            },
            "output": {
                "technical": "An `AttributeError` is raised because the variable is `None` (a `NoneType` object), which does not have an `append` method like a list does.",
                "beginner": "You tried to add an item to something that is completely empty (None), rather than an actual list.",
                "analogy": "It's like trying to put groceries into a cart, but you don't actually have a cart yet.",
                "solution": "Initialize the variable as an empty list `[]` instead of `None`.",
                "prevention": "Ensure variables are instantiated to their correct object types before calling methods on them.",
                "optimized_code": f"{vn} = []\n{vn}.append(5)\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["none", "attribute-error"]}
        })

    # 7. NameError (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["name_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the NameError caused by an undefined variable.",
            "input": {
                "title": "NameError",
                "code": f"print({vn})\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    print({vn})\nNameError: name '{vn}' is not defined"
            },
            "output": {
                "technical": f"A `NameError` is raised because the local or global name `{vn}` has not been bound to any value.",
                "beginner": f"You told Python to print `{vn}`, but you never created `{vn}` or gave it a value.",
                "analogy": "It's like asking a teacher for 'that student's' grade, but you haven't said who 'that student' is.",
                "solution": f"Assign a value to `{vn}` before trying to use it.",
                "prevention": "Check for typos in variable names and ensure they are assigned before use.",
                "optimized_code": f"{vn} = 0\nprint({vn})\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["variables", "name-error"]}
        })

    # 8. RecursionError (63)
    for i in range(63):
        fn = get_unique_name(func_names, i)
        py_files["recursion_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "runtime_error",
            "instruction": "Fix the infinite recursion.",
            "input": {
                "title": "RecursionError",
                "code": f"def {fn}():\n    return {fn}()\n\n{fn}()\n",
                "error_message": f"Traceback (most recent call last):\n  File \"main.py\", line 4, in <module>\n    {fn}()\n  File \"main.py\", line 2, in {fn}\n    return {fn}()\nRecursionError: maximum recursion depth exceeded"
            },
            "output": {
                "technical": "A `RecursionError` is raised because the function calls itself infinitely without a base case, hitting Python's maximum recursion depth.",
                "beginner": "Your function is stuck in an endless loop calling itself.",
                "analogy": "Like looking into two mirrors facing each other, it never ends.",
                "solution": "Add a base case to your recursive function to tell it when to stop.",
                "prevention": "Ensure all recursive functions have a condition that will eventually be met to stop the recursion.",
                "optimized_code": f"def {fn}(limit):\n    if limit <= 0:\n        return\n    return {fn}(limit - 1)\n\n{fn}(5)\n",
                "complexity": {"before": "O(infinity)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["recursion", "recursion-error"]}
        })

    for filename, content in py_files.items():
        with open(f"datasets/runtime_errors/python/{filename}", "w") as f:
            json.dump(content, f, indent=2)

if __name__ == "__main__":
    generate_cpp_samples()
    generate_python_samples()
    print("Generated 500 C++ and 500 Python samples for Runtime Errors.")
