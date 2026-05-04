"""
Incident service layer handling business logic.
"""

from sqlalchemy.orm import Session

from app.models.incident import Incident, IncidentStatus
from app.repositories.incident_repository import IncidentRepository
from app.core.exceptions import ValidationException


class IncidentService:
    """
    Service layer for incident-related operations.
    """

    def __init__(self):
        self.repo = IncidentRepository()

    def create_incident(
        self,
        db: Session,
        data: dict,
    ) -> Incident:
        """
        Create a new incident with basic validation.
        """

        # 1️ Validate required fields
        if "title" not in data or not data["title"]:
            raise ValidationException("Title is required")

        # 2️ Apply defaults
        data.setdefault("status", IncidentStatus.OPEN)
        data.setdefault("priority", "P3")

        # 3️ (Future) Validate user/team existence
        # Skipped for now — will add UserRepository later

        # 4️ Persist using repository
        incident = self.repo.create(db, data)

        return incident