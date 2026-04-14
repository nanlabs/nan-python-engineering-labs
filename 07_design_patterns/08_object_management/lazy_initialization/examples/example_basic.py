class Connection:
    def __init__(self) -> None:
        self._resource: str | None = None

    @property
    def resource(self) -> str:
        if self._resource is None:
            self._resource = 'db-connection'
        return self._resource


def main() -> None:
    conn = Connection()
    print(conn.resource)


if __name__ == '__main__':
    main()
