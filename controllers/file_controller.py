from fastapi import APIRouter, UploadFile, File, Depends
from services import file_service
from services.vector_service import VectorService

file_controller = APIRouter()
vector_service = VectorService()

@file_controller.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    chunks = await file_service.ingest_file(file)    # Break into chunks

    vector_service.upsert(chunks=chunks)             # Embed into FAISS
    # TODO: Add support for Pinecone

    return {
        "filename": file.filename,
        "num_chunks_indexed": len(chunks),
        "first_chunk_id": chunks[0].chunk_id if chunks else None
    }

