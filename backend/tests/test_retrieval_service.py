import numpy as np

from backend.app.retrieval.service import RetrievalService
from backend.app.retrieval.vector_store import VectorStore


class FakeEmbedder:
    def embed(self, texts):
        vectors = []

        for text in texts:
            lowered = text.lower()
            vectors.append([
                float("python" in lowered or "machine" in lowered),
                float("food" in lowered or "cooking" in lowered),
            ])

        return np.array(vectors, dtype=float)


def test_index_and_search():
    service = RetrievalService(
        embedder=FakeEmbedder(),
        store=VectorStore(),
    )

    service.index_text(
        "Python is useful for machine learning.",
        source="ml.txt",
        chunk_size=100,
        overlap=0,
    )

    service.index_text(
        "Cooking food requires good ingredients.",
        source="food.txt",
        chunk_size=100,
        overlap=0,
    )

    results = service.search("python machine learning", top_k=1)

    assert len(results) == 1
    assert results[0].source == "ml.txt"
    assert results[0].score > 0.9
