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
from app.api.deps import get_current_user

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentResponse)
def create_incident(
    payload: IncidentCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Create a new incident.
    """
    service = IncidentService()
    data = payload.model_dump()

    # Enforce ownership from token (not client input)
    data["created_by"] = current_user["sub"]

    incident = service.create_incident(db, data)

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
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    List incidents with optional filters, search, and pagination.
    """
    service = IncidentService()

    incidents = service.list_incidents(
        db=db,
        status=status,
        priority=priority,
        team_id=team_id,
        search=search,
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