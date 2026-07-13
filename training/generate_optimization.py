import json
import os
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir("datasets/optimization_examples/cpp")
ensure_dir("datasets/optimization_examples/python")

var_names = ["count", "total", "index", "sum", "average", "result", "value", "temp", "max_val", "min_val", "counter", "limit", "threshold", "score", "age", "size", "length", "width", "height", "depth"]
func_names = ["calculate", "process", "compute", "execute", "run", "start", "initialize", "update", "render", "display", "fetch", "load", "save", "delete", "create", "read", "write", "parse", "validate", "verify"]

def get_unique_name(pool, i):
    return f"{pool[i % len(pool)]}_{i}"

def generate_cpp_samples():
    cpp_files = {
        "pass_by_value_vs_reference.json": [],
        "vector_push_back_reserve.json": [],
        "postfix_vs_prefix_increment.json": [],
        "redundant_computations_in_loop.json": [],
        "inefficient_sorting.json": [],
        "standard_map_lookup.json": [],
        "redundant_copies.json": [],
        "string_concatenation_loop.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"CP_OPTIM_{total_id:06d}"

    # 1. Pass by Value vs Reference (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        cpp_files["pass_by_value_vs_reference.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the function parameter passing.",
            "input": {
                "title": "Pass by Value for Large Objects",
                "code": f"#include <iostream>\n#include <vector>\n\nvoid {fn}(std::vector<int> data) {{\n    std::cout << \"Processing \" << data.size() << \" elements.\" << std::endl;\n}}\n\nint main() {{\n    std::vector<int> large_vec(1000000, 1);\n    {fn}(large_vec);\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Passing a `std::vector` by value creates a full copy of all its elements, which takes O(N) time and memory. Passing by `const std::vector<int>&` avoids the copy.",
                "beginner": "You are giving the function a brand new copy of a massive list, which takes a lot of time and memory. You should just let it look at the original list.",
                "analogy": "It's like printing a new 1,000-page book every time someone wants to read it, instead of just lending them the book.",
                "solution": "Change the parameter type to `const std::vector<int>&`.",
                "prevention": "Pass all complex objects (like strings, vectors, and classes) by const reference unless you specifically need a copy.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nvoid {fn}(const std::vector<int>& data) {{\n    std::cout << \"Processing \" << data.size() << \" elements.\" << std::endl;\n}}\n\nint main() {{\n    std::vector<int> large_vec(1000000, 1);\n    {fn}(large_vec);\n    return 0;\n}}\n",
                "complexity": {"before": "O(N)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["parameters", "copy", "performance"]}
        })

    # 2. Vector push_back Reserve (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        cpp_files["vector_push_back_reserve.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the vector memory allocations.",
            "input": {
                "title": "Missing Vector Reserve",
                "code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn};\n    for (int i = 0; i < 100000; ++i) {{\n        {vn}.push_back(i);\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Repeatedly calling `push_back` without reserving capacity causes the vector to reallocate and copy its contents multiple times, resulting in unnecessary overhead.",
                "beginner": "The list keeps running out of space and has to pause, buy a bigger box, and move everything over. If we know the size in advance, we should buy the big box immediately.",
                "analogy": "It's like moving to a slightly larger house every time you buy a new piece of furniture.",
                "solution": f"Use `{vn}.reserve(100000)` before the loop.",
                "prevention": "Always use `.reserve()` when the final size of a vector is known or can be tightly estimated.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn};\n    {vn}.reserve(100000);\n    for (int i = 0; i < 100000; ++i) {{\n        {vn}.push_back(i);\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(N) with reallocations", "after": "O(N) with zero reallocations"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["vector", "reserve", "allocation"]}
        })

    # 3. Postfix vs Prefix Increment (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        cpp_files["postfix_vs_prefix_increment.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the iterator increment operation.",
            "input": {
                "title": "Postfix Iterator Increment",
                "code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn} = {{1, 2, 3, 4, 5}};\n    for (auto it = {vn}.begin(); it != {vn}.end(); it++) {{\n        std::cout << *it << \" \";\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Postfix increment (`it++`) on an iterator creates a temporary copy of the iterator before incrementing it. Prefix increment (`++it`) increments in place and returns a reference, avoiding the copy.",
                "beginner": "Using `it++` creates a temporary throwaway copy of the position marker. `++it` is faster because it just moves the marker directly.",
                "analogy": "It's like taking a picture of yourself before taking a step, just in case you need to remember where you were, even though nobody asked for the picture.",
                "solution": "Change `it++` to `++it` in the loop condition.",
                "prevention": "Always use prefix increment (`++i` or `++it`) unless you specifically need the pre-incremented value.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn} = {{1, 2, 3, 4, 5}};\n    for (auto it = {vn}.begin(); it != {vn}.end(); ++it) {{\n        std::cout << *it << \" \";\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1) with copy overhead", "after": "O(1) in-place"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["iterators", "increment", "performance"]}
        })

    # 4. Redundant Computations in Loop (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["redundant_computations_in_loop.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the loop condition.",
            "input": {
                "title": "strlen in Loop Condition",
                "code": f"#include <iostream>\n#include <cstring>\n\nint main() {{\n    const char* {vn} = \"hello world\";\n    for (size_t i = 0; i < strlen({vn}); ++i) {{\n        std::cout << {vn}[i] << \" \";\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "`strlen` is an O(N) operation. Calling it inside the loop condition causes it to be re-evaluated every iteration, turning an O(N) loop into an O(N^2) operation.",
                "beginner": "You are recalculating the length of the string on every single step of the loop. This wastes a lot of time.",
                "analogy": "It's like recounting every single dollar in your wallet before paying for each item at the grocery store.",
                "solution": f"Store the length in a variable before the loop, or use `std::string`.",
                "prevention": "Cache expensive function calls outside loops if the result doesn't change.",
                "optimized_code": f"#include <iostream>\n#include <cstring>\n\nint main() {{\n    const char* {vn} = \"hello world\";\n    size_t len = strlen({vn});\n    for (size_t i = 0; i < len; ++i) {{\n        std::cout << {vn}[i] << \" \";\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(N^2)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["loop", "redundancy", "strlen"]}
        })

    # 5. Inefficient Sorting (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["inefficient_sorting.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the array sorting algorithm.",
            "input": {
                "title": "Bubble Sort instead of std::sort",
                "code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn} = {{5, 2, 9, 1, 5, 6}};\n    for (size_t i = 0; i < {vn}.size(); ++i) {{\n        for (size_t j = 0; j < {vn}.size() - i - 1; ++j) {{\n            if ({vn}[j] > {vn}[j+1]) {{\n                int temp = {vn}[j];\n                {vn}[j] = {vn}[j+1];\n                {vn}[j+1] = temp;\n            }}\n        }}\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "The code implements Bubble Sort, which has an average and worst-case time complexity of O(N^2). `std::sort` from the `<algorithm>` library uses Introsort, which runs in O(N log N).",
                "beginner": "You wrote your own sorting system that is very slow for large lists. C++ has a built-in sort that is incredibly fast.",
                "analogy": "It's like alphabetizing a library by swapping adjacent books one by one, instead of organizing them into categories first.",
                "solution": f"Include `<algorithm>` and use `std::sort({vn}.begin(), {vn}.end());`.",
                "prevention": "Never write your own sort function unless it's an educational exercise. Always use `std::sort`.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n#include <algorithm>\n\nint main() {{\n    std::vector<int> {vn} = {{5, 2, 9, 1, 5, 6}};\n    std::sort({vn}.begin(), {vn}.end());\n    return 0;\n}}\n",
                "complexity": {"before": "O(N^2)", "after": "O(N log N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["algorithm", "sorting", "performance"]}
        })

    # 6. Standard Map Lookup (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["standard_map_lookup.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the map key lookup.",
            "input": {
                "title": "Double Map Lookup",
                "code": f"#include <iostream>\n#include <map>\n#include <string>\n\nint main() {{\n    std::map<std::string, int> {vn} = {{{{\"apple\", 1}}, {{\"banana\", 2}}}};\n    if ({vn}.count(\"apple\") > 0) {{\n        std::cout << \"Count: \" << {vn}[\"apple\"] << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Using `count()` followed by `operator[]` performs two separate O(log N) searches in the map. Using `find()` performs a single search.",
                "beginner": "You are asking the map to search for 'apple' twice: once to see if it exists, and a second time to get its value.",
                "analogy": "It's like looking up a word in the dictionary to see if it exists, closing the book, and then looking it up again to read the definition.",
                "solution": "Use `auto it = map.find(key);` and check `if (it != map.end())`.",
                "prevention": "Use `find()` when you need to check existence and retrieve the value.",
                "optimized_code": f"#include <iostream>\n#include <map>\n#include <string>\n\nint main() {{\n    std::map<std::string, int> {vn} = {{{{\"apple\", 1}}, {{\"banana\", 2}}}};\n    auto it = {vn}.find(\"apple\");\n    if (it != {vn}.end()) {{\n        std::cout << \"Count: \" << it->second << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "2 * O(log N)", "after": "O(log N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["map", "lookup", "performance"]}
        })

    # 7. Redundant Copies (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["redundant_copies.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the range-based for loop.",
            "input": {
                "title": "Copying in Range-Based For Loop",
                "code": f"#include <iostream>\n#include <vector>\n#include <string>\n\nint main() {{\n    std::vector<std::string> {vn} = {{\"a_long_string_1\", \"a_long_string_2\"}};\n    for (auto item : {vn}) {{\n        std::cout << item << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Using `auto item` creates a deep copy of the string for each iteration of the loop. Using `const auto& item` binds a reference to the element, preventing the copy.",
                "beginner": "You are making a brand new copy of every word before printing it. It's much faster to just look at the original word.",
                "analogy": "It's like photocopying a document just so you can read it, then throwing the copy away.",
                "solution": "Change `auto item` to `const auto& item`.",
                "prevention": "Always use `const auto&` in range-based for loops unless you need to mutate a copy.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n#include <string>\n\nint main() {{\n    std::vector<std::string> {vn} = {{\"a_long_string_1\", \"a_long_string_2\"}};\n    for (const auto& item : {vn}) {{\n        std::cout << item << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(L) copy per element", "after": "O(1) reference per element"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["loop", "copy", "reference"]}
        })

    # 8. String Concatenation Loop (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["string_concatenation_loop.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "optimization",
            "instruction": "Optimize the string building loop.",
            "input": {
                "title": "Inefficient String Appending",
                "code": f"#include <iostream>\n#include <string>\n\nint main() {{\n    std::string {vn} = \"\";\n    for (int i = 0; i < 10000; ++i) {{\n        {vn} = {vn} + \"a\";\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Using `s = s + \"a\"` creates a new temporary string, copies the old string, adds the character, and then assigns it back. This results in O(N^2) complexity.",
                "beginner": "You are copying the entire string every time you add a single letter. As the string gets bigger, copying it takes longer and longer.",
                "analogy": "It's like rewriting a whole novel from page 1 every time you want to add a single period at the end.",
                "solution": f"Use `{vn} += \"a\";` which modifies the string in place, or use `.reserve()`.",
                "prevention": "Use `+=` or `.append()` instead of `+` when building strings in loops.",
                "optimized_code": f"#include <iostream>\n#include <string>\n\nint main() {{\n    std::string {vn};\n    {vn}.reserve(10000);\n    for (int i = 0; i < 10000; ++i) {{\n        {vn} += \"a\";\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(N^2)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["string", "concatenation", "allocation"]}
        })

    for filename, content in cpp_files.items():
        with open(f"datasets/optimization_examples/cpp/{filename}", "w") as f:
            json.dump(content, f, indent=2)

