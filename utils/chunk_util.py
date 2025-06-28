from uuid import uuid4
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings
from models.chunk import Chunk

def split_document(docs: list[Document], source: str, suffix: str) -> list[Chunk]:
    """
    Split a list of LangChain Document objects into our Pydantic Chunk models.

    Uses settings.chunk_size and settings.chunk_overlap to create overlapping
    text windows, then wraps each in a Chunk with metadata.

    Args:
        docs (List[Document]): Loaded documents, each with .page_content and .metadata.
        source (str): Original filename or URL (for citation later).
        suffix (str): File extension (without leading dot), used as the Chunk.type.

    Returns:
        List[Chunk]: A list of chunks with unique IDs and preserved metadata.
    """
    # Split documents into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    split_docs = splitter.split_documents(docs)

    # Wrap the docs into Chunks
    chunks: list[Chunk] = []
    for index, doc in enumerate(split_docs):
        chunk = Chunk(
            chunk_id=uuid4().hex,
            text=doc.page_content,
            source=source,
            type=suffix.lstrip("."),
            index=index,
            metadata=doc.metadata
        )
        chunks.append(chunk)
    return chunks