"""
Document chunk repository.
"""

from app.models.document import DocumentChunk
from app.repositories.base_repository import BaseRepository


class ChunkRepository(BaseRepository[DocumentChunk]):
    """
    Repository for document chunk persistence.
    """

    def __init__(self):
        super().__init__(DocumentChunk)