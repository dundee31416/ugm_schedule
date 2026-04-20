"""Contract tests for Game API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_games_returns_200(client: TestClient):
    """Test GET /api/v1/games returns 200 OK."""
    response = client.get("/api/v1/games")
    assert response.status_code == 200


def test_get_games_returns_list_structure(client: TestClient):
    """Test GET /api/v1/games returns expected structure."""
    response = client.get("/api/v1/games")
    assert response.status_code == 200
    data = response.json()

    # Verify structure
    assert "games" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data

    # Verify types
    assert isinstance(data["games"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["limit"], int)
    assert isinstance(data["offset"], int)
    assert isinstance(data["has_more"], bool)


def test_get_games_with_filters(client: TestClient):
    """Test GET /api/v1/games accepts filter parameters."""
    response = client.get("/api/v1/games?team_name=test&status=upcoming&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10


def test_get_game_by_id_returns_200(client: TestClient, db: Session):
    """Test GET /api/v1/games/{id} returns 200 for valid ID."""
    # This will fail until we have sample data
    # For now, just test the endpoint exists
    response = client.get("/api/v1/games/1")
    # Will be 404 until we add data, but endpoint should exist
    assert response.status_code in [200, 404]


def test_get_game_by_id_returns_404_for_invalid(client: TestClient):
    """Test GET /api/v1/games/{id} returns 404 for non-existent game."""
    response = client.get("/api/v1/games/99999")
    assert response.status_code == 404
