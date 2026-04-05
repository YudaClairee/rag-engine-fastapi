from fastapi import APIRouter
from fastapi import UploadFile, File
import uuid
import datetime

from app.core import ocr, chunker, vector

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_name = file.filename
    doc_id = str(uuid.uuid4())
    text = ocr.extract_text(file_bytes)
    chunks = chunker.chunk_text(text)
    vector.add_document(
        doc_id,
        chunks,
        {
            "filename": file_name,
            "uploaded_at": str(datetime.datetime.now()),
        },
    )
    return {
        "id": doc_id,
        "filename": file_name,
        "chunk_count": len(chunks),
    }
