"""
C++ rule-based analyzer for DebugGPT.

This module contains lightweight static analysis rules for C++ source code.
Only source-code-based rules are implemented here.
"""

from __future__ import annotations

import re


def analyze_cpp(code: str) -> list[dict]:
    """
    Run all C++ source code rules.

    Args:
        code: C++ source code.

    Returns:
        List of detected issues.
    """

    issues: list[dict] = []

    issues.extend(check_missing_main(code))
    issues.extend(check_missing_header(code))
    issues.extend(check_missing_semicolon(code))
    issues.extend(check_bracket_balance(code))
    issues.extend(check_array_out_of_bounds(code))

    return issues


def check_array_out_of_bounds(code: str) -> list[dict]:
    """
    Detect potential array out-of-bounds access for static array declarations.
    """

    issues: list[dict] = []

    # Find static array declarations like: int arr[5];
    decl_pattern = re.compile(
        r"\b(?:int|double|float|char|bool|long|short)\s+(\w+)\s*\[\s*(\d+)\s*\]"
    )
    arrays = {}  # name -> (size, line_number)

    for line_number, raw_line in enumerate(code.splitlines(), start=1):
        for match in decl_pattern.finditer(raw_line):
            name, size_str = match.groups()
            arrays[name] = (int(size_str), line_number)

    # Find subsequent accesses like: arr[10]
    access_pattern = re.compile(r"\b(\w+)\s*\[\s*(\d+)\s*\]")

    for line_number, raw_line in enumerate(code.splitlines(), start=1):
        for match in access_pattern.finditer(raw_line):
            name, index_str = match.groups()
            if name in arrays:
                size, decl_line = arrays[name]
                index = int(index_str)
                # Only warn if access index >= array size and it's not the declaration line
                if line_number != decl_line and index >= size:
                    issues.append({
                        "issue": "Array out of bounds",
                        "language": "cpp",
                        "severity": "error",
                        "confidence": 0.95,
                        "line": line_number,
                        "message": (
                            f"Array '{name}' has size {size}, but is accessed "
                            f"at index {index}."
                        ),
                        "suggestion": (
                            "Ensure the index is less than the array size."
                        ),
                        "rule_id": "cpp_array_out_of_bounds",
                    })

    return issues


def check_missing_main(code: str) -> list[dict]:
    """
    Detect missing main() function.
    """

    if re.search(r"\b(main)\s*\(", code):
        return []

    return [{
        "issue": "Missing main() function",
        "language": "cpp",
        "severity": "error",
        "confidence": 1.0,
        "line": None,
        "message": "No main() function was found.",
        "suggestion": "Define an entry point using int main().",
        "rule_id": "cpp_missing_main",
    }]


def check_missing_header(code: str) -> list[dict]:
    """
    Detect missing #include directives.
    """

    if "#include" in code:
        return []

    return [{
        "issue": "Missing header",
        "language": "cpp",
        "severity": "warning",
        "confidence": 0.98,
        "line": 1,
        "message": "No #include directive was found.",
        "suggestion": "Include the required standard library headers.",
        "rule_id": "cpp_missing_header",
    }]


def check_missing_semicolon(code: str) -> list[dict]:
    """
    Detect simple missing semicolons.

    This is a heuristic, not a compiler.
    """

    issues: list[dict] = []

    ignore_prefixes = (
        "#",
        "//",
        "/*",
        "*",
    )

    control_keywords = (
        "if",
        "for",
        "while",
        "switch",
        "else",
        "do",
        "try",
        "catch",
    )

    for line_number, raw_line in enumerate(code.splitlines(), start=1):

        line = raw_line.strip()

        if not line:
            continue

        if line.startswith(ignore_prefixes):
            continue

        if line.endswith(("{", "}", ";", ":")):
            continue

        if any(line.startswith(keyword) for keyword in control_keywords):
            continue

        if re.match(r".+\)\s*$", line):
            continue

        issues.append({
            "issue": "Possible missing semicolon",
            "language": "cpp",
            "severity": "warning",
            "confidence": 0.90,
            "line": line_number,
            "message": "This line may be missing a semicolon.",
            "suggestion": "Check whether this statement should end with ';'.",
            "rule_id": "cpp_missing_semicolon",
        })

    return issues


def check_bracket_balance(code: str) -> list[dict]:
    """
    Detect unmatched braces and parentheses.
    """

    issues: list[dict] = []

    if code.count("{") != code.count("}"):

        issues.append({
            "issue": "Unmatched curly braces",
            "language": "cpp",
            "severity": "error",
            "confidence": 1.0,
            "line": None,
            "message": "Opening and closing braces do not match.",
            "suggestion": "Check '{' and '}' pairs.",
            "rule_id": "cpp_unmatched_braces",
        })

    if code.count("(") != code.count(")"):

        issues.append({
            "issue": "Unmatched parentheses",
            "language": "cpp",
            "severity": "error",
            "confidence": 1.0,
            "line": None,
            "message": "Opening and closing parentheses do not match.",
            "suggestion": "Check '(' and ')' pairs.",
            "rule_id": "cpp_unmatched_parentheses",
        })

    return issues