import threading


class SharedDoc:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.text = 'v1'

    def read(self) -> str:
        with self._lock:
            return self.text

    def write(self, value: str) -> None:
        with self._lock:
            self.text = value


def main() -> None:
    doc = SharedDoc()
    doc.write('v2')
    print(doc.read())


if __name__ == '__main__':
    main()
