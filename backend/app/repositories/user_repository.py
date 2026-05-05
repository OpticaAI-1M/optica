"""
User repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for user-related operations.
    """

    def __init__(self):
        super().__init__(User)

    def get_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        """
        return (
            db.query(self.model)
            .filter(self.model.id == user_id)
            .first()
        )