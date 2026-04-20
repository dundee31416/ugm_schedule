"""Team service for business logic."""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.team import Team


class TeamService:
    """Service for team-related operations."""

    @staticmethod
    def get_teams(
        db: Session,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Team]:
        """
        Get teams with optional search.

        Args:
            db: Database session
            search: Search in team name
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Team objects
        """
        query = db.query(Team)

        if search:
            query = query.filter(Team.name.ilike(f"%{search}%"))

        query = query.order_by(Team.name)
        query = query.offset(skip).limit(limit)

        return query.all()

    @staticmethod
    def get_team_by_id(db: Session, team_id: int) -> Optional[Team]:
        """Get a single team by ID."""
        return db.query(Team).filter(Team.id == team_id).first()

    @staticmethod
    def get_or_create_team(db: Session, name: str) -> Team:
        """
        Get an existing team by normalized name or create a new one.

        Args:
            db: Database session
            name: Team name

        Returns:
            Existing or newly created Team object
        """
        normalized_name = name.lower().strip()
        team = db.query(Team).filter(Team.normalized_name == normalized_name).first()

        if team is None:
            team = Team(name=name)
            db.add(team)
            db.flush()  # Flush to get the ID without committing

        return team
