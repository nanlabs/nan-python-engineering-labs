"""Interpreter pattern example: evaluate simple boolean expressions."""
from __future__ import annotations
from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def interpret(self, context: dict[str, bool]) -> bool: ...

class Literal(Expression):
    def __init__(self, value: bool) -> None:
        self.value = value
    def interpret(self, context: dict[str, bool]) -> bool:
        return self.value

class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name
    def interpret(self, context: dict[str, bool]) -> bool:
        return context[self.name]

class And(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right
    def interpret(self, context: dict[str, bool]) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)

class Or(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right
    def interpret(self, context: dict[str, bool]) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)

class Not(Expression):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
    def interpret(self, context: dict[str, bool]) -> bool:
        return not self.expression.interpret(context)

def main() -> None:
    expr = And(Or(Variable("is_admin"), Variable("is_support")), Not(Variable("is_suspended")))
    users = {
        "Alice": {"is_admin": True, "is_support": False, "is_suspended": False},
        "Bob": {"is_admin": False, "is_support": True, "is_suspended": True},
        "Carol": {"is_admin": False, "is_support": False, "is_suspended": False},
    }
    for name, ctx in users.items():
        print(f"{name}: access={expr.interpret(ctx)}")
    print("Literal check:", Literal(True).interpret({}))

if __name__ == "__main__":
    main()
