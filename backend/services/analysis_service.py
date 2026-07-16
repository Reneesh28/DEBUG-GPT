"""
backend/services/analysis_service.py

Purpose:
    Coordinate the Rule Engine and RAG services.

Workflow:
    Request
        ↓
    Rule-Based Analysis
        ↓
    RAG Retrieval
        ↓
    Format Response
        ↓
    Return Structured Result
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.services.analyzer import analyze
from backend.services.rag_service import retrieve_context
from backend.services.llm_service import llm_service

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _format_issues(
    issues: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert analyzer output into a consistent API structure.
    """

    formatted = []

    for issue in issues:
        formatted.append(
            {
                "issue": issue.get("issue"),
                "severity": issue.get("severity"),
                "confidence": issue.get("confidence", 1.0),
                "line": issue.get("line"),
                "message": issue.get("message"),
                "suggestion": issue.get("suggestion"),
                "rule_id": issue.get("rule_id"),
            }
        )

    return formatted


def _format_rag_results(
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert raw ChromaDB results into API format.
    """

    formatted = []

    for result in results:
        formatted.append(
            {
                "id": result.get("id"),
                "document": result.get("document"),
                "metadata": result.get("metadata"),
                "distance": result.get("distance"),
                "collection": result.get("collection"),
            }
        )

    return formatted


# ---------------------------------------------------------------------
# Public Service Functions
# ---------------------------------------------------------------------


def analyze_code(
    code: str,
    language: str,
) -> dict[str, Any]:
    """
    Run Rule Engine analysis and retrieve RAG context.
    """

    logger.info("Starting code analysis.")

    start_time = time.perf_counter()

    try:

        issues = analyze(
            code=code,
            language=language,
        )

        if not isinstance(issues, list):
            raise TypeError(
                "Rule Engine returned an invalid response."
            )

        rag_results = retrieve_context(
            query=code,
            top_k=5,
        )

        execution_time = round(
            time.perf_counter() - start_time,
            4,
        )

        logger.info(
            "Analysis completed in %.4f seconds.",
            execution_time,
        )

        logger.info(
            "Detected %d issue(s).",
            len(issues),
        )

        return {
            "success": True,
            "language": language,
            "issues": _format_issues(issues),
            "rag_context": _format_rag_results(rag_results),
            "execution_time": execution_time,
        }

    except Exception:

        logger.exception("Rule Engine analysis failed.")

        raise


def debug_code(
    code: str,
    language: str,
) -> dict[str, Any]:
    """
    Generate debugging suggestions using Rule Engine and LLM.
    """

    analysis = analyze_code(
        code=code,
        language=language,
    )

    suggestions = []

    for issue in analysis["issues"]:
        suggestion = issue.get("suggestion")

        if suggestion:
            suggestions.append(suggestion)

    # Use LLM to find logical bugs
    llm_raw = llm_service.generate(
        instruction="Find and fix the logical bug in this code.",
        input_text=f"Code:\n{code}"
    )
    llm_parsed = llm_service.parse_output(llm_raw)

    return {
        "success": True,
        "issues": analysis["issues"],
        "debug_suggestions": suggestions,
        "llm_analysis": llm_parsed,
        "rag_context": analysis["rag_context"],
        "execution_time": analysis["execution_time"],
    }


def explain_error(
    error: str,
    language: str | None = None,
) -> dict[str, Any]:
    """
    Retrieve similar debugging cases and use LLM to explain the error.
    """

    logger.info("Explaining error using LLM.")

    start_time = time.perf_counter()

    try:

        rag_results = retrieve_context(
            query=error,
            top_k=5,
        )

        llm_raw = llm_service.generate(
            instruction="Explain this compiler error and provide a fix.",
            input_text=f"Error:\n{error}"
        )
        llm_parsed = llm_service.parse_output(llm_raw)

        execution_time = round(
            time.perf_counter() - start_time,
            4,
        )

        return {
            "success": True,
            "technical": llm_parsed.get("technical", "Analysis failed to generate technical explanation."),
            "beginner": llm_parsed.get("beginner", "Analysis failed to generate beginner explanation."),
            "analogy": llm_parsed.get("analogy", "Analysis failed to generate analogy."),
            "solution": llm_parsed.get("solution", ""),
            "optimized_code": llm_parsed.get("optimized_code", ""),
            "references": _format_rag_results(
                rag_results
            ),
            "execution_time": execution_time,
        }

    except Exception:

        logger.exception("Error explanation failed.")

        raise


def optimize_code(
    code: str,
    language: str,
) -> dict[str, Any]:
    """
    Generate optimization recommendations using Rule Engine and LLM.
    """

    analysis = analyze_code(
        code=code,
        language=language,
    )

    recommendations = []

    for issue in analysis["issues"]:
        suggestion = issue.get("suggestion")

        if suggestion:
            recommendations.append(suggestion)

    llm_raw = llm_service.generate(
        instruction="Suggest performance optimizations for this code.",
        input_text=f"Code:\n{code}"
    )
    llm_parsed = llm_service.parse_output(llm_raw)

    if llm_parsed.get("solution"):
        recommendations.append(llm_parsed["solution"])

    return {
        "success": True,
        "current_complexity": llm_parsed.get("complexity_before"),
        "optimized_complexity": llm_parsed.get("complexity_after"),
        "recommendations": recommendations,
        "optimized_code": llm_parsed.get("optimized_code"),
        "rag_context": analysis["rag_context"],
        "execution_time": analysis["execution_time"],
    }


def health_status(
    version: str,
) -> dict[str, str]:
    """
    Return backend health information.
    """

    logger.info("Health check requested.")

    return {
        "status": "healthy",
        "version": version,
    }