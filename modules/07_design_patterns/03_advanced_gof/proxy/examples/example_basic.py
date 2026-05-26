"""Proxy pattern example: lazy-load a heavy image object."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        ...


class RealImage(Image):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._data = f"binary:{filename}".encode()

    def display(self) -> str:
        return f"Displaying {self.filename} ({len(self._data)} bytes loaded)"


class ImageProxy(Image):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> str:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    image = ImageProxy("architecture-diagram.png")
    print("Proxy created, image not loaded yet.")
    print(image.display())
    print(image.display())


if __name__ == "__main__":
    main()
