from app.models.users import UsersModel
from app.repositories.base import BaseRepository
from app.schemas.users import SUserGet


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = SUserGet