"""
Base repository providing common database operations.
"""

from typing import Generic, Type, TypeVar, Optional, List

from sqlalchemy.orm import Session

from app.core.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository for CRUD operations.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id) -> Optional[ModelType]:
        """
        Get a single record by ID.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session) -> List[ModelType]:
        """
        Get all records.
        """
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict) -> ModelType:
        """
        Create a new record.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id) -> Optional[ModelType]:
        """
        Delete a record by ID.
        """
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj