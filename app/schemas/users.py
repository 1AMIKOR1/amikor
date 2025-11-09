from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.users import UsersRoles

class SUserAddRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UsersRoles | None = UsersRoles.USER


class SUserAdd(BaseModel):
    name: str
    email: EmailStr
    hash_password: str
    role: UsersRoles | None = UsersRoles.USER


class SUserGet(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)