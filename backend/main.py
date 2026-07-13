"""
Main FastAPI application for DebugGPT.
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from backend.exceptions.handlers import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
)
from pydantic import ValidationError

from backend.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
)
from backend.routes import (
    analyze,
    debug,
    explain,
    health,
    optimize,
)
from backend.utils.logging_config import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown lifecycle.
    """

    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("Starting DebugGPT Backend...")

    yield

    logger.info("Shutting down DebugGPT Backend...")


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(debug.router)
app.include_router(explain.router)
app.include_router(optimize.router)

# Register exception handlers

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    ValidationError,
    pydantic_validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler,
)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to DebugGPT Backend",
        "version": APP_VERSION,
    }


@app.get("/test-error")
async def test_error():
    """
    Endpoint that raises a general exception for testing purposes.
    """
    raise Exception("Forced error for E2E testing")