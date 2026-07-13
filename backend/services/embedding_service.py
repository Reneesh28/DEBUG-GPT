"""
backend/services/embedding_service.py

Purpose:
    Generate embeddings using the BAAI/bge-small-en-v1.5 model.

Responsibilities:
    - Load the embedding model only once.
    - Generate embeddings for a single text.
    - Generate embeddings for multiple texts (batch mode).
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Handles embedding generation."""

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self):
        print(f"\nLoading embedding model: {self.MODEL_NAME}")

        self.model = SentenceTransformer(self.MODEL_NAME, device="cpu")

        print("Embedding model loaded successfully.\n")

    def generate_embedding(self, text: str) -> list:
        """
        Generate an embedding for a single piece of text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def generate_embeddings(self, texts: list[str]) -> list:
        """
        Generate embeddings for multiple texts.

        Parameters
        ----------
        texts : list[str]

        Returns
        -------
        list[list[float]]
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings.tolist()


embedding_service = EmbeddingService()