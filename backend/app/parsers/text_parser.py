"""
Plain text parser implementation.
"""


class TextParser:
    """
    Parser for text-based uploaded documents.
    """

    @staticmethod
    def extract_text(file_content: bytes) -> str:
        """
        Extract UTF-8 text from uploaded document bytes.
        """

        return file_content.decode("utf-8")