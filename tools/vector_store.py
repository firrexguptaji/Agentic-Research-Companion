from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np
import os


class PaperVectorStore:
    """
    Lightweight in-memory Vector DB for research papers.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        normalize: bool = True,
    ):
        self.embedder = SentenceTransformer(model_name)
        self.normalize = normalize

        self.embeddings: List[np.ndarray] = []
        self.text_chunks: List[Dict] = []

    # -------------------------
    # Indexing
    # -------------------------
    def add_documents(
        self,
        chunks: List[str],
        metadatas: List[Dict],
    ):
        if not chunks:
            return

        vectors = self.embedder.encode(
            chunks,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        if self.normalize:
            vectors = self._normalize(vectors)

        for vec, text, meta in zip(vectors, chunks, metadatas):
            self.embeddings.append(vec)
            self.text_chunks.append(
                {
                    "text": text,
                    "metadata": meta,
                }
            )

    # -------------------------
    # Search
    # -------------------------
    def similarity_search(
        self,
        query: str,
        top_k: int = 3,
        section_filter: str | None = None,
    ) -> List[Dict]:
        if not self.embeddings:
            return []

        query_vec = self.embedder.encode(
            query,
            convert_to_numpy=True,
        )

        if self.normalize:
            query_vec = query_vec / np.linalg.norm(query_vec)

        scores = np.dot(self.embeddings, query_vec)

        ranked_indices = np.argsort(scores)[::-1]

        results = []
        for idx in ranked_indices:
            item = self.text_chunks[idx]

            if section_filter:
                if item["metadata"].get("section") != section_filter:
                    continue

            results.append(
                {
                    "score": float(scores[idx]),
                    "text": item["text"],
                    "metadata": item["metadata"],
                }
            )

            if len(results) >= top_k:
                break

        return results

    # -------------------------
    # Utils
    # -------------------------
    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-10)