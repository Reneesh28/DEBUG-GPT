import json
import os
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir("datasets/compiler_errors/cpp")
ensure_dir("datasets/compiler_errors/python")

# Data pools
var_types = ["int", "float", "double", "char", "long", "short", "unsigned int"]
var_names = ["count", "total", "index", "sum", "average", "result", "value", "temp", "max_val", "min_val", "counter", "limit", "threshold", "score", "age", "size", "length", "width", "height", "depth"]
func_names = ["calculate", "process", "compute", "execute", "run", "start", "initialize", "update", "render", "display", "fetch", "load", "save", "delete", "create", "read", "write", "parse", "validate", "verify"]
classes = ["Manager", "Handler", "Processor", "Controller", "Service", "Repository", "Factory", "Builder", "Observer", "Strategy"]

def get_unique_name(pool, i):
    return f"{pool[i % len(pool)]}_{i}"

def generate_cpp_samples():
    cpp_files = {
        "missing_main.json": [],
        "undefined_reference.json": [],
        "missing_semicolon.json": [],
        "syntax_error.json": [],
        "undeclared_identifier.json": [],
        "type_mismatch.json": [],
        "missing_header.json": [],
        "multiple_definition.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"CP_COMPILER_{total_id:06d}"

    # 1. Missing Main (62 samples)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        cpp_files["missing_main.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Fix the missing entry point error.",
            "input": {
                "title": "Missing main function",
                "code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::cout << \"Hello World!\" << std::endl;\n}}\n",
                "error_message": "/usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/Scrt1.o: In function `_start':\n(.text+0x24): undefined reference to `main'\ncollect2: error: ld returned 1 exit status"
            },
            "output": {
                "technical": "The linker failed to find the entry point of the program, which must be the `main` function in C++ executables.",
                "beginner": "Your program is missing the `main` function. Without it, the computer doesn't know where to start running.",
                "analogy": "Imagine a book with no first page. You open it, but don't know where the story begins.",
                "solution": "Add an `int main()` function to your code.",
                "prevention": "Ensure your executable C++ files always have a defined `main` function.",
                "optimized_code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::cout << \"Hello World!\" << std::endl;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["linker", "entry-point", "main"]}
        })

    # 2. Undefined Reference (62 samples)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        cpp_files["undefined_reference.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Resolve the undefined reference linker error.",
            "input": {
                "title": "Undefined Reference",
                "code": f"#include <iostream>\n\nvoid {fn}();\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "error_message": f"/tmp/ccXXXXXX.o: In function `main':\nmain.cpp:(.text+0x5): undefined reference to `{fn}()'\ncollect2: error: ld returned 1 exit status"
            },
            "output": {
                "technical": f"The function prototype for `{fn}()` exists, but the linker failed because its implementation is missing.",
                "beginner": f"You promised the computer a function named `{fn}` exists, but you didn't write its actual code.",
                "analogy": "It's like handing out a menu with a dish on it, but the kitchen doesn't know the recipe.",
                "solution": f"Provide the definition (body) for the `{fn}` function.",
                "prevention": "Ensure declared functions have a definition.",
                "optimized_code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::cout << \"Executed\" << std::endl;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["linker", "undefined-reference"]}
        })

    # 3. Missing Semicolon (62 samples)
    for i in range(62):
        vt = var_types[i % len(var_types)]
        vn = get_unique_name(var_names, i)
        val = random.randint(1, 100)
        cpp_files["missing_semicolon.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Fix the missing semicolon syntax error.",
            "input": {
                "title": "Missing Semicolon",
                "code": f"#include <iostream>\n\nint main() {{\n    {vt} {vn} = {val}\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘int main()’:\nmain.cpp:4:5: error: expected ‘,’ or ‘;’ before ‘std’\n    4 |     std::cout << {vn} << std::endl;\n      |     ^~~"
            },
            "output": {
                "technical": f"A statement in C++ must be terminated with a semicolon. The compiler encountered `std::cout` but the previous statement declaring `{vn}` was not terminated.",
                "beginner": f"You forgot to put a semicolon (;) at the end of the line where you created `{vn}`. Semicolons are like periods in English sentences.",
                "analogy": "Imagine writing a paragraph without any punctuation. The computer gets confused about where one instruction ends and the next begins.",
                "solution": "Add a semicolon at the end of the variable declaration line.",
                "prevention": "Always double-check the ends of your statements for semicolons.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    {vt} {vn} = {val};\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["syntax", "semicolon"]}
        })

    # 4. Syntax Error / Mismatched Parentheses (62 samples)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        cpp_files["syntax_error.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Fix the mismatched parenthesis syntax error.",
            "input": {
                "title": "Mismatched Parenthesis",
                "code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 5;\n    if ({vn} > 0 {{\n        std::cout << \"Positive\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘int main()’:\nmain.cpp:5:17: error: expected ‘)’ before ‘{{’ token\n    5 |     if ({vn} > 0 {{\n      |        ~        ^\n      |                 )"
            },
            "output": {
                "technical": "The `if` statement requires its boolean expression to be fully enclosed in parentheses.",
                "beginner": "Your `if` condition is missing a closing parenthesis `)`. Every opening parenthesis needs a partner.",
                "analogy": "It's like opening a quote in a sentence but forgetting to close it.",
                "solution": "Add the missing closing parenthesis to the `if` condition.",
                "prevention": "Use IDE features like bracket matching to avoid structural typos.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 5;\n    if ({vn} > 0) {{\n        std::cout << \"Positive\" << std::endl;\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["syntax", "parenthesis"]}
        })

    # 5. Undeclared Identifier (63 samples)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["undeclared_identifier.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": f"Fix the undeclared identifier '{vn}' error.",
            "input": {
                "title": "Undeclared Identifier",
                "code": f"#include <iostream>\n\nint main() {{\n    {vn} = 10;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘int main()’:\nmain.cpp:4:5: error: ‘{vn}’ was not declared in this scope\n    4 |     {vn} = 10;\n      |     ^~~~"
            },
            "output": {
                "technical": f"The identifier `{vn}` is used before it has been declared with a specific type. C++ requires all variables to be explicitly declared before use.",
                "beginner": f"You tried to use `{vn}`, but you didn't tell the computer what type of data it holds (like `int` or `float`).",
                "analogy": "It's like asking someone to fetch 'the thing' without explaining what 'the thing' is. The computer needs an introduction to every variable.",
                "solution": f"Declare the variable with its type before assigning a value, e.g., `int {vn} = 10;`.",
                "prevention": "Always declare your variables at the beginning of their scope or exactly where you need them.",
                "optimized_code": f"#include <iostream>\n\nint main() {{\n    int {vn} = 10;\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["identifier", "scope", "declaration"]}
        })

    # 6. Type Mismatch (63 samples)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["type_mismatch.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Fix the invalid type conversion.",
            "input": {
                "title": "Invalid Conversion",
                "code": f"#include <iostream>\n\nint main() {{\n    int {vn} = \"hello\";\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘int main()’:\nmain.cpp:4:16: error: invalid conversion from ‘const char*’ to ‘int’\n    4 |     int {vn} = \"hello\";\n      |                ^~~~~~~"
            },
            "output": {
                "technical": "A string literal (`const char*`) cannot be implicitly converted to an integer (`int`).",
                "beginner": "You are trying to store text in a variable designed only for numbers.",
                "analogy": "It's like trying to pour water into a paper bag. The container isn't made for that type of content.",
                "solution": f"Change the assigned value to a number, or change the variable type to `std::string`.",
                "prevention": "Ensure variable types match the data being assigned to them.",
                "optimized_code": f"#include <iostream>\n#include <string>\n\nint main() {{\n    std::string {vn} = \"hello\";\n    std::cout << {vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["types", "conversion"]}
        })

    # 7. Missing Header (63 samples)
    for i in range(63):
        fn = get_unique_name(func_names, i)
        cpp_files["missing_header.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Include the missing header file.",
            "input": {
                "title": "Missing Header for vector",
                "code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::vector<int> numbers;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘void {fn}()’:\nmain.cpp:4:5: error: ‘vector’ is not a member of ‘std’\n    4 |     std::vector<int> numbers;\n      |     ^~~"
            },
            "output": {
                "technical": "The `std::vector` container requires the `<vector>` header to be included. Without it, the compiler cannot find its definition.",
                "beginner": "You used a `vector` but forgot to tell the compiler where the instructions for it are.",
                "analogy": "It's like trying to build a Lego castle without the instruction manual.",
                "solution": "Add `#include <vector>` at the top of your file.",
                "prevention": "Always include the required STL headers for standard components.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nvoid {fn}() {{\n    std::vector<int> numbers;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["header", "include", "vector"]}
        })

    # 8. Multiple Definition (63 samples)
    for i in range(63):
        fn = get_unique_name(func_names, i)
        cpp_files["multiple_definition.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "compiler_error",
            "instruction": "Resolve the function redefinition error.",
            "input": {
                "title": "Function Redefinition",
                "code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::cout << \"A\" << std::endl;\n}}\n\nvoid {fn}() {{\n    std::cout << \"B\" << std::endl;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "error_message": f"main.cpp: In function ‘void {fn}()’:\nmain.cpp:7:6: error: redefinition of ‘void {fn}()’\n    7 | void {fn}() {{\n      |      ^~~~~\nmain.cpp:3:6: note: ‘void {fn}()’ previously defined here"
            },
            "output": {
                "technical": f"The function `{fn}()` is defined multiple times, violating the One Definition Rule (ODR).",
                "beginner": f"You wrote two functions with the exact same name `{fn}`. The compiler doesn't know which one to use.",
                "analogy": "It's like having two houses with the exact same address on the same street. The mail carrier is confused.",
                "solution": "Remove the duplicate function definition or rename one of them.",
                "prevention": "Keep function names unique within the same namespace.",
                "optimized_code": f"#include <iostream>\n\nvoid {fn}() {{\n    std::cout << \"A\" << std::endl;\n}}\n\nint main() {{\n    {fn}();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["redefinition", "odr"]}
        })

    for filename, content in cpp_files.items():
        with open(f"datasets/compiler_errors/cpp/{filename}", "w") as f:
            json.dump(content, f, indent=2)

def generate_python_samples():
    py_files = {
        "indentation_error.json": [],
        "syntax_error.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"PY_COMPILER_{total_id:06d}"

    # 1. IndentationError (250 samples)
    for i in range(250):
        fn = get_unique_name(func_names, i)
        py_files["indentation_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "compiler_error",
            "instruction": "Fix the Python indentation error.",
            "input": {
                "title": "IndentationError",
                "code": f"def {fn}():\nprint(\"Executing {fn}\")\n\n{fn}()\n",
                "error_message": f"  File \"main.py\", line 2\n    print(\"Executing {fn}\")\n    ^\nIndentationError: expected an indented block after function definition on line 1"
            },
            "output": {
                "technical": f"Python uses indentation to define code blocks. The body of `{fn}` must be indented.",
                "beginner": "You forgot to indent (add spaces) before the `print` line.",
                "analogy": "Think of it like an outline. Sub-points are indented under main points so you know they belong together.",
                "solution": "Indent the `print` statement with 4 spaces.",
                "prevention": "Consistently use 4 spaces for indentation.",
                "optimized_code": f"def {fn}():\n    print(\"Executing {fn}\")\n\n{fn}()\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["indentation", "syntax"]}
        })

    # 2. SyntaxError (250 samples)
    for i in range(250):
        vn = get_unique_name(var_names, i)
        val = random.randint(10, 50)
        py_files["syntax_error.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "compiler_error",
            "instruction": "Fix the missing colon syntax error.",
            "input": {
                "title": "Missing Colon in If Statement",
                "code": f"{vn} = {val}\nif {vn} >= {val}\n    print(\"Match\")\n",
                "error_message": f"  File \"main.py\", line 2\n    if {vn} >= {val}\n                   ^\nSyntaxError: expected ':'"
            },
            "output": {
                "technical": "Python requires a colon `:` at the end of control flow statements like `if`.",
                "beginner": "You missed a colon `:` at the end of your `if` statement.",
                "analogy": "It's like a speaker saying, 'And the winner is:' before pausing.",
                "solution": f"Add a colon `:` at the end of the `if {vn} >= {val}` line.",
                "prevention": "Double-check control flow statements end with a colon.",
                "optimized_code": f"{vn} = {val}\nif {vn} >= {val}:\n    print(\"Match\")\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["syntax", "colon"]}
        })

    for filename, content in py_files.items():
        with open(f"datasets/compiler_errors/python/{filename}", "w") as f:
            json.dump(content, f, indent=2)

if __name__ == "__main__":
    generate_cpp_samples()
    generate_python_samples()
    print("Generated 500 C++ and 500 Python samples grouped into the original files.")
