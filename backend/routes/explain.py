"""
Error explanation endpoints.
"""

import logging

from fastapi import APIRouter

from backend.schemas.request_models import ExplainRequest
from backend.schemas.response_models import ExplainResponse
from backend.services.analysis_service import explain_error

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Explain"])


@router.post(
    "/explain",
    response_model=ExplainResponse,
    summary="Explain Compiler or Runtime Error",
)
async def explain(
    request: ExplainRequest,
) -> ExplainResponse:
    """
    Explain a compiler or runtime error.
    """

    logger.info("Received explain request.")

    result = explain_error(
        error=request.error,
        language=request.language,
    )

    return ExplainResponse(**result)