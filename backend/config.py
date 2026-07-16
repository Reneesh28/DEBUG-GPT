"""
Application configuration for DebugGPT backend.
"""

from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# API metadata
APP_NAME = "DebugGPT Backend"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "FastAPI backend for the DebugGPT AI-powered debugging assistant."
)

# Supported languages
SUPPORTED_LANGUAGES = {"cpp", "python"}

# Supported upload types
SUPPORTED_FILE_TYPES = {
    ".cpp",
    ".py",
    ".log",
    ".ipynb",
}

# Maximum upload size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# LLM Configuration
BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
LORA_ADAPTER_PATH = BASE_DIR / "models" / "debuggpt-lora"