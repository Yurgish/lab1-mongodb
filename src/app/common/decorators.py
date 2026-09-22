from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, Protocol, TypeVar, cast

from pydantic import ValidationError as PydanticValidationError

from app.common.errors import AppError, UnexpectedAppError, ValidationAppError

Params = ParamSpec("Params")
Result = TypeVar("Result")


class ErrorHandler(Protocol):
    def _handle_error(self, error: AppError) -> None: ...


def handle_errors(method: Callable[Params, Result]) -> Callable[Params, Result | None]:
    """Route controller errors to its _handle_error method."""

    @wraps(method)
    def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> Result | None:
        try:
            return method(*args, **kwargs)
        except AppError as error:
            cast(ErrorHandler, args[0])._handle_error(error)
        except PydanticValidationError as error:
            cast(ErrorHandler, args[0])._handle_error(ValidationAppError(str(error)))
        except Exception as error:
            cast(ErrorHandler, args[0])._handle_error(UnexpectedAppError(str(error)))
        return None

    return wrapper
