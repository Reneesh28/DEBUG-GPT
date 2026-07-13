"""
Code analysis endpoints.
"""

import logging

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from backend.schemas.request_models import AnalyzeRequest
from backend.schemas.response_models import AnalyzeResponse
from backend.services.analysis_service import analyze_code
from backend.utils.file_handler import read_file

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze Source Code",
)
async def analyze(
    language: str = Form(...),
    code: str | None = Form(None),
    file: UploadFile | None = File(None),
) -> AnalyzeResponse:
    """
    Analyze submitted source code.

    Accepts either:
    - pasted code
    - uploaded source file
    """

    logger.info("Received analyze request.")

    if file is not None:
        code = await read_file(file)

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Either 'code' or 'file' must be provided.",
        )

    request = AnalyzeRequest(
        language=language,
        code=code,
    )

    result = analyze_code(
        code=request.code,
        language=request.language,
    )

    return AnalyzeResponse(**result)