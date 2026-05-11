"""
Document repository.
"""

from app.models.document import UploadedDocument
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[UploadedDocument]):
    """
    Repository for uploaded document operations.
    """

    def __init__(self):
        super().__init__(UploadedDocument)