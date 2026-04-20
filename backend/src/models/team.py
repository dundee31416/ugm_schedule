"""Team model."""
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from src.database.session import Base


class Team(Base):
    """Team model representing a team participating in games."""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    normalized_name = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    home_games = relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    away_games = relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")

    # Indexes
    __table_args__ = (
        Index('idx_team_name', 'name'),
    )

    def __init__(self, **kwargs):
        """Initialize team and set normalized_name."""
        super().__init__(**kwargs)
        if 'name' in kwargs and 'normalized_name' not in kwargs:
            self.normalized_name = kwargs['name'].lower().strip()

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}')>"
