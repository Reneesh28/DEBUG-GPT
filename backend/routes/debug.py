"""
Debugging endpoints.
"""

import logging

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from backend.schemas.request_models import DebugRequest
from backend.schemas.response_models import DebugResponse
from backend.services.analysis_service import debug_code
from backend.utils.file_handler import read_file

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Debug"])


@router.post(
    "/debug",
    response_model=DebugResponse,
    summary="Debug Source Code",
)
async def debug(
    language: str = Form(...),
    code: str | None = Form(None),
    file: UploadFile | None = File(None),
) -> DebugResponse:
    """
    Generate debugging suggestions.
    """

    logger.info("Received debug request.")

    if file is not None:
        code = await read_file(file)

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Either 'code' or 'file' must be provided.",
        )

    request = DebugRequest(
        language=language,
        code=code,
    )

    result = debug_code(
        code=request.code,
        language=request.language,
    )

    return DebugResponse(**result)