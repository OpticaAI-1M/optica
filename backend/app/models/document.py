"""
Document-related database models.
"""

from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    Text,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UploadedDocument(Base):
    """
    Stores uploaded documents linked to incidents.
    """

    __tablename__ = "uploaded_documents"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    incident_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incidents.id"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    uploaded_by: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    processing_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunk(Base):
    """
    Stores chunked document content for retrieval.
    """

    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    document_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("uploaded_documents.id"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    document = relationship(
        "UploadedDocument",
        back_populates="chunks",
    )

    embedding = relationship(
        "Embedding",
        back_populates="chunk",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Embedding(Base):
    """
    Stores embedding metadata for document chunks.
    """

    __tablename__ = "embeddings"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    chunk_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_chunks.id"),
        nullable=False,
        unique=True,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    vector_reference: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    chunk = relationship(
        "DocumentChunk",
        back_populates="embedding",
    )