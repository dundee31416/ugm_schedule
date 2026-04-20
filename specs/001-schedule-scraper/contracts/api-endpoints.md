# API Contracts: REST Endpoints

**Feature**: Schedule Scraper and Display System
**Phase**: 1 - Design & Contracts
**Date**: 2026-04-07
**API Version**: v1

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.ugmschedule.com` (TBD)

## Global Headers

**Request**:
```
Content-Type: application/json
Accept: application/json
```

**Response**:
```
Content-Type: application/json
X-Request-ID: <uuid>
```

## Error Response Format

All errors follow this schema:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Endpoints

### GET /api/health

Health check endpoint for monitoring.

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-04-07T10:00:00Z",
  "database": "connected"
}
```

---

### GET /api/v1/games

List games with optional filtering.

**Query Parameters**:
- `team_name` (string, optional): Filter by team name (case-insensitive partial match)
- `field` (string, optional): Filter by exact field name
- `start_date` (string ISO 8601, optional): Filter games on or after this date
- `end_date` (string ISO 8601, optional): Filter games on or before this date
- `status` (enum, optional): Filter by status - `upcoming` | `completed` | `cancelled`
- `league_id` (integer, optional): Filter by league ID
- `limit` (integer, optional): Max results to return (default: 100, max: 500)
- `offset` (integer, optional): Results offset for pagination (default: 0)

**Response**: `200 OK`
```json
{
  "games": [
    {
      "id": 1,
      "league": {
        "id": 1,
        "name": "Ligues Récréatives Hiver 2025-2026"
      },
      "home_team": {
        "id": 5,
        "name": "Les Faucons"
      },
      "away_team": {
        "id": 12,
        "name": "Les Aigles"
      },
      "field": {
        "id": 3,
        "name": "Parc Jean-Drapeau - Terrain 3",
        "city": "Montréal"
      },
      "game_date": "2026-04-15",
      "game_time": "19:00:00",
      "home_score": 15,
      "away_score": 12,
      "status": "completed",
      "notes": null
    }
  ],
  "total": 48,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

**Examples**:
```
GET /api/v1/games?team_name=faucons
GET /api/v1/games?field=Parc Jean-Drapeau - Terrain 3
GET /api/v1/games?start_date=2026-04-01&end_date=2026-04-30
GET /api/v1/games?status=upcoming&league_id=1
GET /api/v1/games?team_name=aigles&status=completed&limit=20&offset=0
```

---

### GET /api/v1/games/{id}

Get details for a specific game.

**Path Parameters**:
- `id` (integer, required): Game ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "league": {
    "id": 1,
    "name": "Ligues Récréatives Hiver 2025-2026",
    "source_url": "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026"
  },
  "home_team": {
    "id": 5,
    "name": "Les Faucons"
  },
  "away_team": {
    "id": 12,
    "name": "Les Aigles"
  },
  "field": {
    "id": 3,
    "name": "Parc Jean-Drapeau - Terrain 3",
    "address": "1 Circuit Gilles-Villeneuve, Montréal",
    "city": "Montréal"
  },
  "game_date": "2026-04-15",
  "game_time": "19:00:00",
  "home_score": 15,
  "away_score": 12,
  "status": "completed",
  "notes": null,
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-16T08:30:00Z",
  "scraped_at": "2026-04-16T02:00:00Z"
}
```

**Errors**:
- `404 Not Found`: Game ID does not exist

---

### GET /api/v1/teams

List all teams.

**Query Parameters**:
- `name` (string, optional): Filter by team name (case-insensitive partial match)
- `limit` (integer, optional): Max results (default: 100, max: 500)
- `offset` (integer, optional): Results offset (default: 0)

**Response**: `200 OK`
```json
{
  "teams": [
    {
      "id": 1,
      "name": "Les Faucons",
      "game_count": 24
    },
    {
      "id": 2,
      "name": "Les Aigles",
      "game_count": 22
    }
  ],
  "total": 15,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

**Notes**:
- `game_count` includes both home and away games (upcoming and completed)

---

### GET /api/v1/teams/{id}

Get details for a specific team.

**Path Parameters**:
- `id` (integer, required): Team ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Les Faucons",
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-07T10:00:00Z",
  "upcoming_games": [
    {
      "id": 25,
      "opponent": {
        "id": 8,
        "name": "Les Requins"
      },
      "game_date": "2026-04-20",
      "game_time": "18:00:00",
      "field": "Parc Jarry - Terrain 1",
      "is_home": true
    }
  ],
  "recent_games": [
    {
      "id": 1,
      "opponent": {
        "id": 12,
        "name": "Les Aigles"
      },
      "game_date": "2026-04-15",
      "home_score": 15,
      "away_score": 12,
      "result": "win",
      "is_home": true
    }
  ],
  "stats": {
    "total_games": 24,
    "wins": 15,
    "losses": 8,
    "ties": 1
  }
}
```

**Errors**:
- `404 Not Found`: Team ID does not exist

---

### GET /api/v1/fields

List all fields/venues.

**Query Parameters**:
- `city` (string, optional): Filter by city
- `name` (string, optional): Filter by field name (partial match)
- `limit` (integer, optional): Max results (default: 100)
- `offset` (integer, optional): Results offset (default: 0)

