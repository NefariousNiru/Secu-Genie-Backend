import os
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import List
from fastapi import UploadFile, HTTPException
from models.chunk import Chunk
from services.loaders import loaders
from utils import chunk_util


async def ingest_file(file: UploadFile) -> List[Chunk]:
    """
    Ingests an uploaded file, loads its content, splits into overlapping chunks,
    and returns a list of Chunk models.

    Process:
    1. Save the UploadFile to a temporary local path.
    2. Select the appropriate loader based on the file extension.
    3. Use LangChain loader to read the file into Document objects.
    4. Split Documents into chunks using RecursiveCharacterTextSplitter.
    5. Wrap each chunk into a Pydantic Chunk model with metadata.

    Args:
        file (UploadFile): The incoming file from the HTTP request.

    Returns:
        List[Chunk]: A list of Chunk instances ready for embedding.
    """
    # Determine file extension and loader
    suffix = Path(file.filename).suffix.lower()
    loader_cls = loaders.EXTENSION_LOADER_MAP.get(suffix, None)

    if not loader_cls:
        raise HTTPException(status_code=415, detail=f"Invalid File Format: {suffix}")

    # Save to a temporary file for loader compatibility
    with NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Load documents from the temporary file and then delete it
    loader = loader_cls(tmp_path)
    docs = loader.load()
    os.remove(tmp_path)

    chunks: List[Chunk] = chunk_util.split_document(docs, file.filename, suffix)
    return chunks
