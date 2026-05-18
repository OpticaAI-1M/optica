"""
Sentence-transformers embedding provider.
"""

from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


settings = get_settings()


class SentenceTransformerProvider:
    """
    Local embedding provider using sentence-transformers.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.embedding_model
        )

    def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding vector for text.
        """

        embedding = self.model.encode(text)

        return embedding.tolist()