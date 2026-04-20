"""
Static and class methods in PyO3.
"""


class MathUtils:
    """Math utilities with static methods."""

    version = "1.0"

    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

    @classmethod
    def create_default(cls):
        """Factory method."""
        return MathUtils()

    @classmethod
    def get_version(cls) -> str:
        return cls.version


if __name__ == "__main__":
    print("Add:", MathUtils.add(3, 4))
    print("Multiply:", MathUtils.multiply(3, 4))
    print("Version:", MathUtils.get_version())
