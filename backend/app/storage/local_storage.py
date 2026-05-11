"""
Local filesystem storage implementation.

IMPORTANT:
This implementation is intentionally isolated behind a storage layer
so it can later be replaced with:
- Amazon S3
- MinIO
- Google Cloud Storage
without changing API or service logic.
"""

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("/data/uploads")


class LocalStorage:
    """
    Handles local filesystem storage for uploaded documents.
    """

    def __init__(self) -> None:
        """
        Ensure upload directory exists.
        """
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        """
        Save uploaded file to local storage.

        Returns:
            str: Absolute file path of stored file.
        """

        unique_filename = f"{uuid4()}_{file.filename}"

        file_path = UPLOAD_DIR / unique_filename

        with open(file_path, "wb") as output_file:
            content = await file.read()
            output_file.write(content)

        return str(file_path)