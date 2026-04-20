"""Build and execute a tiny GraphQL-like schema with optional fields using stdlib only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    """Represents data returned by a query resolver."""

    user_id: int
    name: str
    email: str | None
    nickname: str | None


USERS = {
    1: User(user_id=1, name="Ada", email="ada@example.com", nickname=None),
    2: User(user_id=2, name="Grace", email=None, nickname="Amazing Grace"),
}


def resolve_user(user_id: int, fields: list[str]) -> dict:
    user = USERS[user_id]
    result = {}
    for field in fields:
        result[field] = getattr(user, field)
    return result


def parse_query(query: str) -> tuple[int, list[str]]:
    normalized = " ".join(query.replace("{", " { ").replace("}", " } ").split())
    if "user(" not in normalized:
        raise ValueError("Only user query is supported")

    start = normalized.index("user(id:") + len("user(id:")
    end = normalized.index(")", start)
    user_id = int(normalized[start:end].strip())

    fields_start = normalized.index("{", end) + 1
    fields_end = normalized.index("}", fields_start)
    fields = [f for f in normalized[fields_start:fields_end].split() if f]
    return user_id, fields


def main() -> None:
    """Entry point to demonstrate the implementation."""
    query = "{ user(id: 2) { user_id name email nickname } }"
    user_id, fields = parse_query(query)
    payload = {"data": {"user": resolve_user(user_id, fields)}}
    print(payload)


if __name__ == "__main__":
    main()
