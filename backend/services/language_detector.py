"""
Language detection module for DebugGPT.

This module determines whether the provided source code is
written in C++ or Python using lightweight heuristic rules.

Supported languages:
- cpp
- python

Returns:
    "cpp"
    "python"
    "unknown"
"""

from typing import Dict


CPP_INDICATORS: Dict[str, int] = {
    "#include": 3,
    "using namespace": 2,
    "std::": 2,
    "int main(": 4,
    "cout": 2,
    "cin": 2,
    "vector<": 2,
    "->": 1,
    "::": 1,
}

PYTHON_INDICATORS: Dict[str, int] = {
    "def ": 3,
    "import ": 2,
    "from ": 2,
    "print(": 2,
    "if __name__": 3,
    "class ": 2,
    "elif ": 2,
    "lambda ": 2,
    "pass": 1,
    "None": 1,
}


def _calculate_score(code: str, indicators: Dict[str, int]) -> int:
    """
    Calculate the language score based on keyword matches.

    Args:
        code: Source code.
        indicators: Dictionary containing keywords and weights.

    Returns:
        Integer score.
    """
    score = 0

    for keyword, weight in indicators.items():
        if keyword in code:
            score += weight

    return score


def detect_language(code: str) -> str:
    """
    Detect whether the source code is C++ or Python.

    Args:
        code: Source code as a string.

    Returns:
        "cpp"
        "python"
        "unknown"
    """

    if not code or not code.strip():
        return "unknown"

    source = code.strip()

    cpp_score = _calculate_score(source, CPP_INDICATORS)
    python_score = _calculate_score(source, PYTHON_INDICATORS)

    if cpp_score == 0 and python_score == 0:
        return "unknown"

    if cpp_score > python_score:
        return "cpp"

    if python_score > cpp_score:
        return "python"

    return "unknown"