"""Contract tests for League API endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_get_leagues_returns_200(client: TestClient):
    """Test GET /api/v1/leagues returns 200 OK."""
    response = client.get("/api/v1/leagues")
    assert response.status_code == 200


def test_get_leagues_returns_list_structure(client: TestClient):
    """Test GET /api/v1/leagues returns expected structure."""
    response = client.get("/api/v1/leagues")
    assert response.status_code == 200
    data = response.json()

    assert "leagues" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data

    assert isinstance(data["leagues"], list)


def test_get_leagues_with_active_filter(client: TestClient):
    """Test GET /api/v1/leagues accepts is_active filter."""
    response = client.get("/api/v1/leagues?is_active=true")
    assert response.status_code == 200
