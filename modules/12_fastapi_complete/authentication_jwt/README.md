# JWT Authentication

Estimated time: 2.5 hours

## 1. Definition

**JSON Web Tokens (JWT)** are self-contained, signed tokens that encode authentication claims (user identity, roles, expiration). The server issues them on login; the client sends them as `Authorization: Bearer <token>` on subsequent requests. The server verifies the signature without a database lookup.

### Key Characteristics

- **Structure**: three Base64-encoded parts separated by dots — `header.payload.signature`.
- **Stateless**: verification requires only the secret key — no session store needed.
- **Claims**: `sub` (subject/user), `exp` (expiry), `roles`, and any custom data.
- **Access + refresh pair**: short-lived access token (minutes) + long-lived refresh token (days).
- **Token blacklist**: revoked tokens must be tracked (in Redis) because JWTs cannot be invalidated otherwise.

## 2. Practical Application

### Use Cases

- Single-page applications authenticating against a REST API.
- Microservices authenticating inter-service calls.
- Mobile apps keeping users logged in across sessions via refresh tokens.
- Role-based access: embedding `roles` in the token payload.

### Code Example

```python
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET = "change-me-in-production"

def create_token(username: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm="HS256")
```

## 3. Why Is It Important?

### Problem It Solves

Session-based auth stores session data server-side, requiring shared storage across servers. JWTs are self-contained — any server that knows the secret can verify any token, enabling stateless horizontal scaling.

### Solution and Benefits

Stateless verification, compact token size, and standardized claim names make JWTs portable across services and languages. `python-jose` handles signing and verification with a clean API.

## 4. References

- [FastAPI OAuth2 + JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [JWT.io](https://jwt.io/)
- [python-jose](https://python-jose.readthedocs.io/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Implement `POST /login` that returns an access token for valid credentials (hardcoded users). Implement `GET /me` that decodes the token and returns the username.

### Intermediate Level

Add a refresh token (7-day TTL) returned alongside the access token. Implement `POST /refresh` that issues a new token pair and revokes the old refresh token.

### Advanced Level

Add role-based access: embed `roles` in the token. Create a `require_admin` dependency that raises 403 for non-admin tokens. Implement `POST /logout` that adds the token to an in-memory blacklist.

### Success Criteria

- `GET /me` with an expired token returns 401.
- `GET /me` with a revoked (blacklisted) token returns 401.
- `GET /admin` with a non-admin token returns 403.

## 6. Summary

JWTs are signed tokens carrying authentication claims. FastAPI + `python-jose` + `OAuth2PasswordBearer` provide a complete auth stack. The access/refresh token pair balances security (short access TTL) and usability (long refresh TTL). Stateless verification scales horizontally without shared session storage.

## 7. Reflection Prompt

JWTs cannot be invalidated before their `exp` claim expires — unless you maintain a blacklist. How does this fundamental property affect your choice of access token TTL? What are the trade-offs between a 5-minute and a 60-minute access token?
