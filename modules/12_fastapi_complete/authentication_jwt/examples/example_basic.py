"""
Basic example: JWT Authentication
====================================

JSON Web Tokens (JWT) are a compact, self-contained way to transmit
authentication information between parties as a digitally signed JSON object.

This example demonstrates:
1. User login endpoint that issues a JWT access token
2. Token refresh endpoint using a separate refresh token
3. Protected routes that require a valid Bearer token
4. Role-based access control using JWT claims
5. Token blacklisting (logout) via in-memory store

Dependencies:
    pip install "python-jose[cryptography]" passlib[bcrypt]

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

    Step 1: POST /auth/login with username/password
    Step 2: Copy the access_token
    Step 3: Use "Authorize" in Swagger UI or pass header:
            Authorization: Bearer <token>
"""

import os
from datetime import UTC, datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# In production: load from environment variables, never hardcode.
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-only-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# In-memory token blacklist (use Redis in production)
revoked_tokens: set[str] = set()


# =============================================================================
# MODELS
# =============================================================================


class User(BaseModel):
    username: str
    email: str
    roles: list[str] = ["user"]
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    username: str | None = None
    roles: list[str] = []


class RefreshRequest(BaseModel):
    refresh_token: str


# =============================================================================
# FAKE USER DATABASE
# =============================================================================

USERS_DB: dict[str, UserInDB] = {
    "alice": UserInDB(
        username="alice",
        email="alice@example.com",
        roles=["user", "admin"],
        hashed_password=pwd_context.hash("password123"),
    ),
    "bob": UserInDB(
        username="bob",
        email="bob@example.com",
        roles=["user"],
        hashed_password=pwd_context.hash("password456"),
    ),
}


# =============================================================================
# JWT UTILITIES
# =============================================================================


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token with an expiration claim."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str) -> str:
    """Create a long-lived refresh token."""
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": username, "exp": expire, "type": "refresh"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def decode_token(token: str, expected_type: str = "access") -> TokenData:
    """Decode and validate a JWT, returning the embedded claims."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        token_type: str = payload.get("type", "")
        if username is None or token_type != expected_type:
            raise ValueError("Invalid token structure")
        return TokenData(username=username, roles=payload.get("roles", []))
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


# =============================================================================
# DEPENDENCIES
# =============================================================================


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Dependency: validate the Bearer token and return the user."""
    if token in revoked_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    token_data = decode_token(token, expected_type="access")
    user = USERS_DB.get(token_data.username or "")
    if user is None or user.disabled:
        raise HTTPException(status_code=401, detail="User not found or disabled")
    return user


async def require_admin(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Dependency: enforce admin role."""
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="JWT Authentication Example", version="1.0.0")


@app.post("/auth/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with username + password, receive JWT tokens.

    - `access_token`: short-lived (30 min), used for API requests
    - `refresh_token`: long-lived (7 days), used only to get a new access_token
    """
    user = USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "roles": user.roles})
    refresh_token = create_refresh_token(user.username)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest):
    """
    Exchange a valid refresh token for a new access + refresh token pair.

    The old refresh token is revoked after use (rotation strategy).
    """
    token_data = decode_token(body.refresh_token, expected_type="refresh")
    if body.refresh_token in revoked_tokens:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    user = USERS_DB.get(token_data.username or "")
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Revoke old refresh token (rotation)
    revoked_tokens.add(body.refresh_token)

    new_access = create_access_token({"sub": user.username, "roles": user.roles})
    new_refresh = create_refresh_token(user.username)

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.post("/auth/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Revoke the current access token (add to blacklist).

    After logout, the token is rejected even if not expired.
    """
    revoked_tokens.add(token)
    return {"message": f"User {current_user.username} logged out"}


@app.get("/me", response_model=User)
async def get_me(current_user: UserInDB = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return current_user


@app.get("/protected")
async def protected_route(current_user: UserInDB = Depends(get_current_user)):
    """Any authenticated user can access this endpoint."""
    return {"message": f"Hello, {current_user.username}!", "roles": current_user.roles}


@app.get("/admin")
async def admin_route(admin_user: UserInDB = Depends(require_admin)):
    """Only users with the 'admin' role can access this endpoint."""
    return {"message": f"Admin panel — welcome, {admin_user.username}!"}


@app.get("/users", dependencies=[Depends(require_admin)])
async def list_users():
    """List all users — admin only."""
    return [User(**u.model_dump()) for u in USERS_DB.values()]


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("JWT AUTHENTICATION — DEMO")
    print("=" * 65)
    print()
    print("Test credentials:")
    print("  alice / password123  (roles: user, admin)")
    print("  bob   / password456  (roles: user)")
    print()
    print("Auth flow:")
    print("  1. POST /auth/login  → get access_token + refresh_token")
    print("  2. GET  /protected   → Authorization: Bearer <access_token>")
    print("  3. GET  /admin       → requires admin role (alice only)")
    print("  4. POST /auth/refresh → rotate tokens")
    print("  5. POST /auth/logout → revoke token")
    print()
    print("In Swagger UI (/docs): click 'Authorize', enter credentials")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
