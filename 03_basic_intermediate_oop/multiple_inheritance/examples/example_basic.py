class Printer:
    def print_report(self, text: str) -> str:
        return f"Printed: {text}"


class Saver:
    def save_report(self, text: str) -> str:
        return f"Saved: {text}"


class ReportService(Printer, Saver):
    pass


def main() -> None:
    service = ReportService()
    print(service.print_report('Q1 Results'))
    print(service.save_report('Q1 Results'))


if __name__ == '__main__':
    main()
