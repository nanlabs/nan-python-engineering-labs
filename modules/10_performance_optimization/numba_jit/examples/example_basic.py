"""JIT-friendly function shape for later Numba decoration."""


def integrate_trapezoid(steps: int) -> float:
    width = 1.0 / steps
    area = 0.0
    for i in range(steps):
        x0 = i * width
        x1 = (i + 1) * width
        y0 = x0 * x0
        y1 = x1 * x1
        area += (y0 + y1) * width * 0.5
    return area


def main() -> None:
    """Entry point to demonstrate the implementation."""
    result = integrate_trapezoid(200000)
    print(f"Integral approximation of x^2 in [0,1]: {result:.8f}")
    print("This loop-oriented function can benefit from numba.njit.")


if __name__ == "__main__":
    main()
