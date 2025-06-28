from fastapi import APIRouter, UploadFile, File, HTTPException
from models.upload_response import UploadResponse
from services import file_service
from services.vector_service import VectorService

vector_service = VectorService()
file_controller = APIRouter()

@file_controller.post(
    path="/upload",
    response_model=UploadResponse,
    summary="Upload a document, ingest it into chunks, and index with FAISS"
)
async def upload_file(file: UploadFile = File(...)):
    try:
        chunks = await file_service.ingest_file(file)    # Break into chunks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    try:
        vector_service.upsert(chunks=chunks)             # Embed into FAISS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

    # TODO: Add support for Pinecone

    return UploadResponse(
        filename=file.filename,
        num_chunks_indexed=len(chunks),
        first_chunk_id=chunks[0].chunk_id if chunks else None
    )

