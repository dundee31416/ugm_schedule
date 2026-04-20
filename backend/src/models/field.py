"""Field model."""
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.session import Base


class Field(Base):
    """Field model representing a physical location where games are played."""

    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    games = relationship("Game", back_populates="field")

    def __repr__(self) -> str:
        return f"<Field(id={self.id}, name='{self.name}', city='{self.city}')>"
