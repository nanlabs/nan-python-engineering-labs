"""Exercise 01 for Sbom Introduction.

Goal:
- Implement a small validation pipeline for security-relevant input.
- Produce structured output that can be inspected by tests.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Represents the result of input validation."""

    accepted: bool
    reason: str


def validate_input(candidate: str) -> ValidationResult:
    """Validate a candidate string using simple defensive rules.

    Rules:
    - Candidate must not be empty after trimming.
    - Candidate length must be between 3 and 80 characters.
    - Candidate must contain at least one alphabetic character.
    """
    normalized = candidate.strip()
    if not normalized:
        return ValidationResult(False, "Input is empty")
    if not 3 <= len(normalized) <= 80:
        return ValidationResult(False, "Input length is outside allowed range")
    if not any(ch.isalpha() for ch in normalized):
        return ValidationResult(False, "Input must include alphabetic characters")
    return ValidationResult(True, "Input accepted")


def main() -> None:
    samples = ["", "42", "valid-sample"]
    for sample in samples:
        result = validate_input(sample)
        print(f"sample={sample!r} accepted={result.accepted} reason={result.reason}")


if __name__ == "__main__":
    main()
