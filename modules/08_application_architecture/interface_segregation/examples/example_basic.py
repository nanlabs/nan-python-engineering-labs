"""Interface segregation: clients only depend on methods they use."""

from abc import ABC, abstractmethod


class Worker(ABC):
    @abstractmethod
    def work(self) -> str:
        ...


class Eater(ABC):
    @abstractmethod
    def eat(self) -> str:
        ...


class Robot(Worker):
    def work(self) -> str:
        return "Robot assembling parts"


class Human(Worker, Eater):
    def work(self) -> str:
        return "Human planning sprint"

    def eat(self) -> str:
        return "Human eating lunch"


if __name__ == "__main__":
    print(Robot().work())
    person = Human()
    print(person.work())
    print(person.eat())
