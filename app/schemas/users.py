from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.users import UsersRoles


class SUserAddRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str | None = "USER"


class SUserAdd(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    role: str | None = "USER"


class SUserGet(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
