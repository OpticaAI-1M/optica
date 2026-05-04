"""
Incident API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.services.incident_service import IncidentService
from app.schemas.incident_schema import (
    IncidentCreateRequest,
    IncidentResponse,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentResponse)
def create_incident(
    payload: IncidentCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new incident.
    """
    service = IncidentService()
    incident = service.create_incident(db, payload.model_dump())

    return IncidentResponse(
        id=incident.id,
        title=incident.title,
        description=incident.description,
        priority=incident.priority,
    )