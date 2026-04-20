"""Field schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FieldBase(BaseModel):
    """Base Field schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Field name")
    address: Optional[str] = Field(None, max_length=500, description="Field address")
    city: Optional[str] = Field(None, max_length=100, description="City where field is located")


class FieldCreate(FieldBase):
    """Schema for creating a new Field."""

    pass


class FieldUpdate(BaseModel):
    """Schema for updating an existing Field."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)


class Field(FieldBase):
    """Schema for Field responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
