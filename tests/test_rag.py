"""
tests/test_rag.py

Purpose:
    Test the Retrieval-Augmented Generation (RAG) retrieval layer.

This test verifies:

✓ Query embedding generation
✓ ChromaDB search
✓ Metadata retrieval
✓ Top-K retrieval
✓ Search across all collections

This test DOES NOT:

✗ Call an LLM
✗ Read dataset JSON files
✗ Insert into ChromaDB
"""

from backend.services.rag_service import (
    search,
    search_all,
)


TEST_CASES = [
    {
        "name": "Compiler Error",
        "collection": "compiler_errors",
        "query": "SyntaxError expected ':' in Python if statement",
    },
    {
        "name": "Runtime Error",
        "collection": "runtime_errors",
        "query": "IndexError list index out of range",
    },
    {
        "name": "Logical Bug",
        "collection": "logical_bugs",
        "query": "Binary search returns incorrect result",
    },
    {
        "name": "Optimization",
        "collection": "optimization_examples",
        "query": "Optimize nested loops",
    },
    {
        "name": "Educational",
        "collection": "educational_explanations",
        "query": "Explain recursion for beginners",
    },
]


def print_result(result_number, result):

    print(f"\nResult #{result_number}")
    print("-" * 60)

    print(f"ID        : {result['id']}")
    print(f"Distance  : {result['distance']:.4f}")

    metadata = result.get("metadata", {})

    print(f"Language  : {metadata.get('language')}")
    print(f"Category  : {metadata.get('category')}")
    print(f"Title     : {metadata.get('title')}")

    print("\nDocument Preview:")

    document = result["document"]

    preview = document[:300]

    print(preview)

    if len(document) > 300:
        print("...")


def test_single_collection():

    print("=" * 80)
    print("TESTING INDIVIDUAL COLLECTIONS")
    print("=" * 80)

    for case in TEST_CASES:

        print("\n")
        print("=" * 80)

        print(case["name"])

        print("=" * 80)

        results = search(
            query=case["query"],
            collection_name=case["collection"],
            top_k=5,
        )

        print(f"Returned Results : {len(results)}")

        if not results:
            print("FAILED")
            continue

        print("PASSED")

        print_result(1, results[0])


def test_global_search():

    print("\n")
    print("=" * 80)
    print("GLOBAL SEARCH")
    print("=" * 80)

    query = "Python syntax error missing colon"

    results = search_all(
        query=query,
        top_k=5,
    )

    print(f"Returned Results : {len(results)}")

    if not results:
        print("FAILED")
        return

    print("PASSED")

    for i, result in enumerate(results, start=1):

        print(f"\nRank {i}")

        print(f"Collection : {result['collection']}")

        print_result(i, result)


def main():

    test_single_collection()

    test_global_search()

    print("\n")
    print("=" * 80)
    print("RAG TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()