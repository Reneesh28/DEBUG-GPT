"""
Logical rule-based analyzer for DebugGPT.

This module contains lightweight heuristic rules that detect
common logical programming mistakes.
"""

from __future__ import annotations

import re


def analyze_logical(code: str, language: str) -> list[dict]:
    """
    Run all logical bug detection rules.

    Args:
        code: Source code.
        language: Detected programming language.

    Returns:
        List of detected logical issues.
    """

    issues: list[dict] = []

    issues.extend(check_off_by_one(code, language))
    issues.extend(check_infinite_loop(code, language))
    issues.extend(check_incorrect_comparison(code, language))

    return issues


def check_off_by_one(code: str, language: str) -> list[dict]:
    """
    Detect possible off-by-one loops.
    """

    pattern = r"for\s*\(.*<=.*;"

    if re.search(pattern, code):
        return [
            {
                "issue": "Possible off-by-one error",
                "language": language,
                "severity": "warning",
                "confidence": 0.85,
                "line": None,
                "message": "Loop uses '<=' which may iterate one extra time.",
                "suggestion": "Verify whether '<' should be used instead.",
                "rule_id": "logical_off_by_one",
            }
        ]

    return []


def check_infinite_loop(code: str, language: str) -> list[dict]:
    """
    Detect obvious infinite loop patterns.
    """

    patterns = [
        r"while\s*\(\s*true\s*\)",
        r"for\s*\(\s*;\s*;\s*\)",
    ]

    for pattern in patterns:

        if re.search(pattern, code, re.IGNORECASE):

            return [
                {
                    "issue": "Possible infinite loop",
                    "language": language,
                    "severity": "warning",
                    "confidence": 0.80,
                    "line": None,
                    "message": "Loop appears to run indefinitely.",
                    "suggestion": "Ensure the loop has a valid termination condition.",
                    "rule_id": "logical_infinite_loop",
                }
            ]

    return []


def check_incorrect_comparison(code: str, language: str) -> list[dict]:
    """
    Detect assignment inside conditional expressions.

    Example:
        if(a = b)
    """

    pattern = r"(if|while)\s*\([^)]*[^=!<>]=[^=][^)]*\)"

    if re.search(pattern, code):

        return [
            {
                "issue": "Possible incorrect comparison",
                "language": language,
                "severity": "warning",
                "confidence": 0.90,
                "line": None,
                "message": "Assignment detected inside a conditional expression.",
                "suggestion": "Did you mean '==' instead of '='?",
                "rule_id": "logical_incorrect_comparison",
            }
        ]

    return []