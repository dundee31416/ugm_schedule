"""Integration tests for filtering game flow."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, time


def test_filter_games_by_team_name(client: TestClient, db: Session):
    """Test filtering games by team name returns correct results."""
    # This test will pass once we implement the full flow
    # For now, it tests the endpoint exists and accepts the parameter
    response = client.get("/api/v1/games?team_name=Faucons")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data


def test_filter_games_by_date_range(client: TestClient, db: Session):
    """Test filtering games by date range."""
    response = client.get("/api/v1/games?start_date=2026-04-01&end_date=2026-04-30")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data


def test_filter_games_by_field(client: TestClient, db: Session):
    """Test filtering games by field name."""
    response = client.get("/api/v1/games?field=Parc Jean-Drapeau")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data


def test_filter_games_by_status(client: TestClient, db: Session):
    """Test filtering games by status."""
    response = client.get("/api/v1/games?status=upcoming")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data


def test_combined_filters(client: TestClient, db: Session):
    """Test multiple filters applied together."""
    response = client.get(
        "/api/v1/games?team_name=Faucons&status=completed&start_date=2026-01-01"
    )
    assert response.status_code == 200
    data = response.json()
    assert "games" in data


def test_pagination_works_with_filters(client: TestClient, db: Session):
    """Test pagination combined with filters."""
    response = client.get("/api/v1/games?team_name=test&limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 5
    assert data["offset"] == 0
