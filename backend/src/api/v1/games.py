"""Game API endpoints."""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.models.game import GameStatus
from src.schemas.game import Game
from src.schemas.responses import GameListResponse
from src.services.game_service import GameService

router = APIRouter()


@router.get("", response_model=GameListResponse)
def get_games(
    league_id: Optional[int] = Query(None, description="Filter by league ID"),
    team_id: Optional[int] = Query(None, description="Filter by team ID (home or away)"),
    field_id: Optional[int] = Query(None, description="Filter by field ID"),
    start_date: Optional[date] = Query(None, description="Filter games on or after this date"),
    end_date: Optional[date] = Query(None, description="Filter games on or before this date"),
    status: Optional[GameStatus] = Query(None, description="Filter by game status"),
    search: Optional[str] = Query(None, description="Search in team names"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> GameListResponse:
    """
    Get games with optional filtering.

    Supports filtering by:
    - league_id: Filter by league
    - team_id: Filter by team (home or away)
    - field_id: Filter by field
    - start_date: Games on or after this date
    - end_date: Games on or before this date
    - status: Filter by game status (upcoming, completed, cancelled)
    - search: Search in team names

    Results are paginated using skip and limit parameters.
    """
    games = GameService.get_games(
        db=db,
        league_id=league_id,
        team_id=team_id,
        field_id=field_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        search=search,
        skip=skip,
        limit=limit,
    )

    total = GameService.count_games(
        db=db,
        league_id=league_id,
        team_id=team_id,
        field_id=field_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        search=search,
    )

    return GameListResponse(
        games=games,
        total=total,
        limit=limit,
        offset=skip,
        has_more=(skip + len(games)) < total,
    )


@router.get("/dates", response_model=List[str])
def get_game_dates(
    league_id: int = Query(..., description="League ID to get game dates for"),
    db: Session = Depends(get_db),
) -> List[str]:
    """Get unique game dates for a specific league."""
    dates = GameService.get_unique_game_dates(db=db, league_id=league_id)
    return [d.isoformat() for d in dates]


@router.get("/{game_id}", response_model=Game)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
) -> Game:
    """Get a single game by ID."""
    game = GameService.get_game_by_id(db=db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
