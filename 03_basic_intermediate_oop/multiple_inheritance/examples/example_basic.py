class Printer:
    def print_report(self, text: str) -> str:
        return f"Printed: {text}"


class Saver:
    def save_report(self, text: str) -> str:
        return f"Saved: {text}"


class ReportService(Printer, Saver):
    def publish(self, text: str) -> list[str]:
        return [self.print_report(text), self.save_report(text)]


def main() -> None:
    service = ReportService()
    for action in service.publish("Q1 Results"):
        print(action)


if __name__ == "__main__":
    main()
