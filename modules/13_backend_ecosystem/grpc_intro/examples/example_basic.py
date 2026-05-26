"""Basic example: typed request/response RPC contract."""

from dataclasses import dataclass


@dataclass
class Request:
    user_id: int


@dataclass
class Response:
    user_id: int
    name: str


def get_user(req: Request) -> Response:
    names = {1: "Alice", 2: "Bob"}
    return Response(user_id=req.user_id, name=names.get(req.user_id, "Unknown"))


print(get_user(Request(1)))
print(get_user(Request(7)))
