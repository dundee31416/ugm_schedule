"""League schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class LeagueBase(BaseModel):
    """Base League schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="League name")
    source_url: str = Field(..., min_length=1, max_length=500, description="URL to scrape schedules from")
    is_active: bool = Field(default=True, description="Whether the league is actively being scraped")


class LeagueCreate(LeagueBase):
    """Schema for creating a new League."""

    pass


class LeagueUpdate(BaseModel):
    """Schema for updating an existing League."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    source_url: Optional[str] = Field(None, min_length=1, max_length=500)
    is_active: Optional[bool] = None


class League(LeagueBase):
    """Schema for League responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
