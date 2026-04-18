"""
Cryptographic hashing and encryption with Rust.
"""

def compute_hash(data: str) -> str:
    """Compute hash of data."""
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()

def hash_multiple(items: list) -> dict:
    """Hash multiple items."""
    return {item: compute_hash(item) for item in items}

if __name__ == "__main__":
    data = "secret_data"
    print(f"Hash: {compute_hash(data)}")
    
    items = ["password1", "password2"]
    print(f"Hashes: {hash_multiple(items)}")
