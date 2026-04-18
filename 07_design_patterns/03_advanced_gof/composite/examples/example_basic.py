"""Composite pattern example: treat files and folders uniformly."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

class Node(ABC):
    @abstractmethod
    def size(self) -> int: ...
    @abstractmethod
    def display(self, depth: int = 0) -> list[str]: ...

@dataclass
class File(Node):
    name: str
    bytes_size: int
    def size(self) -> int:
        return self.bytes_size
    def display(self, depth: int = 0) -> list[str]:
        return [f"{'  ' * depth}- {self.name} ({self.bytes_size}B)"]

@dataclass
class Folder(Node):
    name: str
    children: list[Node] = field(default_factory=list)
    def add(self, node: Node) -> None:
        self.children.append(node)
    def size(self) -> int:
        return sum(child.size() for child in self.children)
    def display(self, depth: int = 0) -> list[str]:
        lines = [f"{'  ' * depth}+ {self.name} ({self.size()}B)"]
        for child in self.children:
            lines.extend(child.display(depth + 1))
        return lines

def main() -> None:
    root = Folder("project")
    src = Folder("src")
    src.add(File("main.py", 420))
    src.add(File("utils.py", 280))
    docs = Folder("docs")
    docs.add(File("README.md", 180))
    root.add(src)
    root.add(docs)
    print("\n".join(root.display()))

if __name__ == "__main__":
    main()
