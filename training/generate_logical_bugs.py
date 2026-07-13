import json
import os
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir("datasets/logical_bugs/cpp")
ensure_dir("datasets/logical_bugs/python")

var_names = ["count", "total", "index", "sum", "average", "result", "value", "temp", "max_val", "min_val", "counter", "limit", "threshold", "score", "age", "size", "length", "width", "height", "depth"]
func_names = ["calculate", "process", "compute", "execute", "run", "start", "initialize", "update", "render", "display", "fetch", "load", "save", "delete", "create", "read", "write", "parse", "validate", "verify"]

def get_unique_name(pool, i):
    return f"{pool[i % len(pool)]}_{i}"

def generate_cpp_samples():
    cpp_files = {
        "off_by_one.json": [],
        "incorrect_condition.json": [],
        "infinite_loop.json": [],
        "wrong_variable_used.json": [],
        "integer_overflow.json": [],
        "silent_truncation.json": [],
        "unexpected_fallthrough_switch.json": [],
        "shadowing_variable.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"CP_LOGIC_{total_id:06d}"

    # 1. Off-by-one (62)
    for i in range(62):
        arr = get_unique_name(var_names, i)
        cpp_files["off_by_one.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the off-by-one error in the loop boundary.",
            "input": {
                "title": "Off-By-One Array Traversal",
                "code": f"#include <iostream>\n\nint main() {{\n    int {arr}[5] = {{1, 2, 3, 4, 5}};\n    for (int i = 0; i <= 5; i++) {{\n        std::cout << {arr}[i] << \" \";\n    }}\n    return 0;\n}}\n",
                "error_message": "No compiler error, but runtime behavior prints garbage or crashes due to out-of-bounds access."
            },
            "output": {
                "technical": "The loop condition `i <= 5` attempts to access index 5, which is outside the bounds of a 5-element array (valid indices are 0 to 4). This results in undefined behavior.",
                "beginner": "Your loop goes one step too far. Since arrays start counting at 0, the 5th item is at index 4.",
                "analogy": "It's like walking a dog on a 4-foot leash, but throwing the ball 5 feet away. The dog will hit the end of the leash and choke.",
                "solution": "Change the loop condition from `<=` to `<`.",
                "prevention": "When iterating over arrays, always use `< length` instead of `<= length`.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {arr}[5] = {{1, 2, 3, 4, 5}};\n    for (int i = 0; i < 5; i++) {{\n        std::cout << {arr}[i] << \" \";\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(N)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["loop", "off-by-one", "array"]}
        })

    # 2. Incorrect Condition (62)
    for i in range(62):
        val = get_unique_name(var_names, i)
        cpp_files["incorrect_condition.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the assignment inside the if condition.",
            "input": {
                "title": "Assignment Instead of Comparison",
                "code": f"#include <iostream>\n\nint main() {{\n    int {val} = 10;\n    if ({val} = 5) {{\n        std::cout << \"Value is 5!\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": "No error. The code prints 'Value is 5!' incorrectly."
            },
            "output": {
                "technical": "The condition `{val} = 5` performs an assignment, which evaluates to 5 (true in C++). It should use the equality operator `==`.",
                "beginner": "You used a single equals sign (`=`), which means 'make this equal to', instead of double equals (`==`), which means 'check if this is equal to'.",
                "analogy": "It's the difference between asking 'Is the sky blue?' (`==`) and commanding 'Make the sky blue!' (`=`).",
                "solution": "Replace the single `=` with `==` in the `if` statement.",
                "prevention": "Enable compiler warnings (like `-Wparentheses`) which warn when an assignment is used as a truth value.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {val} = 10;\n    if ({val} == 5) {{\n        std::cout << \"Value is 5!\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["if", "assignment", "equality"]}
        })

    # 3. Infinite Loop (62)
    for i in range(62):
        ctr = get_unique_name(var_names, i)
        cpp_files["infinite_loop.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the infinite loop.",
            "input": {
                "title": "Missing Increment in While Loop",
                "code": f"#include <iostream>\n\nint main() {{\n    int {ctr} = 0;\n    while ({ctr} < 10) {{\n        std::cout << {ctr} << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": "No error. Program hangs, printing 0 infinitely."
            },
            "output": {
                "technical": f"The variable `{ctr}` is never modified inside the `while` loop body, so the condition `{ctr} < 10` remains perpetually true.",
                "beginner": "You forgot to increase your counter variable, so it stays at 0 forever, and the loop never finishes.",
                "analogy": "It's like telling someone to run until they reach the finish line, but they're running on a treadmill.",
                "solution": f"Increment `{ctr}` inside the loop (e.g., `{ctr}++;`).",
                "prevention": "Always verify that loop conditions are updated within the loop body.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {ctr} = 0;\n    while ({ctr} < 10) {{\n        std::cout << {ctr} << std::endl;\n        {ctr}++;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(infinity)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["loop", "infinite", "while"]}
        })

    # 4. Wrong Variable Used (62)
    for i in range(62):
        n1 = f"first_{get_unique_name(var_names, i)}"
        n2 = f"second_{get_unique_name(var_names, i)}"
        cpp_files["wrong_variable_used.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the variable copy-paste error.",
            "input": {
                "title": "Copy-Paste Variable Error",
                "code": f"#include <iostream>\n\nint main() {{\n    int {n1} = 5;\n    int {n2} = 10;\n    int sum = {n1} + {n1};\n    std::cout << \"Sum: \" << sum << std::endl;\n    return 0;\n}}\n",
                "error_message": "No error. Calculates wrong sum (10 instead of 15)."
            },
            "output": {
                "technical": f"The variable `{n1}` is added to itself instead of `{n2}` due to a likely typo or copy-paste error.",
                "beginner": f"You added the first number to itself instead of adding the second number.",
                "analogy": "It's like trying to make a peanut butter and jelly sandwich by using two scoops of peanut butter.",
                "solution": f"Change `{n1} + {n1}` to `{n1} + {n2}`.",
                "prevention": "Carefully review formulas and equations, especially when duplicating variable names.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {n1} = 5;\n    int {n2} = 10;\n    int sum = {n1} + {n2};\n    std::cout << \"Sum: \" << sum << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["typo", "variables", "logic"]}
        })

    # 5. Integer Overflow (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["integer_overflow.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the integer overflow bug.",
            "input": {
                "title": "Integer Overflow",
                "code": f"#include <iostream>\n\nint main() {{\n    short {vn} = 32767;\n    {vn} = {vn} + 1;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": "No compiler error. Prints -32768."
            },
            "output": {
                "technical": f"The `short` integer type typically holds up to 32,767. Adding 1 causes a signed integer overflow, resulting in a wrap-around to -32,768.",
                "beginner": "You tried to put a number bigger than the container can hold, so it looped back around to a negative number.",
                "analogy": "It's like an old car's odometer hitting 999,999 miles and rolling back to 000,000.",
                "solution": f"Use a larger data type, such as `int` or `long long`, for `{vn}`.",
                "prevention": "Choose appropriate data types based on the expected maximum values of variables.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 32767;\n    {vn} = {vn} + 1;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["overflow", "types", "math"]}
        })

    # 6. Silent Truncation (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["silent_truncation.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the loss of precision during division.",
            "input": {
                "title": "Silent Truncation in Float Division",
                "code": f"#include <iostream>\n\nint main() {{\n    int a = 5;\n    int b = 2;\n    float {vn} = a / b;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": "No error. Output is 2.0 instead of 2.5."
            },
            "output": {
                "technical": "Integer division (`a / b`) is performed first, truncating the fractional part (5/2 = 2). The result is then implicitly cast to a float (2.0).",
                "beginner": "The computer divides the integers completely before turning it into a decimal. So 5 divided by 2 becomes 2, not 2.5.",
                "analogy": "It's like cutting a pie into halves, but deciding to throw away the crumbs before putting it on a scale.",
                "solution": "Cast one of the operands to a float before dividing, e.g., `(float)a / b`.",
                "prevention": "Be cautious when dividing integers and expecting a fractional result.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int a = 5;\n    int b = 2;\n    float {vn} = static_cast<float>(a) / b;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["types", "division", "truncation"]}
        })

    # 7. Unexpected Fallthrough (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["unexpected_fallthrough_switch.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the switch statement fallthrough.",
            "input": {
                "title": "Switch Statement Fallthrough",
                "code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 1;\n    switch ({vn}) {{\n        case 1:\n            std::cout << \"One\" << std::endl;\n        case 2:\n            std::cout << \"Two\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": "No error. Prints both 'One' and 'Two'."
            },
            "output": {
                "technical": "The `case 1` block lacks a `break` statement. Execution 'falls through' to `case 2`, executing its statements as well.",
                "beginner": "Because you didn't tell the code to stop after case 1, it just kept going and ran case 2 as well.",
                "analogy": "It's like rolling down a hill; unless you hit the brakes (`break`), you'll keep rolling through the next stop sign.",
                "solution": "Add `break;` at the end of `case 1`.",
                "prevention": "Always end switch cases with `break`, `return`, or the `[[fallthrough]]` attribute if intentional.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 1;\n    switch ({vn}) {{\n        case 1:\n            std::cout << \"One\" << std::endl;\n            break;\n        case 2:\n            std::cout << \"Two\" << std::endl;\n            break;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["switch", "fallthrough", "control-flow"]}
        })

    # 8. Shadowing Variable (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["shadowing_variable.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "logical_bug",
            "instruction": "Fix the local variable shadowing.",
            "input": {
                "title": "Variable Shadowing",
                "code": f"#include <iostream>\n\nint {vn} = 100;\n\nvoid print() {{\n    int {vn} = 50;\n    std::cout << {vn} << std::endl;\n}}\n\nint main() {{\n    print();\n    return 0;\n}}\n",
                "error_message": "No error. Prints 50 instead of global 100 if the intent was to use the global."
            },
            "output": {
                "technical": f"The local variable `{vn}` declared inside `print()` shadows the global variable of the same name. Changes or accesses within the function apply only to the local variable.",
                "beginner": f"You created a new variable with the same name `{vn}` inside the function, hiding the original one from outside.",
                "analogy": "If you have a friend named John in the room and someone yells 'Hey John!', your friend will answer, even if the president (also named John) is in the next room over.",
                "solution": f"Remove the `int ` type declaration inside the function to use the global variable, or rename the local variable.",
                "prevention": "Avoid naming local variables identically to global variables or class members. Turn on `-Wshadow` compiler warnings.",
                "optimized_code": f"#include <iostream>\n\nint {vn} = 100;\n\nvoid print() {{\n    {vn} = 50;\n    std::cout << {vn} << std::endl;\n}}\n\nint main() {{\n    print();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["scope", "shadowing", "variables"]}
        })

    for filename, content in cpp_files.items():
        with open(f"datasets/logical_bugs/cpp/{filename}", "w") as f:
            json.dump(content, f, indent=2)

