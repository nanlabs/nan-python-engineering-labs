class Student:
    def __init__(self, name: str, cohort: str) -> None:
        self.name = name
        self.cohort = cohort

    def summary(self) -> str:
        return f"{self.name} ({self.cohort})"


def main() -> None:
    student = Student('Ada', '2026-A')
    print(student.summary())


if __name__ == '__main__':
    main()
