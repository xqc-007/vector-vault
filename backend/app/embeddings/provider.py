from __future__ import annotations

import numpy as np


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            raise ValueError("At least one text value is required.")

        cleaned = [text.strip() for text in texts]
        if any(not text for text in cleaned):
            raise ValueError("Text values cannot be empty.")

        model = self._load_model()
        vectors = model.encode(
            cleaned,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return np.asarray(vectors, dtype=float)
