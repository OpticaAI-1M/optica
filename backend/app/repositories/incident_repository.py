"""
Incident repository with custom queries.
"""

from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.incident import Incident, IncidentStatus
from app.repositories.base_repository import BaseRepository


class IncidentRepository(BaseRepository[Incident]):
    """
    Repository for Incident-specific database operations.
    """

    def __init__(self):
        super().__init__(Incident)

    def get_by_team(self, db: Session, team_id: UUID) -> List[Incident]:
        """
        Get all incidents for a given team.
        """
        return (
            db.query(self.model)
            .filter(self.model.team_id == team_id)
            .all()
        )

    def get_by_status(
        self, db: Session, status: IncidentStatus
    ) -> List[Incident]:
        """
        Get incidents by status.
        """
        return (
            db.query(self.model)
            .filter(self.model.status == status)
            .all()
        )

    def get_by_priority(self, db: Session, priority: str) -> List[Incident]:
        """
        Get incidents by priority.
        """
        return (
            db.query(self.model)
            .filter(self.model.priority == priority)
            .all()
        )

    def list_incidents(
        self,
        db: Session,
        status: IncidentStatus | None = None,
        priority: str | None = None,
        team_id: UUID | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Incident]:
        """
        List incidents with optional filters and pagination.
        """

        query = db.query(self.model)

        if status:
            query = query.filter(self.model.status == status)

        if priority:
            query = query.filter(self.model.priority == priority)

        if team_id:
            query = query.filter(self.model.team_id == team_id)

        return query.offset(offset).limit(limit).all()