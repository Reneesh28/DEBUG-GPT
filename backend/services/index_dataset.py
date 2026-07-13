"""
backend/services/index_dataset.py

Purpose:
    Read dataset JSON files and index them into ChromaDB.

Responsibilities:
    ONLY
        Read JSON
            ↓
        Embedding
            ↓
        Insert

    This file should NEVER perform similarity search.
    This file should NEVER call an LLM.

Workflow:
    for every json
        ↓
    for every sample
        ↓
    document = build_document(sample)
        ↓
    embedding = generate_embedding(document)
        ↓
    metadata = build_metadata(sample)
        ↓
    collection.add()
"""

import json
from pathlib import Path

from backend.services.chroma_service import get_collection
from backend.services.embedding_service import embedding_service


# ── Configuration ──────────────────────────────────────────────────────────

project_root = Path(__file__).resolve().parents[2]
dataset_root = project_root / "datasets"

DATASETS = {
    "compiler_errors":          dataset_root / "compiler_errors",
    "runtime_errors":           dataset_root / "runtime_errors",
    "logical_bugs":             dataset_root / "logical_bugs",
    "optimization_examples":    dataset_root / "optimization_examples",
    "educational_explanations":  dataset_root / "educational_explanations",
}


# ── Document Builder ───────────────────────────────────────────────────────

def build_document(sample: dict) -> str:
    """
    Create searchable text by combining:
    - instruction
    - input
    - output
    """

    instruction = str(sample.get("instruction", ""))

    user_input = sample.get("input", "")
    if isinstance(user_input, dict):
        user_input_text = "\n".join(
            str(value)
            for value in user_input.values()
            if value
        )
    else:
        user_input_text = str(user_input)

    output = sample.get("output", {})

    if isinstance(output, dict):
        output_text = "\n".join(
            str(value)
            for value in output.values()
            if value
        )
    else:
        output_text = str(output)

    document = "\n\n".join([
        instruction,
        user_input_text,
        output_text
    ])

    return document.strip()


# ── Metadata Builder ───────────────────────────────────────────────────────

def build_metadata(sample: dict) -> dict:
    """
    Extract metadata for ChromaDB.

    Metadata schema:
    {
        "language":   "...",
        "category":   "...",
        "title":      "...",
        "difficulty": "...",
        "tags":       "...",
        "source":     "..."
    }
    """

    metadata_info = sample.get("metadata", {})

    tags = metadata_info.get("tags", [])

    if isinstance(tags, list):
        tags = ", ".join(tags)

    metadata = {
        "language":   sample.get("language", ""),
        "category":   sample.get("category", ""),
        "title":      sample.get("title", ""),
        "difficulty": metadata_info.get("difficulty", ""),
        "tags":       tags,
        "source":     metadata_info.get("source", ""),
    }

    return metadata


# ── File Indexer ───────────────────────────────────────────────────────────

def index_file(json_file: Path, collection_name: str):
    """Index a single JSON file into one ChromaDB collection."""

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    collection = get_collection(collection_name)

    inserted = 0

    for sample in data:

        document = build_document(sample)

        embedding = embedding_service.generate_embedding(document)

        metadata = build_metadata(sample)

        try:

            collection.add(
                ids=[sample["id"]],
                documents=[document],
                embeddings=[embedding],
                metadatas=[metadata],
            )

            inserted += 1

        except Exception as error:
            print(f"Skipped {sample.get('id')} : {error}")

    print(f"Indexed {inserted} samples from {json_file.name}")


# ── Directory Indexer ──────────────────────────────────────────────────────

def index_directory(directory: Path, collection_name: str):
    """Index every JSON file inside a directory."""

    json_files = sorted(directory.rglob("*.json"))

    if not json_files:
        print(f"No JSON files found in {directory}")
        return

    for json_file in json_files:
        index_file(json_file, collection_name)


# ── Index All Datasets ─────────────────────────────────────────────────────

def index_all():
    """Index all dataset categories and display statistics."""

    total_files = 0
    total_samples = 0

    print("\nStarting Dataset Indexing...\n")

    for collection_name, folder in DATASETS.items():

        print("=" * 70)
        print(f"Collection : {collection_name}")
        print("=" * 70)

        json_files = sorted(folder.rglob("*.json"))

        print(f"Files Found : {len(json_files)}")

        category_samples = 0

        for json_file in json_files:

            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            print(
                f"Indexing {json_file.name:<40} "
                f"{len(data):>5} samples"
            )

            index_file(json_file, collection_name)

            category_samples += len(data)

        print(f"Total Samples : {category_samples}\n")

        total_files += len(json_files)
        total_samples += category_samples

    print("=" * 70)
    print("INDEXING COMPLETE")
    print("=" * 70)
    print(f"Collections     : {len(DATASETS)}")
    print(f"Files Indexed   : {total_files}")
    print(f"Samples Indexed : {total_samples}")


# ── Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    index_all()