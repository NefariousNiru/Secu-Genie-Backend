# backend/services/vector_service.py

import torch
from typing import List, Tuple
from faiss import IndexFlatL2
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config.settings import settings
from models.chunk import Chunk


class VectorService:
    """
    Wrapper around LangChain's FAISS vectorstore for chunk embeddings.

    - Stores embeddings + metadata (via the Document.metadata field).
    - Persists index to disk automatically.
    - Supports similarity_search_with_score for citations.
    """

    def __init__(self, embedder=None):
        # Prepare index directory
        self.index_path = settings.faiss_index_dir
        self.index_path.mkdir(parents=True, exist_ok=True)

        # Use the provided embedder, or default to local all-MiniLM-L6-v2
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embedder = embedder or HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": device},
        )

        # Load existing index or start fresh
        if (self.index_path / "index.faiss").exists():
            self.store = FAISS.load_local(
                str(self.index_path),
                self.embedder,
                allow_dangerous_deserialization=True,
            )
        else:
            sample_vector = self.embedder.embed_query("test")
            dim = len(sample_vector)
            self.store = FAISS(
                embedding_function=self.embedder,
                index=IndexFlatL2(dim),
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

    def upsert(self, chunks: List[Chunk]) -> None:
        """
        Embed and add a list of Chunk objects to the FAISS index.

        Each Chunk’s metadata is stored in the Document.metadata,
        so we can retrieve source/index later for citation.
        """
        # Convert Chunk → LangChain Document
        docs = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk.text,
                metadata={
                    "chunk_id": chunk.chunk_id,
                    "source": chunk.source,
                    "type": chunk.type,
                    "index": chunk.index,
                    **chunk.metadata,
                },
            )
            docs.append(doc)

        # Add to index and persist
        self.store.add_documents(docs)
        self.store.save_local(str(self.index_path))

    def search(self, query: str, top_k: int) -> List[Tuple[Chunk, float]]:
        """
        Perform a similarity search on the query text.

        Returns a list of (Chunk, score) tuples for the top_k hits.
        """
        # similarity_search_with_score returns List[(Document, score)]
        results = self.store.similarity_search_with_score(query, top_k)
        hits = []
        for doc, score in results:
            meta = doc.metadata
            # Reconstruct our Chunk object (or a lightweight Citation)
            chunk = Chunk(
                chunk_id=meta["chunk_id"],
                text=doc.page_content,
                source=meta["source"],
                type=meta["type"],
                index=meta["index"],
                metadata={
                    k: v
                    for k, v in meta.items()
                    if k not in {"chunk_id", "source", "type", "index"}
                },
            )
            hits.append((chunk, score))
        return hits
