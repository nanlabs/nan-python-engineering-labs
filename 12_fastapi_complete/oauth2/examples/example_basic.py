"""
Basic example: OAuth2 Password Flow
======================================

FastAPI has first-class support for OAuth2. The Password Grant (Resource
Owner Password Credentials) flow is the simplest: the user sends their
credentials directly to your API, which returns tokens.

This example demonstrates:
1. OAuth2PasswordBearer scheme — reads Bearer token from Authorization header
2. OAuth2PasswordRequestForm — parses username/password from form body
3. Token endpoint following the OAuth2 specification
4. Scopes — fine-grained permission claims inside the token
5. Swagger UI integration (click "Authorize" button)

Note: For real OAuth2 (authorization code, PKCE, etc.) you would integrate
with an identity provider like Auth0, Keycloak, or Google.

Dependencies:
    pip install "python-jose[cryptography]" passlib[bcrypt]

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
    Click "Authorize" and enter: alice / password123
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional
import os

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError


# =============================================================================
# CONFIG
# =============================================================================

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-secret-replace-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =============================================================================
# OAUTH2 SCHEME (reads Bearer token from Authorization header)
# =============================================================================

# The `scopes` dict is shown in the Swagger UI "Authorize" dialog.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    scopes={
        "me": "Read your own profile",
        "items:read": "Read items",
        "items:write": "Create and update items",
        "admin": "Full administrative access",
    },
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =============================================================================
# MODELS
# =============================================================================


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str


class TokenData(BaseModel):
    username: str
    scopes: List[str] = []


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: bool = False


class UserInDB(UserBase):
    hashed_password: str
    scopes: List[str] = []


class Item(BaseModel):
    id: int
    title: str
    owner: str


# =============================================================================
# FAKE DATABASE
# =============================================================================

USERS_DB: dict[str, UserInDB] = {
    "alice": UserInDB(
        username="alice",
        email="alice@example.com",
        full_name="Alice Smith",
        hashed_password=pwd_context.hash("password123"),
        scopes=["me", "items:read", "items:write", "admin"],
    ),
    "bob": UserInDB(
        username="bob",
        email="bob@example.com",
        full_name="Bob Jones",
        hashed_password=pwd_context.hash("password456"),
        scopes=["me", "items:read"],
    ),
}

ITEMS_DB: list[Item] = [
    Item(id=1, title="FastAPI Book", owner="alice"),
    Item(id=2, title="Python Cookbook", owner="bob"),
    Item(id=3, title="Clean Code", owner="alice"),
]


# =============================================================================
# HELPERS
# =============================================================================


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = USERS_DB.get(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =============================================================================
# DEPENDENCY: get_current_user WITH SCOPE VALIDATION
# =============================================================================


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
) -> UserInDB:
    """
    Dependency that decodes the token AND checks that all required scopes
    are present in the token's scope list.

    SecurityScopes.scopes is populated automatically from the `scopes`
    parameter on Security(get_current_user, scopes=[...]).
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = USERS_DB.get(token_data.username)
    if user is None or user.disabled:
        raise credentials_exception

    # Verify required scopes are present in the token
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient scope: '{scope}' required",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: UserInDB = Security(get_current_user, scopes=["me"])
) -> UserInDB:
    """Shortcut dependency for routes that just need any authenticated user."""
    return current_user


# =============================================================================
# APP
# =============================================================================

app = FastAPI(
    title="OAuth2 Password Flow Example",
    version="1.0.0",
    description=(
        "Demonstrates the OAuth2 Password Grant with scopes. "
        "Click 'Authorize' and enter alice/password123."
    ),
)


# ── Token endpoint (OAuth2 spec: POST /token with form body) ─────────────────


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 token endpoint.

    The client sends `username`, `password`, and optionally `scope` as
    application/x-www-form-urlencoded form data. The server returns a
    JSON Token object.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Intersect requested scopes with user's allowed scopes
    requested_scopes = form_data.scopes or user.scopes
    granted_scopes = [s for s in requested_scopes if s in user.scopes]

    access_token = create_access_token(
        data={"sub": user.username, "scopes": granted_scopes}
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        scope=" ".join(granted_scopes),
    )


# ── Protected routes ──────────────────────────────────────────────────────────


@app.get("/users/me", response_model=UserBase)
async def read_users_me(
    current_user: UserInDB = Security(get_current_user, scopes=["me"])
):
    """Return the authenticated user's profile. Requires 'me' scope."""
    return current_user


@app.get("/items", response_model=List[Item])
async def read_items(
    current_user: UserInDB = Security(get_current_user, scopes=["items:read"])
):
    """List all items. Requires 'items:read' scope."""
    return ITEMS_DB


@app.post("/items", response_model=Item, status_code=201)
async def create_item(
    title: str,
    current_user: UserInDB = Security(get_current_user, scopes=["items:write"]),
):
    """Create an item. Requires 'items:write' scope."""
    new_item = Item(id=len(ITEMS_DB) + 1, title=title, owner=current_user.username)
    ITEMS_DB.append(new_item)
    return new_item


@app.get("/admin/users", response_model=List[UserBase])
async def admin_list_users(
    current_user: UserInDB = Security(get_current_user, scopes=["admin"])
):
    """List all users. Requires 'admin' scope."""
    return list(USERS_DB.values())


@app.get("/")
async def root():
    return {
        "message": "OAuth2 Demo",
        "docs": "/docs",
        "token_endpoint": "/token",
        "test_credentials": [
            {"username": "alice", "password": "password123", "scopes": "me items:read items:write admin"},
            {"username": "bob", "password": "password456", "scopes": "me items:read"},
        ],
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("OAUTH2 PASSWORD FLOW — DEMO")
    print("=" * 65)
    print()
    print("Test users:")
    print("  alice / password123 → scopes: me, items:read, items:write, admin")
    print("  bob   / password456 → scopes: me, items:read")
    print()
    print("Scopes:")
    print("  me          → GET /users/me")
    print("  items:read  → GET /items")
    print("  items:write → POST /items")
    print("  admin       → GET /admin/users")
    print()
    print("Flow:")
    print("  curl -X POST http://localhost:8000/token \\")
    print("       -d 'username=alice&password=password123'")
    print("  → returns access_token")
    print()
    print("  curl -H 'Authorization: Bearer <token>' \\")
    print("       http://localhost:8000/users/me")
    print()
    print("  Or use Swagger UI /docs → click Authorize")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
