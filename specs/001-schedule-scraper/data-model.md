# Data Model: Schedule Scraper Database Schema

**Feature**: Schedule Scraper and Display System
**Phase**: 1 - Design & Contracts
**Date**: 2026-04-07

## Overview

This document defines the database schema for the schedule scraper application. All models use SQLAlchemy ORM with PostgreSQL as the target database.

## Entity Relationship Diagram

```
┌─────────────┐
│   League    │
└─────┬───────┘
      │ 1
      │
      │ *
┌─────▼───────┐         ┌─────────────┐
│    Game     ├────*────┤    Team     │
└─────┬───────┘    home └─────────────┘
      │ *           away
      │
      │ *
┌─────▼───────┐
│    Field    │
└─────────────┘

┌─────────────┐
│ ScrapeLog   │ (independent, tracks scraping operations)
└─────────────┘
```

## Entities

### League

Represents a sports league or competition that is being scraped.

**Attributes**:
- `id`: Integer, primary key, auto-increment
- `name`: String(255), required, unique - Display name of the league
- `source_url`: String(500), required - URL to scrape schedule from
- `is_active`: Boolean, default True - Whether to include in scraping
- `created_at`: DateTime, default now - When league was added
- `updated_at`: DateTime, auto-update - Last modification timestamp

**Relationships**:
- `games`: One-to-many relationship with Game

**Validation Rules**:
- `name` must not be empty
- `source_url` must be valid HTTP/HTTPS URL
- `source_url` must be unique across leagues

**Indexes**:
- Primary key on `id`
- Unique index on `source_url`
- Index on `is_active` for filtering active leagues

**Example**:
```json
{
  "id": 1,
  "name": "Ligues Récréatives Hiver 2025-2026",
  "source_url": "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026",
  "is_active": true,
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-07T10:00:00Z"
}
```

---

### Team

Represents a team that participates in games.

**Attributes**:
- `id`: Integer, primary key, auto-increment
- `name`: String(255), required, unique - Team name as scraped
- `normalized_name`: String(255), computed - Lowercase, trimmed for matching
- `created_at`: DateTime, default now
- `updated_at`: DateTime, auto-update

**Relationships**:
- `home_games`: One-to-many relationship with Game (as home team)
- `away_games`: One-to-many relationship with Game (as away team)

**Validation Rules**:
- `name` must not be empty
- `name` uniqueness enforced case-insensitively via `normalized_name`

**Indexes**:
- Primary key on `id`
- Unique index on `normalized_name`
- Index on `name` for search queries

**Notes**:
- `normalized_name` is auto-generated: `name.lower().strip()`
- Used for deduplication when scraping (e.g., "Team A" vs "team a")

**Example**:
```json
{
  "id": 1,
  "name": "Les Faucons",
  "normalized_name": "les faucons",
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-07T10:00:00Z"
}
```

---

### Field

Represents a physical location where games are played.

**Attributes**:
- `id`: Integer, primary key, auto-increment
- `name`: String(255), required, unique - Field/venue name
- `address`: String(500), nullable - Full address if available
- `city`: String(100), nullable - City name
- `created_at`: DateTime, default now
- `updated_at`: DateTime, auto-update

**Relationships**:
- `games`: One-to-many relationship with Game

**Validation Rules**:
- `name` must not be empty
- `name` must be unique

**Indexes**:
- Primary key on `id`
- Unique index on `name`
- Index on `city` for location-based filtering

**Example**:
```json
{
  "id": 1,
  "name": "Parc Jean-Drapeau - Terrain 3",
  "address": "1 Circuit Gilles-Villeneuve, Montréal",
  "city": "Montréal",
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-07T10:00:00Z"
}
```

---

### Game

Represents a single scheduled game between two teams.

**Attributes**:
- `id`: Integer, primary key, auto-increment
- `league_id`: Integer, foreign key to League, required
- `home_team_id`: Integer, foreign key to Team, required
- `away_team_id`: Integer, foreign key to Team, required
- `field_id`: Integer, foreign key to Field, nullable
- `game_date`: Date, required - Date of the game
- `game_time`: Time, nullable - Start time (null if TBD)
- `home_score`: Integer, nullable - Home team score (null if not played)
- `away_score`: Integer, nullable - Away team score (null if not played)
- `status`: Enum('upcoming', 'completed', 'cancelled'), default 'upcoming'
- `notes`: Text, nullable - Additional information (e.g., "Rescheduled", "Playoffs")
- `external_id`: String(255), nullable - ID from source website (for deduplication)
- `created_at`: DateTime, default now
- `updated_at`: DateTime, auto-update
- `scraped_at`: DateTime, auto-update - Last time this game was seen during scraping

**Relationships**:
- `league`: Many-to-one relationship with League
- `home_team`: Many-to-one relationship with Team
- `away_team`: Many-to-one relationship with Team
- `field`: Many-to-one relationship with Field

