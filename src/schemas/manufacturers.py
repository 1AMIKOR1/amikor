from pydantic import BaseModel, EmailStr

class SManufacturerlAdd(BaseModel):
    title: str
    email: EmailStr

class SManufacturerlGet(SManufacturerlAdd):
    id: int

class SManufacturerlPatch(BaseModel):
    title: str | None = None
    email: EmailStr | None = None