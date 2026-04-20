"""Game model."""
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, Enum, Text, Index, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from src.database.session import Base


class GameStatus(str, enum.Enum):
    """Game status enumeration."""

    UPCOMING = "upcoming"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Game(Base):
    """Game model representing a single scheduled game."""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False, index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False, index=True)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)

    game_date = Column(Date, nullable=False, index=True)
    game_time = Column(Time, nullable=True)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    status = Column(Enum(GameStatus), default=GameStatus.UPCOMING, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    external_id = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    league = relationship("League", back_populates="games")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    field = relationship("Field", back_populates="games")

    # Constraints
    __table_args__ = (
        CheckConstraint('home_team_id != away_team_id', name='check_different_teams'),
        CheckConstraint('home_score >= 0', name='check_home_score_non_negative'),
        CheckConstraint('away_score >= 0', name='check_away_score_non_negative'),
        Index('idx_game_date', 'game_date'),
        Index('idx_game_status_date', 'status', 'game_date'),
        Index('idx_league_external_id', 'league_id', 'external_id', unique=True),
    )

    def __repr__(self) -> str:
        return f"<Game(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id}, date={self.game_date})>"
