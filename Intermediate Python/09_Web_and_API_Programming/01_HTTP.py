"""
01_HTTP.py

HTTP fundamentals for backend engineers, illustrated against a realistic
scientific API surface (samples, experiments, measurements).

This module does not stand up a real server. It demonstrates, with runnable
code, how HTTP methods, status codes, headers, and semantics map onto
backend decisions: what is safe, what is idempotent, what status code a
given outcome deserves, and how authentication differs from authorization.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class HTTPMethod(str, Enum):
    """HTTP methods relevant to a resource-oriented scientific API."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


# Safe methods must not change server state (RFC 9110 §9.2.1).
SAFE_METHODS: frozenset[HTTPMethod] = frozenset({HTTPMethod.GET})

# Idempotent methods may be retried safely; repeating them has the same
# effect as calling them once (RFC 9110 §9.2.2).
IDEMPOTENT_METHODS: frozenset[HTTPMethod] = frozenset(
    {HTTPMethod.GET, HTTPMethod.PUT, HTTPMethod.DELETE}
)


def is_safe(method: HTTPMethod) -> bool:
    return method in SAFE_METHODS


def is_idempotent(method: HTTPMethod) -> bool:
    return method in IDEMPOTENT_METHODS


class HTTPStatus(int, Enum):
    """Subset of status codes actually used by this service, each tied to
    a specific, non-arbitrary outcome. Do not default everything to 200."""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_CONTENT = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


@dataclass(frozen=True, slots=True)
class HTTPRequest:
    """A simplified representation of an inbound HTTP request, enough to
    reason about routing, headers, and body semantics."""

    method: HTTPMethod
    path: str
    query_params: dict[str, str] = field(default_factory=dict)
    path_params: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    body: dict[str, Any] | None = None

    def content_type(self) -> str | None:
        return self.headers.get("content-type")

    def bearer_token(self) -> str | None:
        """Extract a bearer token from the Authorization header. This is
        purely an *authentication* concern -- it identifies who is
        calling, not what they are allowed to do."""
        auth = self.headers.get("authorization", "")
        if auth.startswith("Bearer "):
            return auth.removeprefix("Bearer ").strip()
        return None


@dataclass(frozen=True, slots=True)
class HTTPResponse:
    status: HTTPStatus
    headers: dict[str, str] = field(default_factory=dict)
    body: dict[str, Any] | None = None


class SampleNotFoundError(LookupError):
    """Raised when a requested sample does not exist."""


class DuplicateSampleError(ValueError):
    """Raised when a sample with the same accession already exists."""


class AuthenticationError(PermissionError):
    """Raised when the caller's identity cannot be established."""


class AuthorizationError(PermissionError):
    """Raised when an authenticated caller lacks permission for the action."""


# In-memory store standing in for a database, purely to demonstrate
# request/response lifecycle without external infrastructure.
_SAMPLES: dict[str, dict[str, Any]] = {
    "SMP-001": {"id": "SMP-001", "species": "Arabidopsis thaliana", "tissue": "leaf"},
}

# Toy identity/authorization mapping: token -> (subject, role).
_VALID_TOKENS: dict[str, tuple[str, str]] = {
    "tok-researcher-abc": ("dr.alvarez", "researcher"),
    "tok-admin-xyz": ("ops-admin", "admin"),
}

_WRITE_ROLES = frozenset({"admin", "researcher"})


def _authenticate(request: HTTPRequest) -> tuple[str, str]:
    """Authentication: establish *who* is making the request.

    Raises AuthenticationError if no valid credential is present. This is
    distinct from authorization, which decides *what* the caller may do.
    """
    token = request.bearer_token()
    if token is None or token not in _VALID_TOKENS:
        raise AuthenticationError("missing or invalid bearer token")
    return _VALID_TOKENS[token]


def _authorize(role: str, method: HTTPMethod) -> None:
    """Authorization: given a known identity, decide if the action is
    permitted. A valid token does not imply access to every operation."""
    if method in {HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH, HTTPMethod.DELETE}:
        if role not in _WRITE_ROLES:
            raise AuthorizationError(f"role '{role}' cannot perform {method.value}")


def handle_get_sample(request: HTTPRequest) -> HTTPResponse:
    """GET /samples/{sample_id} -- safe, idempotent, no auth required for
    read access in this demo API (read endpoints are often public/limited)."""
    sample_id = request.path_params.get("sample_id", "")
    sample = _SAMPLES.get(sample_id)
    if sample is None:
        logger.info("sample lookup miss id=%s", sample_id)
        return HTTPResponse(
            status=HTTPStatus.NOT_FOUND,
            body={"error": "sample_not_found", "sample_id": sample_id},
        )
    return HTTPResponse(status=HTTPStatus.OK, body=sample)


