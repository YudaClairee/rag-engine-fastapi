from fastapi import APIRouter

from app.core import vector

document_router = APIRouter()


@document_router.get("/document")
def get_all_documents():
    return {"documents": vector.list_documents()}


@document_router.get("/document/{doc_id}")
def get_document_by_id(doc_id: str):
    result = vector.get_document_chunks(doc_id)
    chunks = [
        {
            "id": result["ids"][i],
            "text": result["documents"][i] if result["documents"] else None,
            "chunk_index": result["metadatas"][i]["chunk_index"]
            if result["metadatas"]
            else None,
        }
        for i in range(len(result["ids"]))
    ]
    return {"document": chunks}
