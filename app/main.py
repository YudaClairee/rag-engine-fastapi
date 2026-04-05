from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.modules.document.route import document_router
from app.modules.upload.route import upload_router
from app.modules.search.route import search_router

app = FastAPI()
app.include_router(document_router)
app.include_router(upload_router)
app.include_router(search_router)


@app.get("/")
def read_root():
    return {"message": "Halo kids"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
