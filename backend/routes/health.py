"""
Health check endpoints.
"""

from fastapi import APIRouter

from backend.config import APP_VERSION
from backend.schemas.response_models import HealthResponse
from backend.services.analysis_service import health_status

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def get_health() -> HealthResponse:
    """
    Verify backend status.
    """

    result = health_status(APP_VERSION)

    return HealthResponse(**result)