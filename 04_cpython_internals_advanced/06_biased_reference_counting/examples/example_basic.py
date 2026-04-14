def update_bias(local: int, shared: int, delta: int) -> tuple[int, int]:
    local += delta
    if local < 0:
        shared += local
        local = 0
    return local, shared


def main() -> None:
    local, shared = 5, 10
    local, shared = update_bias(local, shared, -7)
    print(f"local={local}, shared={shared}")


if __name__ == "__main__":
    main()
