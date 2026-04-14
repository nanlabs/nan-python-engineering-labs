"""Interface Segregation - specific interfaces."""
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self): pass

class Eater(ABC):
    @abstractmethod
    def eat(self): pass

class Robot(Worker):
    def work(self): print("Robot working")

class Human(Worker, Eater):
    def work(self): print("Human working")
    def eat(self): print("Human eating")

if __name__ == "__main__":
    Robot().work()
    Human().work()
    print("✓ Interface Segregation")
