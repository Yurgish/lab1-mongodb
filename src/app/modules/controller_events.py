from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Generic, Literal, TypeAlias, TypeVar

T = TypeVar("T", covariant=True)


@dataclass(frozen=True)
class Loaded(Generic[T]):
    """Data returned by a controller load operation."""

    resource: Literal["stores", "departments", "sellers"]
    items: Sequence[T]


@dataclass(frozen=True)
class Succeeded:
    message: str


@dataclass(frozen=True)
class Failed:
    title: str
    message: str


ControllerEvent: TypeAlias = Loaded[object] | Succeeded | Failed
ControllerEventHandler: TypeAlias = Callable[[ControllerEvent], None]


def discard_event(event: ControllerEvent) -> None:
    del event


__all__ = [
    "ControllerEvent",
    "ControllerEventHandler",
    "discard_event",
    "Failed",
    "Loaded",
    "Succeeded",
]
