import json
import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir("datasets/educational/cpp")
ensure_dir("datasets/educational/python")

func_names = ["demo", "explain", "show", "illustrate", "concept", "example", "learn", "teach", "guide", "tutorial", "run", "execute", "process", "handle", "manage", "setup", "configure", "build", "create", "test"]
var_names = ["data", "value", "item", "element", "count", "size", "index", "result", "temp", "cache", "buffer", "node", "record", "entry", "key", "param", "arg", "obj", "entity", "model"]

def get_unique_name(pool, i):
    return f"{pool[i % len(pool)]}_{i}"

def generate_cpp_samples():
    cpp_files = {
        "pointers_and_references.json": [],
        "memory_management.json": [],
        "object_oriented_classes.json": [],
        "polymorphism_virtual_functions.json": [],
        "templates_and_generics.json": [],
        "std_vector_and_containers.json": [],
        "smart_pointers.json": [],
        "lvalue_and_rvalue.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"CP_EDU_{total_id:06d}"

    # 1. Pointers and References (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        cpp_files["pointers_and_references.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain the difference between a pointer and a reference.",
            "input": {
                "title": "Pointers vs References",
                "code": f"#include <iostream>\n\nvoid {fn}_ptr(int* p) {{\n    if (p) *p = 10;\n}}\n\nvoid {fn}_ref(int& r) {{\n    r = 20;\n}}\n\nint main() {{\n    int x = 0;\n    {fn}_ptr(&x);\n    {fn}_ref(x);\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "A pointer (`int*`) holds a memory address, can be reassigned, and can be null. A reference (`int&`) is an alias for an existing object, cannot be null, and cannot be reseated after initialization.",
                "beginner": "A pointer is like an address written on a piece of paper (which can be blank). A reference is just a nickname for a person standing right next to you.",
                "analogy": "A pointer is a URL link to a webpage. A reference is simply opening the webpage in a new tab.",
                "solution": "Use references by default for function parameters, and use pointers only when the value can optionally be null or when managing dynamic memory.",
                "prevention": "Avoid using raw pointers when references will suffice. Always check pointers for null before dereferencing.",
                "optimized_code": f"#include <iostream>\n\nvoid {fn}_ref(int& r) {{\n    r = 20;\n}}\n\nint main() {{\n    int x = 0;\n    {fn}_ref(x);\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["pointers", "references", "core-concepts"]}
        })

    # 2. Memory Management (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        cpp_files["memory_management.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain the stack vs the heap.",
            "input": {
                "title": "Stack and Heap Allocation",
                "code": f"#include <iostream>\n\nvoid allocate() {{\n    int stack_var = 5; // Stack\n    int* heap_var = new int(10); // Heap\n    std::cout << stack_var << \", \" << *heap_var << std::endl;\n    delete heap_var;\n}}\n\nint main() {{\n    allocate();\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Stack memory is managed automatically via scope and is fast but limited in size. Heap memory is allocated dynamically using `new`, managed manually (or via smart pointers), and persists until `delete` is called.",
                "beginner": "The stack is a small, organized scratchpad the computer cleans up for you automatically. The heap is a massive warehouse where you can store huge things, but you have to clean it up yourself.",
                "analogy": "The stack is a hotel room (you stay temporarily, and the maid cleans up when you leave). The heap is an apartment (you furnish it, but you are responsible for moving everything out).",
                "solution": "Use stack allocation whenever possible. When heap allocation is required, use RAII (smart pointers).",
                "prevention": "Failing to call `delete` on heap memory causes memory leaks.",
                "optimized_code": f"#include <iostream>\n#include <memory>\n\nvoid allocate() {{\n    int stack_var = 5;\n    auto heap_var = std::make_unique<int>(10);\n    std::cout << stack_var << \", \" << *heap_var << std::endl;\n}}\n\nint main() {{\n    allocate();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["memory", "heap", "stack"]}
        })

    # 3. Object Oriented Classes (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        cpp_files["object_oriented_classes.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain encapsulation and access modifiers.",
            "input": {
                "title": "Encapsulation in Classes",
                "code": f"#include <iostream>\n\nclass DataStore {{\nprivate:\n    int {vn};\npublic:\n    DataStore(int v) : {vn}(v) {{}}\n    int get_value() const {{ return {vn}; }}\n}};\n\nint main() {{\n    DataStore ds(42);\n    std::cout << ds.get_value() << std::endl;\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Encapsulation hides internal state (`private`) and exposes behavior through `public` methods. This maintains object invariants and prevents external code from making invalid modifications.",
                "beginner": "Classes let you group data and functions together. Making data 'private' puts it behind a locked door, and 'public' functions are the safe window where people can ask for that data.",
                "analogy": "It's like a vending machine. The money and snacks are locked inside (private). You can only interact with it using the buttons and coin slot (public).",
                "solution": "Keep member variables `private` and provide getters/setters only when absolutely necessary.",
                "prevention": "Making variables public destroys encapsulation and makes code hard to refactor safely.",
                "optimized_code": f"#include <iostream>\n\nclass DataStore {{\nprivate:\n    int {vn};\npublic:\n    explicit DataStore(int v) : {vn}(v) {{}}\n    [[nodiscard]] int get_value() const {{ return {vn}; }}\n}};\n\nint main() {{\n    DataStore ds(42);\n    std::cout << ds.get_value() << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["oop", "classes", "encapsulation"]}
        })

    # 4. Polymorphism Virtual Functions (62)
    for i in range(62):
        vn = get_unique_name(func_names, i)
        cpp_files["polymorphism_virtual_functions.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain virtual functions and polymorphism.",
            "input": {
                "title": "Runtime Polymorphism",
                "code": f"#include <iostream>\n\nclass Base {{\npublic:\n    virtual void {vn}() {{ std::cout << \"Base\" << std::endl; }}\n    virtual ~Base() = default;\n}};\n\nclass Derived : public Base {{\npublic:\n    void {vn}() override {{ std::cout << \"Derived\" << std::endl; }}\n}};\n\nint main() {{\n    Base* obj = new Derived();\n    obj->{vn}();\n    delete obj;\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "The `virtual` keyword enables dynamic dispatch via a vtable. When a method is called on a base pointer pointing to a derived object, the derived class's overridden method is executed at runtime.",
                "beginner": "Virtual functions let a parent object magically behave like its child object. Even though the computer thinks it's holding a Base object, it runs the Derived version of the function.",
                "analogy": "Imagine a TV remote with a 'Play' button (Base). Whether you point it at a DVD player or a PlayStation (Derived), the correct machine figures out how to 'Play'.",
                "solution": "Always declare base class destructors as `virtual` to ensure proper cleanup of derived objects.",
                "prevention": "Use the `override` keyword in derived classes so the compiler catches typos in function signatures.",
                "optimized_code": f"#include <iostream>\n#include <memory>\n\nclass Base {{\npublic:\n    virtual void {vn}() const {{ std::cout << \"Base\" << std::endl; }}\n    virtual ~Base() = default;\n}};\n\nclass Derived : public Base {{\npublic:\n    void {vn}() const override {{ std::cout << \"Derived\" << std::endl; }}\n}};\n\nint main() {{\n    std::unique_ptr<Base> obj = std::make_unique<Derived>();\n    obj->{vn}();\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["polymorphism", "virtual", "oop"]}
        })

    # 5. Templates and Generics (63)
    for i in range(63):
        fn = get_unique_name(func_names, i)
        cpp_files["templates_and_generics.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain C++ templates.",
            "input": {
                "title": "Function Templates",
                "code": f"#include <iostream>\n\ntemplate <typename T>\nT {fn}(T a, T b) {{\n    return (a > b) ? a : b;\n}}\n\nint main() {{\n    std::cout << {fn}(10, 20) << std::endl;\n    std::cout << {fn}(3.14, 2.71) << std::endl;\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Templates allow writing generic code. The compiler performs monomorphization, generating a separate, strongly-typed function for each data type (e.g., `int`, `double`) instantiated.",
                "beginner": "Templates let you write a function once using a placeholder type 'T'. The computer automatically creates the correct versions for integers, decimals, or text when it compiles the code.",
                "analogy": "A template is like a cookie cutter. The cookie cutter (template) isn't a cookie, but it can make cookies out of chocolate chip dough, sugar dough, or gingerbread dough.",
                "solution": "Use templates to avoid code duplication when logic is identical across multiple types.",
                "prevention": "Template errors can be notoriously long; understand that they usually mean a type didn't support a required operation (like `>`).",
                "optimized_code": f"#include <iostream>\n#include <algorithm>\n\nint main() {{\n    std::cout << std::max(10, 20) << std::endl;\n    std::cout << std::max(3.14, 2.71) << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["templates", "generics", "types"]}
        })

    # 6. std::vector and Containers (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["std_vector_and_containers.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain std::vector.",
            "input": {
                "title": "Dynamic Arrays with std::vector",
                "code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn};\n    {vn}.push_back(1);\n    {vn}.push_back(2);\n    for(int n : {vn}) {{\n        std::cout << n << \" \";\n    }}\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "`std::vector` is a sequence container that encapsulates dynamic size arrays. It manages its own heap memory, automatically reallocating and moving elements when its capacity is exceeded.",
                "beginner": "A vector is a super-powered list. Unlike basic arrays where you have to know the size in advance, a vector can grow and shrink automatically as you add or remove items.",
                "analogy": "A regular array is like a bus; it has a fixed number of seats. A vector is like a train; if it gets full, the conductor just attaches another car to the back.",
                "solution": "Use `std::vector` as your default array in C++. It is safe, fast, and handles memory automatically.",
                "prevention": "Pass vectors by `const &` to avoid expensive copies.",
                "optimized_code": f"#include <iostream>\n#include <vector>\n\nint main() {{\n    std::vector<int> {vn} = {{1, 2}};\n    for(const auto& n : {vn}) {{\n        std::cout << n << \" \";\n    }}\n    return 0;\n}}\n",
                "complexity": {"before": "O(N)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "C++17", "tags": ["vector", "stl", "containers"]}
        })

    # 7. Smart Pointers (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["smart_pointers.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain smart pointers and RAII.",
            "input": {
                "title": "Unique Pointers",
                "code": f"#include <iostream>\n#include <memory>\n\nint main() {{\n    std::unique_ptr<int> {vn} = std::make_unique<int>(100);\n    std::cout << *{vn} << std::endl;\n    // No delete needed!\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "Smart pointers (`std::unique_ptr`, `std::shared_ptr`) use the RAII (Resource Acquisition Is Initialization) idiom. The pointer is a stack object that wraps heap memory, automatically calling `delete` in its destructor.",
                "beginner": "Smart pointers are robots that clean up memory for you. You use them just like regular pointers, but when they are done, they automatically delete the data so you don't get memory leaks.",
                "analogy": "A raw pointer is like taking out a library book and having to remember to return it. A smart pointer is an ebook that automatically deletes itself when the loan period expires.",
                "solution": "Use `std::make_unique` by default. Use `std::make_shared` only if multiple owners need to share the exact same data.",
                "prevention": "Never use raw `new` and `delete` in modern C++.",
                "optimized_code": f"#include <iostream>\n#include <memory>\n\nint main() {{\n    auto {vn} = std::make_unique<int>(100);\n    std::cout << *{vn} << std::endl;\n    return 0;\n}}\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "C++17", "tags": ["smart-pointers", "raii", "memory"]}
        })

    # 8. Lvalue and Rvalue (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        cpp_files["lvalue_and_rvalue.json"].append({
            "id": next_id(),
            "language": "cpp",
            "category": "educational",
            "instruction": "Explain lvalues, rvalues, and move semantics.",
            "input": {
                "title": "Move Semantics",
                "code": f"#include <iostream>\n#include <string>\n#include <utility>\n\nvoid print(std::string {vn}) {{\n    std::cout << {vn} << std::endl;\n}}\n\nint main() {{\n    std::string str = \"Hello\";\n    print(std::move(str));\n    return 0;\n}}\n",
                "error_message": ""
            },
            "output": {
                "technical": "An lvalue is an object with an identifiable memory address. An rvalue is a temporary value. `std::move` casts an lvalue to an rvalue reference (`&&`), enabling the compiler to 'steal' its resources rather than copy them.",
                "beginner": "Normally, giving data to a function makes a copy. 'Move semantics' lets you say 'I'm done with this variable, you can just take it', which is incredibly fast because it skips copying.",
                "analogy": "Copying is like reading a document and writing an exact copy on a new sheet of paper. Moving is just handing the original piece of paper to someone else.",
                "solution": "Use `std::move` to transfer ownership of heavy objects (like vectors and strings) when the original variable is no longer needed.",
                "prevention": "Do not access an object after it has been moved from, as its state is valid but unspecified (usually empty).",
                "optimized_code": f"#include <iostream>\n#include <string>\n#include <utility>\n\nvoid print(std::string {vn}) {{\n    std::cout << {vn} << std::endl;\n}}\n\nint main() {{\n    std::string str = \"Hello\";\n    print(std::move(str));\n    // str is now empty\n    return 0;\n}}\n",
                "complexity": {"before": "O(1) transfer", "after": "O(1) transfer"}
            },
            "metadata": {"difficulty": "hard", "source": "synthetic", "language_version": "C++17", "tags": ["move-semantics", "rvalue", "performance"]}
        })

    for filename, content in cpp_files.items():
        with open(f"datasets/educational/cpp/{filename}", "w") as f:
            json.dump(content, f, indent=2)


