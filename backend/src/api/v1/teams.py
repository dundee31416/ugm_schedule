"""Team API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.schemas.team import Team
from src.schemas.responses import TeamListResponse
from src.services.team_service import TeamService
from src.models.team import Team as TeamModel

router = APIRouter()


@router.get("", response_model=TeamListResponse)
def get_teams(
    search: Optional[str] = Query(None, description="Search in team name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(1000, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> TeamListResponse:
    """
    Get teams with optional search.

    Supports:
    - search: Search in team name

    Results are paginated using skip and limit parameters.
    """
    teams = TeamService.get_teams(db=db, search=search, skip=skip, limit=limit)

    # Count total teams with filter
    query = db.query(TeamModel)
    if search:
        query = query.filter(TeamModel.name.ilike(f"%{search}%"))
    total = query.count()

    return TeamListResponse(
        teams=teams,
        total=total,
        limit=limit,
        offset=skip,
        has_more=(skip + len(teams)) < total,
    )


@router.get("/{team_id}", response_model=Team)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
) -> Team:
    """Get a single team by ID."""
    team = TeamService.get_team_by_id(db=db, team_id=team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
