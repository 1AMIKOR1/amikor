from pydantic import BaseModel


class SRolesAdd(BaseModel):
    title: str


class SRoleGet(SRolesAdd):
    id: int