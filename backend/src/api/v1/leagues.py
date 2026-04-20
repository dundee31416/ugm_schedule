"""League API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.schemas.league import League
from src.schemas.responses import LeagueListResponse
from src.services.league_service import LeagueService
from src.models.league import League as LeagueModel

router = APIRouter()


@router.get("", response_model=LeagueListResponse)
def get_leagues(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> LeagueListResponse:
    """
    Get leagues with optional filtering.

    Supports filtering by:
    - is_active: Filter by active status

    Results are paginated using skip and limit parameters.
    """
    leagues = LeagueService.get_leagues(db=db, is_active=is_active, skip=skip, limit=limit)

    # Count total leagues with filter
    query = db.query(LeagueModel)
    if is_active is not None:
        query = query.filter(LeagueModel.is_active == is_active)
    total = query.count()

    return LeagueListResponse(
        leagues=leagues,
        total=total,
        limit=limit,
        offset=skip,
        has_more=(skip + len(leagues)) < total,
    )


@router.get("/{league_id}", response_model=League)
def get_league(
    league_id: int,
    db: Session = Depends(get_db),
) -> League:
    """Get a single league by ID."""
    league = LeagueService.get_league_by_id(db=db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return league
