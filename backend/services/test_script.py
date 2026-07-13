"""
backend/services/test_script.py

Tests the Phase 3 knowledge retrieval pipeline:
    1. Collections exist
    2. Embedding works
    3. Indexing works (checks document counts)
    4. Retrieval works
"""

from backend.services.chroma_service import list_collections, get_collection
from backend.services.embedding_service import embedding_service
from backend.services.rag_service import search, search_all


def test_collections():
    """Test that all ChromaDB collections exist."""

    print("\n" + "=" * 60)
    print("TEST 1 : COLLECTIONS")
    print("=" * 60)

    collections = list_collections()

    print(f"\nCollections Found: {len(collections)}\n")

    total_documents = 0

    for collection_name in collections:

        collection = get_collection(collection_name)

        count = collection.count()

        total_documents += count

        print(f"{collection_name:<30} {count} documents")

    print("\n" + "=" * 60)
    print(f"TOTAL DOCUMENTS : {total_documents}")
    print("=" * 60)


def test_embedding():
    """Test that embedding generation works."""

    print("\n" + "=" * 60)
    print("TEST 2 : EMBEDDING")
    print("=" * 60)

    test_text = "IndexError: list index out of range"

    embedding = embedding_service.generate_embedding(test_text)

    print(f"\nInput Text  : {test_text}")
    print(f"Vector Size : {len(embedding)}")
    print(f"First 5     : {embedding[:5]}")
    print(f"\n[OK] Embedding works.")


def test_retrieval():
    """Test that similarity search works."""

    print("\n" + "=" * 60)
    print("TEST 3 : RETRIEVAL")
    print("=" * 60)

    query = "list index out of range"

    # Check if any collection has documents
    has_documents = False
    for name in list_collections():
        if get_collection(name).count() > 0:
            has_documents = True
            break

    if not has_documents:
        print("\n[!!] No documents indexed yet. Run index_dataset.py first.")
        print("     Skipping retrieval test.")
        return

    print(f"\nQuery : \"{query}\"")
    print(f"\nSearching all collections...\n")

    results = search_all(query, top_k=5)

    for i, result in enumerate(results, 1):

        print(f"  Result {i}")
        print(f"    ID         : {result['id']}")
        print(f"    Collection : {result['collection']}")
        print(f"    Distance   : {result['distance']:.4f}")
        print(f"    Language   : {result['metadata'].get('language', 'N/A')}")
        print(f"    Category   : {result['metadata'].get('category', 'N/A')}")
        print(f"    Document   : {result['document'][:100]}...")
        print()

    print(f"[OK] Retrieval works. {len(results)} results returned.")


def main():

    test_collections()
    test_embedding()
    test_retrieval()


if __name__ == "__main__":
    main()