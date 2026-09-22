from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QueryOptions:
    sort_by: str
    descending: bool = False
    search: str | None = None


def get_sort_spec(
    options: QueryOptions, allowed_fields: Mapping[str, str]
) -> list[tuple[str, int]]:
    field = allowed_fields.get(options.sort_by, next(iter(allowed_fields.values())))
    return [(field, -1 if options.descending else 1)]


def text_search(search: str | None, fields: tuple[str, ...]) -> dict[str, Any]:
    if not search:
        return {}
    return {"$or": [{field: {"$regex": search, "$options": "i"}} for field in fields]}
