
from sqlalchemy import select
from src.schemas.produtcs import SProductGet
from src.models.products import ProductsModel
from src.repositories.base import BaseRepository
from sqlalchemy.orm import joinedload


class ProductsRepository(BaseRepository):
    model = ProductsModel
    schema = SProductGet

    async def get_filtered(
         self,
         **filter_by,
     ):
         filter_by = {k: v for k, v in filter_by.items() if v is not None}
         query = (
             select(self.model)
             .options(joinedload(self.model.manufacturer))
             .filter_by(**filter_by)
         )

         result = await self.session.execute(query)

         result = result.unique().scalars().all()

         return [
             self.schema.model_validate(model, from_attributes=True)
             for model in result
         ]

    async def get_one_or_none(
        self,
        **filter_by,
    ):
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        query = (
            select(self.model)
            .options(joinedload(self.model.manufacturer))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)

        result = result.unique().scalars().one_or_none()

  
        return  self.schema.model_validate(result, from_attributes=True)
         
    