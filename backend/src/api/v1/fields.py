"""Field API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.schemas.field import Field
from src.schemas.responses import FieldListResponse
from src.services.field_service import FieldService
from src.models.field import Field as FieldModel

router = APIRouter()


@router.get("", response_model=FieldListResponse)
def get_fields(
    city: Optional[str] = Query(None, description="Filter by city"),
    search: Optional[str] = Query(None, description="Search in field name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> FieldListResponse:
    """
    Get fields with optional filtering.

    Supports filtering by:
    - city: Filter by city
    - search: Search in field name

    Results are paginated using skip and limit parameters.
    """
    fields = FieldService.get_fields(db=db, city=city, search=search, skip=skip, limit=limit)

    # Count total fields with filters
    query = db.query(FieldModel)
    if city:
        query = query.filter(FieldModel.city.ilike(f"%{city}%"))
    if search:
        query = query.filter(FieldModel.name.ilike(f"%{search}%"))
    total = query.count()

    return FieldListResponse(
        fields=fields,
        total=total,
        limit=limit,
        offset=skip,
        has_more=(skip + len(fields)) < total,
    )


@router.get("/{field_id}", response_model=Field)
def get_field(
    field_id: int,
    db: Session = Depends(get_db),
) -> Field:
    """Get a single field by ID."""
    field = FieldService.get_field_by_id(db=db, field_id=field_id)
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return field