**Response**: `200 OK`
```json
{
  "fields": [
    {
      "id": 1,
      "name": "Parc Jean-Drapeau - Terrain 3",
      "address": "1 Circuit Gilles-Villeneuve, Montréal",
      "city": "Montréal",
      "game_count": 48
    },
    {
      "id": 2,
      "name": "Parc Jarry - Terrain 1",
      "address": null,
      "city": "Montréal",
      "game_count": 36
    }
  ],
  "total": 8,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### GET /api/v1/leagues

List all leagues.

**Query Parameters**:
- `is_active` (boolean, optional): Filter by active status
- `limit` (integer, optional): Max results (default: 100)
- `offset` (integer, optional): Results offset (default: 0)

**Response**: `200 OK`
```json
{
  "leagues": [
    {
      "id": 1,
      "name": "Ligues Récréatives Hiver 2025-2026",
      "source_url": "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026",
      "is_active": true,
      "game_count": 48,
      "last_scraped_at": "2026-04-07T02:00:00Z",
      "last_scrape_status": "success"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### POST /api/admin/trigger-scrape

Manually trigger a scraping operation (admin/testing only).

**Request Body**:
```json
{
  "league_id": 1
}
```

**Parameters**:
- `league_id` (integer, optional): Scrape specific league. If omitted, scrapes all active leagues.

**Response**: `202 Accepted`
```json
{
  "message": "Scrape job initiated",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "leagues": [1, 2, 3]
}
```

**Rate Limit**: 5 requests/hour per IP

**Notes**:
- Scraping runs asynchronously
- Check `/api/v1/scrape-logs` for results

---

### GET /api/v1/scrape-logs

View scraping operation logs (admin/monitoring).

**Query Parameters**:
- `league_id` (integer, optional): Filter by league
- `status` (enum, optional): Filter by status - `success` | `failed` | `in_progress`
- `start_date` (string ISO 8601, optional): Logs after this date
- `limit` (integer, optional): Max results (default: 50, max: 200)
- `offset` (integer, optional): Results offset (default: 0)

**Response**: `200 OK`
```json
{
  "logs": [
    {
      "id": 1,
      "league": {
        "id": 1,
        "name": "Ligues Récréatives Hiver 2025-2026"
      },
      "started_at": "2026-04-07T02:00:00Z",
      "completed_at": "2026-04-07T02:03:45Z",
      "status": "success",
      "games_found": 48,
      "games_created": 5,
      "games_updated": 43,
      "error_message": null,
      "source_url": "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026"
    },
    {
      "id": 2,
      "league": {
        "id": 2,
        "name": "Summer League 2026"
      },
      "started_at": "2026-04-07T02:04:00Z",
      "completed_at": "2026-04-07T02:04:15Z",
      "status": "failed",
      "games_found": 0,
      "games_created": 0,
      "games_updated": 0,
      "error_message": "HTTP 404: Page not found",
      "source_url": "https://example.com/schedules/summer-2026"
    }
  ],
  "total": 125,
  "limit": 50,
  "offset": 0,
  "has_more": true
}
```

---

## Pydantic Schemas

### GameResponse

```python
from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
from enum import Enum

class GameStatus(str, Enum):
    upcoming = "upcoming"
    completed = "completed"
    cancelled = "cancelled"

class TeamSummary(BaseModel):
    id: int
    name: str

class LeagueSummary(BaseModel):
    id: int
    name: str

class FieldSummary(BaseModel):
    id: int
    name: str
    city: Optional[str]

class GameResponse(BaseModel):
    id: int
    league: LeagueSummary
    home_team: TeamSummary
    away_team: TeamSummary
    field: Optional[FieldSummary]
    game_date: date
    game_time: Optional[time]
    home_score: Optional[int]
    away_score: Optional[int]
    status: GameStatus
    notes: Optional[str]

    class Config:
        from_attributes = True
```

### GameListResponse

```python
class GameListResponse(BaseModel):
    games: list[GameResponse]
    total: int
    limit: int
    offset: int
    has_more: bool
```

### GameFilters

```python
from datetime import date
from typing import Optional

class GameFilters(BaseModel):
    team_name: Optional[str] = None
    field: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[GameStatus] = None
    league_id: Optional[int] = None
    limit: int = 100
    offset: int = 0

    class Config:
        extra = "forbid"  # Reject unknown query parameters
```

## Rate Limiting

**Default Limits**:
- `/api/v1/*`: 100 requests/minute per IP
- `/api/admin/trigger-scrape`: 5 requests/hour per IP

**Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1649318400
```

**Exceeded**:
```
HTTP/1.1 429 Too Many Requests
{
  "detail": "Rate limit exceeded. Try again in 45 seconds."
}
```

## CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:5173` (Vite default)
- Production: `https://ugmschedule.com` (TBD)

**Allowed Methods**: GET, POST, OPTIONS
**Allowed Headers**: Content-Type, Accept
**Max Age**: 3600 seconds

## OpenAPI Documentation

FastAPI will auto-generate OpenAPI 3.0 documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Summary

This API contract provides:
- ✅ RESTful resource design
- ✅ Clear filtering and pagination
- ✅ Consistent error responses
- ✅ Rate limiting for abuse prevention
- ✅ OpenAPI auto-documentation
- ✅ Type-safe request/response schemas
- ✅ Admin endpoints for manual operations

Frontend can consume these endpoints with full type safety via generated TypeScript types from OpenAPI schema.
