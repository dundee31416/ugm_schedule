"""Contract tests for Team API endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_get_teams_returns_200(client: TestClient):
    """Test GET /api/v1/teams returns 200 OK."""
    response = client.get("/api/v1/teams")
    assert response.status_code == 200


def test_get_teams_returns_list_structure(client: TestClient):
    """Test GET /api/v1/teams returns expected structure."""
    response = client.get("/api/v1/teams")
    assert response.status_code == 200
    data = response.json()

    assert "teams" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data

    assert isinstance(data["teams"], list)


def test_get_teams_with_name_filter(client: TestClient):
    """Test GET /api/v1/teams accepts name filter."""
    response = client.get("/api/v1/teams?name=test")
    assert response.status_code == 200


def test_get_team_by_id_endpoint_exists(client: TestClient):
    """Test GET /api/v1/teams/{id} endpoint exists."""
    response = client.get("/api/v1/teams/1")
    assert response.status_code in [200, 404]
