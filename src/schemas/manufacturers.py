from pydantic import BaseModel, ConfigDict, EmailStr

class SManufacturerAdd(BaseModel):
    title: str
    email: EmailStr
   
class SManufacturerGet(SManufacturerAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
