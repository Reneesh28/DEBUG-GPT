"""
Logging configuration for the DebugGPT backend.
"""

from __future__ import annotations

import logging


def configure_logging() -> None:
    """
    Configure application logging.

    This function should be called once during
    FastAPI startup.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)