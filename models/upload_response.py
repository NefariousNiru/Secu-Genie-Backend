# backend/models/upload.py

from pydantic import BaseModel, Field
from typing import Optional


class UploadResponse(BaseModel):
    """
    Response returned after successful file upload and indexing.
    """

    filename: str = Field(..., description="Original filename uploaded by the user")
    num_chunks_indexed: int = Field(
        ..., description="Number of text chunks created and indexed"
    )
    first_chunk_id: Optional[str] = Field(
        None, description="ID of the first chunk (for preview or verification)"
    )