**Validation Rules**:
- `home_team_id` != `away_team_id` (team can't play itself)
- `game_date` must not be more than 2 years in the past (data retention)
- If `status` is 'completed', both `home_score` and `away_score` must be non-null
- If `status` is 'upcoming', both scores must be null
- `external_id` + `league_id` combination must be unique (prevents duplicates from same source)

**Indexes**:
- Primary key on `id`
- Index on `league_id` for league-specific queries
- Index on `home_team_id` for team game lookups
- Index on `away_team_id` for team game lookups
- Index on `field_id` for field-specific queries
- Index on `game_date` for date range filtering
- Composite index on (`status`, `game_date`) for upcoming/past game queries
- Unique index on (`league_id`, `external_id`) for deduplication

**Computed Properties** (not stored in DB):
- `is_past`: Boolean - `game_date < today`
- `is_today`: Boolean - `game_date == today`
- `display_time`: String - Formatted time or "TBD" if null

**Example**:
```json
{
  "id": 1,
  "league_id": 1,
  "home_team_id": 5,
  "away_team_id": 12,
  "field_id": 3,
  "game_date": "2026-04-15",
  "game_time": "19:00:00",
  "home_score": 15,
  "away_score": 12,
  "status": "completed",
  "notes": null,
  "external_id": "game-12345",
  "created_at": "2026-04-07T10:00:00Z",
  "updated_at": "2026-04-16T08:30:00Z",
  "scraped_at": "2026-04-16T02:00:00Z"
}
```

---

### ScrapeLog

Tracks scraping operations for monitoring and debugging.

**Attributes**:
- `id`: Integer, primary key, auto-increment
- `league_id`: Integer, foreign key to League, required
- `started_at`: DateTime, required - When scrape started
- `completed_at`: DateTime, nullable - When scrape finished (null if failed/in-progress)
- `status`: Enum('in_progress', 'success', 'failed'), required
- `games_found`: Integer, nullable - Number of games scraped
- `games_created`: Integer, nullable - Number of new games added
- `games_updated`: Integer, nullable - Number of existing games updated
- `error_message`: Text, nullable - Error details if failed
- `source_url`: String(500), required - URL that was scraped (snapshot)

**Relationships**:
- `league`: Many-to-one relationship with League

**Validation Rules**:
- If `status` is 'success', `completed_at` must be non-null
- If `status` is 'failed', `error_message` must be non-null
- `started_at` must be <= `completed_at`

**Indexes**:
- Primary key on `id`
- Index on `league_id` for league-specific logs
- Index on `started_at` for chronological queries
- Index on `status` for filtering by success/failure

**Example**:
```json
{
  "id": 1,
  "league_id": 1,
  "started_at": "2026-04-07T02:00:00Z",
  "completed_at": "2026-04-07T02:03:45Z",
  "status": "success",
  "games_found": 48,
  "games_created": 5,
  "games_updated": 43,
  "error_message": null,
  "source_url": "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026"
}
```

## Database Migrations

**Initial Migration** (`001_initial_schema.py`):
- Create all tables with columns as defined above
- Create all foreign key constraints
- Create all indexes

**Future Migration Considerations**:
- Add `division` field to Team if leagues have divisions
- Add `season` field to League for multi-season tracking
- Add `venue_capacity` to Field if needed
- Add `weather` to Game if outdoor games are affected by weather

## Data Integrity Rules

### Cascade Behavior

**League deletion**:
- Cascade delete all associated Games
- Cascade delete all associated ScrapeLogs
- Rationale: Games without a league context are meaningless

**Team deletion**:
- Restrict deletion if any Games reference the team
- Rationale: Preserve historical game data, teams should be marked inactive instead

**Field deletion**:
- Set `field_id` to NULL in Games (allow deletion)
- Rationale: Game can still be meaningful without field information

### Constraints

**Check Constraints**:
- `Game.home_score` >= 0 (if not null)
- `Game.away_score` >= 0 (if not null)
- `Game.home_team_id` != `Game.away_team_id`

**Unique Constraints**:
- `League.source_url`
- `Team.normalized_name`
- `Field.name`
- (`Game.league_id`, `Game.external_id`) - prevents duplicate games from same source

## Query Patterns

### Common Queries (for optimization)

**Get all upcoming games for a team**:
```sql
SELECT g.* FROM games g
WHERE (g.home_team_id = :team_id OR g.away_team_id = :team_id)
  AND g.status = 'upcoming'
  AND g.game_date >= CURRENT_DATE
ORDER BY g.game_date ASC, g.game_time ASC;
```

**Get all games at a field within date range**:
```sql
SELECT g.* FROM games g
WHERE g.field_id = :field_id
  AND g.game_date BETWEEN :start_date AND :end_date
ORDER BY g.game_date ASC, g.game_time ASC;
```

**Search games by team name (partial match)**:
```sql
SELECT g.* FROM games g
JOIN teams ht ON g.home_team_id = ht.id
JOIN teams at ON g.away_team_id = at.id
WHERE ht.name ILIKE :search_pattern OR at.name ILIKE :search_pattern
ORDER BY g.game_date DESC;
```

**Get scrape success rate for a league**:
```sql
SELECT
  COUNT(*) as total_scrapes,
  SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_scrapes,
  (SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END)::float / COUNT(*)) * 100 as success_rate
FROM scrape_logs
WHERE league_id = :league_id
  AND started_at >= CURRENT_DATE - INTERVAL '30 days';
```

## Sample Data

For testing and development, seed database with:
- 2-3 Leagues (including the Montreal Ultimate example)
- 10-20 Teams
- 5-10 Fields
- 50-100 Games (mix of upcoming and completed)
- 10-20 ScrapeLogs (mix of success and failure)

## Summary

This schema provides:
- ✅ Clear entity relationships (League → Game → Team/Field)
- ✅ Deduplication mechanisms (external_id, normalized_name)
- ✅ Audit trails (created_at, updated_at, scraped_at)
- ✅ Scraping monitoring (ScrapeLog)
- ✅ Efficient querying (indexes on filter columns)
- ✅ Data integrity (foreign keys, check constraints)
- ✅ Flexibility (nullable fields for incomplete data like TBD times)

Ready for contract definition and implementation.
