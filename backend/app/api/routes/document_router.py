"""
Document upload API routes.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_user,
)
from app.core.database import get_db
from app.schemas.document_schema import (
    UploadedDocumentResponse,
)
from app.services.document_service import (
    DocumentService,
)

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    "/upload",
    response_model=UploadedDocumentResponse,
)
async def upload_document(
    incident_id: UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Upload a document linked to an incident.
    """

    service = DocumentService()

    document = await service.upload_document(
        db=db,
        file=file,
        incident_id=incident_id,
        uploaded_by=current_user["sub"],
    )

    return UploadedDocumentResponse(
        id=document.id,
        incident_id=document.incident_id,
        filename=document.filename,
        content_type=document.content_type,
        processing_status=document.processing_status,
        created_at=document.created_at,
    )