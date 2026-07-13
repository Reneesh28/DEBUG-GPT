from backend.services.language_detector import detect_language


def test_cpp_detection():
    code = """
    #include <iostream>

    using namespace std;

    int main() {
        cout << "Hello";
    }
    """

    assert detect_language(code) == "cpp"


def test_python_detection():
    code = """
    import math

    def square(x):
        return x * x
    """

    assert detect_language(code) == "python"


def test_unknown_detection():
    code = "Hello World"

    assert detect_language(code) == "unknown"


def test_empty_code():
    assert detect_language("") == "unknown"


def test_whitespace():
    assert detect_language("      ") == "unknown"


def test_ambiguous_code():
    code = """
    x = 5
    y = 10
    """

    assert detect_language(code) == "unknown"