"""
Retrieval-Augmented Generation (RAG).
"""

def retrieve_documents(query: str, top_k: int = 3) -> list:
    """Retrieve relevant documents."""
    return [
        {"id": i, "text": f"Document {i}", "score": 0.9 - i * 0.1}
        for i in range(top_k)
    ]

def augment_prompt(query: str, documents: list) -> str:
    """Augment prompt with retrieved docs."""
    doc_text = "\n".join([d["text"] for d in documents])
    return f"Context:\n{doc_text}\n\nQuestion: {query}"

if __name__ == "__main__":
    query = "What is Python?"
    docs = retrieve_documents(query)
    augmented = augment_prompt(query, docs)
    print(f"Augmented prompt length: {len(augmented)} chars")
