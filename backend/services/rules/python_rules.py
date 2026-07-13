"""
Python rule-based analyzer for DebugGPT.

This module contains lightweight static analysis rules for Python source code.
Only source-code-based rules are implemented here.
"""

from __future__ import annotations

import ast
import importlib.util


def analyze_python(code: str) -> list[dict]:
    """
    Run all Python source code rules.

    Args:
        code: Python source code.

    Returns:
        List of detected issues.
    """

    issues: list[dict] = []

    issues.extend(check_syntax(code))
    issues.extend(check_imports(code))

    return issues


def check_syntax(code: str) -> list[dict]:
    """
    Detect Python syntax-related issues using Python's built-in AST parser.
    """

    try:
        ast.parse(code)
        return []

    except SyntaxError as error:

        message = str(error)

        if "expected ':'" in message:
            issue = "Missing colon"

        elif (
            "unexpected indent" in message
            or "expected an indented block" in message
        ):
            issue = "Indentation error"

        else:
            issue = "Invalid syntax"

        return [
            {
                "issue": issue,
                "language": "python",
                "severity": "error",
                "confidence": 1.0,
                "line": error.lineno,
                "message": message,
                "suggestion": "Correct the Python syntax.",
                "rule_id": "python_syntax_error",
            }
        ]


def check_imports(code: str) -> list[dict]:
    """
    Detect missing Python modules.

    Uses importlib without importing the modules.
    """

    issues: list[dict] = []

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for module in node.names:

                if importlib.util.find_spec(module.name) is None:

                    issues.append(
                        {
                            "issue": "Missing module",
                            "language": "python",
                            "severity": "warning",
                            "confidence": 0.95,
                            "line": node.lineno,
                            "message": f"Module '{module.name}' was not found.",
                            "suggestion": "Install the module or verify the module name.",
                            "rule_id": "python_missing_import",
                        }
                    )

        elif isinstance(node, ast.ImportFrom):

            if (
                node.module
                and importlib.util.find_spec(node.module) is None
            ):

                issues.append(
                    {
                        "issue": "Missing module",
                        "language": "python",
                        "severity": "warning",
                        "confidence": 0.95,
                        "line": node.lineno,
                        "message": f"Module '{node.module}' was not found.",
                        "suggestion": "Install the module or verify the module name.",
                        "rule_id": "python_missing_import",
                    }
                )

    return issues