"""Game schemas."""
from datetime import date, datetime, time
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from src.schemas.league import League
from src.schemas.team import Team
from src.schemas.field import Field as FieldSchema


class GameStatus(str, Enum):
    """Game status enumeration."""

    UPCOMING = "upcoming"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GameBase(BaseModel):
    """Base Game schema with common fields."""

    league_id: int = Field(..., gt=0, description="League ID")
    home_team_id: int = Field(..., gt=0, description="Home team ID")
    away_team_id: int = Field(..., gt=0, description="Away team ID")
    field_id: Optional[int] = Field(None, gt=0, description="Field ID")
    game_date: date = Field(..., description="Date of the game")
    game_time: Optional[time] = Field(None, description="Time of the game")
    home_score: Optional[int] = Field(None, ge=0, description="Home team score")
    away_score: Optional[int] = Field(None, ge=0, description="Away team score")
    status: GameStatus = Field(default=GameStatus.UPCOMING, description="Game status")
    notes: Optional[str] = Field(None, description="Additional notes about the game")
    external_id: Optional[str] = Field(None, max_length=255, description="External ID from source system")

    @field_validator('away_team_id')
    @classmethod
    def validate_different_teams(cls, v: int, info) -> int:
        """Ensure home and away teams are different."""
        if 'home_team_id' in info.data and v == info.data['home_team_id']:
            raise ValueError('Home team and away team must be different')
        return v


class GameCreate(GameBase):
    """Schema for creating a new Game."""

    pass


class GameUpdate(BaseModel):
    """Schema for updating an existing Game."""

    league_id: Optional[int] = Field(None, gt=0)
    home_team_id: Optional[int] = Field(None, gt=0)
    away_team_id: Optional[int] = Field(None, gt=0)
    field_id: Optional[int] = Field(None, gt=0)
    game_date: Optional[date] = None
    game_time: Optional[time] = None
    home_score: Optional[int] = Field(None, ge=0)
    away_score: Optional[int] = Field(None, ge=0)
    status: Optional[GameStatus] = None
    notes: Optional[str] = None
    external_id: Optional[str] = Field(None, max_length=255)

    @field_validator('away_team_id')
    @classmethod
    def validate_different_teams(cls, v: Optional[int], info) -> Optional[int]:
        """Ensure home and away teams are different."""
        if v is not None and 'home_team_id' in info.data and info.data['home_team_id'] is not None:
            if v == info.data['home_team_id']:
                raise ValueError('Home team and away team must be different')
        return v


class Game(GameBase):
    """Schema for Game responses with nested relationships."""

    id: int
    created_at: datetime
    updated_at: datetime
    scraped_at: datetime

    # Nested relationships
    league: League
    home_team: Team
    away_team: Team
    field: Optional[FieldSchema] = None

    class Config:
        from_attributes = True
