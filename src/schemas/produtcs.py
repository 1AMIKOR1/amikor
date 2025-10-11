from pydantic import BaseModel
from src.schemas.manufacturers import SManufacturerGet
class SProductAdd(BaseModel):
    manufacture_id: int
    title: str
    price: int
    quantity: int

class SProductGet(SProductAdd):
    id: int
    manufacturere: SManufacturerGet

class SProductPatch(BaseModel):
    manufacture_id: int | None = None
    title: str | None = None
    price: int | None = None
    quantity: int | None = None

