"""
Operator overloading in PyO3.
Shows __add__, __mul__, __eq__, etc.
"""

class Vector:
    """2D Vector with operators."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)
    
    def __mul__(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

if __name__ == "__main__":
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print("Sum:", v1 + v2)
    print("Scaled:", v1 * 2)
