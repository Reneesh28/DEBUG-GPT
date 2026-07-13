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
    issues.extend(check_undefined_variables(code))
    issues.extend(check_division_by_zero(code))

    return issues


class UndefinedVariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined_names = set()
        self.used_names = []  # List of tuples (name, lineno)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined_names.add(name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined_names.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used_names.append((node.id, node.lineno))
        self.generic_visit(node)

    def visit_arg(self, node):
        self.defined_names.add(node.arg)
        self.generic_visit(node)


def check_undefined_variables(code: str) -> list[dict]:
    """
    Detect references to undefined variables.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    visitor = UndefinedVariableVisitor()
    visitor.visit(tree)

    import builtins
    builtins_set = set(dir(builtins))

    issues = []
    seen = set()
    for name, lineno in visitor.used_names:
        if name not in visitor.defined_names and name not in builtins_set:
            key = (name, lineno)
            if key not in seen:
                seen.add(key)
                issues.append({
                    "issue": "Undefined variable",
                    "language": "python",
                    "severity": "error",
                    "confidence": 0.90,
                    "line": lineno,
                    "message": (
                        f"Variable '{name}' is referenced before assignment "
                        f"or is not defined."
                    ),
                    "suggestion": (
                        f"Define variable '{name}' before using it or correct the spelling."
                    ),
                    "rule_id": "python_undefined_variable",
                })
    return issues


class DivisionByZeroVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            denominator = node.right
            is_zero = False
            if isinstance(denominator, ast.Constant) and denominator.value in (0, 0.0):
                is_zero = True
            elif isinstance(denominator, ast.Num) and denominator.n in (0, 0.0):
                is_zero = True

            if is_zero:
                self.errors.append(node.lineno)
        self.generic_visit(node)


def check_division_by_zero(code: str) -> list[dict]:
    """
    Detect division or modulo by zero.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    visitor = DivisionByZeroVisitor()
    visitor.visit(tree)

    issues = []
    for lineno in visitor.errors:
        issues.append({
            "issue": "Division by zero",
            "language": "python",
            "severity": "error",
            "confidence": 1.0,
            "line": lineno,
            "message": "Division or modulo by zero detected.",
            "suggestion": "Ensure the denominator is not zero.",
            "rule_id": "python_division_by_zero",
        })
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