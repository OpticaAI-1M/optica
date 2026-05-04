"""
Custom application exceptions.
"""


class AppException(Exception):
    """
    Base application exception.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationException(AppException):
    """
    Raised when validation fails.
    """


class NotFoundException(AppException):
    """
    Raised when a resource is not found.
    """


class ConflictException(AppException):
    """
    Raised when a conflict occurs (e.g., duplicate).
    """