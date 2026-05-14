"""
Document ingestion worker tasks.
"""

from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.document import UploadedDocument
from app.workers.celery_app import celery_app


@celery_app.task(name="process_uploaded_document")
def process_uploaded_document(document_id: str) -> None:
    """
    Process uploaded document asynchronously.

    Current responsibilities:
    - validate file exists
    - update processing status

    Future responsibilities:
    - text extraction
    - chunking
    - embedding generation
    """

    db: Session = SessionLocal()

    try:
        document = (
            db.query(UploadedDocument)
            .filter(UploadedDocument.id == document_id)
            .first()
        )

        if not document:
            return

        document.processing_status = "PROCESSING"
        db.commit()

        file_path = Path(document.file_path)

        if not file_path.exists():
            document.processing_status = "FAILED"
            db.commit()
            return

        # Future ingestion pipeline starts here

        document.processing_status = "COMPLETED"
        db.commit()

    except Exception:
        if document:
            document.processing_status = "FAILED"
            db.commit()

        raise

    finally:
        db.close()