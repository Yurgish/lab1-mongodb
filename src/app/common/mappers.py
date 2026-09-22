from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


def map_document(document: Mapping[str, Any], model_type: type[ModelT]) -> ModelT:
    data = dict(document)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))

    return model_type.model_validate(data)
