from pydantic import BaseModel, EmailStr

class SManufacturerAdd(BaseModel):
    title: str
    email: EmailStr
   
class SManufacturerGet(SManufacturerAdd):
    id: int
