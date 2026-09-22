class AppError(Exception):
    title = "Application error"


class EntityNotFoundError(AppError):
    title = "Not found"


class OperationError(AppError):
    title = "Operation error"


class ValidationAppError(AppError):
    """Raised when user input does not satisfy a model."""

    title = "Validation error"


class UnexpectedAppError(AppError):
    title = "Unexpected error"
