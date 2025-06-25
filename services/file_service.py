from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader  # Extend for PDF, DOCX, etc.


async def ingest_file(file: UploadFile):
    contents = await file.read()
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    try:
        loader = TextLoader(path)
        docs = loader.load()
    except Exception as e:
        return {"status": "error", "message": f"Failed to process file: {str(e)}"}

    return {
        "status": "success",
        "filename": file.filename,
        "chunks": len(docs),
        "preview": docs[0].page_content[:300] if docs else "No content found"
    }