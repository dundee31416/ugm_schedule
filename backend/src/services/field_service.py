"""Field service for business logic."""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.field import Field


class FieldService:
    """Service for field-related operations."""

    @staticmethod
    def get_fields(
        db: Session,
        city: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Field]:
        """
        Get fields with optional filtering.

        Args:
            db: Database session
            city: Filter by city
            search: Search in field name
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Field objects
        """
        query = db.query(Field)

        if city:
            query = query.filter(Field.city.ilike(f"%{city}%"))

        if search:
            query = query.filter(Field.name.ilike(f"%{search}%"))

        query = query.order_by(Field.name)
        query = query.offset(skip).limit(limit)

        return query.all()

    @staticmethod
    def get_field_by_id(db: Session, field_id: int) -> Optional[Field]:
        """Get a single field by ID."""
        return db.query(Field).filter(Field.id == field_id).first()

    @staticmethod
    def get_or_create_field(db: Session, name: str, address: Optional[str] = None, city: Optional[str] = None) -> Field:
        """
        Get an existing field by name or create a new one.

        Args:
            db: Database session
            name: Field name
            address: Field address (optional)
            city: City where field is located (optional)

        Returns:
            Existing or newly created Field object
        """
        # Ensure name is a string to prevent type mismatch errors
        if not isinstance(name, str):
            name = str(name) if name else "Unknown Field"

        field = db.query(Field).filter(Field.name == name).first()

        if field is None:
            field = Field(name=name, address=address, city=city)
            db.add(field)
            db.flush()  # Flush to get the ID without committing

        return field
