"""Repository Pattern - abstract data access."""
from abc import ABC, abstractmethod

class Post:
    def __init__(self, id, title):
        self.id, self.title = id, title

class PostRepo(ABC):
    @abstractmethod
    def add(self, post): pass
    @abstractmethod
    def find(self, id): pass

class Memory(PostRepo):
    def __init__(self): self.posts = {}
    def add(self, p): self.posts[p.id] = p
    def find(self, id): return self.posts.get(id)

if __name__ == "__main__":
    r = Memory()
    r.add(Post(1, "Hello"))
    p = r.find(1)
    print(f"✓ Repository: {p.title}")
