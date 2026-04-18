"""
Loading documents from various sources.
"""

def load_text_file(path: str) -> str:
    """Load text document."""
    return "Mock document content"

def load_pdf_document(path: str) -> dict:
    """Load PDF document."""
    return {
        "path": path,
        "pages": 5,
        "text": "Mock PDF content",
    }

def load_documents_batch(paths: list) -> list:
    """Load multiple documents."""
    return [{"path": p, "content": load_text_file(p)} for p in paths]

if __name__ == "__main__":
    docs = load_documents_batch(["doc1.txt", "doc2.txt"])
    print(f"Loaded {len(docs)} documents")
