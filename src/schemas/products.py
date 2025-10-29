from pydantic import BaseModel, EmailStr

from src.schemas.manufacturers import SManufacturersGet

class SProductsAdd(BaseModel):
    title: str
    manufacturer_id: int
    price: int
    quantity: int

class SProductsGet(SProductsAdd):
    id: int
    manufacturer: SManufacturersGet




