"""
Pydantic schemas for document operations.
"""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class UploadedDocumentResponse(BaseModel):
    """
    Response schema for uploaded documents.
    """

    id: UUID
    incident_id: UUID
    filename: str
    content_type: str
    processing_status: str
    created_at: datetime