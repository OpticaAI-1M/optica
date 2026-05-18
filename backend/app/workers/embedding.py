"""
Embedding generation worker tasks.
"""

from sqlalchemy.orm import Session

from app.ai.embedder import Embedder
from app.core.database import SessionLocal
from app.models.document import (
    DocumentChunk,
    Embedding,
)
from app.workers.celery_app import celery_app


@celery_app.task(name="generate_chunk_embedding")
def generate_chunk_embedding(
    chunk_id: str,
) -> None:
    """
    Generate embedding vector for document chunk.
    """

    db: Session = SessionLocal()

    try:
        chunk = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.id == chunk_id)
            .first()
        )

        if not chunk:
            return

        embedder = Embedder()

        embedding_vector = embedder.generate_embedding(
            chunk.content
        )

        embedding = Embedding(
            chunk_id=chunk.id,
            vector=embedding_vector,
        )

        db.add(embedding)
        db.commit()

    finally:
        db.close()