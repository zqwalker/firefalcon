from pydantic import BaseModel, validator


class BaseSchema(BaseModel):
    class Config:
        extra = "allow"


class BaseQuerySchema(BaseModel):
    where: list = None
    limit: int = 100
    offset: int = 0
    order_by: str = "ASCENDING"

    @validator("where", pre=True)
    def split_str(cls, v):
        if v is None:
            return v
        return v.split(" AND ")
