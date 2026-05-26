"""Basic example: resource pagination and links."""

from urllib.parse import urlencode

items = [{"id": i, "name": f"item-{i}"} for i in range(1, 16)]


def list_items(page=1, per_page=5):
    start = (page - 1) * per_page
    end = start + per_page
    data = items[start:end]
    mk = lambda p: "/items?" + urlencode({"page": p, "per_page": per_page})
    return {
        "data": data,
        "meta": {"page": page, "total": len(items)},
        "links": {"self": mk(page), "next": mk(page + 1) if end < len(items) else None},
    }


print(list_items(page=2, per_page=5))
