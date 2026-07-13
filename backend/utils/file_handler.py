"""
Utility functions for validating and reading uploaded files.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, UploadFile

from backend.config import (
    MAX_FILE_SIZE,
    SUPPORTED_FILE_TYPES,
)


async def validate_file(file: UploadFile) -> None:
    """
    Validate an uploaded file.

    Checks:
        - File exists
        - Supported extension
        - Maximum size
        - UTF-8 encoding
        - Not empty
    """

    if file is None:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=(
                f"Unsupported file type '{extension}'. "
                f"Supported types: "
                f"{', '.join(sorted(SUPPORTED_FILE_TYPES))}"
            ),
        )

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                f"File exceeds maximum size "
                f"({MAX_FILE_SIZE // (1024 * 1024)} MB)."
            ),
        )

    try:
        content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="File must use UTF-8 encoding.",
        ) from exc

    await file.seek(0)


async def read_file(file: UploadFile) -> str:
    """
    Read uploaded file as UTF-8 text.
    """

    await validate_file(file)

    content = await file.read()

    await file.seek(0)

    return content.decode("utf-8")