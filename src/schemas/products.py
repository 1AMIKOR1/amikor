from pydantic import BaseModel, ConfigDict

from src.schemas.manufacturers import SManufacturerGet

class SProductAdd(BaseModel):
    manufacturer_id: int
    title: str
    price: int
    quantity: int
   
class SProductGet(SProductAdd):
    id: int
    manufacturer: SManufacturerGet
    model_config = ConfigDict(from_attributes=True)
