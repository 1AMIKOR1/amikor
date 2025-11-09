from pydantic import BaseModel

class SProductAdd(BaseModel):
    manufacturer_id: int
    title: str
    price: int
    quantity: int
   
class SProductGet(SProductAdd):
    id: int