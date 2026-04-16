# Security Best Practices

Estimated time: 2 hours

## 1. Definition

API security requires multiple overlapping defences at different layers. No single control is sufficient. This topic covers the foundational patterns every FastAPI application should implement: password hashing, timing-safe comparison, input sanitization, security headers, rate limiting, and secrets management.

### Key Characteristics

- **bcrypt**: adaptive password hashing with a configurable cost factor.
- **`hmac.compare_digest`**: constant-time string comparison that prevents timing attacks.
- **Input sanitization**: validate and restrict input at system boundaries using Pydantic validators.
- **Security headers**: HTTP headers that harden the browser against XSS, clickjacking, MIME sniffing.
- **`SecretStr`**: Pydantic type that hides sensitive values in repr and logs.

## 2. Practical Application

### Use Cases

- Storing user passwords with bcrypt (never plain text or MD5/SHA1).
- Validating API keys without leaking timing information.
- Sanitizing user input to prevent injection attacks.
- Adding HSTS, CSP, and X-Frame-Options headers via middleware.
- Loading secrets from environment variables with validation.

### Code Example

```python
import bcrypt, hmac

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()

def safe_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())
```

## 3. Why Is It Important?

### Problem It Solves

Common security failures — plain-text passwords, timing attacks on token comparison, SQL injection via unvalidated input — are not hypothetical. They appear in the OWASP Top 10 and are consistently exploited in production systems.

### Solution and Benefits

Each control addresses a specific attack vector. bcrypt makes offline dictionary attacks computationally infeasible. `compare_digest` prevents oracle attacks. Security headers block entire classes of browser-based attacks.

## 4. References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [bcrypt documentation](https://pypi.org/project/bcrypt/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Hash a password with bcrypt and verify it. Demonstrate that two hashes of the same password are different (different salts).

### Intermediate Level

Create an input validator using Pydantic that rejects usernames containing special characters. Add `hmac.compare_digest` for API key comparison.

### Advanced Level

Create a `SecurityHeadersMiddleware` adding HSTS, CSP, X-Frame-Options, and Referrer-Policy. Add an in-memory token-bucket rate limiter to `POST /login`.

### Success Criteria

- bcrypt hash verification works correctly for valid and invalid passwords.
- SQL injection strings in username are rejected with a validation error.
- All security headers appear in every response.
- `POST /login` is blocked after 5 attempts within 60 seconds.

## 6. Summary

API security is layered. bcrypt for passwords, `hmac.compare_digest` for secrets, Pydantic validators for input, security headers via middleware, rate limiting for brute-force defence, and `SecretStr` to prevent log leakage — each layer addresses a specific threat class.

## 7. Reflection Prompt

bcrypt is intentionally slow. How do you choose the cost factor (`rounds`) in production? What is the trade-off between security (higher cost) and performance (login latency + server load)?
