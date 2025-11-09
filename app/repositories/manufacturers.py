from app.models.manufacturers import ManufacturersModel
from app.repositories.base import BaseRepository
from app.schemas.manufacturers import SManufacturerGet


class ManufacturersRepository(BaseRepository):
    model = ManufacturersModel
    schema = SManufacturerGet