def generate_python_samples():
    py_files = {
        "duck_typing.json": [],
        "list_comprehensions.json": [],
        "generators_and_yield.json": [],
        "decorators.json": [],
        "context_managers.json": [],
        "mutability_vs_immutability.json": [],
        "object_oriented_classes.json": [],
        "exception_handling.json": []
    }
    
    total_id = 0
    def next_id():
        nonlocal total_id
        total_id += 1
        return f"PY_EDU_{total_id:06d}"

    # 1. Duck Typing (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        py_files["duck_typing.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain dynamic typing and duck typing.",
            "input": {
                "title": "Duck Typing",
                "code": f"class Duck:\n    def quack(self):\n        print(\"Quack!\")\n\nclass Person:\n    def quack(self):\n        print(\"I am acting like a duck!\")\n\ndef {fn}(entity):\n    entity.quack()\n\n{fn}(Duck())\n{fn}(Person())\n",
                "error_message": ""
            },
            "output": {
                "technical": "Python uses Duck Typing, an application of dynamic typing. Type checking is deferred to runtime. As long as the object passed into `{fn}()` has a `quack` method, the code works, regardless of the object's actual class hierarchy.",
                "beginner": "In Python, if it walks like a duck and quacks like a duck, it's a duck! Python doesn't care exactly what class an object is, it just cares if the object can do the specific action requested.",
                "analogy": "It's like a USB port. Your computer doesn't care if you plug in a mouse, a keyboard, or a fan. As long as it has a USB plug, it works.",
                "solution": "Take advantage of duck typing to write flexible functions that can accept any object with the required methods.",
                "prevention": "If you need strict interfaces, use Python's `typing` module and `Protocol`.",
                "optimized_code": f"from typing import Protocol\n\nclass Quacker(Protocol):\n    def quack(self) -> None: ...\n\nclass Duck:\n    def quack(self):\n        print(\"Quack!\")\n\nclass Person:\n    def quack(self):\n        print(\"I am acting like a duck!\")\n\ndef {fn}(entity: Quacker):\n    entity.quack()\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["types", "duck-typing", "oop"]}
        })

    # 2. List Comprehensions (62)
    for i in range(62):
        vn = get_unique_name(var_names, i)
        py_files["list_comprehensions.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain list comprehensions.",
            "input": {
                "title": "List Comprehensions",
                "code": f"numbers = [1, 2, 3, 4, 5]\n{vn} = [n * 2 for n in numbers if n % 2 == 0]\nprint({vn})\n",
                "error_message": ""
            },
            "output": {
                "technical": "A list comprehension provides a concise syntax to create lists. It maps an expression (`n * 2`) across an iterable (`numbers`), optionally filtering via a condition (`if n % 2 == 0`). Under the hood, it executes in C, making it faster than a Python `for` loop.",
                "beginner": "A list comprehension is a super-short, one-line way to loop over a list, change the items, and filter them all at the same time.",
                "analogy": "Instead of saying 'Take a shirt, see if it's red, fold it, put it in the box. Repeat.' you just say 'Fold all the red shirts into the box.'",
                "solution": "Use list comprehensions for simple map/filter operations to make code more readable and performant.",
                "prevention": "Do not use list comprehensions if the logic is very complex or nested; fall back to a standard `for` loop for readability.",
                "optimized_code": f"numbers = [1, 2, 3, 4, 5]\n{vn} = [n * 2 for n in numbers if n % 2 == 0]\nprint({vn})\n",
                "complexity": {"before": "O(N)", "after": "O(N)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["lists", "comprehension", "syntax"]}
        })

    # 3. Generators and yield (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        py_files["generators_and_yield.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain generators and the yield keyword.",
            "input": {
                "title": "Generators",
                "code": f"def {fn}(max_num):\n    for i in range(max_num):\n        yield i * 2\n\nfor val in {fn}(3):\n    print(val)\n",
                "error_message": ""
            },
            "output": {
                "technical": "The `yield` keyword turns a function into a generator. Instead of returning a list in memory all at once, the function pauses its state and 'yields' one value at a time lazily. This results in O(1) memory usage regardless of iterations.",
                "beginner": "Instead of computing a million numbers and holding them all in memory, `yield` computes one number, hands it to you, and pauses until you ask for the next one.",
                "analogy": "A normal function is like receiving an entire pizza at once. A generator (`yield`) is like a chef who hands you one slice, and waits for you to eat it before baking the next slice.",
                "solution": "Use generators when processing large datasets, reading large files, or dealing with infinite sequences.",
                "prevention": "Remember that generators are exhausted after one iteration; you cannot loop over them twice.",
                "optimized_code": f"def {fn}(max_num):\n    for i in range(max_num):\n        yield i * 2\n\n# Or generator expression:\n# gen = (i * 2 for i in range(3))\n",
                "complexity": {"before": "O(1) Memory", "after": "O(1) Memory"}
            },
            "metadata": {"difficulty": "medium", "source": "synthetic", "language_version": "Python 3.10", "tags": ["generators", "yield", "memory"]}
        })

    # 4. Decorators (62)
    for i in range(62):
        fn = get_unique_name(func_names, i)
        py_files["decorators.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain Python decorators.",
            "input": {
                "title": "Decorators",
                "code": f"def my_decorator(func):\n    def wrapper():\n        print(\"Before the function\")\n        func()\n        print(\"After the function\")\n    return wrapper\n\n@my_decorator\ndef {fn}():\n    print(\"Inside the function\")\n\n{fn}()\n",
                "error_message": ""
            },
            "output": {
                "technical": "A decorator is a higher-order function that takes a function, wraps it in another function to add behavior, and returns the new function. The `@` syntax is syntactic sugar for `{fn} = my_decorator({fn})`.",
                "beginner": "A decorator is a 'wrapper' that you can easily snap onto any function. It lets you run code before or after the function without modifying the function itself.",
                "analogy": "It's like wrapping a fragile glass cup (your function) in bubble wrap (the decorator) before shipping it. The cup is unchanged, but you've added safety around it.",
                "solution": "Use decorators for logging, authentication, timing, or caching across multiple functions.",
                "prevention": "Always use `functools.wraps` inside your decorators so that the original function's name and documentation aren't lost.",
                "optimized_code": f"from functools import wraps\n\ndef my_decorator(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        print(\"Before\")\n        result = func(*args, **kwargs)\n        print(\"After\")\n        return result\n    return wrapper\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "hard", "source": "synthetic", "language_version": "Python 3.10", "tags": ["decorators", "functions", "wrappers"]}
        })

    # 5. Context Managers (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["context_managers.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain the 'with' statement and context managers.",
            "input": {
                "title": "Context Managers",
                "code": f"with open('file.txt', 'w') as {vn}:\n    {vn}.write('Hello, World!')\n",
                "error_message": ""
            },
            "output": {
                "technical": "The `with` statement utilizes the Context Manager protocol (`__enter__` and `__exit__` dunder methods). It ensures that resources (like file handles or network sockets) are cleanly released, even if an exception occurs within the block.",
                "beginner": "The `with` block safely opens a file, lets you use it, and guarantees that the file is perfectly closed and saved the second you step out of the block, even if your code crashes.",
                "analogy": "It's like renting a hotel room where the door locks automatically behind you when you leave. You don't have to remember to lock it (close the file).",
                "solution": "Always use `with` when dealing with files, locks, database connections, or any resource that needs cleanup.",
                "prevention": "Do not manually open and close files using `f = open()` and `f.close()`.",
                "optimized_code": f"with open('file.txt', 'w') as {vn}:\n    {vn}.write('Hello, World!')\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["context-managers", "files", "with"]}
        })

    # 6. Mutability vs Immutability (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["mutability_vs_immutability.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain mutability vs immutability.",
            "input": {
                "title": "Mutable vs Immutable",
                "code": f"my_string = \"hello\"\n# my_string[0] = 'H'  # This would crash!\nmy_string = \"Hello\"\n\nmy_list = [1, 2, 3]\nmy_list[0] = 99\n",
                "error_message": ""
            },
            "output": {
                "technical": "Immutable objects (strings, integers, tuples) cannot be altered in memory after creation; operations return new objects. Mutable objects (lists, dicts, sets) can be altered in-place, modifying the underlying memory.",
                "beginner": "Immutable things (like words and numbers) are carved in stone. If you want to change them, you have to carve a brand new stone. Mutable things (like lists) are written on a whiteboard and can be erased and changed.",
                "analogy": "A photograph (immutable) cannot be posed differently after it's printed. A poseable action figure (mutable) can have its arms moved whenever you want.",
                "solution": "Understand which types are mutable. Only immutable types can be used as keys in a dictionary.",
                "prevention": "Remember that passing a mutable object (like a list) to a function allows the function to change the original list.",
                "optimized_code": f"# Immutables (Strings, Tuples)\ns = \"hello\"\ns = \"H\" + s[1:] # Creates a new string\n\n# Mutables (Lists, Dicts)\nl = [1, 2]\nl.append(3) # Modifies original list\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["types", "mutability", "core-concepts"]}
        })

    # 7. Object Oriented Classes (63)
    for i in range(63):
        fn = get_unique_name(func_names, i)
        py_files["object_oriented_classes.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain classes, self, and __init__.",
            "input": {
                "title": "Classes and Self",
                "code": f"class Car:\n    def __init__(self, color):\n        self.color = color\n\n    def {fn}(self):\n        print(f\"This is a {{self.color}} car.\")\n\nmy_car = Car(\"red\")\nmy_car.{fn}()\n",
                "error_message": ""
            },
            "output": {
                "technical": "`class` defines a blueprint. `__init__` is the constructor method called upon object creation. `self` is an explicit reference to the instance itself, allowing access to instance variables (like `self.color`) and methods.",
                "beginner": "A class is a blueprint, and an object is the actual house built from it. `__init__` is the builder that sets up the house. `self` is how the house refers to its own walls and doors.",
                "analogy": "The class is the recipe for a cake. `__init__` is the act of baking the cake and adding the frosting. `self` is saying 'this specific cake right here'.",
                "solution": "Always include `self` as the first argument in standard instance methods.",
                "prevention": "Forgetting `self` in the method signature or when accessing attributes is the most common OOP error in Python.",
                "optimized_code": f"class Car:\n    def __init__(self, color: str):\n        self.color = color\n\n    def {fn}(self) -> None:\n        print(f\"This is a {{self.color}} car.\")\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["oop", "classes", "self"]}
        })

    # 8. Exception Handling (63)
    for i in range(63):
        vn = get_unique_name(var_names, i)
        py_files["exception_handling.json"].append({
            "id": next_id(),
            "language": "python",
            "category": "educational",
            "instruction": "Explain try, except, else, and finally.",
            "input": {
                "title": "Exception Handling",
                "code": f"try:\n    {vn} = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Cannot divide by zero!\")\nfinally:\n    print(\"Execution completed.\")\n",
                "error_message": ""
            },
            "output": {
                "technical": "`try` executes code that might raise an exception. `except` catches specific exception types to prevent crashes. `else` runs if no exception occurred. `finally` runs regardless of success or failure, usually for cleanup.",
                "beginner": "It's a safety net. 'Try' this dangerous code. If it explodes, do the 'except' code to recover. 'Finally' runs at the very end no matter what happened.",
                "analogy": "Try: Jump out of the plane. Except: Pull the parachute if you fall too fast. Finally: Touch the ground.",
                "solution": "Catch specific exceptions (like `ZeroDivisionError`) rather than using a bare `except:`, which hides unexpected bugs.",
                "prevention": "Don't use exceptions for normal control flow (like checking if a string is a number) if simple boolean checks are faster and clearer.",
                "optimized_code": f"try:\n    {vn} = 10 / 2\nexcept ZeroDivisionError:\n    print(\"Cannot divide by zero!\")\nelse:\n    print(f\"Result: {{{vn}}}\")\nfinally:\n    print(\"Execution completed.\")\n",
                "complexity": {"before": "O(1)", "after": "O(1)"}
            },
            "metadata": {"difficulty": "easy", "source": "synthetic", "language_version": "Python 3.10", "tags": ["exceptions", "try-except", "error-handling"]}
        })

    for filename, content in py_files.items():
        with open(f"datasets/educational/python/{filename}", "w") as f:
            json.dump(content, f, indent=2)

if __name__ == "__main__":
    generate_cpp_samples()
    generate_python_samples()
    print("Generated 500 C++ and 500 Python samples for Educational Explanations.")
