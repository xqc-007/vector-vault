from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chunk_endpoint():
    response = client.post(
        "/chunks",
        json={
            "text": "Retrieval systems need useful chunks before embeddings.",
            "chunk_size": 30,
            "overlap": 5,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["chunk_count"] >= 2
    assert len(body["chunks"]) == body["chunk_count"]


def test_load_document_returns_404_for_missing_file():
    response = client.post(
        "/documents/load",
        json={"path": "data/sample_docs/does-not-exist.md"},
    )

    assert response.status_code == 404
