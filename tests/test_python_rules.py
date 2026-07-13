from backend.services.rules.python_rules import analyze_python


def test_valid_python_code():
    code = """
import math

def square(x):
    return x * x
"""

    issues = analyze_python(code)

    assert issues == []


def test_missing_colon():
    code = """
def greet()
    print("Hello")
"""

    issues = analyze_python(code)

    assert len(issues) == 1
    assert issues[0]["issue"] == "Missing colon"


def test_indentation_error():
    code = """
def greet():
print("Hello")
"""

    issues = analyze_python(code)

    assert len(issues) == 1
    assert issues[0]["issue"] == "Indentation error"


def test_invalid_syntax():
    code = """
def greet():
    return 1 +
"""

    issues = analyze_python(code)

    assert len(issues) == 1
    assert issues[0]["issue"] == "Invalid syntax"


def test_missing_import():
    code = """
import module_that_does_not_exist
"""

    issues = analyze_python(code)

    assert len(issues) == 1
    assert issues[0]["issue"] == "Missing module"