
import logging
from sqlalchemy import select
from src.schemas.produtcs import SProductGet
from src.models.products import ProductsModel
from src.repositories.base import BaseRepository
from sqlalchemy.orm import joinedload
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError



class ProductsRepository(BaseRepository):
    model = ProductsModel
    schema = SProductGet

    async def add(self, data: BaseModel):
        try:
            add_stmt = (
                insert(self.model)
                .values(**data.model_dump())
                
            )
            await self.session.execute(add_stmt)
            

        except IntegrityError as ex:
            logging.error(
                "Не удалось добавить данные в БД тип ошибки:%s",
                type(ex.orig.__cause__),
            )
            logging.error(
                "незнакомая ошибка: тип ошибки:%s", type(ex.orig.__cause__)
            )
            raise ex

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
        if result is None:
            return None  
        return  self.schema.model_validate(result, from_attributes=True)
         
    