"""
Basic example: Security Best Practices
=========================================

Secure APIs combine multiple defenses at different layers.
This example is a standalone runnable script that demonstrates
the key patterns — no HTTP server needed.

Demonstrates:
1. Password hashing with bcrypt (adaptive cost factor)
2. Secrets comparison with hmac.compare_digest (timing-safe)
3. Input sanitization to prevent injection
4. Security headers reference
5. Rate limiting concept (in-memory, token bucket)
6. Environment-based secret loading
7. HTTPS-only cookie attributes

Run:
    python example_basic.py
"""

import hmac
import os
import re
import time
from datetime import datetime, timedelta
from typing import Optional

import bcrypt as _bcrypt_lib
from pydantic import BaseModel, field_validator, SecretStr


# =============================================================================
# 1. PASSWORD HASHING — bcrypt (adaptive cost factor)
# =============================================================================

BCRYPT_ROUNDS = 12  # Cost factor: higher = slower = more brute-force resistant


def hash_password(plain: str) -> str:
    """
    Hash a password with bcrypt.

    bcrypt automatically generates a random salt and embeds it in the hash.
    Never store plain-text passwords.
    """
    return _bcrypt_lib.hashpw(plain.encode(), _bcrypt_lib.gensalt(rounds=BCRYPT_ROUNDS)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password against its bcrypt hash.

    bcrypt.checkpw uses constant-time comparison internally.
    """
    return _bcrypt_lib.checkpw(plain.encode(), hashed.encode())


def demo_password_hashing():
    print("─" * 55)
    print("1. PASSWORD HASHING (bcrypt)")
    print("─" * 55)

    plain = "MyS3cure!Password"
    hashed = hash_password(plain)
    print(f"  Plain:  {plain}")
    print(f"  Hashed: {hashed[:40]}…")
    print(f"  Verify correct:   {verify_password(plain, hashed)}")
    print(f"  Verify wrong:     {verify_password('wrong', hashed)}")

    # Two hashes of the SAME password are different (random salt)
    hashed2 = hash_password(plain)
    print(f"  Hash deterministic? {hashed == hashed2}  (salts differ)")


# =============================================================================
# 2. TIMING-SAFE COMPARISON — prevent timing attacks
# =============================================================================

def safe_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time.

    Regular string equality (==) short-circuits on the first different byte,
    leaking timing information that attackers can use to guess secrets byte
    by byte. hmac.compare_digest always takes the same time regardless of
    where strings differ.
    """
    return hmac.compare_digest(a.encode(), b.encode())


def demo_timing_safe():
    print()
    print("─" * 55)
    print("2. TIMING-SAFE COMPARISON")
    print("─" * 55)
    api_key = "super-secret-key-0001"
    print(f"  safe_compare match:   {safe_compare(api_key, api_key)}")
    print(f"  safe_compare no match: {safe_compare(api_key, 'wrong-key')}")
    print("  Unlike ==, no timing difference leaks information.")


# =============================================================================
# 3. INPUT SANITIZATION — prevent SQL injection / XSS
# =============================================================================

SAFE_STRING_PATTERN = re.compile(r"^[a-zA-Z0-9 _\-\.@]+$")
SAFE_SLUG_PATTERN = re.compile(r"^[a-z0-9\-]+$")


def sanitize_string(value: str, max_length: int = 200) -> str:
    """
    Strip leading/trailing whitespace and enforce allowed character set.

    For usernames, slugs, and search queries — never trust raw user input.
    Use parameterized queries for database interactions (no string formatting).
    """
    value = value.strip()[:max_length]
    if not SAFE_STRING_PATTERN.match(value):
        raise ValueError(f"Input contains disallowed characters: {value!r}")
    return value


class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: SecretStr  # SecretStr: hides value in repr/logs

    @field_validator("username")
    @classmethod
    def username_safe(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", v):
            raise ValueError("Username must be 3–30 alphanumeric chars or underscores")
        return v

    @field_validator("email")
    @classmethod
    def email_safe(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Invalid email format")
        return v


def demo_sanitization():
    print()
    print("─" * 55)
    print("3. INPUT SANITIZATION")
    print("─" * 55)

    # Valid input
    try:
        req = UserCreateRequest(
            username="alice_dev",
            email="  Alice@Example.COM  ",
            password="MyS3cure!Pass",
        )
        print(f"  Valid user: username={req.username!r}, email={req.email!r}")
        print(f"  Password in repr: {req}")  # SecretStr hides value
    except Exception as e:
        print(f"  Error: {e}")

    # Invalid username (SQL injection attempt)
    try:
        UserCreateRequest(
            username="'; DROP TABLE users; --",
            email="a@b.com",
            password="pass",
        )
    except Exception as e:
        print(f"  Injection attempt blocked: {e}")


# =============================================================================
# 4. SECURITY HEADERS REFERENCE
# =============================================================================

RECOMMENDED_SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "Content-Security-Policy": "default-src 'self'; script-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=()",
    "Cache-Control": "no-store",
}


def demo_security_headers():
    print()
    print("─" * 55)
    print("4. SECURITY HEADERS (add via middleware)")
    print("─" * 55)
    for header, value in RECOMMENDED_SECURITY_HEADERS.items():
        print(f"  {header}: {value[:60]}")


# =============================================================================
# 5. IN-MEMORY RATE LIMITER (token bucket concept)
# =============================================================================


class RateLimiter:
    """
    Simple in-memory rate limiter (token bucket per key).

    In production, use Redis with a sliding window for distributed setups.
    """

    def __init__(self, max_calls: int, period_seconds: float):
        self.max_calls = max_calls
        self.period = period_seconds
        self._buckets: dict[str, list[float]] = {}

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.period
        bucket = self._buckets.get(key, [])
        # Remove timestamps outside the window
        bucket = [ts for ts in bucket if ts > window_start]
        if len(bucket) >= self.max_calls:
            self._buckets[key] = bucket
            return False
        bucket.append(now)
        self._buckets[key] = bucket
        return True


def demo_rate_limiter():
    print()
    print("─" * 55)
    print("5. RATE LIMITING (3 calls / second)")
    print("─" * 55)
    limiter = RateLimiter(max_calls=3, period_seconds=1.0)
    client_ip = "192.168.1.1"
    for i in range(5):
        allowed = limiter.is_allowed(client_ip)
        print(f"  Request {i + 1}: {'ALLOWED' if allowed else 'BLOCKED (rate limit)'}")


# =============================================================================
# 6. SECRETS LOADED FROM ENVIRONMENT
# =============================================================================

def demo_env_secrets():
    print()
    print("─" * 55)
    print("6. SECRETS FROM ENVIRONMENT VARIABLES")
    print("─" * 55)
    # Safe pattern: load at startup with a clear error if missing
    secret = os.environ.get("JWT_SECRET_KEY")
    if secret:
        print(f"  JWT_SECRET_KEY loaded: {secret[:6]}…")
    else:
        print("  JWT_SECRET_KEY not set — using DEVELOPMENT placeholder")
        print("  In production, always set this via environment/secrets manager")

    # SecretStr: hides the value in logs and repr
    class AppConfig(BaseModel):
        api_key: SecretStr = SecretStr("dev-key-placeholder")
        db_password: SecretStr = SecretStr("dev-pass-placeholder")

    cfg = AppConfig()
    print(f"  Config repr: {cfg}")  # api_key and db_password are hidden


# =============================================================================
# 7. SECURE COOKIE ATTRIBUTES
# =============================================================================

def demo_secure_cookies():
    print()
    print("─" * 55)
    print("7. SECURE COOKIE ATTRIBUTES")
    print("─" * 55)
    print("  When setting cookies via FastAPI response.set_cookie():")
    print("  response.set_cookie(")
    print('      key="session_id",')
    print('      value=token,')
    print("      httponly=True,   # Cannot be read by JS (prevents XSS theft)")
    print("      secure=True,     # Only sent over HTTPS")
    print("      samesite='lax',  # Mitigates CSRF (use 'strict' for APIs)")
    print("      max_age=1800,    # 30 minutes")
    print("  )")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 55)
    print("SECURITY BEST PRACTICES — DEMO")
    print("=" * 55)
    demo_password_hashing()
    demo_timing_safe()
    demo_sanitization()
    demo_security_headers()
    demo_rate_limiter()
    demo_env_secrets()
    demo_secure_cookies()
    print()
    print("=" * 55)
    print("Key takeaways:")
    print("  • Never store plain-text passwords — use bcrypt/Argon2")
    print("  • Use hmac.compare_digest for secret comparison")
    print("  • Validate and sanitize all user input at system boundaries")
    print("  • Add security headers via middleware")
    print("  • Rate-limit endpoints to prevent brute force")
    print("  • Load secrets from environment — never hardcode")
    print("  • Set HttpOnly + Secure + SameSite on session cookies")
    print("=" * 55)


if __name__ == "__main__":
    main()
