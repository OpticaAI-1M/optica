"""
Pydantic schemas for Incident.
"""

from uuid import UUID
from pydantic import BaseModel, Field


class IncidentCreateRequest(BaseModel):
    """
    Request schema for creating an incident.
    """

    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: str = Field(default="P3")
    # will be set from token, not client input
    created_by: UUID
    team_id: UUID


class IncidentResponse(BaseModel):
    """
    Response schema for incident.
    """

    id: UUID
    title: str
    description: str | None
    priority: str