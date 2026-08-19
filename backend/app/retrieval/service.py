from __future__ import annotations

from backend.app.embeddings.provider import SentenceTransformerEmbedder
from backend.app.ingestion.chunker import chunk_text
from backend.app.retrieval.vector_store import VectorStore


class RetrievalService:
    def __init__(self, embedder=None, store: VectorStore | None = None):
        self.embedder = embedder or SentenceTransformerEmbedder()
        self.store = store or VectorStore()

    def index_text(
        self,
        text: str,
        source: str,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> int:
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        vectors = self.embedder.embed(chunks)
        return self.store.add(chunks, vectors, source)

    def search(self, query: str, top_k: int = 5):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_vector = self.embedder.embed([query])[0]
        return self.store.search(query_vector, top_k=top_k)


retrieval_service = RetrievalService()
