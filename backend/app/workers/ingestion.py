"""
Document ingestion worker tasks.
"""

from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.document import UploadedDocument
from app.workers.celery_app import celery_app
from app.parsers.text_parser import TextParser
from app.chunking.text_chunker import TextChunker
from app.repositories.chunk_repository import ChunkRepository


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

        # Read uploaded file
        with open(file_path, "rb") as uploaded_file:
            file_content = uploaded_file.read()

        # Extract raw text
        extracted_text = TextParser.extract_text(
            file_content
        )

        # Generate chunks
        chunks = TextChunker.chunk_text(
            extracted_text
        )

        chunk_repository = ChunkRepository()

        # Persist chunks
        for index, chunk_content in enumerate(chunks):
            chunk_repository.create(
                db,
                {
                    "document_id": document.id,
                    "chunk_index": index,
                    "content": chunk_content,
                },
            )

        document.processing_status = "COMPLETED"
        db.commit()

    except Exception:
        if document:
            document.processing_status = "FAILED"
            db.commit()

        raise

    finally:
        db.close()