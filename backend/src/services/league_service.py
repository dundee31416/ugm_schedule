"""League service for business logic."""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.league import League


class LeagueService:
    """Service for league-related operations."""

    @staticmethod
    def get_leagues(
        db: Session,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[League]:
        """
        Get leagues with optional filtering.

        Args:
            db: Database session
            is_active: Filter by active status
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of League objects
        """
        query = db.query(League)

        if is_active is not None:
            query = query.filter(League.is_active == is_active)

        query = query.order_by(League.name)
        query = query.offset(skip).limit(limit)

        return query.all()

    @staticmethod
    def get_league_by_id(db: Session, league_id: int) -> Optional[League]:
        """Get a single league by ID."""
        return db.query(League).filter(League.id == league_id).first()

    @staticmethod
    def get_active_leagues(db: Session) -> List[League]:
        """Get all active leagues."""
        return db.query(League).filter(League.is_active == True).order_by(League.name).all()
