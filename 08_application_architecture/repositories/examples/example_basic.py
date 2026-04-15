"""Repository pattern: isolate persistence behind a collection-like interface."""
from abc import ABC, abstractmethod


class Post:
    def __init__(self, post_id: int, title: str):
        self.id = post_id
        self.title = title


class PostRepo(ABC):
    @abstractmethod
    def add(self, post: Post) -> None:
        ...

    @abstractmethod
    def find(self, post_id: int) -> Post | None:
        ...


class MemoryPostRepo(PostRepo):
    def __init__(self) -> None:
        self.posts: dict[int, Post] = {}

    def add(self, post: Post) -> None:
        self.posts[post.id] = post

    def find(self, post_id: int) -> Post | None:
        return self.posts.get(post_id)


if __name__ == "__main__":
    repo = MemoryPostRepo()
    repo.add(Post(1, "Hello"))
    found = repo.find(1)
    print(found.title if found else "Post not found")
