import numpy as np
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.retrieval.service import retrieval_service


class FakeEmbedder:
    def embed(self, texts):
        vectors = []

        for text in texts:
            lowered = text.lower()
            vectors.append([
                float("retrieval" in lowered or "vector" in lowered),
                float("database" in lowered),
            ])

        return np.array(vectors, dtype=float)


client = TestClient(app)


def setup_function():
    retrieval_service.store.clear()
    retrieval_service.embedder = FakeEmbedder()


def test_index_endpoint():
    response = client.post(
        "/index",
        json={
            "text": "Vector retrieval finds relevant text.",
            "source": "notes.md",
            "chunk_size": 100,
            "overlap": 0,
        },
    )

    assert response.status_code == 200
    assert response.json()["indexed_chunks"] == 1


def test_search_endpoint_returns_ranked_result():
    client.post(
        "/index",
        json={
            "text": "Vector retrieval finds relevant text.",
            "source": "retrieval.md",
            "chunk_size": 100,
            "overlap": 0,
        },
    )

    client.post(
        "/index",
        json={
            "text": "A database stores structured records.",
            "source": "database.md",
            "chunk_size": 100,
            "overlap": 0,
        },
    )

    response = client.post(
        "/search",
        json={"query": "vector retrieval", "top_k": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result_count"] == 1
    assert data["results"][0]["source"] == "retrieval.md"
