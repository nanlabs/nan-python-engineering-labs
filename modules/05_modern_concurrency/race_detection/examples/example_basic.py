import threading


def detect_risk(shared_mutable: bool, synchronized: bool) -> str:
    if shared_mutable and not synchronized:
        return "risk detected"
    return "no obvious race"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(detect_risk(True, False))
    print(threading.current_thread().name)


if __name__ == "__main__":
    main()
