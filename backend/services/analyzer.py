"""
Main Rule-Based Analysis Engine for DebugGPT.

Pipeline:
1. Detect programming language (if not provided).
2. Execute language-specific rules.
3. Execute logical rules.
4. Return detected issues.
"""

from backend.services.language_detector import detect_language
from backend.services.rules.cpp_rules import analyze_cpp
from backend.services.rules.python_rules import analyze_python
from backend.services.rules.logical_rules import analyze_logical


SUPPORTED_LANGUAGES = {"cpp", "python"}


def analyze(
    code: str,
    language: str | None = None,
) -> list[dict]:
    """
    Analyze source code using the DebugGPT Rule-Based Analysis Engine.

    Args:
        code:
            Source code.

        language:
            Optional language supplied by the API.
            If None, language is detected automatically.

    Returns:
        List of detected issues.
    """

    if language is None:
        language = detect_language(code)

    if language not in SUPPORTED_LANGUAGES:
        return [
            {
                "issue": "Unsupported or unknown language",
                "language": language,
                "severity": "error",
                "confidence": 1.0,
                "line": None,
                "message": (
                    "DebugGPT currently supports only "
                    "C++ and Python."
                ),
                "suggestion": (
                    "Provide valid C++ or Python source code."
                ),
                "rule_id": "unsupported_language",
            }
        ]

    issues: list[dict] = []

    if language == "cpp":
        issues.extend(analyze_cpp(code))
    else:
        issues.extend(analyze_python(code))

    issues.extend(
        analyze_logical(
            code=code,
            language=language,
        )
    )

    return issues