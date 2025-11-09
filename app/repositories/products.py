from app.models.products import ProductsModel
from app.repositories.base import BaseRepository
from app.schemas.products import SProductGet


class ProductsRepository(BaseRepository):
    model = ProductsModel
    schema = SProductGet