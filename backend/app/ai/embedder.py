"""
Embedding orchestration layer.
"""

from typing import List

from app.core.config import get_settings
from app.ai.providers.sentence_transformer_provider import (
    SentenceTransformerProvider,
)


settings = get_settings()


class Embedder:
    """
    Provider-agnostic embedding orchestrator.
    """

    def __init__(self) -> None:

        if settings.embedding_provider == "sentence_transformers":
            self.provider = SentenceTransformerProvider()

        else:
            raise ValueError(
                f"Unsupported embedding provider: "
                f"{settings.embedding_provider}"
            )

    def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding vector using configured provider.
        """

        return self.provider.generate_embedding(text)