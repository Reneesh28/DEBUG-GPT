"""
Optimization endpoints.
"""

import logging

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from backend.schemas.request_models import OptimizeRequest
from backend.schemas.response_models import OptimizeResponse
from backend.services.analysis_service import optimize_code
from backend.utils.file_handler import read_file

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Optimization"])


@router.post(
    "/optimize",
    response_model=OptimizeResponse,
    summary="Optimize Source Code",
)
async def optimize(
    language: str = Form(...),
    code: str | None = Form(None),
    file: UploadFile | None = File(None),
) -> OptimizeResponse:
    """
    Generate optimization recommendations.
    """

    logger.info("Received optimize request.")

    if file is not None:
        code = await read_file(file)

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Either 'code' or 'file' must be provided.",
        )

    request = OptimizeRequest(
        language=language,
        code=code,
    )

    result = optimize_code(
        code=request.code,
        language=request.language,
    )

    return OptimizeResponse(**result)