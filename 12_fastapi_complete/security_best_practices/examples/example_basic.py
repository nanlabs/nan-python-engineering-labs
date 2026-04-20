"""Security best practices demo for API-like workflows using stdlib only."""

import hmac
import os
import re
import secrets
from hashlib import pbkdf2_hmac


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_bytes(16)
    digest = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex(), digest.hex()


def verify_password(password: str, salt_hex: str, digest_hex: str) -> bool:
    _, new_digest = hash_password(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(new_digest, digest_hex)


def sanitize_username(raw: str) -> str:
    name = raw.strip()
    if not re.fullmatch(r"[a-zA-Z0-9_]{3,30}", name):
        raise ValueError("invalid username")
    return name


def build_security_headers() -> dict[str, str]:
    return {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Cache-Control": "no-store",
    }


def main() -> None:
    """Entry point to demonstrate the implementation."""
    salt, digest = hash_password("MyS3cure!Password")
    print("password verified:", verify_password("MyS3cure!Password", salt, digest))
    print("password rejected:", verify_password("wrong", salt, digest))
    print("sanitized username:", sanitize_username("alice_dev"))
    print("header count:", len(build_security_headers()))
    print("secret configured:", bool(os.getenv("JWT_SECRET_KEY")))


if __name__ == "__main__":
    main()
