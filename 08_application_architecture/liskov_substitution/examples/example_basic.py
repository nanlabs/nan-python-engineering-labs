"""Liskov Substitution - subtypes substitutable."""
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self): pass

class Sparrow(Bird):
    def move(self): return "Flying 20mph"

class Penguin(Bird):
    def move(self): return "Swimming 10mph"

def describe_bird(bird: Bird): print(bird.move())

if __name__ == "__main__":
    describe_bird(Sparrow())
    describe_bird(Penguin())
    print("✓ Liskov Substitution")
