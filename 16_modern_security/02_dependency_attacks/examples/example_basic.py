"""Basic runnable example for Dependency Attacks.

This script demonstrates a compact, topic-aware security check using only the Python standard library.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class SecuritySignal:
    """Represents a normalized security observation."""

    topic_slug: str
    score: int
    evidence: list[str]

    def as_dict(self) -> dict[str, object]:
        return {
            "topic_slug": self.topic_slug,
            "score": self.score,
            "evidence": self.evidence,
            "captured_at": datetime.now(UTC).isoformat(),
        }


def evaluate_signal(topic_slug: str) -> SecuritySignal:
    """Create a deterministic score derived from the topic slug."""
    token = hashlib.sha256(topic_slug.encode("utf-8")).hexdigest()
    score = int(token[:8], 16) % 41 + 60
    words = topic_slug.split("_")
    evidence = [
        f"control_family={words[-1] if words else topic_slug}",
        f"digest_prefix={token[:12]}",
        "policy=baseline_v1",
    ]
    return SecuritySignal(topic_slug=topic_slug, score=score, evidence=evidence)


def main() -> None:
    """Run the example and print normalized output."""
    topic_slug = "02_dependency_attacks"
    topic_title = "Dependency Attacks"
    signal = evaluate_signal(topic_slug)
    payload = signal.as_dict()
    payload["topic_title"] = topic_title
    payload["status"] = "pass" if signal.score >= 70 else "review"
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
