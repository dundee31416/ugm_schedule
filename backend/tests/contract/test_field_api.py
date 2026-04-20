"""Contract tests for Field API endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_get_fields_returns_200(client: TestClient):
    """Test GET /api/v1/fields returns 200 OK."""
    response = client.get("/api/v1/fields")
    assert response.status_code == 200


def test_get_fields_returns_list_structure(client: TestClient):
    """Test GET /api/v1/fields returns expected structure."""
    response = client.get("/api/v1/fields")
    assert response.status_code == 200
    data = response.json()

    assert "fields" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data

    assert isinstance(data["fields"], list)


def test_get_fields_with_filters(client: TestClient):
    """Test GET /api/v1/fields accepts filter parameters."""
    response = client.get("/api/v1/fields?city=Montreal&name=Parc")
    assert response.status_code == 200
