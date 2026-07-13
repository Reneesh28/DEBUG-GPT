"""
backend/services/rag_service.py

Purpose:
    Perform similarity search against ChromaDB collections.

Responsibilities:
    Query
        ↓
    Generate Query Embedding
        ↓
    Search ChromaDB
        ↓
    Return Top-K Results

This file NEVER:
    - Reads dataset JSON files
    - Inserts data into ChromaDB
    - Calls an LLM
"""

from typing import Any

from backend.services.chroma_service import (
    get_collection,
    list_collections,
)
from backend.services.embedding_service import embedding_service


def search(
    query: str,
    collection_name: str,
    top_k: int = 5,
    where: dict | None = None,
) -> list[dict[str, Any]]:
    """
    Search a single ChromaDB collection.

    Args:
        query:
            User query.

        collection_name:
            Collection to search.

        top_k:
            Number of results to return.

        where:
            Optional ChromaDB metadata filter.

    Returns:
        List of search results.
    """

    available = list_collections()

    if collection_name not in available:
        raise ValueError(
            f"Collection '{collection_name}' does not exist.\n"
            f"Available collections: {available}"
        )

    collection = get_collection(collection_name)

    query_embedding = embedding_service.generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    ids = results.get("ids", [[]])[0]

    if not ids:
        return []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    output = []

    for doc_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        output.append(
            {
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return output


def search_all(
    query: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Search across all collections and return
    the globally most relevant results.

    Args:
        query:
            User query.

        top_k:
            Number of results to return.

    Returns:
        Top-K results sorted by distance.
    """

    all_results = []

    for collection_name in list_collections():

        results = search(
            query=query,
            collection_name=collection_name,
            top_k=top_k,
        )

        for result in results:
            result["collection"] = collection_name
            all_results.append(result)

    all_results.sort(key=lambda item: item["distance"])

    return all_results[:top_k]


def search_by_language(
    query: str,
    collection_name: str,
    language: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Search within a collection filtered by language.
    """

    return search(
        query=query,
        collection_name=collection_name,
        top_k=top_k,
        where={
            "language": language,
        },
    )


def search_by_difficulty(
    query: str,
    collection_name: str,
    difficulty: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Search within a collection filtered by difficulty.
    """

    return search(
        query=query,
        collection_name=collection_name,
        top_k=top_k,
        where={
            "difficulty": difficulty,
        },
    )


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Retrieve the most relevant debugging context.

    This is the function the FastAPI backend should use.
    It searches across all ChromaDB collections.

    Args:
        query:
            User code or error.

        top_k:
            Number of retrieved documents.

    Returns:
        List of retrieved debugging examples.
    """

    return search_all(
        query=query,
        top_k=top_k,
    )