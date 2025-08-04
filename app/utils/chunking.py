from typing import List

def chunk_text(text: str, max_tokens: int = 500, overlap: int = 100) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    # Use larger chunk size and more overlap for better context
    max_tokens = max(max_tokens, 800)
    overlap = max(overlap, 200)
    while i < len(words):
        chunk = words[i:i+max_tokens]
        chunks.append(' '.join(chunk))
        i += max_tokens - overlap
    return chunks
