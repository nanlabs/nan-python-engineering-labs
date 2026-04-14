class Exporter:
    def export(self, payload: dict[str, object]) -> str:
        header = self.build_header()
        body = self.build_body(payload)
        return f"{header}|{body}"

    def build_header(self) -> str:
        raise NotImplementedError

    def build_body(self, payload: dict[str, object]) -> str:
        raise NotImplementedError


class CsvExporter(Exporter):
    def build_header(self) -> str:
        return 'csv'

    def build_body(self, payload: dict[str, object]) -> str:
        return ','.join(f"{k}={v}" for k, v in payload.items())


def main() -> None:
    print(CsvExporter().export({'ok': True, 'count': 2}))


if __name__ == '__main__':
    main()
