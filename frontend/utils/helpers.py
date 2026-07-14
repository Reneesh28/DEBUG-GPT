"""
Utility helper functions for the Streamlit frontend.
"""

from pathlib import Path


SUPPORTED_SOURCE_EXTENSIONS = {
    ".py",
    ".cpp",
    ".ipynb",
}

SUPPORTED_LOG_EXTENSIONS = {
    ".log",
}


def read_uploaded_file(uploaded_file):
    """
    Read uploaded file contents as UTF-8 text.
    """

    if uploaded_file is None:
        return ""

    return uploaded_file.getvalue().decode("utf-8")


def validate_extension(filename, allowed_extensions):
    """
    Validate uploaded file extension.
    """

    extension = Path(filename).suffix.lower()

    return extension in allowed_extensions


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes into a human-readable string.
    """

    if size_bytes < 1024:
        return f"{size_bytes} B"

    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"

    return f"{size_bytes / (1024 * 1024):.2f} MB"