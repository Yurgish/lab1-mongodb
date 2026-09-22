from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    floor: int = Field(ge=1, le=100)
    description: str = Field(min_length=2, max_length=500)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    floor: int | None = Field(default=None, ge=1, le=100)
    description: str | None = Field(default=None, min_length=2, max_length=500)


class DepartmentModel(DepartmentBase):
    id: str
    sellers_count: int = 0
