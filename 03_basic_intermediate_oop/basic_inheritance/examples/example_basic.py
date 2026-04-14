class Employee:
    def __init__(self, name: str) -> None:
        self.name = name

    def role(self) -> str:
        return 'Employee'


class Manager(Employee):
    def role(self) -> str:
        return 'Manager'


def main() -> None:
    person = Manager('Grace')
    print(person.name, person.role())


if __name__ == '__main__':
    main()
