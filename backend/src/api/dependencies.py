"""FastAPI dependencies."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.session import get_db

# Database session dependency
DBSession = Annotated[Session, Depends(get_db)]
