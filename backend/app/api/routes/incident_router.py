"""
Incident API routes.
"""

from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.incident import IncidentStatus
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


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(
    status: Optional[IncidentStatus] = None,
    priority: Optional[str] = None,
    team_id: Optional[UUID] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List incidents with optional filters and pagination.
    """
    service = IncidentService()

    incidents = service.list_incidents(
        db=db,
        status=status,
        priority=priority,
        team_id=team_id,
        limit=limit,
        offset=offset,
    )

    return [
        IncidentResponse(
            id=incident.id,
            title=incident.title,
            description=incident.description,
            priority=incident.priority,
        )
        for incident in incidents
    ]