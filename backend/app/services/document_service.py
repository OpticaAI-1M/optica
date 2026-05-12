"""
Document service layer.
"""

from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import UploadedDocument
from app.repositories.document_repository import DocumentRepository
from app.storage.local_storage import LocalStorage
from app.core.exceptions import ValidationException
from app.workers.ingestion import process_uploaded_document


ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/json",
    "text/markdown",
    "application/pdf",
}


MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50MB


class DocumentService:
    """
    Service for uploaded document operations.
    """

    def __init__(self):
        self.repository = DocumentRepository()
        self.storage = LocalStorage()

    async def upload_document(
        self,
        db: Session,
        file: UploadFile,
        incident_id: UUID,
        uploaded_by: UUID,
    ) -> UploadedDocument:
        """
        Upload and persist document metadata.
        """

        # Validate content type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationException(
                "Unsupported file type"
            )

        # Read file for size validation
        file_contents = await file.read()

        if len(file_contents) > MAX_FILE_SIZE_BYTES:
            raise ValidationException(
                "File size exceeds 50MB limit"
            )

        # Reset stream after validation
        await file.seek(0)

        # Save file to storage backend
        file_path = await self.storage.save_file(file)

        document = self.repository.create(
            db,
            {
                "incident_id": incident_id,
                "filename": file.filename,
                "file_path": file_path,
                "content_type": file.content_type,
                "uploaded_by": uploaded_by,
                "processing_status": "PENDING",
            },
        )

        # Trigger async ingestion pipeline
        process_uploaded_document.delay(str(document.id))

        return document