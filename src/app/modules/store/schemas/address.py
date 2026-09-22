from pydantic import BaseModel, Field


class AddressModel(BaseModel):
    city: str = Field(min_length=2, max_length=100)
    street: str = Field(min_length=2, max_length=150)
    building: str = Field(min_length=1, max_length=20)
