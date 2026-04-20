"""ScrapeLog model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from src.database.session import Base


class ScrapeStatus(str, enum.Enum):
    """Scrape status enumeration."""

    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


class ScrapeLog(Base):
    """ScrapeLog model tracking scraping operations."""

    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(ScrapeStatus), nullable=False, index=True)
    games_found = Column(Integer, nullable=True)
    games_created = Column(Integer, nullable=True)
    games_updated = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=False)

    # Relationships
    league = relationship("League", back_populates="scrape_logs")

    def __repr__(self) -> str:
        return f"<ScrapeLog(id={self.id}, league_id={self.league_id}, status={self.status})>"
