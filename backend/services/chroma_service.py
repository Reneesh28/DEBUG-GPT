"""
backend/services/chroma_service.py

Purpose:
    Initialize the local ChromaDB database and create the required collections.

Responsibilities:
    ONLY
        PersistentClient
            ↓
        Collections

    This file should NEVER know SentenceTransformer exists.

Collections:
    - compiler_errors
    - runtime_errors
    - logical_bugs
    - optimization_examples
    - educational_explanations
"""

from pathlib import Path

import chromadb
from chromadb.config import Settings


# ── Configuration ──────────────────────────────────────────────────────────

COLLECTION_NAMES = [
    "compiler_errors",
    "runtime_errors",
    "logical_bugs",
    "optimization_examples",
    "educational_explanations",
]

# ── Database Client ────────────────────────────────────────────────────────

project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "chroma_db"
db_path.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(
    path=str(db_path),
    settings=Settings(anonymized_telemetry=False),
)

# ── Collections ────────────────────────────────────────────────────────────

collections = {}

for _name in COLLECTION_NAMES:
    collections[_name] = client.get_or_create_collection(name=_name)


# ── Helper Functions ───────────────────────────────────────────────────────

def get_collection(collection_name: str):
    """Return a collection by name."""

    if collection_name not in collections:
        raise ValueError(f"Collection '{collection_name}' does not exist.")

    return collections[collection_name]


def list_collections():
    """Return a list of available collection names."""

    return list(collections.keys())