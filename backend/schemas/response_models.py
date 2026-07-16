"""
Pydantic response models for DebugGPT API.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class IssueModel(BaseModel):
    """
    Represents a detected issue from the Rule Engine.
    """

    model_config = ConfigDict(from_attributes=True)

    issue: str
    severity: str
    confidence: float

    line: int | None = None
    message: str |None = None
    suggestion: str | None = None
    rule_id: str | None = None


class RagResult(BaseModel):
    """
    Represents a retrieved RAG document.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    document: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    distance: float
    collection: str


class AnalyzeResponse(BaseModel):
    """
    Response returned by /analyze.
    """

    success: bool
    language: str

    issues: list[IssueModel] = Field(default_factory=list)

    rag_context: list[RagResult] = Field(default_factory=list)

    execution_time: float


class DebugResponse(BaseModel):
    """
    Response returned by /debug.
    """

    success: bool

    issues: list[IssueModel] = Field(default_factory=list)

    debug_suggestions: list[str] = Field(default_factory=list)

    llm_analysis: dict[str, Any] = Field(default_factory=dict)

    rag_context: list[RagResult] = Field(default_factory=list)

    execution_time: float


class ExplainResponse(BaseModel):
    """
    Response returned by /explain.
    """

    success: bool

    technical: str

    beginner: str

    analogy: str

    solution: str | None = None

    optimized_code: str | None = None

    references: list[RagResult] = Field(default_factory=list)

    execution_time: float


class OptimizeResponse(BaseModel):
    """
    Response returned by /optimize.
    """

    success: bool

    current_complexity: str | None = None

    optimized_complexity: str | None = None

    recommendations: list[str] = Field(default_factory=list)

    optimized_code: str | None = None

    rag_context: list[RagResult] = Field(default_factory=list)

    execution_time: float


class HealthResponse(BaseModel):
    """
    Response returned by /health.
    """

    status: str
    version: str


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    success: bool = False

    error: str

    details: str | None = None