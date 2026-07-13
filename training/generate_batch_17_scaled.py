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

ensure_dir("../datasets/compiler_errors/python")
output_file = "../datasets/compiler_errors/python/syntax_errors.json"

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
        candidate = f"PY_COMPILER_{i:06d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
        i += 1

samples = []

funcs = ["process", "calculate", "update", "evaluate", "aggregate", "filter_data", "run", "compute", "execute", "analyze"]
var_names = ["items", "data", "results", "values", "numbers", "records", "points", "scores", "dataset", "collection"]
local_vars = ["total", "count", "average", "sum_val", "index", "current", "maximum", "minimum", "temp", "val"]

for i in range(1000):
    variation = i % 5
    func = funcs[(i // 5) % len(funcs)]
    vname = var_names[(i // 10) % len(var_names)]
    lvar = local_vars[(i // 20) % len(local_vars)]
    
    if variation == 0:
        # Missing Colon (SyntaxError: invalid syntax)
        code = f"def {func}({vname})\n    {lvar} = 0\n    if {vname}\n        print({vname})\n    return {lvar}\n\n{func}(True)"
        error = f"  File \"main.py\", line 1\n    def {func}({vname})\n                    ^\nSyntaxError: expected ':'"
        opt_code = f"def {func}({vname}):\n    {lvar} = 0\n    if {vname}:\n        print({vname})\n    return {lvar}\n\n{func}(True)"
        technical = f"Python requires a colon (`:`) at the end of statements that introduce a new code block, such as `def`, `if`, `for`, `while`, `class`, and `try`. Omitting it results in a SyntaxError during the parsing phase before execution."
        beginner = f"You forgot to put a colon `:` at the end of the `def` and `if` lines. Python uses the colon to know that a new indented block is about to start."
        title = "Missing Colon"
        tags = ["compiler-error", "syntax-error", "missing-colon"]
    
    elif variation == 1:
        # Missing Indentation (IndentationError: expected an indented block)
        code = f"def {func}():\n{lvar} = 10\nprint({lvar})\n\n{func}()"
        error = f"  File \"main.py\", line 2\n    {lvar} = 10\n    ^\nIndentationError: expected an indented block after function definition on line 1"
        opt_code = f"def {func}():\n    {lvar} = 10\n    print({lvar})\n\n{func}()"
        technical = f"Unlike C-like languages that use curly braces `{{}}` to define scope, Python relies strictly on whitespace indentation. When a block-initiating statement (ending with `:`) is encountered, the subsequent line MUST be indented."
        beginner = f"After writing `def {func}():`, you need to press 'Tab' or 'Space' for the lines underneath it. Python uses that space to understand which lines belong inside the function."
        title = "Missing Indented Block"
        tags = ["compiler-error", "indentation-error", "whitespace"]
    
    elif variation == 2:
        # Unclosed String (SyntaxError: EOL while scanning string literal)
        code = f"def {func}():\n    message = \"Hello World\n    print(message)\n\n{func}()"
        error = f"  File \"main.py\", line 2\n    message = \"Hello World\n                          ^\nSyntaxError: unterminated string literal (detected at line 2)"
        opt_code = f"def {func}():\n    message = \"Hello World\"\n    print(message)\n\n{func}()"
        technical = f"The Python parser reached the End Of Line (EOL) character while still in the middle of parsing a string literal because the closing quote (`\"` or `'`) was missing."
        beginner = f"You opened a text string with a quote `\"`, but forgot to close it with another quote at the end of the sentence. Python kept reading until the line ended, got confused, and crashed."
        title = "Unterminated String Literal"
        tags = ["compiler-error", "syntax-error", "strings", "quotes"]

    elif variation == 3:
        # Unbalanced Parentheses (SyntaxError: unmatched ')')
        code = f"def {func}(a, b):\n    {lvar} = (a + b)) * 2\n    return {lvar}\n\n{func}(5, 5)"
        error = f"  File \"main.py\", line 2\n    {lvar} = (a + b)) * 2\n                    ^\nSyntaxError: unmatched ')'"
        opt_code = f"def {func}(a, b):\n    {lvar} = (a + b) * 2\n    return {lvar}\n\n{func}(5, 5)"
        technical = f"The parser encountered a closing parenthesis `)` that did not have a corresponding opening parenthesis `(`. Python requires all grouping characters `()`, `[]`, and `{{}}` to be perfectly balanced."
        beginner = f"You have an extra closing parenthesis `)` that doesn't match up with any opening parenthesis `(`. Make sure every `(` has exactly one `)`."
        title = "Unmatched Parentheses"
        tags = ["compiler-error", "syntax-error", "parentheses"]

    else:
        # Mismatched Indentation Level (IndentationError: unindent does not match any outer indentation level)
        code = f"def {func}():\n    if True:\n        {lvar} = 1\n      print({lvar})\n\n{func}()"
        error = f"  File \"main.py\", line 4\n    print({lvar})\n                 ^\nIndentationError: unindent does not match any outer indentation level"
        opt_code = f"def {func}():\n    if True:\n        {lvar} = 1\n        print({lvar})\n\n{func}()"
        technical = f"Python enforces strict block alignment. The parser encountered a line with a level of indentation (e.g., 6 spaces) that does not match the current block (8 spaces) or any outer block (4 or 0 spaces). This often happens when mixing tabs and spaces."
        beginner = f"Your indentation is crooked. The `print({lvar})` line has a different number of spaces in front of it compared to the lines above it. Make sure you use exactly 4 spaces consistently."
        title = "Mismatched Outer Indentation Level"
        tags = ["compiler-error", "indentation-error", "whitespace", "alignment"]

    sample = {
        "id": get_next_id(),
        "language": "python",
        "category": "compiler_error",
        "instruction": f"Fix the Python syntax/compiler error caused by {title.lower()}.",
        "input": {
            "title": title,
            "code": code,
            "error_message": error
        },
        "output": {
            "technical": technical,
            "beginner": beginner,
            "analogy": "It's like writing a sentence but forgetting the period at the end, or putting a random comma in the middle of a word. The grammar reader gets confused.",
            "solution": "Correct the syntax formatting, balance all brackets/quotes, and ensure uniform indentation (preferably using 4 spaces).",
            "prevention": "Use a modern code editor with automatic formatting (like Black) and syntax highlighting to spot these errors instantly.",
            "optimized_code": opt_code,
            "complexity": {"before": "O(1)", "after": "O(1)"}
        },
        "metadata": {
            "difficulty": "easy",
            "source": "Generated Python Syntax Error Variations",
            "language_version": "Python 3.x",
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
