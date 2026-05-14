from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    user_id: int
    total: float = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float

    model_config = ConfigDict(from_attributes=True)