from backend.services.analyzer import analyze


def test_valid_cpp_program():
    code = """
    #include <iostream>

    int main()
    {
        return 0;
    }
    """

    issues = analyze(code)

    assert issues == []


def test_cpp_missing_main():
    code = """
    #include <iostream>

    void hello()
    {
    }
    """

    issues = analyze(code)

    assert any(
        issue["rule_id"] == "cpp_missing_main"
        for issue in issues
    )


def test_python_missing_colon():
    code = """
    def greet()
        print("Hello")
    """

    issues = analyze(code)

    assert any(
        issue["rule_id"] == "python_syntax_error"
        for issue in issues
    )


def test_cpp_off_by_one():
    code = """
    #include <iostream>

    int main()
    {
        for(int i = 0; i <= n; i++)
        {
        }
    }
    """

    issues = analyze(code)

    assert any(
        issue["rule_id"] == "logical_off_by_one"
        for issue in issues
    )


def test_cpp_infinite_loop():
    code = """
    #include <iostream>

    int main()
    {
        while(true)
        {
        }
    }
    """

    issues = analyze(code)

    assert any(
        issue["rule_id"] == "logical_infinite_loop"
        for issue in issues
    )


def test_cpp_incorrect_comparison():
    code = """
    #include <iostream>

    int main()
    {
        if(a = b)
        {
        }
    }
    """

    issues = analyze(code)

    assert any(
        issue["rule_id"] == "logical_incorrect_comparison"
        for issue in issues
    )


def test_unknown_language():
    code = """
    Hello World
    """

    issues = analyze(code)

    assert len(issues) == 1
    assert issues[0]["rule_id"] == "unsupported_language"
    assert issues[0]["language"] == "unknown"