"""League model."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.session import Base


class League(Base):
    """League model representing a sports league/competition."""

    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    source_url = Column(String(500), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    games = relationship("Game", back_populates="league", cascade="all, delete-orphan")
    scrape_logs = relationship("ScrapeLog", back_populates="league", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<League(id={self.id}, name='{self.name}')>"
