"""
Incident service layer handling business logic.
"""

from sqlalchemy.orm import Session

from app.models.incident import Incident, IncidentStatus
from app.repositories.user_repository import UserRepository
from app.repositories.team_repository import TeamRepository
from app.repositories.incident_repository import IncidentRepository
from app.core.exceptions import ValidationException
from app.core.exceptions import NotFoundException


class IncidentService:
    """
    Service layer for incident-related operations.
    """

    def __init__(self):
        self.repo = IncidentRepository()
        self.user_repo = UserRepository()
        self.team_repo = TeamRepository()

    def create_incident(
        self,
        db: Session,
        data: dict,
    ) -> Incident:
        """
        Create a new incident with basic validation.
        """

        # Validate required fields (still keep for safety)
        if "title" not in data or not data["title"]:
            raise ValidationException("Title is required")

        # Validate user exists
        user = self.user_repo.get_by_id(db, data["created_by"])
        if not user:
            raise NotFoundException("User not found")

        # Validate team exists
        team = self.team_repo.get_by_id(db, data["team_id"])
        if not team:
            raise NotFoundException("Team not found")

        # Apply defaults
        data.setdefault("status", IncidentStatus.OPEN)
        data.setdefault("priority", "P3")

        # 4️ Persist using repository
        incident = self.repo.create(db, data)

        return incident