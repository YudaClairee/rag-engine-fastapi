from fastapi import APIRouter

from app.core import vector

search_router = APIRouter()


@search_router.get("/search")
def search(query: str, n_results: int = 5):
    return {"results": vector.search(query, n_results)}
