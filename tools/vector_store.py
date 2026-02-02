from typing import Dict, List
from sentence_transformers import SentenceTransformer
import chromadb


class PaperVectorStore:
    """
    Lightweight VectorDB wrapper for paper sections.
    """

    def __init__(self, collection_name: str = "paper_sections"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_sections(self, sections: Dict[str, str]):
        """
        Add paper sections to the vector store.
        """
        documents = []
        metadatas = []
        ids = []

        for idx, (section, text) in enumerate(sections.items()):
            if not text.strip():
                continue

            documents.append(text)
            metadatas.append({"section": section})
            ids.append(f"{section}_{idx}")

        if not documents:
            return

        embeddings = self.embedder.encode(documents).tolist()

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    def query(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Query the vector store for relevant sections.
        """
        embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        matches = []
        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            matches.append(
                {
                    "section": meta["section"],
                    "content": doc[:500],  # truncate for safety
                }
            )

        return matches