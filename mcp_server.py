from mcp.server.fastmcp import FastMCP

from app.core import vector

app = FastMCP(name="rag-engine", json_response=True)


@app.tool()
def search_documents(query: str, n_results: int = 5):
    """Search through uploaded documents using semantic search."""
    return str(vector.search(query, n_results))


@app.tool()
def list_documents():
    """List all uploaded documents."""
    return str(vector.list_documents())


@app.tool()
def get_document_by_id(doc_id: str):
    """Get details and chunks of a specific document."""
    return str(vector.get_document_chunks(doc_id))


if __name__ == "__main__":
    app.run(transport="streamable-http")