def generate_python_samples():
    py_files = {
        "off_by_one.json": [],
        "list_mutation_while_iterating.json": [],
        "default_mutable_args.json": [],
        "incorrect_boolean_logic.json": [],
        "floating_point_imprecision.json": [],
        "shallow_copy_modification.json": [],
        "infinite_while_loop.json": [],
        "shadowing_builtin.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"PY_LOGIC_{total_id:06d}"

    # 1. Off-by-one (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        py_files["off_by_one.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the range() off-by-one error.",
            "input": {
                "title": "Range Off-By-One",
                "code": f"def {fn}():\n    for i in range(1, 5):\n        print(i)\n\n{fn}()\n",
                "error_message": "No error, but prints 1 to 4 instead of 1 to 5."
            },
            "output": {
                "technical": "The `range(start, stop)` function generates numbers up to, but not including, the `stop` value.",
                "beginner": "The `range` tool stops right *before* the second number you give it. So `range(1, 5)` gives 1, 2, 3, 4.",
                "analogy": "If a store is open from 1 PM to 5 PM, it closes exactly AT 5 PM, so you can't shop at 5:00.",
                "solution": "Change the end value to 6: `range(1, 6)`.",
                "prevention": "Remember that Python ranges are exclusive at the upper bound.",
                "optimized_code": f"def {fn}():\n    for i in range(1, 6):\n        print(i)\n\n{fn}()\n",
                "complexity": {"before": "O(N)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["loop", "range", "off-by-one"]}
        })

    # 2. List Mutation While Iterating (62)
    for i in range(62):
        arr = get_unique_name(var_names, i)
        py_files["list_mutation_while_iterating.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the bug where iterating and removing from the same list skips items.",
            "input": {
                "title": "Mutating List During Iteration",
                "code": f"{arr} = [1, 2, 3, 4]\nfor item in {arr}:\n    if item % 2 == 0:\n        {arr}.remove(item)\nprint({arr})\n",
                "error_message": "No error, but skips items (e.g. consecutive elements matching condition might not be removed)."
            },
            "output": {
                "technical": "Modifying a list (like using `.remove()`) while iterating over it with a `for` loop disrupts the internal index tracker, causing elements to be skipped.",
                "beginner": "You are pulling items out of a list while looping through it. The loop loses its place and accidentally skips over items.",
                "analogy": "It's like reading a book while someone rips out the page you just finished. You'll accidentally skip the next page.",
                "solution": "Iterate over a copy of the list, or use list comprehension.",
                "prevention": "Never mutate the length of an array while iterating over it directly. Use a copy `for item in list[:]`.",
                "optimized_code": f"{arr} = [1, 2, 3, 4]\n{arr} = [item for item in {arr} if item % 2 != 0]\nprint({arr})\n",
                "complexity": {"before": "O(N^2)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["list", "iteration", "mutation"]}
        })

    # 3. Default Mutable Args (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        py_files["default_mutable_args.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the mutable default argument.",
            "input": {
                "title": "Mutable Default Argument",
                "code": f"def {fn}(val, arr=[]):\n    arr.append(val)\n    return arr\n\nprint({fn}(1))\nprint({fn}(2))\n",
                "error_message": "No error, but prints [1] then [1, 2] instead of [1] and [2]."
            },
            "output": {
                "technical": "Default arguments in Python are evaluated once at function definition time. The list `arr` is shared across all function calls that don't provide their own list.",
                "beginner": "The empty list is created once when Python reads the file. Every time you call the function, it uses that exact same shared list.",
                "analogy": "It's like placing a blank piece of paper on a shared desk. Every person who visits the desk writes on the exact same piece of paper.",
                "solution": "Set the default to `None` and initialize the list inside the function.",
                "prevention": "Never use mutable objects (like lists or dictionaries) as default arguments.",
                "optimized_code": f"def {fn}(val, arr=None):\n    if arr is None:\n        arr = []\n    arr.append(val)\n    return arr\n\nprint({fn}(1))\nprint({fn}(2))\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["functions", "mutable-default"]}
        })

    # 4. Incorrect Boolean Logic (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["incorrect_boolean_logic.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the chained equality / or condition.",
            "input": {
                "title": "Misusing OR in IF Statement",
                "code": f"{vn} = 5\nif {vn} == 3 or 5:\n    print(\"Matches\")\n",
                "error_message": "No error, but ALWAYS evaluates to True."
            },
            "output": {
                "technical": f"The condition `{vn} == 3 or 5` is evaluated as `({vn} == 3) or (5)`. Since the integer 5 is truthy, the entire expression is always True.",
                "beginner": "Python reads this as 'Check if the variable equals 3. If not, check if 5 is true.' Since 5 is a number, it's considered 'true'.",
                "analogy": "It's like asking 'Is the pet a cat, or is 5 a number?' The answer will always be 'yes' because 5 is a number.",
                "solution": f"Be explicit: `if {vn} == 3 or {vn} == 5:` or use `in`: `if {vn} in [3, 5]:`.",
                "prevention": "Remember that `or` separates complete logical expressions, not just values.",
                "optimized_code": f"{vn} = 5\nif {vn} in [3, 5]:\n    print(\"Matches\")\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["if", "boolean", "logic"]}
        })

    # 5. Floating Point Imprecision (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["floating_point_imprecision.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the floating point equality check.",
            "input": {
                "title": "Float Precision Bug",
                "code": f"{vn} = 0.1 + 0.2\nif {vn} == 0.3:\n    print(\"Equal\")\nelse:\n    print(\"Not Equal\")\n",
                "error_message": "No error. Prints 'Not Equal'."
            },
            "output": {
                "technical": "Floating-point numbers are represented in binary, leading to precision loss. `0.1 + 0.2` actually equals `0.30000000000000004`, so strict equality `== 0.3` fails.",
                "beginner": "Computers do math in base-2 (binary). Some simple decimals like 0.1 cannot be perfectly represented, causing microscopic math errors.",
                "analogy": "It's like trying to write 1/3 as a decimal (0.333...). You can never write it perfectly. Computers have the same issue with 0.1.",
                "solution": "Use `math.isclose()` to compare floats with a tolerance, or round the result.",
                "prevention": "Never use strict equality `==` to compare floating-point numbers.",
                "optimized_code": f"import math\n{vn} = 0.1 + 0.2\nif math.isclose({vn}, 0.3):\n    print(\"Equal\")\nelse:\n    print(\"Not Equal\")\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["math", "floats", "precision"]}
        })

    # 6. Shallow Copy Modification (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["shallow_copy_modification.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the list modification impacting both variables.",
            "input": {
                "title": "Shallow Copy Assignment",
                "code": f"list_a = [1, 2, 3]\nlist_b = list_a\nlist_b.append(4)\nprint(list_a)\n",
                "error_message": "No error. Modifies list_a unexpectedly (prints [1, 2, 3, 4])."
            },
            "output": {
                "technical": "Assigning `list_b = list_a` does not copy the list; it assigns a reference to the same underlying memory object. Modifying `list_b` mutates the single shared list.",
                "beginner": "You didn't make a copy of the list. You just gave the same list two different names.",
                "analogy": "If you call a person 'John' and 'Mr. Smith', changing the shirt on 'John' means 'Mr. Smith' is also wearing a new shirt. They are the same person.",
                "solution": "Create a true copy using `.copy()`, `[:]`, or the `copy` module.",
                "prevention": "Use `.copy()` when you need a distinct clone of a list or dictionary.",
                "optimized_code": f"list_a = [1, 2, 3]\nlist_b = list_a.copy()\nlist_b.append(4)\nprint(list_a)\n",
                "complexity": {"before": "O(1)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["list", "references", "copy"]}
        })

    # 7. Infinite While Loop (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["infinite_while_loop.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the infinite loop.",
            "input": {
                "title": "Missing Iterator Update",
                "code": f"{vn} = 5\nwhile {vn} > 0:\n    print({vn})\n",
                "error_message": "No error. Program hangs, printing 5 infinitely."
            },
            "output": {
                "technical": f"The condition `{vn} > 0` is always true because `{vn}` is never decremented inside the loop.",
                "beginner": "The loop keeps checking if the number is greater than zero, but the number never changes.",
                "analogy": "It's like waiting for water to boil, but you forgot to turn on the stove.",
                "solution": f"Decrease the value of `{vn}` inside the loop.",
                "prevention": "Verify that all while loops contain a mechanism to eventually alter their condition to False.",
                "optimized_code": f"{vn} = 5\nwhile {vn} > 0:\n    print({vn})\n    {vn} -= 1\n",
                "complexity": {"before": "O(infinity)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["loop", "infinite"]}
        })

    # 8. Shadowing Built-in (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["shadowing_builtin.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "logical_bug",
            "instruction": "Fix the shadowing of the built-in function 'sum'.",
            "input": {
                "title": "Overwriting Built-in Functions",
                "code": f"sum = 10\nmy_list = [1, 2, 3]\ntotal = sum(my_list)\nprint(total)\n",
                "error_message": "TypeError: 'int' object is not callable"
            },
            "output": {
                "technical": "The variable name `sum` shadows the built-in Python function `sum()`. When the code tries to call `sum(my_list)`, it attempts to call the integer `10`, causing a TypeError.",
                "beginner": "You created a variable named `sum`, which destroyed Python's built-in `sum` math tool.",
                "analogy": "It's like hiring a guy named 'Doctor' to mow your lawn, and then getting confused when he doesn't know how to treat a patient.",
                "solution": "Rename the variable `sum` to something else, like `total_sum`.",
                "prevention": "Avoid using Python keywords and built-in function names (e.g., list, dict, str, int, sum, max, min) as variable names.",
                "optimized_code": f"total_val = 10\nmy_list = [1, 2, 3]\ntotal = sum(my_list)\nprint(total)\n",
                "complexity": {"before": "O(1)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["variables", "built-ins", "shadowing"]}
        })

    for filename, content in py_files.items():
        with open(f"datasets/logical_bugs/python/{filename}", "w") as f:
            json.dump(content, f, indent=2)

if __name__ == "__main__":
    generate_cpp_samples()
    generate_python_samples()
    print("Generated 500 C++ and 500 Python samples for Logical Bugs.")
