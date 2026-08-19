import numpy as np

from backend.app.retrieval.vector_store import VectorStore


def test_adds_chunks_to_store():
    store = VectorStore()
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])

    added = store.add(
        texts=["cats", "cars"],
        vectors=vectors,
        source="test.txt",
    )

    assert added == 2
    assert store.count() == 2


def test_search_returns_closest_vector_first():
    store = VectorStore()
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])

    store.add(
        texts=["machine learning", "cooking"],
        vectors=vectors,
        source="notes.md",
    )

    results = store.search(np.array([0.9, 0.1]), top_k=2)

    assert results[0].text == "machine learning"
    assert results[0].score > results[1].score


def test_search_empty_store_returns_empty_list():
    store = VectorStore()
    assert store.search(np.array([1.0, 0.0]), top_k=3) == []
