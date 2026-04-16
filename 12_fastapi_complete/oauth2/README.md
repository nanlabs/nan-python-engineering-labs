# OAuth2

Estimated time: 2 hours

## 1. Definition

**OAuth2** is an authorization framework that lets applications obtain limited access to user accounts on third-party services. FastAPI's `OAuth2PasswordBearer` and `OAuth2PasswordRequestForm` implement the **Resource Owner Password Credentials** grant, where the user sends credentials directly to your API's `/token` endpoint.

### Key Characteristics

- **`OAuth2PasswordBearer`**: reads the `Bearer` token from the `Authorization` header and integrates with Swagger UI's "Authorize" dialog.
- **`OAuth2PasswordRequestForm`**: parses `username`, `password`, and `scope` from `application/x-www-form-urlencoded` body.
- **Scopes**: fine-grained permissions embedded in the token (`me`, `items:read`, `admin`).
- **`SecurityScopes`**: used with `Security()` to declare and enforce required scopes per route.
- **Token endpoint**: must be at `POST /token` for Swagger UI to auto-discover it.

## 2. Practical Application

### Use Cases

- Internal APIs where users authenticate directly with username/password.
- Enforcing per-route permission scopes without a full external IdP.
- Integrating Swagger UI's "Authorize" button for interactive API testing.
- Issuing scoped tokens for third-party clients (limited scope).

### Code Example

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()

@app.get("/items")
def read_items(token: str = Depends(oauth2)):
    return {"token": token}
```

## 3. Why Is It Important?

### Problem It Solves

API keys are opaque — they carry no claims. JWTs alone don't prescribe how clients should obtain them. OAuth2 standardizes the token endpoint format and scope system, making your API compatible with any OAuth2 client library.

### Solution and Benefits

`OAuth2PasswordBearer` makes Swagger UI automatically discover the token endpoint and display an "Authorize" button. Scopes let you enforce minimum-privilege access at the route level.

## 4. References

- [FastAPI Security OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [OAuth2 Specification (RFC 6749)](https://tools.ietf.org/html/rfc6749)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `POST /token` returning `{"access_token": "...", "token_type": "bearer"}`. Add `GET /users/me` protected by `OAuth2PasswordBearer`.

### Intermediate Level

Add scopes (`me`, `items:read`, `items:write`) to `OAuth2PasswordBearer`. Use `Security(get_current_user, scopes=["items:write"])` on `POST /items`.

### Advanced Level

Create two users with different scope sets. Verify that a user with only `items:read` gets 403 on `POST /items` (write scope required) but 200 on `GET /items`.

### Success Criteria

- Swagger UI "Authorize" dialog discovers `/token` automatically.
- Insufficient scope returns 403 with `WWW-Authenticate: Bearer scope="..."`.
- Valid token with correct scope returns 200.

## 6. Summary

OAuth2 standardizes token issuance and scope enforcement. FastAPI's `OAuth2PasswordBearer` wires the Authorization header directly into Swagger UI. Scopes with `Security()` provide per-route minimum-privilege access control without extra boilerplate.

## 7. Reflection Prompt

The Password Grant (sending credentials directly to your API) is simpler but has security limitations. When would you need to implement the Authorization Code Grant with PKCE instead, and what infrastructure changes would that require?
