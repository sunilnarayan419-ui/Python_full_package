"""
07_API_Authentication.py

Production-oriented authentication and authorization for a FastAPI
scientific data API.

Authentication (who are you):
    - Bearer JWT tokens, verified via a FastAPI security dependency.
    - Signing secret is loaded from the environment, never hard-coded.

Authorization (what can you do):
    - Role-based access control (researcher / analyst / admin).
    - A valid token proves identity only; each protected route separately
      checks whether that identity's role permits the action.

Passwords, if ever stored, are hashed (never plaintext) using passlib's
bcrypt scheme. No secret material is logged or echoed back to clients.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

try:
    import jwt  # PyJWT
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "The 'PyJWT' package is required for this module. "
        "Install it with: pip install PyJWT"
    ) from exc

try:
    from passlib.context import CryptContext
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "The 'passlib' package is required for this module. "
        "Install it with: pip install passlib[bcrypt]"
    ) from exc

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration boundary -- secrets come from the environment only.
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuthConfig:
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 30

    @classmethod
    def from_env(cls) -> "AuthConfig":
        secret = os.environ.get("API_JWT_SECRET")
        if not secret:
            raise RuntimeError(
                "API_JWT_SECRET is not set. Configure it via environment "
                "variable / secret manager before starting the service."
            )
        return cls(jwt_secret=secret)


def _get_auth_config() -> AuthConfig:
    # In a real deployment this would be constructed once at startup and
    # injected; kept lazy here so the module can be imported without a
    # secret configured (e.g. for documentation generation).
    return AuthConfig.from_env()


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _pwd_context.verify(plain_password, password_hash)


# ---------------------------------------------------------------------------
# Roles & identity
# ---------------------------------------------------------------------------

class Role(str, Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    subject: str
    role: Role


class UserRecord(BaseModel):
    username: str
    password_hash: str
    role: Role


# In-memory user store for demonstration only; a real deployment backs this
# with a database and never keeps plaintext passwords anywhere.
_USERS: dict[str, UserRecord] = {
    "dr.alvarez": UserRecord(
        username="dr.alvarez", password_hash=hash_password("not-a-real-password"), role=Role.RESEARCHER
    ),
    "ops-admin": UserRecord(
        username="ops-admin", password_hash=hash_password("not-a-real-password-either"), role=Role.ADMIN
    ),
}


class AuthenticationError(Exception):
    """Raised when credentials cannot be verified."""


def authenticate_user(username: str, password: str) -> UserRecord:
    record = _USERS.get(username)
    if record is None or not verify_password(password, record.password_hash):
        # Deliberately identical error for "no such user" and "wrong
        # password" -- do not leak which case occurred.
        raise AuthenticationError("invalid username or password")
    return record


def issue_access_token(user: UserRecord, config: AuthConfig) -> str:
    now = datetime.now(UTC)
    claims = {
        "sub": user.username,
        "role": user.role.value,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=config.access_token_ttl_minutes)).timestamp()),
    }
    return jwt.encode(claims, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_access_token(token: str, config: AuthConfig) -> AuthenticatedUser:
    try:
        claims = jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationError("token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError("invalid token") from exc

    try:
        role = Role(claims["role"])
    except (KeyError, ValueError) as exc:
        raise AuthenticationError("token missing valid role claim") from exc

    return AuthenticatedUser(subject=claims["sub"], role=role)


# ---------------------------------------------------------------------------
# FastAPI security dependencies
# ---------------------------------------------------------------------------

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> AuthenticatedUser:
    """Authentication dependency: resolves *who* is calling. Never returns
    partial/anonymous identities -- raises 401 on any failure."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        config = _get_auth_config()
        return decode_access_token(credentials.credentials, config)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*allowed: Role):
    """Authorization dependency factory: given an already-authenticated
    user, enforce that their role is one of `allowed`. A valid token alone
    never grants access; the role must match the route's requirement."""

    def _dependency(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if user.role not in allowed:
            logger.warning("authorization denied subject=%s role=%s", user.subject, user.role)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="insufficient permissions for this operation",
            )
        return user

    return _dependency


# ---------------------------------------------------------------------------
# Application & routes
# ---------------------------------------------------------------------------

app = FastAPI(title="Scientific API -- Authentication & Authorization")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


@app.post("/auth/token", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    try:
        user = authenticate_user(payload.username, payload.password)
    except AuthenticationError:
        # Never reveal whether the username exists.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    config = _get_auth_config()
    token = issue_access_token(user, config)
    return TokenResponse(access_token=token, expires_in_minutes=config.access_token_ttl_minutes)


@app.get("/samples/{sample_id}")
def read_sample(sample_id: str, _user: AuthenticatedUser = Depends(get_current_user)) -> dict[str, str]:
    # Any authenticated role may read.
    return {"id": sample_id, "species": "Arabidopsis thaliana"}


@app.post("/samples", status_code=status.HTTP_201_CREATED)
def create_sample(
    sample_id: str,
    user: AuthenticatedUser = Depends(require_roles(Role.RESEARCHER, Role.ADMIN)),
) -> dict[str, str]:
    logger.info("sample created id=%s by=%s", sample_id, user.subject)
    return {"id": sample_id, "created_by": user.subject}


@app.delete("/samples/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(
    sample_id: str,
    user: AuthenticatedUser = Depends(require_roles(Role.ADMIN)),
) -> None:
    # Only admins may delete -- researchers and analysts are forbidden even
    # though they hold a perfectly valid token.
    logger.info("sample deleted id=%s by=%s", sample_id, user.subject)
    return None
