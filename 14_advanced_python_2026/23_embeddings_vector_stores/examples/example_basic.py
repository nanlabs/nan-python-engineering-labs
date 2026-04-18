"""
Embeddings and vector store fundamentals.
"""

def create_embeddings_example() -> dict:
    """Create sample embeddings."""
    return {
        "text": "Python is great for AI",
        "embedding": [0.1, 0.2, 0.3, 0.4],  # Mock embedding
        "dimension": 4,
    }

def store_embeddings(texts: list) -> list:
    """Store multiple embeddings."""
    return [
        {"text": t, "embedding": [0.1 * (i + 1)] * 4}
        for i, t in enumerate(texts)
    ]

if __name__ == "__main__":
    embedding = create_embeddings_example()
    print("Embedding:", embedding)
    
    stored = store_embeddings(["text1", "text2"])
    print(f"Stored {len(stored)} embeddings")
