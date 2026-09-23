from dataclasses import dataclass, field
from typing import Any

from .selection_state import SelectionState


@dataclass
class AppState:
    stores: list[Any] = field(default_factory=list)
    departments: list[Any] = field(default_factory=list)
    sellers: list[Any] = field(default_factory=list)
    selection: SelectionState = field(default_factory=SelectionState)
    store_search: str = ""
    department_search: str = ""
    seller_search: str = ""
