"""
Team repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.team import Team
from app.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """
    Repository for team-related operations.
    """

    def __init__(self):
        super().__init__(Team)

    def get_by_id(self, db: Session, team_id: UUID) -> Optional[Team]:
        """
        Get team by ID.
        """
        return (
            db.query(self.model)
            .filter(self.model.id == team_id)
            .first()
        )