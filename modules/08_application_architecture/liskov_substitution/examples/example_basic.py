"""Liskov substitution: every subtype can replace the base contract."""

from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def move(self) -> str:
        ...


class Sparrow(Bird):
    def move(self) -> str:
        return "Flying at 20 mph"


class Penguin(Bird):
    def move(self) -> str:
        return "Swimming at 10 mph"


def describe_bird(bird: Bird) -> str:
    return bird.move()


if __name__ == "__main__":
    print(describe_bird(Sparrow()))
    print(describe_bird(Penguin()))
