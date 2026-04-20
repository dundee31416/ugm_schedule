"""Response schemas with pagination metadata."""
from typing import List, Generic, TypeVar
from pydantic import BaseModel

from src.schemas.game import Game
from src.schemas.team import Team
from src.schemas.field import Field
from src.schemas.league import League

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    items: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool


class GameListResponse(BaseModel):
    """Response schema for game list."""

    games: List[Game]
    total: int
    limit: int
    offset: int
    has_more: bool


class TeamListResponse(BaseModel):
    """Response schema for team list."""

    teams: List[Team]
    total: int
    limit: int
    offset: int
    has_more: bool


class FieldListResponse(BaseModel):
    """Response schema for field list."""

    fields: List[Field]
    total: int
    limit: int
    offset: int
    has_more: bool


class LeagueListResponse(BaseModel):
    """Response schema for league list."""

    leagues: List[League]
    total: int
    limit: int
    offset: int
    has_more: bool
