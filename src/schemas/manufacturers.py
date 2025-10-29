from pydantic import BaseModel, EmailStr

class SManufacturersAdd(BaseModel):
    title: str
    email: EmailStr

class SManufacturersGet(SManufacturersAdd):
    id: int




