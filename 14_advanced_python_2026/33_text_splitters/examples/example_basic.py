"""
Splitting text into chunks for embedding.
"""

def split_by_character(text: str, chunk_size: int = 100) -> list:
    """Split text by character count."""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def split_by_sentence(text: str) -> list:
    """Split text by sentences."""
    sentences = text.split(". ")
    return [s + "." for s in sentences if s]

if __name__ == "__main__":
    text = "This is a sample text. It has multiple sentences. Each one matters."
    chunks = split_by_character(text)
    print(f"Character chunks: {len(chunks)}")
    
    sentences = split_by_sentence(text)
    print(f"Sentence chunks: {len(sentences)}")
