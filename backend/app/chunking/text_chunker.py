"""
Text chunking implementation.
"""

from typing import List


CHUNK_SIZE = 1000


class TextChunker:
    """
    Splits extracted document text into smaller chunks.
    """

    @staticmethod
    def chunk_text(text: str) -> List[str]:
        """
        Split text into fixed-size chunks.

        Args:
            text: Extracted document text.

        Returns:
            List[str]: Chunked text segments.
        """

        return [
            text[i:i + CHUNK_SIZE]
            for i in range(0, len(text), CHUNK_SIZE)
        ]