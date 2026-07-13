from backend.services.rules.logical_rules import analyze_logical


def test_off_by_one_detection():
    code = """
    for(int i = 0; i <= n; i++)
    {
    }
    """

    issues = analyze_logical(code, "cpp")

    assert len(issues) == 1
    assert issues[0]["issue"] == "Possible off-by-one error"


def test_infinite_loop_detection():
    code = """
    while(true)
    {
    }
    """

    issues = analyze_logical(code, "cpp")

    assert len(issues) == 1
    assert issues[0]["issue"] == "Possible infinite loop"


def test_assignment_in_condition():
    code = """
    if(a = b)
    {
    }
    """

    issues = analyze_logical(code, "cpp")

    assert len(issues) == 1
    assert issues[0]["issue"] == "Possible incorrect comparison"


def test_no_logical_issue():
    code = """
    for(int i = 0; i < n; i++)
    {
    }

    if(a == b)
    {
    }
    """

    issues = analyze_logical(code, "cpp")

    assert issues == []


def test_python_infinite_loop():
    code = """
while(True):
    pass
"""

    issues = analyze_logical(code, "python")

    assert len(issues) == 1
    assert issues[0]["issue"] == "Possible infinite loop"