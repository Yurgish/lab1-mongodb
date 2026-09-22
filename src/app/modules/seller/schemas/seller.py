from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.common.types import PhoneNumber


class SellerBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=80)
    phone: PhoneNumber
    email: EmailStr
    position: str = Field(min_length=3, max_length=100)
    salary: float = Field(gt=0)
    store_id: str
    department_id: str


class SellerCreate(SellerBase):
    pass


class SellerUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=18, le=80)
    phone: PhoneNumber | None = None
    email: EmailStr | None = None
    position: str | None = Field(default=None, min_length=3, max_length=100)
    salary: float | None = Field(default=None, gt=0)
    store_id: str | None = None
    department_id: str | None = None


class SellerModel(SellerBase):
    id: str

    created_at: datetime
    updated_at: datetime
