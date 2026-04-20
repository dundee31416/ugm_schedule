"""API v1 routes package."""
from fastapi import APIRouter

from src.api.v1 import games, teams, fields, leagues, sync

api_router = APIRouter()

api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(fields.router, prefix="/fields", tags=["fields"])
api_router.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])

__all__ = ["api_router"]
