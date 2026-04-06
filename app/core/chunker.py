from chonkie import SemanticChunker, OverlapRefinery

_chunker = SemanticChunker(
    threshold=0.7,
    chunk_size=512,
)

_refinery = OverlapRefinery(
    context_size=0.15,
    method="suffix",
    merge=True,
)


def chunk_text(text: str) -> list[str]:
    chunks = _chunker.chunk(text)
    refined = _refinery(chunks)
    return [chunk.text for chunk in refined]
