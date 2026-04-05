# RAG Engine

A document ingestion and semantic search engine built with FastAPI, ChromaDB, and Mistral OCR. Upload documents (PDF/images), extract text via Mistral's OCR, chunk them semantically, store embeddings in ChromaDB, and search through them — all exposed as both a REST API and an MCP server.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Upload     │────▶│  Mistral OCR │────▶│  Semantic    │────▶│   ChromaDB   │
│   (PDF/IMG)  │     │  (extract)   │     │  Chunker     │     │  (store)     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │   Search     │
                                                               │   (query)    │
                                                               └──────────────┘
```

**Core modules:**

- `app/core/ocr.py` — Text extraction from PDFs and images using Mistral OCR (`mistral-ocr-latest`)
- `app/core/chunker.py` — Semantic text chunking via [Chonkie](https://github.com/chonkie-ai/chonkie) (threshold 0.7, chunk size 512)
- `app/core/vector.py` — ChromaDB persistence layer for storing/searching document chunks

## Tech Stack

| Component        | Library                                                    |
| ---------------- | ---------------------------------------------------------- |
| Web framework    | [FastAPI](https://fastapi.tiangolo.com/)                   |
| OCR              | [Mistral AI](https://docs.mistral.ai/) (`mistral-ocr-latest`) |
| Text chunking    | [Chonkie](https://github.com/chonkie-ai/chonkie) (semantic mode) |
| Vector store     | [ChromaDB](https://www.trychroma.com/)                     |
| MCP server       | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) |
| API docs         | [Scalar](https://scalar.com/)                              |

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A Mistral AI API key

## Getting Started

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd assignment-6
uv sync
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 3. Run the API server

```bash
make dev
# or directly:
uv run uvicorn app.main:app --reload
```

The server starts at `http://localhost:8000`.

### 4. Run the MCP server

```bash
uv run mcp_server.py
```

This launches the MCP server with `streamable-http` transport, exposing tools for AI assistants/agents to interact with the RAG engine.

## API Endpoints

| Method | Path               | Description                          |
| ------ | ------------------ | ------------------------------------ |
| GET    | `/`                | Health check                         |
| GET    | `/scalar`          | Interactive API documentation        |
| POST   | `/upload`          | Upload a document (PDF, PNG, JPG)    |
| GET    | `/search`          | Semantic search across all documents |
| GET    | `/document`        | List all uploaded documents          |
| GET    | `/document/{id}`   | Get chunks of a specific document    |

### Upload a document

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@your-document.pdf"
```

**Response:**

```json
{
  "id": "uuid-of-the-document",
  "filename": "your-document.pdf",
  "chunk_count": 12
}
```

### Search documents

```bash
curl "http://localhost:8000/search?query=your+search+term&n_results=5"
```

### List all documents

```bash
curl http://localhost:8000/document
```

### Get document chunks

```bash
curl http://localhost:8000/document/<doc-id>
```

## MCP Tools

The MCP server (`mcp_server.py`) exposes three tools for AI agent integration:

| Tool                 | Description                                      |
| -------------------- | ------------------------------------------------ |
| `search_documents`   | Semantic search through uploaded documents       |
| `list_documents`     | List all uploaded documents with metadata         |
| `get_document_by_id` | Retrieve all chunks of a specific document by ID |

## Project Structure

```
.
├── app/
│   ├── core/
│   │   ├── chunker.py       # Semantic text chunking
│   │   ├── ocr.py           # Mistral OCR integration
│   │   └── vector.py        # ChromaDB vector store
│   ├── modules/
│   │   ├── document/
│   │   │   └── route.py     # Document listing & retrieval
│   │   ├── search/
│   │   │   └── route.py     # Semantic search endpoint
│   │   └── upload/
│   │       └── route.py     # File upload & processing
│   └── main.py              # FastAPI app entrypoint
├── chroma_db/                # ChromaDB persistent storage
├── mcp_server.py             # MCP server for AI agent tools
├── Makefile                  # Dev commands
├── pyproject.toml            # Project config & dependencies
└── .env                      # Environment variables (not committed)
```
