"""
Pydantic request models for DebugGPT API.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


SUPPORTED_LANGUAGES = {"cpp", "python"}


class AnalyzeRequest(BaseModel):
    """
    Request model for code analysis.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    language: Literal["cpp", "python"]
    code: str = Field(..., min_length=1)

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code cannot be empty.")
        return value


class DebugRequest(BaseModel):
    """
    Request model for debugging.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    language: Literal["cpp", "python"]
    code: str = Field(..., min_length=1)

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code cannot be empty.")
        return value


class ExplainRequest(BaseModel):
    """
    Request model for compiler/runtime error explanation.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    error: str = Field(..., min_length=1)
    language: Literal["cpp", "python"] | None = None

    @field_validator("error")
    @classmethod
    def validate_error(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Error message cannot be empty.")
        return value


class OptimizeRequest(BaseModel):
    """
    Request model for code optimization.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    language: Literal["cpp", "python"]
    code: str = Field(..., min_length=1)

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code cannot be empty.")
        return value


class FileUploadRequest(BaseModel):
    """
    Metadata for uploaded files.

    Note:
    The actual uploaded file will be handled by FastAPI's UploadFile
    in the API endpoint.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    language: Literal["cpp", "python"]
    filename: str = Field(..., min_length=1)

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Filename cannot be empty.")
        return value