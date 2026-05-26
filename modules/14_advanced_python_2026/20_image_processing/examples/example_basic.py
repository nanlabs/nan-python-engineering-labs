"""
Image processing with Rust-Python integration.
Simulates fast image operations.
"""


def apply_filter(width: int, height: int, filter_type: str) -> dict:
    """Apply filter to image."""
    return {
        "width": width,
        "height": height,
        "filter": filter_type,
        "processed": True,
    }


def resize_image(width: int, height: int, scale: float) -> dict:
    """Resize image."""
    return {
        "new_width": int(width * scale),
        "new_height": int(height * scale),
        "scale_factor": scale,
    }


if __name__ == "__main__":
    img = apply_filter(800, 600, "blur")
    print("Filtered:", img)

    resized = resize_image(800, 600, 0.5)
    print("Resized:", resized)
