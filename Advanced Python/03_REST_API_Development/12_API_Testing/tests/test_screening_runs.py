from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import AsyncClient

from src.domain.entities import AssayType, ScreeningRunStatus
from src.repositories.screening_run_repository import InMemoryScreeningRunRepository

pytestmark = pytest.mark.asyncio


class TestSubmitScreeningRun:
    async def test_submit_creates_run_with_queued_status(self, client: AsyncClient) -> None:
        compound_id = str(uuid4())

        response = await client.post(
            "/api/v1/screening-runs",
            json={"compound_id": compound_id, "assay_type": AssayType.BINDING.value},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["compound_id"] == compound_id
        assert body["status"] == ScreeningRunStatus.QUEUED.value
        assert body["score"] is None

    async def test_submit_rejects_invalid_assay_type(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/screening-runs",
            json={"compound_id": str(uuid4()), "assay_type": "not-a-real-assay"},
        )

        assert response.status_code == 422

    async def test_submit_rejects_missing_compound_id(self, client: AsyncClient) -> None:
        response = await client.post("/api/v1/screening-runs", json={"assay_type": AssayType.BINDING.value})

        assert response.status_code == 422


class TestGetScreeningRun:
    async def test_get_existing_run_returns_200(self, client: AsyncClient, seeded_run) -> None:
        response = await client.get(f"/api/v1/screening-runs/{seeded_run.run_id}")

        assert response.status_code == 200
        assert response.json()["run_id"] == str(seeded_run.run_id)

    async def test_get_missing_run_returns_404_with_error_contract(self, client: AsyncClient) -> None:
        response = await client.get(f"/api/v1/screening-runs/{uuid4()}")

        assert response.status_code == 404
        body = response.json()
        assert body["error"]["code"] == "SCREENING_RUN_NOT_FOUND"
        assert "request_id" in body["error"]


class TestTransitionScreeningRun:
    async def test_valid_transition_updates_status_and_score(self, client: AsyncClient, seeded_run) -> None:
        response = await client.patch(
            f"/api/v1/screening-runs/{seeded_run.run_id}",
            json={"target_status": ScreeningRunStatus.RUNNING.value},
        )

        assert response.status_code == 200
        assert response.json()["status"] == ScreeningRunStatus.RUNNING.value

    async def test_invalid_transition_returns_409(self, client: AsyncClient, seeded_run) -> None:
        response = await client.patch(
            f"/api/v1/screening-runs/{seeded_run.run_id}",
            json={"target_status": ScreeningRunStatus.VALIDATED.value},
        )

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "INVALID_STATUS_TRANSITION"

    async def test_transition_score_out_of_range_returns_422(self, client: AsyncClient, seeded_run) -> None:
        response = await client.patch(
            f"/api/v1/screening-runs/{seeded_run.run_id}",
            json={"target_status": ScreeningRunStatus.RUNNING.value, "score": 1.5},
        )

        assert response.status_code == 422


class TestListScreeningRuns:
    async def test_list_returns_pagination_metadata(
        self, client: AsyncClient, repository: InMemoryScreeningRunRepository, seeded_run
    ) -> None:
        response = await client.get(
            f"/api/v1/compounds/{seeded_run.compound_id}/screening-runs",
            params={"limit": 10, "offset": 0},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["meta"] == {"limit": 10, "offset": 0, "count": 1}
        assert len(body["items"]) == 1

    async def test_list_respects_limit(self, client: AsyncClient, repository: InMemoryScreeningRunRepository) -> None:
        compound_id = uuid4()
        for _ in range(5):
            from src.domain.entities import ScreeningRun

            await repository.add(ScreeningRun.create(compound_id=compound_id, assay_type=AssayType.ADMET))

        response = await client.get(f"/api/v1/compounds/{compound_id}/screening-runs", params={"limit": 2, "offset": 0})

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
