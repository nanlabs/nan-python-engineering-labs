"""
Structured outputs using Pydantic models.
"""

from pydantic import BaseModel

class ExtractionResult(BaseModel):
    """Structured extraction result."""
    entity: str
    sentiment: str
    confidence: float

def extract_structured(text: str) -> ExtractionResult:
    """Extract structured data from text."""
    return ExtractionResult(
        entity="Python",
        sentiment="positive",
        confidence=0.95,
    )

if __name__ == "__main__":
    result = extract_structured("Python is awesome")
    print(f"Result: {result}")
