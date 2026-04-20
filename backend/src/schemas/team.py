"""Team schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    """Base Team schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Team name")


class TeamCreate(TeamBase):
    """Schema for creating a new Team."""

    pass


class TeamUpdate(BaseModel):
    """Schema for updating an existing Team."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)


class Team(TeamBase):
    """Schema for Team responses."""

    id: int
    normalized_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
