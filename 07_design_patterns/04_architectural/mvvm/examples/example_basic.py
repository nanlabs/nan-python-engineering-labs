class ViewModel:
    def __init__(self) -> None:
        self.title = 'dashboard'

    @property
    def title_upper(self) -> str:
        return self.title.upper()


def main() -> None:
    vm = ViewModel()
    print(vm.title_upper)


if __name__ == '__main__':
    main()
