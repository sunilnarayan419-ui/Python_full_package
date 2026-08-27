from __future__ import annotations

import pytest
import responses

from src.drug_database_client import DrugDatabaseClient, DrugNotFoundError


@pytest.fixture
def client() -> DrugDatabaseClient:
    with DrugDatabaseClient(base_url="https://drugdb.test", api_key="test-key") as db_client:
        yield db_client


@responses.activate
def test_get_drug_returns_parsed_record(client: DrugDatabaseClient) -> None:
    responses.add(
        responses.GET,
        "https://drugdb.test/drugs/DB00001",
        json={"drug_id": "DB00001", "name": "Lepirudin", "approval_status": "approved", "indications": ["anticoagulation"]},
        status=200,
    )

    record = client.get_drug("DB00001")

    assert record.name == "Lepirudin"
    assert record.indications == ["anticoagulation"]


@responses.activate
def test_get_drug_not_found_raises_typed_error(client: DrugDatabaseClient) -> None:
    responses.add(responses.GET, "https://drugdb.test/drugs/DB99999", json={"detail": "not found"}, status=404)

    with pytest.raises(DrugNotFoundError):
        client.get_drug("DB99999")


@responses.activate
def test_search_drugs_returns_list_of_records(client: DrugDatabaseClient) -> None:
    responses.add(
        responses.GET,
        "https://drugdb.test/drugs",
        json={"results": [{"drug_id": "DB00002", "name": "Cetuximab", "approval_status": "approved", "indications": []}]},
        status=200,
    )

    results = client.search_drugs("cetuximab", limit=10)

    assert len(results) == 1
    assert results[0].drug_id == "DB00002"
