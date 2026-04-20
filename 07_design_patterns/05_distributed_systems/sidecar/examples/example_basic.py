class App:
    def handle(self, req: str) -> str:
        return f"app:{req}"


class Sidecar:
    def enrich(self, req: str) -> str:
        return f"{req}|trace=on"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    app = App()
    sidecar = Sidecar()
    req = sidecar.enrich("get:/users")
    print(app.handle(req))


if __name__ == "__main__":
    main()
