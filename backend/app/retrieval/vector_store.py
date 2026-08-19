from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class StoredChunk:
    text: str
    source: str
    chunk_index: int
    vector: np.ndarray


@dataclass
class SearchMatch:
    text: str
    source: str
    chunk_index: int
    score: float


class VectorStore:
    def __init__(self):
        self._chunks: list[StoredChunk] = []

    def clear(self) -> None:
        self._chunks.clear()

    def count(self) -> int:
        return len(self._chunks)

    def add(self, texts: list[str], vectors: np.ndarray, source: str) -> int:
        if len(texts) != len(vectors):
            raise ValueError("Texts and vectors must have the same length.")

        for chunk_index, (text, vector) in enumerate(zip(texts, vectors)):
            self._chunks.append(
                StoredChunk(
                    text=text,
                    source=source,
                    chunk_index=chunk_index,
                    vector=np.asarray(vector, dtype=float),
                )
            )

        return len(texts)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[SearchMatch]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not self._chunks:
            return []

        query = np.asarray(query_vector, dtype=float)
        query_norm = np.linalg.norm(query)

        if query.ndim != 1:
            raise ValueError("Query vector must be one-dimensional.")
        if query_norm == 0:
            raise ValueError("Query vector cannot be all zeros.")

        scored = []

        for chunk in self._chunks:
            chunk_norm = np.linalg.norm(chunk.vector)
            score = 0.0 if chunk_norm == 0 else float(
                np.dot(query, chunk.vector) / (query_norm * chunk_norm)
            )

            scored.append(
                SearchMatch(
                    text=chunk.text,
                    source=chunk.source,
                    chunk_index=chunk.chunk_index,
                    score=score,
                )
            )

        scored.sort(key=lambda match: match.score, reverse=True)
        return scored[:top_k]