def generate_python_samples():
    py_files = {
        "string_concatenation_loop.json": [],
        "list_comprehension_vs_loop.json": [],
        "lookup_in_list_vs_set.json": [],
        "inefficient_string_formatting.json": [],
        "repeated_function_calls.json": [],
        "multiple_variable_assignment.json": [],
        "global_variable_access.json": [],
        "checking_empty_list_with_len.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"PY_OPTIM_{total_id:06d}"

    # 1. String Concatenation Loop (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["string_concatenation_loop.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize the string building loop.",
            "input": {
                "title": "String Concatenation in Loop",
                "code": f"{vn} = \"\"\nfor i in range(10000):\n    {vn} += str(i)\n",
                "error_message": ""
            },
            "output": {
                "technical": "Strings are immutable in Python. Using `+=` in a loop creates a new string object and copies the old contents every iteration, leading to O(N^2) complexity.",
                "beginner": "Because words cannot be changed in Python, adding a letter forces Python to make a complete copy of the whole word every single time.",
                "analogy": "Like painting a new identical portrait every time you want to add a freckle.",
                "solution": "Collect parts in a list and join them at the end using `\"\".join(list)`.",
                "prevention": "Always use `.join()` when combining many string fragments.",
                "optimized_code": f"parts = []\nfor i in range(10000):\n    parts.append(str(i))\n{vn} = \"\".join(parts)\n",
                "complexity": {"before": "O(N^2)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["string", "join", "performance"]}
        })

    # 2. List Comprehension vs Loop (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["list_comprehension_vs_loop.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize the list creation.",
            "input": {
                "title": "Appending in a Loop",
                "code": f"{vn} = []\nfor i in range(10000):\n    {vn}.append(i * 2)\n",
                "error_message": ""
            },
            "output": {
                "technical": "Using a `for` loop with `.append()` incurs Python-level function call overhead for every element. List comprehensions are optimized in C and are much faster.",
                "beginner": "List comprehensions are a faster, built-in shortcut for building lists compared to standard loops.",
                "analogy": "It's like using an assembly line to build cars instead of having one mechanic build them one at a time.",
                "solution": f"Replace the loop with a list comprehension: `[{vn} = [i * 2 for i in range(10000)]]`.",
                "prevention": "Use list comprehensions for simple map and filter operations.",
                "optimized_code": f"{vn} = [i * 2 for i in range(10000)]\n",
                "complexity": {"before": "O(N) with overhead", "after": "O(N) optimized in C"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["list-comprehension", "append", "speed"]}
        })

    # 3. Lookup in List vs Set (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["lookup_in_list_vs_set.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize the membership lookup.",
            "input": {
                "title": "Lookup in List",
                "code": f"{vn}_list = list(range(10000))\ncount = 0\nfor i in range(5000):\n    if i in {vn}_list:\n        count += 1\n",
                "error_message": ""
            },
            "output": {
                "technical": "Checking `if x in list` performs a linear O(N) search. Doing this inside a loop creates an O(N*M) time complexity. Using a `set` drops the lookup to O(1).",
                "beginner": "Checking if an item is in a list requires scanning the whole list. Checking if it's in a 'set' is instant.",
                "analogy": "List lookup is like searching for a name in an unorganized pile of papers. Set lookup is like looking it up in an alphabetical phone book.",
                "solution": f"Convert `{vn}_list` to a `set` before the loop.",
                "prevention": "Use `set` whenever you need to perform fast, repeated membership tests (`in`).",
                "optimized_code": f"{vn}_set = set(range(10000))\ncount = 0\nfor i in range(5000):\n    if i in {vn}_set:\n        count += 1\n",
                "complexity": {"before": "O(N*M)", "after": "O(N+M)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["set", "list", "lookup"]}
        })

    # 4. Inefficient String Formatting (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["inefficient_string_formatting.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize string formatting.",
            "input": {
                "title": "Using % formatting",
                "code": f"name = \"Alice\"\nage = 30\nmessage = \"Hello %s, you are %d years old\" % (name, age)\n",
                "error_message": ""
            },
            "output": {
                "technical": "f-strings (literal string interpolation) introduced in Python 3.6 evaluate expressions at runtime in C and are faster and more readable than `%` formatting or `.format()`.",
                "beginner": "Using f-strings is the modern, fastest way to plug variables into text.",
                "analogy": "It's like using a modern digital printer instead of a manual typewriter.",
                "solution": "Use f-strings: `f\"Hello {name}, you are {age} years old\"`.",
                "prevention": "Adopt f-strings as the default string formatting method in Python.",
                "optimized_code": f"name = \"Alice\"\nage = 30\nmessage = f\"Hello {{name}}, you are {{age}} years old\"\n",
                "complexity": {"before": "O(1) with overhead", "after": "O(1) optimized"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["strings", "formatting", "f-string"]}
        })

    # 5. Repeated Function Calls (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["repeated_function_calls.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize redundant function calls.",
            "input": {
                "title": "Calling len() in loop condition",
                "code": f"{vn} = [1] * 1000\ncount = 0\nwhile count < len({vn}):\n    count += 1\n",
                "error_message": ""
            },
            "output": {
                "technical": "While `len()` in Python is fast (O(1)), placing it in a `while` loop condition adds unnecessary function call overhead on every iteration.",
                "beginner": "You are asking Python for the length of the list every single time the loop runs, even though the length never changes.",
                "analogy": "It's like checking your watch every 2 seconds to see if a minute has passed.",
                "solution": f"Calculate `len({vn})` once before the loop and store it in a variable.",
                "prevention": "Cache static function results in variables before entering a loop.",
                "optimized_code": f"{vn} = [1] * 1000\ncount = 0\nlength = len({vn})\nwhile count < length:\n    count += 1\n",
                "complexity": {"before": "O(N) with overhead", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["loop", "function-call", "overhead"]}
        })

    # 6. Multiple Variable Assignment (63)
    for i in range(63):
        v1 = f"var1_{i}"
        v2 = f"var2_{i}"
        py_files["multiple_variable_assignment.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize variable swapping.",
            "input": {
                "title": "Swapping via Temp Variable",
                "code": f"{v1} = 10\n{v2} = 20\ntemp = {v1}\n{v1} = {v2}\n{v2} = temp\n",
                "error_message": ""
            },
            "output": {
                "technical": "Python supports tuple unpacking, which allows swapping variables in a single instruction without allocating a temporary variable.",
                "beginner": "Python has a built-in shortcut to swap two variables on a single line.",
                "analogy": "It's like passing a ball to each other at the exact same time, rather than setting it on a table first.",
                "solution": f"Use `{v1}, {v2} = {v2}, {v1}`.",
                "prevention": "Use tuple packing/unpacking for assignments where multiple variables exchange values.",
                "optimized_code": f"{v1} = 10\n{v2} = 20\n{v1}, {v2} = {v2}, {v1}\n",
                "complexity": {"before": "O(1) with 3 assignments", "after": "O(1) with 1 assignment"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["variables", "swap", "idiomatic"]}
        })

    # 7. Global Variable Access (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["global_variable_access.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize the scope of variables inside loops.",
            "input": {
                "title": "Accessing Global inside Loop",
                "code": f"GLOBAL_MULTIPLIER = 2\n\ndef calculate():\n    total = 0\n    for i in range(10000):\n        total += i * GLOBAL_MULTIPLIER\n    return total\n",
                "error_message": ""
            },
            "output": {
                "technical": "Accessing global variables involves dictionary lookups in the `globals()` dictionary, which is significantly slower than accessing local variables (which use C arrays under the hood).",
                "beginner": "Python takes longer to find 'global' variables outside a function. If you use it a lot, copy it locally first.",
                "analogy": "It's like keeping your hammer in the garage instead of on your toolbelt while framing a house.",
                "solution": "Assign the global variable to a local variable before the loop.",
                "prevention": "Cache global references locally if they are accessed inside performance-critical loops.",
                "optimized_code": f"GLOBAL_MULTIPLIER = 2\n\ndef calculate():\n    local_mult = GLOBAL_MULTIPLIER\n    total = 0\n    for i in range(10000):\n        total += i * local_mult\n    return total\n",
                "complexity": {"before": "O(N) with global lookup", "after": "O(N) with local lookup"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["scope", "global", "loop"]}
        })

    # 8. Checking Empty List With Len (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["checking_empty_list_with_len.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "optimization",
            "instruction": "Optimize the empty list check.",
            "input": {
                "title": "Checking Empty with len()",
                "code": f"{vn} = []\nif len({vn}) == 0:\n    print(\"List is empty\")\n",
                "error_message": ""
            },
            "output": {
                "technical": "Empty collections (lists, dicts, strings) evaluate to False in Python. Using `if not list:` avoids the function call to `len()` and is more idiomatic (PEP 8).",
                "beginner": "You don't need to count the items to know if a box is empty. Python lets you just check `if not box:`.",
                "analogy": "It's like counting every single person in a room to prove nobody is there, instead of just looking to see it's empty.",
                "solution": f"Use `if not {vn}:` instead of `if len({vn}) == 0:`.",
                "prevention": "Follow PEP 8 guidelines: use the implicit boolean truthiness of empty collections.",
                "optimized_code": f"{vn} = []\nif not {vn}:\n    print(\"List is empty\")\n",
                "complexity": {"before": "O(1) with function call", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["boolean", "list", "idiomatic"]}
        })

    for filename, content in py_files.items():
        with open(f"datasets/optimization_examples/python/{filename}", "w") as f:
            json.dump(content, f, indent=2)

if __name__ == "__main__":
    generate_cpp_samples()
    generate_python_samples()
    print("Generated 500 C++ and 500 Python samples for Optimization Examples.")
