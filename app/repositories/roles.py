from app.models.roles import RolesModel
from app.repositories.base import BaseRepository
from app.schemas.roles import SRoleGet


class RolesRepository(BaseRepository):
    model = RolesModel
    schema = SRoleGet