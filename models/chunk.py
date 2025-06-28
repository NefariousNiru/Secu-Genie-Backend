# backend/models/chunk.py

from pydantic import BaseModel, Field
from typing import Any, Dict

class Chunk(BaseModel):
    """
    Represents a single text chunk extracted from an input document.

    Attributes:
        chunk_id: A unique identifier for this chunk (e.g. UUID or hash).
        text: The chunk’s raw text content.
        source: Original file path or URL where this chunk came from.
        type: File type/loader name (e.g., "pdf", "csv", "notion").
        index: Zero-based chunk index within the document.
        metadata: Additional loader-specific context (e.g. page number, row index).
    """
    chunk_id: str = Field(..., description="Unique ID of this chunk")
    text: str = Field(..., description="Text content of the chunk")
    source: str = Field(..., description="Original document identifier or path")
    type: str = Field(..., description="Loader type or file extension")
    index: int = Field(..., description="Chunk’s sequential index in its source")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional loader-specific metadata for this chunk"
    )
