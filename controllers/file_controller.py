from fastapi import APIRouter, UploadFile, File
from services import file_service

file_controller = APIRouter()

@file_controller.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return file_service.ingest_file(file)