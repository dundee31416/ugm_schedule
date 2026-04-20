"""Game service for business logic."""
from datetime import date
from typing import List, Optional

from sqlalchemy import and_, or_, distinct
from sqlalchemy.orm import Session, joinedload

from src.models.game import Game, GameStatus
from src.models.team import Team


class GameService:
    """Service for game-related operations."""

    @staticmethod
    def get_games(
        db: Session,
        league_id: Optional[int] = None,
        team_id: Optional[int] = None,
        field_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[GameStatus] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Game]:
        """
        Get games with optional filtering.

        Args:
            db: Database session
            league_id: Filter by league ID
            team_id: Filter by team ID (home or away)
            field_id: Filter by field ID
            start_date: Filter games on or after this date
            end_date: Filter games on or before this date
            status: Filter by game status
            search: Search in team names
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Game objects with relationships loaded
        """
        query = db.query(Game).options(
            joinedload(Game.league),
            joinedload(Game.home_team),
            joinedload(Game.away_team),
            joinedload(Game.field),
        )

        # Apply filters
        filters = []

        if league_id is not None:
            filters.append(Game.league_id == league_id)

        if team_id is not None:
            filters.append(or_(Game.home_team_id == team_id, Game.away_team_id == team_id))

        if field_id is not None:
            filters.append(Game.field_id == field_id)

        if start_date is not None:
            filters.append(Game.game_date >= start_date)

        if end_date is not None:
            filters.append(Game.game_date <= end_date)

        if status is not None:
            filters.append(Game.status == status)

        if search:
            # Search in team names
            search_filter = or_(
                Game.home_team.has(Team.name.ilike(f"%{search}%")),
                Game.away_team.has(Team.name.ilike(f"%{search}%")),
            )
            filters.append(search_filter)

        if filters:
            query = query.filter(and_(*filters))

        # Order by date and time
        query = query.order_by(Game.game_date.desc(), Game.game_time.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        return query.all()

    @staticmethod
    def get_game_by_id(db: Session, game_id: int) -> Optional[Game]:
        """Get a single game by ID with relationships loaded."""
        return (
            db.query(Game)
            .options(
                joinedload(Game.league),
                joinedload(Game.home_team),
                joinedload(Game.away_team),
                joinedload(Game.field),
            )
            .filter(Game.id == game_id)
            .first()
        )

    @staticmethod
    def count_games(
        db: Session,
        league_id: Optional[int] = None,
        team_id: Optional[int] = None,
        field_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[GameStatus] = None,
        search: Optional[str] = None,
    ) -> int:
        """Count games matching the filters."""
        query = db.query(Game)

        # Apply the same filters as get_games
        filters = []

        if league_id is not None:
            filters.append(Game.league_id == league_id)

        if team_id is not None:
            filters.append(or_(Game.home_team_id == team_id, Game.away_team_id == team_id))

        if field_id is not None:
            filters.append(Game.field_id == field_id)

        if start_date is not None:
            filters.append(Game.game_date >= start_date)

        if end_date is not None:
            filters.append(Game.game_date <= end_date)

        if status is not None:
            filters.append(Game.status == status)

        if search:
            search_filter = or_(
                Game.home_team.has(Team.name.ilike(f"%{search}%")),
                Game.away_team.has(Team.name.ilike(f"%{search}%")),
            )
            filters.append(search_filter)

        if filters:
            query = query.filter(and_(*filters))

        return query.count()

    @staticmethod
    def get_unique_game_dates(db: Session, league_id: int) -> List[date]:
        """Get unique game dates for a specific league, sorted in descending order."""
        dates = (
            db.query(distinct(Game.game_date))
            .filter(Game.league_id == league_id, Game.game_date.isnot(None))
            .order_by(Game.game_date.desc())
            .all()
        )
        return [d[0] for d in dates]
