from datetime import datetime

from pydantic import BaseModel, Field

from app.common.types import PhoneNumber

from .address import AddressModel
from .department import DepartmentModel


class StoreBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    address: AddressModel
    contact_phone: PhoneNumber
    is_active: bool = True


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    address: AddressModel | None = None
    contact_phone: PhoneNumber | None = None
    is_active: bool | None = None


class StoreModel(StoreBase):
    id: str
    departments: list[DepartmentModel] = Field(default_factory=list)
    departments_count: int = 0

    created_at: datetime
    updated_at: datetime
