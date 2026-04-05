from chonkie import SemanticChunker

_chunker = SemanticChunker(
    threshold=0.7,
    chunk_size=512,
)


def chunk_text(text: str) -> list[str]:
    """Chunk text into semantically coherent pieces. Returns list of chunk strings."""
    chunks = _chunker.chunk(text)
    return [chunk.text for chunk in chunks]
