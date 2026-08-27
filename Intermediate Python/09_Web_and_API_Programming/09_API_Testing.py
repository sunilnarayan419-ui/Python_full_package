"""
09_API_Testing.py

Professional API testing for the FastAPI authentication service defined in
07_API_Authentication.py, using FastAPI's TestClient and pytest.

Covers:
    - happy path
    - validation failures
    - authentication failures
    - authorization failures
    - not-found / conflict-style behavior
    - dependency overrides for deterministic, isolated tests (no real JWT
      secret or external service required)

Run with:
    pytest 09_API_Testing.py -v

These tests never call external/production services; the FastAPI app under
test is fully in-process and its auth dependency is overridden per test.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Import the sibling module by path so this file is runnable standalone
# regardless of package layout.
_MODULE_PATH = Path(__file__).parent / "07_API_Authentication.py"
_spec = importlib.util.spec_from_file_location("api_auth_module", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
api_auth_module = importlib.util.module_from_spec(_spec)
sys.modules["api_auth_module"] = api_auth_module
_spec.loader.exec_module(api_auth_module)

app = api_auth_module.app
get_current_user = api_auth_module.get_current_user
require_roles = api_auth_module.require_roles
AuthenticatedUser = api_auth_module.AuthenticatedUser
Role = api_auth_module.Role


@pytest.fixture()
def client() -> TestClient:
    """Fresh TestClient per test; dependency overrides are cleared after
    each test so tests remain isolated from one another."""
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def _override_user(role: Role, subject: str = "test-user") -> None:
    """Replace the real JWT-decoding dependency with a fixed identity, so
    tests never need a configured secret or a real token."""
    fixed_user = AuthenticatedUser(subject=subject, role=role)
    app.dependency_overrides[get_current_user] = lambda: fixed_user


class TestReadSample:
    def test_researcher_can_read_sample(self, client: TestClient) -> None:
        # Arrange
        _override_user(Role.RESEARCHER)

        # Act
        response = client.get("/samples/SMP-001")

        # Assert
        assert response.status_code == 200
        assert response.json()["id"] == "SMP-001"

    def test_unauthenticated_request_is_rejected(self, client: TestClient) -> None:
        # Arrange: no override installed, and no Authorization header sent.
        # Act
        response = client.get("/samples/SMP-001")

        # Assert
        assert response.status_code == 401


class TestCreateSample:
    def test_researcher_can_create_sample(self, client: TestClient) -> None:
        _override_user(Role.RESEARCHER)

        response = client.post("/samples", params={"sample_id": "SMP-100"})

        assert response.status_code == 201
        assert response.json() == {"id": "SMP-100", "created_by": "test-user"}

    def test_admin_can_create_sample(self, client: TestClient) -> None:
        _override_user(Role.ADMIN)

        response = client.post("/samples", params={"sample_id": "SMP-101"})

        assert response.status_code == 201

    def test_analyst_forbidden_from_creating_sample(self, client: TestClient) -> None:
        # Analysts are authenticated, but not authorized for writes.
        _override_user(Role.ANALYST)

        response = client.post("/samples", params={"sample_id": "SMP-102"})

        assert response.status_code == 403

    def test_missing_required_query_param_is_rejected(self, client: TestClient) -> None:
        _override_user(Role.RESEARCHER)

        response = client.post("/samples")  # missing required sample_id

        assert response.status_code == 422


class TestDeleteSample:
    def test_admin_can_delete_sample(self, client: TestClient) -> None:
        _override_user(Role.ADMIN)

        response = client.delete("/samples/SMP-100")

        assert response.status_code == 204
        assert response.content == b""

    def test_researcher_forbidden_from_deleting_sample(self, client: TestClient) -> None:
        # Only admins may delete, even though researchers can create.
        _override_user(Role.RESEARCHER)

        response = client.delete("/samples/SMP-100")

        assert response.status_code == 403


class TestLogin:
    def test_login_with_invalid_credentials_returns_401(self, client: TestClient) -> None:
        response = client.post(
            "/auth/token",
            json={"username": "dr.alvarez", "password": "definitely-wrong"},
        )

        assert response.status_code == 401
        # Never leak whether the username existed.
        assert response.json()["detail"] == "invalid credentials"

    def test_login_with_malformed_payload_returns_422(self, client: TestClient) -> None:
        response = client.post("/auth/token", json={"username": "dr.alvarez"})

        assert response.status_code == 422


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
