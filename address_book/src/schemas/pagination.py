from pydantic import BaseModel, PositiveInt


class SkipLimit(BaseModel):
    page: int = 1
    limit: PositiveInt = 10
