class AppError(Exception):
    title = "Application error"


class EntityNotFoundError(AppError):
    title = "Not found"


class OperationError(AppError):
    title = "Operation error"


class UnexpectedAppError(AppError):
    title = "Unexpected error"
