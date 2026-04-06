from typing import Any

import chromadb
from chromadb.api.types import GetResult

_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_or_create_collection("documents")


def add_document(
    doc_id: str, chunks: list[str], metadata: dict[str, Any] | None = None
):
    _collection.add(
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {
                "document_id": doc_id,
                "chunk_index": i,
                **(metadata or {}),
            }
            for i in range(len(chunks))
        ],
    )


def search(query: str, n_results: int = 5) -> list[dict[str, Any]]:
    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"]
    metadatas = results["metadatas"]
    distances = results["distances"]
    assert docs is not None and metadatas is not None and distances is not None

    return [
        {
            "document_id": metadatas[0][i].get("document_id", ""),
            "filename": metadatas[0][i].get("filename", ""),
            "chunk_index": metadatas[0][i].get("chunk_index", 0),
            "distance": distances[0][i],
            "text": docs[0][i],
        }
        for i in range(len(docs[0]))
    ]


def get_document_chunks(doc_id: str) -> GetResult:
    return _collection.get(
        where={"document_id": doc_id},
    )


def list_documents() -> list[dict[str, Any]]:
    results = _collection.get()
    seen: dict[str, dict[str, Any]] = {}
    if results["metadatas"]:
        for meta in results["metadatas"]:
            id = str(meta["document_id"])
            if id not in seen:
                seen[id] = {
                    "id": id,
                    "filename": meta.get("filename", ""),
                    "uploaded_at": meta.get("uploaded_at", ""),
                }
    return list(seen.values())