def handle_create_sample(request: HTTPRequest) -> HTTPResponse:
    """POST /samples -- not safe, not idempotent, requires authentication
    and write authorization, and validates the request body."""
    try:
        _, role = _authenticate(request)
    except AuthenticationError as exc:
        logger.warning("authentication failed: %s", exc)
        return HTTPResponse(status=HTTPStatus.UNAUTHORIZED, body={"error": "unauthenticated"})

    try:
        _authorize(role, request.method)
    except AuthorizationError as exc:
        logger.warning("authorization denied: %s", exc)
        return HTTPResponse(status=HTTPStatus.FORBIDDEN, body={"error": "forbidden"})

    body = request.body
    if request.content_type() != "application/json" or body is None:
        return HTTPResponse(
            status=HTTPStatus.UNPROCESSABLE_CONTENT,
            body={"error": "expected application/json body"},
        )

    sample_id = body.get("id")
    species = body.get("species")
    if not sample_id or not species:
        return HTTPResponse(
            status=HTTPStatus.BAD_REQUEST,
            body={"error": "id and species are required"},
        )

    if sample_id in _SAMPLES:
        return HTTPResponse(
            status=HTTPStatus.CONFLICT,
            body={"error": "sample_already_exists", "sample_id": sample_id},
        )

    _SAMPLES[sample_id] = dict(body)
    logger.info("sample created id=%s", sample_id)
    return HTTPResponse(
        status=HTTPStatus.CREATED,
        headers={"Location": f"/samples/{sample_id}"},
        body=_SAMPLES[sample_id],
    )


def handle_delete_sample(request: HTTPRequest) -> HTTPResponse:
    """DELETE /samples/{sample_id} -- idempotent: deleting an already-
    deleted resource still returns a terminal, non-error outcome (204),
    because the end state (resource absent) matches the caller's intent."""
    try:
        _, role = _authenticate(request)
        _authorize(role, request.method)
    except AuthenticationError:
        return HTTPResponse(status=HTTPStatus.UNAUTHORIZED, body={"error": "unauthenticated"})
    except AuthorizationError:
        return HTTPResponse(status=HTTPStatus.FORBIDDEN, body={"error": "forbidden"})

    sample_id = request.path_params.get("sample_id", "")
    _SAMPLES.pop(sample_id, None)
    return HTTPResponse(status=HTTPStatus.NO_CONTENT)


def handle_submit_analysis(request: HTTPRequest) -> HTTPResponse:
    """POST /analyses -- represents long-running work accepted for async
    processing. 202 Accepted signals "queued, not yet complete", distinct
    from 200/201 which imply the operation already finished."""
    try:
        _, role = _authenticate(request)
        _authorize(role, request.method)
    except AuthenticationError:
        return HTTPResponse(status=HTTPStatus.UNAUTHORIZED, body={"error": "unauthenticated"})
    except AuthorizationError:
        return HTTPResponse(status=HTTPStatus.FORBIDDEN, body={"error": "forbidden"})

    job_id = "job-8841"
    return HTTPResponse(
        status=HTTPStatus.ACCEPTED,
        headers={"Location": f"/analyses/{job_id}"},
        body={"job_id": job_id, "status": "queued"},
    )


def handle_rate_limited(request: HTTPRequest, requests_this_window: int, limit: int) -> HTTPResponse:
    """Demonstrates 429 Too Many Requests when a caller exceeds quota."""
    if requests_this_window > limit:
        return HTTPResponse(
            status=HTTPStatus.TOO_MANY_REQUESTS,
            headers={"Retry-After": "30"},
            body={"error": "rate_limit_exceeded", "limit": limit},
        )
    return HTTPResponse(status=HTTPStatus.OK, body={"status": "ok"})


def handle_dependency_down(request: HTTPRequest, sequencer_online: bool) -> HTTPResponse:
    """Demonstrates 503 for a downstream dependency (e.g. a lab instrument
    feed) being unavailable, versus 500 for an unexpected internal fault."""
    if not sequencer_online:
        return HTTPResponse(
            status=HTTPStatus.SERVICE_UNAVAILABLE,
            headers={"Retry-After": "60"},
            body={"error": "sequencer_feed_unavailable"},
        )
    return HTTPResponse(status=HTTPStatus.OK, body={"status": "ok"})


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    ok = handle_get_sample(HTTPRequest(method=HTTPMethod.GET, path="/samples/SMP-001",
                                        path_params={"sample_id": "SMP-001"}))
    assert ok.status is HTTPStatus.OK

    missing = handle_get_sample(HTTPRequest(method=HTTPMethod.GET, path="/samples/SMP-404",
                                             path_params={"sample_id": "SMP-404"}))
    assert missing.status is HTTPStatus.NOT_FOUND

    unauth = handle_create_sample(HTTPRequest(
        method=HTTPMethod.POST, path="/samples",
        headers={"content-type": "application/json"},
        body={"id": "SMP-002", "species": "Oryza sativa"},
    ))
    assert unauth.status is HTTPStatus.UNAUTHORIZED

    created = handle_create_sample(HTTPRequest(
        method=HTTPMethod.POST, path="/samples",
        headers={"content-type": "application/json", "authorization": "Bearer tok-researcher-abc"},
        body={"id": "SMP-002", "species": "Oryza sativa"},
    ))
    assert created.status is HTTPStatus.CREATED

    conflict = handle_create_sample(HTTPRequest(
        method=HTTPMethod.POST, path="/samples",
        headers={"content-type": "application/json", "authorization": "Bearer tok-researcher-abc"},
        body={"id": "SMP-002", "species": "Oryza sativa"},
    ))
    assert conflict.status is HTTPStatus.CONFLICT

    logger.info("HTTP semantics demo completed successfully")


if __name__ == "__main__":
    _demo()
